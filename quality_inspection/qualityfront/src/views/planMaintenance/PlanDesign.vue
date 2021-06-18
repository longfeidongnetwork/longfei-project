<template>
  <div class="plandesign">
    <div class="el-row" style="width: 100%; height: 80px">
      <el-row>
        <div class="design-header-left">
          <div class="back-button">
            <i @click="back" class="el-icon-arrow-left" aria-hidden="true"></i>
          </div>
          <div class="select-name">
            <el-select v-model="planId" @change="searchSeries">
              <el-option
                v-for="item in planOptions"
                :key="item.planId"
                :label="item.planName"
                :value="item.planId"
              >
              </el-option>
            </el-select>
          </div>
        </div>
        <el-upload
          class="upload-design"
          ref="upload"
          action="http://127.0.0.1:8000/api/designController/uploadSeries"
          :on-change="onChange"
          :on-success="onSuccess"
          :auto-upload="false"
          :file-list="fileList"
          :show-file-list="false"
          :limit="1"
        >
          <el-button
            v-show="!isFileName"
            class="choose-file-button"
            size="small"
            slot="trigger"
            >请选择文件 <i class="el-icon-document el-icon--right"></i>
          </el-button>
          <el-tooltip effect="light" transition>
            <div slot="content">{{ fileDesignName }}</div>
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
              >{{ fileDesignName }}</el-button
            >
          </el-tooltip>
          <el-button
            :class="isUpload ? 'upload-before-button' : 'upload-end-button'"
            size="small"
            @click="submitUpload"
            >上传<i class="el-icon-upload el-icon--right"></i
          ></el-button>
          <el-button
            @click="uploadClear()"
            class="clear-empty-button"
            size="small"
            >清空</el-button
          >
          <el-button
            style="
              float: left;
              margin-left: 1.5%;
              margin-top: 3.6%;
              height: 32px;
              border-radius: 8px;
            "
            size="small"
          >
            <a
              href="../../../static/template.xlsx"
              download="模板"
              style="color: #606266; text-decoration: none"
              >模板下载</a
            >
          </el-button>
        </el-upload>
      </el-row>
    </div>
    <div class="right-container">
      <div
        class="el-row"
        style="
          width: auto;
          height: 50px;
          top: 20px;
          margin-left: 20px;
          position: relative;
        "
      >
        <el-radio-group
          v-model="statisticalValue"
          style="display: inline-block"
          size="small"
          @change="searchSeries()"
        >
          <el-radio-button class="radio-button1" :label="1"
            >加分法</el-radio-button
          >
          <el-radio-button class="radio-button2" :label="2"
            >减分法</el-radio-button
          >
        </el-radio-group>
        <div style="display: inline-block; margin-left: 30px; font-size: 14px">
          共8条记录
        </div>

        <el-button
          size="small"
          style="display: inline-block; float: right; margin-right: 30px"
          @click="newVisible = true"
          >新增</el-button
        >
        <el-dialog
          title="新增"
          :visible.sync="newVisible"
          width="30%"
          style="text-align: center"
        >
          <el-form ref="form" :model="form" label-width="80px" :rules="rules">
            <el-form-item
              label="组别"
              prop="seriesName"
              :rules="rules.seriesName"
            >
              <el-input v-model="form.seriesName"></el-input>
            </el-form-item>
            <el-form-item
              label="总分"
              prop="seriesScore"
              :rules="rules.seriesScore"
            >
              <el-input
                type="seriesScore"
                v-model.number="form.seriesScore"
              ></el-input>
            </el-form-item>
            <el-form-item
              label="命中记分"
              prop="everyHitScore"
              :rules="rules.everyHitScore"
            >
              <el-input v-model.number="form.everyHitScore"></el-input>
            </el-form-item>
            <el-form-item
              label="出现次数"
              prop="frequency"
              :rules="rules.frequency"
            >
              <el-input v-model.number="form.frequency"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="newVisible = false">取 消</el-button>
            <el-button type="primary" @click="addseriesName('form')"
              >确 定</el-button
            >
          </span>
        </el-dialog>
        <el-button
          @click="beforeBatchDelete()"
          style="display: inline-block; float: right; margin-right: 15px"
          size="small"
          >批量删除</el-button
        >
        <el-dialog :visible.sync="multiDeleteVisible" title="提示" width="30%">
          <span>确定删除吗?</span>
          <span slot="footer">
            <el-button title="primary" @click="batchdeleteseriesName"
              >确定</el-button
            >
            <el-button @click="multiDeleteVisible = false">取消</el-button>
          </span>
        </el-dialog>
        <!--编辑界面-->
        <el-dialog
          title="编辑"
          :visible.sync="editFormVisible"
          :close-on-click-modal="false"
          center
          width="30%"
        >
          <el-form :model="editForm" label-width="80px" ref="editForm">
            <el-form-item label="组别:" prop="seriesName">
              <el-input
                v-model="editForm.seriesName"
                auto-complete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="总分:">
              <el-input v-model="editForm.seriesScore"></el-input>
            </el-form-item>
            <el-form-item label="命中计分:" prop="everyHitScore">
              <el-input
                v-model="editForm.everyHitScore"
                auto-complete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="出现次数:">
              <el-input v-model="editForm.frequency"></el-input>
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
          max-height="100%"
          height="425px"
          highlight-current-row
          @selection-change="handleSelectionChange"
          @cell-click="overallClick"
          :cell-style="cellStyle"
        >
          <el-table-column type="selection" width="70" align="center">
          </el-table-column>
          <el-table-column label="组别" width="" align="center">
            <template slot-scope="scope">
              <span style="cursor: pointer; color: black">{{
                scope.row.seriesName
              }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="seriesScore"
            label="总分"
            width=""
            align="center"
          >
          </el-table-column>
          <el-table-column
            prop="everyHitScore"
            label="命中记分"
            width=""
            align="center"
          >
          </el-table-column>
          <el-table-column
            prop="frequency"
            label="出现次数"
            width=""
            align="center"
          >
          </el-table-column>
          <el-table-column align="right">
            <template slot="header">
              <i class="icon-more el-icon-s-operation"></i>
            </template>
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
        style="margin-left: 20px; bottom: 10px; position: absolute"
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
import Axios from "../../js/Axios";
export default {
  inject: ["reload"],
  name: "plandesign",
  data() {
    return {
      multiDeleteVisible: false,
      statisticalValue: 1,
      newVisible: false,
      isUpload: false,
      isFileName: false,
      fileDesignName: "",
      planName: "",
      tables: [],
      pageNum: 1,
      pageSize: 20,
      total: 0,
      form: {
        seriesName: "",
        seriesScore: "",
        everyHitScore: "",
        frequency: "",
      },
      //选择框
      planOptions: [],
      planId: "",
      //表单验证规则
      rules: {
        seriesName: [
          {
            type: "string",
            required: true,
            trigger: "blur",
            message: "请输入组别",
          },
        ],
        seriesScore: [
          {
            required: true,
            message: "总分不能为空",
          },
          {
            type: "number",
            message: "总分必须为数字值",
          },
        ],
        everyHitScore: [
          {
            required: true,
            message: "命中计分不能为空",
          },
          {
            type: "number",
            message: "命中计分必须为数字值",
          },
        ],
        frequency: [
          {
            required: true,
            message: "出现次数不能为空",
          },
          {
            type: "number",
            message: "出现次数必须为数字值",
          },
        ],
      },
      editFormVisible: false,
      //编辑界面数据
      editForm: {
        seriesId: 0,
        seriesName: "",
        frequency: 0,
        seriesScore: "",
        everyHitScore: "",
      },
      //上传数据
      fileList: [],
      //表格数据
      tableData: [],
      multipleSelection: [],
    };
  },
  created() {
  },
  mounted: function () {},
  activated: function () {
    // this.planName = localStorage.getItem("planName");
    this.planSelect();
    var planId = localStorage.getItem("planId");
    this.planId = parseInt(planId);
    this.searchSeries();
  },

  methods: {
    //TODO:方案选择
    planSelect() {
      const querystring = require("querystring");
      Axios.post("/api/designController/planSelect", querystring.stringify({}))
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 200) {
            this.planOptions = res.data.result.data.content;
            // console.log(this.planOptions);
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
    //TODO:搜索组别
    searchSeries() {
      let planId = this.planId;
      let statisticalValue = this.statisticalValue;
      var pageNum = this.pageNum;
      var pageSize = this.pageSize;
      const querystring = require("querystring");
      Axios.post(
        "/api/designController/seriesList",
        querystring.stringify({
          planId: planId,
          pageNum: pageNum,
          pageSize: pageSize,
          statisticalValue: statisticalValue
        })
      )
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 200) {
            this.total = res.data.result.data.total;
            // console.log(this.total);
            this.tableData = res.data.result.data.content;
            // console.log(this.tableData);
            this.showTable();
            localStorage.setItem('planId',planId);
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
    // TODO: 表格展示
    showTable() {
      // this.getList 表示请求到的数据
      // this.tables 表格 data
      if (this.tableData.length > 0) {
        this.tableData.forEach((val) => {
          val.flag = false;
        });
      }
      this.tables = this.tableData;
    },
    // TODO：更多弹出删除图标
    more(index, val) {
      // console.log("更多", index, val);
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
    //TODO: 修改组别信息
    handleEdit(index, row) {
      // console.log(index, row);
      this.editFormVisible = true;
      this.editForm = Object.assign({}, row);
    },
    // TODO: 组别修改提交
    editSubmit() {
      var planId = this.planId;
      var seriesId = this.editForm.seriesId;
      // console.log(seriesId);
      var seriesName = this.editForm.seriesName;
      var everyHitScore = this.editForm.everyHitScore;
      var frequency = this.editForm.frequency;
      var seriesScore = this.editForm.seriesScore;
      const querystring = require("querystring");
      Axios.post(
        "/api/designController/updateSeries",
        querystring.stringify({
          planId: planId,
          seriesId: seriesId,
          seriesName: seriesName,
          seriesScore: seriesScore,
          everyHitScore: everyHitScore,
          frequency: frequency,
        })
      )
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 200) {
            this.editFormVisible = false;
            this.searchSeries();
            this.$alert("组别信息修改成功!", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    // TODO: 删除组别
    handleDelete(index, row) {
      this.$confirm("将会删除该文件, 确认删除?", "删除", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        iconClass: "icon-warn el-icon-warning",
        customClass: "deleteMessage",
        center: true,
      })
        .then(() => {
          var seriesId = row.seriesId;
          var planId = this.planId;
          const querystring = require("querystring");
          Axios.post(
            "/api/designController/deleteSeries",
            querystring.stringify({
              planId: planId,
              seriesId: seriesId,
            })
          )
            .then((res) => {
              // console.log(res);
              if (res.data.result.code === 200) {
                this.editFormVisible = false;
                this.searchSeries();
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
        .catch(() => {
          this.$alert("删除操作取消！", "提示", {
            confirmButtonText: "确定",
            callback: (action) => {},
          });
        });
    },
    //TODO: 批量删除组别
    handleSelectionChange(val) {
      // console.log(val);
      this.multipleSelection = val;
    },
    //TODO:批量删除前
    beforeBatchDelete() {
      let checkArr = this.multipleSelection;
      let params = [];
      let self = this;
      checkArr.forEach(function (item) {
        params.push(item.id);
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
    //TODO：批量删除组别方法
    batchdeleteseriesName() {
      this.multiDeleteVisible = false;
      var planId = this.planId;
      let checkArr = this.multipleSelection;
      let params = [];
      let self = this;
      checkArr.forEach(function (item) {
        params.push(item.seriesId);
      });
      // console.log("params************" + params);
      const querystring = require("querystring");
      Axios.post(
        "/api/designController/batchDeleteSeries",
        querystring.stringify({
          seriesIds: params,
          planId: planId,
        })
      )
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 200) {
            this.searchSeries();
            this.$alert("批量删除组别信息成功!", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }else if (res.data.result.code === 400){
            this.$alert('批量删除组别信息失败！', '提示',{
              confirmButtonText: '确定',
              callback: (action) => {},
            })
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    // TODO: 新增组别
    addseriesName(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.newVisible = false;
          let planId = this.planId;
          let statisticalValue = this.statisticalValue;
          let seriesName = this.form.seriesName;
          let seriesScore = this.form.seriesScore;
          let everyHitScore = this.form.everyHitScore;
          let frequency = this.form.frequency;
          const querystring = require("querystring");
          Axios.post(
            "/api/designController/createSeries",
            querystring.stringify({
              planId: planId,
              statisticalValue:statisticalValue,
              seriesName: seriesName,
              seriesScore: seriesScore,
              everyHitScore: everyHitScore,
              frequency: frequency,
            })
          )
            .then((res) => {
              // console.log(res);
              if (res.data.result.code === 200) {
                this.searchSeries();
                this.$alert("新增组别信息成功!", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              }else if(res.data.result.code === 400) {
                this.$alert('新增组别信息失败！',"提示",{
                  confirmButtonText: '确定',
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
        path: "/planquality",
      });
    },
    // TODO:上传相关，后续修改
    submitUpload(file, fileList) {
      this.$refs.upload.submit();
      this.isUpload = false;
      this.isFileName = false;
    },
    //TODO: 清空操作
    uploadClear() {
      this.$refs.upload.clearFiles();
      this.isFileName = false;

      // this.fileDesignName = "";
      this.isUpload = false;
    },
    //TODO：文件上传成功
    onSuccess(res,file){
      // console.log(res,file);
      // console.log(this.$refs);
      this.$refs.upload.clearFiles();
      // console.log(this.$refs);
      this.$alert("文件上传成功!", "提示", {
        confirmButtonText: "确定",
        callback: (action) => {},
        type: "success",
      });
      this.searchSeries();
    },
    //TODO: 文件状态改变
    onChange(file, fileList) {
      if(fileList.length>0){
       this.fileDesignName = fileList[0]["name"]; 
        this.isUpload = true;
      this.isFileName = true;
      }
    },
    //TODO:点击当前行传入要跳转模块的id
    overallClick(row, column, cell, event) {
      // console.log(column);
      if (column.label == "组别") {
        let that = this;
        that.$router.push({
          path: "/plancompile",
        });
        localStorage.setItem("seriesId", row.seriesId);
        localStorage.setItem("seriesName", row.seriesName);
      }
    },
    //TODO: 某一列的样式
    cellStyle({ row, column, rowIndex, columnIndex }) {
      if (columnIndex == 1) {
        return "cursor:pointer";
      }
    },
    //TODO: 分页
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`);
    },
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`);
    },
  },
};
</script>
<style scoped>
.plandesign {
  width: 100%;
  height: 100%;
}
/* 左侧和右测总体布局 */
.design-header-left,
.upload-design {
  width: 50%;
  height: 80px;
  float: left;
}
/* 返回按钮 */
.back-button {
  margin-top: 4%;
  margin-left: 6%;
  font-size: 24px;
  cursor: pointer;
  float: left;
}
/* 下拉框样式 */
.select-name {
  margin-top: 3.2%;
  margin-left: 20px;
  font-size: 16px;
  color: #666666;
  float: left;
  width: 120px;
  background: #f6f6f6;
}
/* 右侧布局 */
/* 清空按钮 */
.el-row .clear-empty-button {
  margin-top: 3.6%;
  margin-left: 1.5%;
  float: left;
  border-radius: 8px;
}
/* 选择按钮 */
.choose-file-button {
  width: 110px;
  height: 32px;
  background: #e0e0e0;
  text-align: left;
  border: none;
}
/* 上传按钮 */
.upload-before-button {
  margin-top: 3.6%;
  margin-left: -10px;
  float: left;
  border-radius: 8px;
  background: #ffffff;
  /* color: #e7e7e7; */
}
.upload-end-button {
  margin-top: 3.6%;
  margin-left: -10px;
  float: left;
  border-radius: 8px;
  background: #ffffff;
  color: #e7e7e7;
}
/* 下方容器样式 */
.right-container {
  position: relative;
  top: 0px;
  bottom: 15px;
  margin-left: 2.5%;
  margin-right: 2.2%;
  height: calc(100% - 95px);
  margin-bottom: 20px;
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
/* 点击出现手指 */
.icon-more {
  cursor: pointer;
  margin-right: 20px;
}
</style>

<style>
.el-dialog__footer {
  text-align: center;
}
.el-dialog__body {
  padding-top: 10px;
  padding-right: 20px;
  padding-bottom: 10px;
  padding-left: 20px;
  text-align: center;
}
/* 单选按钮 */
.radio-button1 .el-radio-button__inner {
  border-radius: 24px 0px 0px 24px !important;
  background: #ececec;
}
.radio-button2 .el-radio-button__inner {
  border-radius: 0px 100px 100px 0px !important;
  background: #ececec;
}
/* 更多图标样式 */
.more-button {
  border: none;
  outline: none;
  background: #f6f6f7;
}
/* 选择框样式 */
.select-name .el-select .el-input__inner {
  background: #f6f6f6;
}
.el-scrollbar {
  background: #f6f6f6;
}
.upload-design .el-upload {
  margin-top: 3.6%;
  margin-left: 38.5%;
  float: left;
}
</style>