<template>
  <div class="plancompile">
    <div class="el-row" style="width: 100%; height: 80px">
      <div class="header-left">
        <div class="back-button">
          <i @click="back" class="el-icon-arrow-left" aria-hidden="true"></i>
        </div>
        <div class="left">
          <i
            @click="left"
            class="el-icon-caret-left"
            aria-hidden="true"
          ></i>
        </div>
        <div class="audio-name">{{ seriesName }}</div>
        <div class="right">
          <i
            @click="right"
            class="el-icon-caret-right"
            aria-hidden="true"
          ></i>
        </div>
      </div>
      <el-upload
        class="upload-plan"
        ref="upload"
        action="http://127.0.0.1:8000/api/designController/uploadSeries"
        :on-success="onSuccess"
        :on-change="onChange"
        :auto-upload="false"
        :file-list="fileList"
        :show-file-list="false"
        :limit="1"
      >
        <div></div>
        <el-button
          v-show="!isFileName"
          class="choose-button"
          size="small"
          slot="trigger"
          >请选择文件 <i class="el-icon-document el-icon--right"></i>
        </el-button>
        <el-tooltip effect="light" transition>
          <div slot="content">{{ fileListName }}</div>
          <el-button
            v-show="isFileName"
            style="
              margin-top: 3.6%;
              float: left;
              background: #e0e0e0;
              width: 120px;
              height: 32px;
              overflow: hidden;
              white-space: nowrap;
              text-overflow: ellipsis;
            "
            size="small"
            >{{ fileListName }}
          </el-button>
        </el-tooltip>
        <el-button
          :class="isUpload ? 'upload-button' : 'upload-button1'"
          size="small"
          @click="submitUpload"
          >上传<i class="el-icon-upload el-icon--right"></i
        ></el-button>
        <el-button @click="uploadClear()" class="empty-button" size="small"
          >清空</el-button
        >
      </el-upload>
    </div>
    <div class="right-container">
      <div
        class="el-row"
        style="width: auto; height: 50px; top: 20px; margin-left: 20px"
      >
        <el-button type="primary" @click="beforeBatchDelete()" size="small"
          >批量删除</el-button
        >
        <el-dialog :visible.sync="multiDeleteVisible" title="提示" width="30%">
          <span>确定删除吗?</span>
          <span slot="footer">
            <el-button title="primary" @click="batchdeleteGroup"
              >确定</el-button
            >
            <el-button @click="multiDeleteVisible = false">取消</el-button>
          </span>
        </el-dialog>

        <el-button
          type="primary"
          size="small"
          style="display: inline-block; float: right; margin-right: 30px"
          @click="newVisible = true"
          >新增</el-button
        >
        <el-dialog
          title="新增"
          :visible.sync="newVisible"
          width="40%"
          style="text-align: center"
          @close="closeNewDialog('form')"
        >
          <el-form ref="form" :model="form" label-width="80px" :rules="rules">
            <el-form-item label="关键词" prop="key">
              <el-input v-model="form.key"></el-input>
            </el-form-item>
            <el-form-item label="谐音词" prop="homophonicWord">
              <el-input>
                <el-tag
                  slot="prefix"
                  :key="tag"
                  v-for="tag in form.homophonicWord"
                  closable
                  :disable-transitions="false"
                  @close="newHandleClose(tag)"
                  type="info"
                >
                  {{ tag }}
                </el-tag>
                <el-input
                  slot="prefix"
                  class="input-new-tag"
                  v-if="inputVisible"
                  v-model="inputValue"
                  ref="saveTagInput"
                  size="small"
                  @keyup.enter.native="newHandleInputConfirm"
                  @blur="newHandleInputConfirm"
                >
                </el-input>
                <el-button
                  v-else
                  slot="prefix"
                  class="button-new-tag"
                  size="small"
                  type="info"
                  @click="newShowInput"
                  >+ New Tag</el-button
                >
              </el-input>
            </el-form-item>
            <el-form-item label="关联词" prop="relevance">
              <el-input v-model="form.relevance"></el-input>
            </el-form-item>
            <el-form-item label="时长(分)" prop="time">
              <el-input v-model.number="form.time"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="newVisible = false">取 消</el-button>
            <el-button type="primary" @click="addInfo('form')">确 定</el-button>
          </span>
        </el-dialog>
        <!--编辑界面-->
        <el-dialog
          title="编辑"
          :visible.sync="editFormVisible"
          :close-on-click-modal="false"
          center
          width="40%"
          @close="closeEditDialog('editForm')"
        >
          <el-form :model="editForm" label-width="80px" ref="editForm">
            <el-form-item label="关键词:" prop="key">
              <el-input v-model="editForm.keyWord" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="谐音词:">
              <el-input>
                <el-tag
                  slot="prefix"
                  :key="tag"
                  v-for="tag in editForm.homophonicWord"
                  closable
                  :disable-transitions="false"
                  @close="handleClose(tag)"
                  type="info"
                >
                  {{ tag }}
                </el-tag>
                <el-input
                  slot="prefix"
                  class="input-new-tag"
                  v-if="inputVisible"
                  v-model="inputValue"
                  ref="saveTagInput"
                  size="small"
                  @keyup.enter.native="handleInputConfirm"
                  @blur="handleInputConfirm"
                >
                </el-input>
                <el-button
                  v-else
                  slot="prefix"
                  class="button-new-tag"
                  size="small"
                  type="info"
                  @click="showInput"
                  >+ New Tag</el-button
                >
              </el-input>
            </el-form-item>
            <el-form-item label="关联词:" prop="relevance">
              <el-input
                v-model="editForm.relatedWord"
                auto-complete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="时长:">
              <el-input v-model="editForm.second"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="editFormVisible = false">取消</el-button>
            <el-button type="primary" @click.native="editSubmit"
              >提交</el-button
            >
          </div>
        </el-dialog>
      </div>
      <div style="position: relative; height: calc(100% - 120px); top: 5px">
        <el-table
          ref="multipleTable"
          :data="tables"
          tooltip-effect="dark"
          style="width: auto; margin-left: 30px; margin-right: 50px"
          @selection-change="handleSelectionChange"
          max-height="100%"
          height="425px"
        >
          <el-table-column type="selection" width="55" align="center"> </el-table-column>
          <el-table-column type="index" width="55" align="center"> </el-table-column>
          <el-table-column label="关键词" width="180" align="center">
            <template slot-scope="scope">{{ scope.row.keyWord }}</template>
          </el-table-column>
          <el-table-column
            prop="homophonicWord"
            label="谐音词"
            :formatter="FhomophonicWord"
            width="200"
            align="center"
          >
            <!-- <template slot-scope="scope">{{scope.row.homophonic}}</template> -->
          </el-table-column>
          <el-table-column
            prop="relatedWord"
            width="200"
            label="关联词"
            show-overflow-tooltip
            align="center"
          >
          </el-table-column>
          <el-table-column prop="second" label="时长(分)" width="" align="center">
          </el-table-column>

          <el-table-column align="right">
            <template slot-scope="scope">
              <div
                style="display: inline; text-align: center; margin-right: 10px"
                v-show="scope.row.flag"
                @click.stop="handleEdit(scope.$index, scope.row)"
              >
                <i class="icon-delete el-icon-edit"></i>
              </div>
              <div
                style="display: inline; text-align: center; margin-right: 10px"
                v-show="scope.row.flag"
              >
                <i
                  class="icon-delete el-icon-delete"
                  @click.stop="handleDelete(scope.$index, scope.row)"
                ></i>
              </div>
              <i
                class="icon-more el-icon-more"
                @click.stop="more(scope.$index, scope.row)"
              ></i>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination
        style="left: 20px; bottom: 10px; position: absolute"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        v-if="tableData.length > 0"
        :current-page="pageNum"
        :page-sizes="[8, 20, 50, 100]"
        :page-size="pageSize"
        background
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import Axios from '../../js/Axios'
export default {
  inject: ["reload"],
  name: "plancompile",
  data() {
    return {
      multiDeleteVisible: false,
      multipleSelection: "",
      newVisible: false,
      dialogVisible: false,
      isUpload: false,
      isFileName: false,
      inputVisible: false,
      inputValue: "",
      seriesName: "",
      pageNum: 1,
      pageSize: 20,
      total: 0,
      tables: [],
      fileListName: "",
      form: {
        key: "",
        homophonicWord: [],
        relevance: "",
        time: 0,
      },
      rules: {
        key: [{ required: true, message: "请输入关键词", trigger: "blur" }],
        time: [{ required: true, message: "请输入数字", type:"number"}]
      },
      editFormVisible: false,
      //编辑界面数据
      editForm: {
        keyWordId: '',
        keyWord: "",
        homophonicWord: [],
        relatedWord: "",
        second: 0,
      },
      //上传数据
      fileList: [],
      //表格数据
      tableData: [
      ],
      multipleSelection: [],
    };
  },
  created() {
  },
  mounted: function () {},
  activated: function () {
    this.seriesName = localStorage.getItem("seriesName");
    this.seriesId = localStorage.getItem("seriesId");
    this.searchKeyWord();
    
  },

  methods: {
    // TODO:上传相关，后续修改
    submitUpload(file, fileList) {
      this.$refs.upload.submit();
      this.isUpload = false;
      this.isFileName = false;
      this.$refs.upload.clearFiles();
    },
    //TODO: 清空操作
    uploadClear(file, fileList) {
      this.$refs.upload.clearFiles();
      this.fileListName = "";
      this.isUpload = false;
      this.isFileName = false;
    },
       //TODO：文件上传成功
    onSuccess(res,file){
      this.$refs.upload.clearFiles();
      this.$alert("文件上传成功!", "提示", {
        confirmButtonText: "确定",
        callback: (action) => {},
        type: "success",
      });
      this.searchKeyWord();
    },
    //TODO:文件状态改变
    onChange(file, fileList) {
      if(fileList.length>0){
       this.fileListName = fileList[0]["name"]; 
        this.isUpload = true;
      this.isFileName = true;
      }
    },
    // TODO: 查询关键词信息
    searchKeyWord(){
      var seriesId = this.seriesId;
      var pageNum = this.pageNum;
      var pageSize = this.pageSize;
      const querystring = require("querystring");
      Axios.post(
        "/api/compileController/keyWordList",
        querystring.stringify({
          seriesId: seriesId,
          pageNum: pageNum,
          pageSize: pageSize,
        })
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.total = res.data.result.data.total;
            // console.log(this.total);
            this.tableData = res.data.result.data.content;
            // console.log(this.tableData);
            this.showTable();
          } else if (res.data.result.code === 400) {
            this.$alert("方案查询失败！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    // TODO：多选
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    // TODO: 表格展示
    showTable() {
      if (this.tableData.length > 0) {
        this.tableData.forEach((val) => {
          val.flag = false;
        });
      }
      this.tables = this.tableData;
    },
    // TODO：更多弹出删除图标
    more(index, val) {
      console.log("更多", index, val);
      if (this.tables[index].flag === false) {
        this.tables[index].flag = true;
        this.tables = Object.assign([], this.tables);
      } else {
        this.tables[index].flag = false;
        // this.tables = JSON.parse(JSON.stringify(this.tables)); // 如果不转化 页面不生效
        this.tables = Object.assign([], this.tables); // 赋值一个新的对象
        // this.tables = this.tables.filter(item => item);
      }
    },
    // TODO: 删除关键词等
    handleDelete(index, row) {
      this.$confirm("将会删除该文件, 确认删除?", "删除", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        iconClass: "icon-warn el-icon-warning",
        customClass: "deleteMessage",
        center: true,
      })
        .then(() => {
          var keywordId = row.keywordId;
          const querystring = require("querystring");
          Axios.post(
            "/api/compileController/deleteKeyword",
            querystring.stringify({
              keywordId: keywordId,
            })
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.editFormVisible = false;
                this.searchKeyWord();
                this.$alert("组别信息删除成功!", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              }
            })
            .catch(function (err) {
              console.log(err);
            });
        })
        .catch(() => {});
    },
    // TODO：修改关键词信息等
    handleEdit(index, row) {
      console.log(index, row);
      this.editFormVisible = true;
      this.editForm = Object.assign({}, row);
    },
    // TODO: 关键词信息修改提交
    editSubmit() {
      let keyWord = this.editForm.keyWord;
      let homophonicWord = this.editForm.homophonicWord;
      let relatedWord = this.editForm.relatedWord;
      let second = this.editForm.second;
      let keywordId = this.editForm.keywordId;
      const querystring = require("querystring");
          Axios.post(
            "/api/compileController/editKeyword",
            querystring.stringify({
              keywordId: keywordId,
              keyWord: keyWord,
              homophonicWord: homophonicWord,
              relatedWord: relatedWord,
              second: second,
            })
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.editFormVisible = false;
                this.searchKeyWord();
                this.$alert("修改组别信息成功!", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              } else if (res.data.result.code === 400) {
                this.$alert("修改组别信息失败！", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              }
            })
            .catch(function (err) {
              console.log(err);
            });
    },
    //TODO: 批量删除关键词等
    handleSelectionChange(val) {
      console.log(val);
      this.multipleSelection = val;
    },
    //TODO：批量删除前
    beforeBatchDelete() {
      let checkArr = this.multipleSelection;
      let params = [];
      let self = this;
      checkArr.forEach(function (item) {
        params.push(item.keywordId);
      });
      if (params.length === 0) {
        self.$alert("请先选择文件!", "提示", {
          confirmButtonText: "确定",
          callback: (action) => {},
          type: "success",
        });
      } else {
        this.multiDeleteVisible = true;
      }
    },
    //TODO：批量删除关键词等方法
    batchdeleteGroup() {
      this.multiDeleteVisible = false;
      let checkArr = this.multipleSelection;
      let params = [];
      let self = this;
      checkArr.forEach(function (item) {
        params.push(item.keywordId);
      });
      const querystring = require("querystring");
      Axios.post(
        "/api/compileController/batchDeleteKeyword",
        querystring.stringify({
          keywordIds: params,
        })
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.searchKeyWord();
            this.$alert("批量删除成功！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          } else if (res.data.result.code === 400) {
            this.$alert("删除失败！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    //TODO: 新增关键词等信息
    addInfo(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let seriesId = this.seriesId;
          let key = this.form.key;

          let homophonicWord = this.form.homophonicWord;
          if (homophonicWord.length === 0) {
            var homophonicWord = key.split(",");
          }
          console.log(homophonicWord);

          let relevance = this.form.relevance;
          let time = this.form.time;
          console.log(seriesId);
          const querystring = require("querystring");
          Axios.post(
            "/api/compileController/createKeyword",
            querystring.stringify({
              seriesId: seriesId,
              keyWord: key,
              homophonicWord: homophonicWord,
              relatedWord: relevance,
              second: time,
            })
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.newVisible = false;
                this.searchKeyWord();
                this.$alert("新增关键词信息成功!", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              } else if (res.data.result.code === 400) {
                this.$alert("新增关键词信息失败！", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              }
            })
            .catch(function (err) {
              console.log(err);
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
      this.$refs[formName].resetFields();
    },
    //TODO: 返回上一页
    back() {
      this.$router.push({
        path: "/plandesign",
      });
    },
    //TODO: 分页
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`);
      this.pageSize = val;
      this.searchKeyWord();
    },
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`);
      this.pageNum= val;
      this.searchKeyWord();
    },
    //TODO: 上一条
    left() {
      let seriesId = this.seriesId;
      let planId = localStorage.getItem("planId");
      console.log(seriesId);
      const querystring = require("querystring");
      Axios.post(
        "/api/compileController/lastSeries",
        querystring.stringify({
          seriesId: seriesId,
          planId: planId,
        })
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.seriesId = res.data.result.data[0].seriesId;
            this.seriesName = res.data.result.data[0].seriesName;
            localStorage.setItem('seriesId', this.seriesId);
            localStorage.setItem('seriesName', this.seriesName);
            this.searchKeyWord();
          } else if (res.data.result.code === 400) {
            this.$alert("没有上一条了！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
      
    },
    //TODO：下一条
    right() {
      let seriesId = this.seriesId;
      let planId = localStorage.getItem("planId");
      console.log(seriesId);
      const querystring = require("querystring");
      Axios.post(
        "/api/compileController/nextSeries",
        querystring.stringify({
          seriesId: seriesId,
          planId: planId,
        })
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.seriesId = res.data.result.data[0].seriesId;
            this.seriesName = res.data.result.data[0].seriesName;
            localStorage.setItem('seriesId', this.seriesId);
            localStorage.setItem('seriesName', this.seriesName);
            this.searchKeyWord();
          } else if (res.data.result.code === 400) {
            this.$alert("没有下一条了！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    //TODO:清空新增标签数据
    closeNewDialog(type) {
      if (type) {
        this.$refs[type].resetFields();
      }
    },
    //TODO：清空编辑标签数据
    closeEditDialog(type) {
      if (type) {
        this.$refs[type].resetFields();
      }
    },
    //TODO:格式化数据
    FhomophonicWord(row, column) {
      var gNamelist = [];
      for (var i = 0; i < row.homophonicWord.length; i++) {
        gNamelist.push(row.homophonicWord[i]);
      }
      return gNamelist.join();
    },
    //TODO:新增标签
    newHandleClose(tag) {
      this.form.homophonicWord.splice(this.form.homophonicWord.indexOf(tag), 1);
    },
    newShowInput() {
      this.inputVisible = true;
      this.$nextTick((_) => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    newHandleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.form.homophonicWord.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = "";
    },
    //TODO:编辑标签
    handleClose(tag) {
      this.editForm.homophonicWord.splice(this.editForm.homophonicWord.indexOf(tag), 1);
    },
    showInput() {
      this.inputVisible = true;
      this.$nextTick((_) => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.editForm.homophonicWord.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = "";
    },
  },
};
</script>
<style scoped>
.plancompile {
  height: 100%;
}
/* 左侧和右测总体布局 */
.header-left,
.upload-plan {
  width: 50%;
  height: 80px;
  float: left;
}
/* 左侧布局 */
.back-button {
  margin-top: 3.8%;
  margin-left: 6%;
  font-size: 24px;
  float: left;
  cursor: pointer;
}
/* 上一个组别 */
.left {
  margin-top: 4.4%;
  color: hsl(0, 0%, 60%);
  float: left;
  margin-left: 20px;
  cursor: pointer;
}
/* 组别名样式 */
.audio-name {
  margin-top: 4%;
  margin-left: 20px;
  font-size: 16px;
  color: #666666;
  float: left;
}
/* 下一个组别 */
.right {
  margin-top: 4.4%;
  margin-left: 20px;
  color: hsl(0, 0%, 60%);
  float: left;
  cursor: pointer;
}
/* 右侧布局 */
/* 清空按钮 */
.el-row .empty-button {
  margin-top: 3.6%;
  margin-left: 3%;
  float: left;
  border-radius: 8px;
}
/* 选择按钮 */
.choose-button {
  width: 120px;
  height: 32px;
  background: #e0e0e0;
  text-align: left;
  border: none;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: el;
}
/* 上传按钮样式 */
.upload-button {
  margin-top: 3.6%;
  margin-left: -10px;
  float: left;
  border-radius: 8px;
  background: #ffffff;
  /* color: #e7e7e7; */
}
/* 上传按钮样式 */
.upload-button1 {
  margin-top: 3.6%;
  margin-left: -10px;
  float: left;
  border-radius: 8px;
  background: #ffffff;
  color: #e7e7e7;
}
/* 下方容器 */
.right-container {
  position: relative;
  top: 0px;
  margin-left: 2.5%;
  margin-right: 2.2%;
  height: calc(100% - 95px);
  margin-bottom: 20px;
  bottom: 15px;
  background: #ffffff;
  border-radius: 18px;
}

/* 删除图标 */
.icon-delete {
  background: #ffb100;
  width: 18px;
  height: 18px;
  text-align: center;
  display: table-cell;
  vertical-align: middle;
  border-radius: 50%;
  margin: 0;
  cursor: pointer;
}
/* 更多图标 */
.icon-more {
  cursor: pointer;
}
/* 上传文件名超出内容提示 */
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}
.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  position: absolute;
  z-index: 1;
  bottom: 100%;
  left: 50%;
  margin-left: -60px;
  /* 淡入 - 1秒内从 0% 到 100% 显示: */
  opacity: 0;
  transition: opacity 1s;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>

<style>
/* 上传 */
.upload-plan .el-upload {
  margin-top: 3.6%;
  margin-left: 51%;
  float: left;
}
/* 样式 */
.el-tag + .el-tag {
  margin-left: 10px;
}
.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
.el-input___suffix {
  left: 5px;
}
</style>