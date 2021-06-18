<template>
  <div class="scoredirectory">
    <div class="header-container">
      <div class="el-row">
        <el-input
          
          placeholder="请输入名称搜索"
          class="input"
          v-model="name"
          @keyup.enter.native="searchDirectory"
          clearable
        >
          <i
            slot="suffix"
            @click="searchDirectory"
            class="input-icon el-input__icon el-icon-search"
          ></i>
        </el-input>
        <el-button
          
          style="float: right"
          class="button"
          @click="beginQuality()"
          >质检</el-button
        >
      </div>
           <el-dialog
          title="选择质检方案"
          :visible.sync="dialogFormVisible"
          width="30%"
          center
        >
          <el-form :model="form">
            <el-form-item label="质检方案" :label-width="formLabelWidth">
              <el-select v-model="form.planId" placeholder="">
              <el-option
                v-for="item in planOptions"
                :key="item.planId"
                :label="item.planName"
                :value="item.planId"
              >
              </el-option>
            </el-select>
            </el-form-item>
            <div style="text-align: center; font-size: 12px; color: #cccccc">
              可以选择多个文件进行二次质检
            </div>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="qualityInspection()"
              >开始质检</el-button
            >
          </div>
        </el-dialog>
    </div>
    <div class="main-container">
      <div style="position: relative; height: calc(100% - 115px);">
        <el-table
          ref="multipleTable"
          :data="tables"
          class="directory-style"
          :header-cell-style="{
            'background-color': '#f6f6f7',
            'font-size': '12px',
            color: '#cccccc',
          }"
          max-height="100%"
          height="438px"
          @selection-change="handleSelectionChange"
          @cell-click="overallClick"
          :cell-style="cellStyle"
        >
          <el-table-column type="selection" width="85"> </el-table-column>
          <el-table-column label="名称" width="">
            <template slot-scope="scope">
              <div style="display: inline; text-align: center">
                <i class="icon-folder el-icon-folder-opened"></i>
              </div>
              <div style="display: inline">
                <span style="margin-left: 10px; text-align: center; cursor:pointer">{{
                  scope.row.taskName
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="录音数量">
            <template slot-scope="scope">
              <div style="display: inline; text-align: center">
                <i class="icon-folder el-icon-files"></i>
              </div>
              <span style="margin-left: 10px">{{ scope.row.audioCount }}</span>
            </template>
          </el-table-column>
          <el-table-column label="质检日期">
            <template slot-scope="scope">
              <div style="display: inline; text-align: center">
                <i class="icon-folder el-icon-time"></i>
              </div>
              <span style="margin-left: 10px">{{ scope.row.lastTime }}</span>
            </template>
          </el-table-column>
          <el-table-column align="right">
            <template slot="header">
              <i class="el-icon-s-operation" style="margin-right: 8px"></i>
            </template>
            <template slot-scope="scope">
              <div style="display: inline; text-align: center; margin-right:10px;" v-show="scope.row.flag" @click.stop="handleEdit(scope.$index, scope.row)">
              <i class="icon-delete el-icon-edit"></i>
            </div>
            <div style="display: inline; text-align: center; margin-right:10px;" v-show="scope.row.flag" @click.stop="handleDelete(scope.$index, scope.row)">
              <i class="icon-delete el-icon-delete"></i>
            </div>
            <div style="display: inline; text-align: center; cursor:pointer"  @click.stop="more(scope.$index, scope.row)">
              <i class="el-icon-more"></i>
            </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination
          style="margin-left: 20px; bottom: 40px; position:absolute"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          v-if="getList.length > 0"
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
  name: "uplaodaudio",
  inject: ["reload"],
  data() {
    return {
      //选择框
      planOptions: [],
      form: {
        planId: "",
      },
      dialogFormVisible: false,
      formLabelWidth: "120px",
      changeStatus: false,
      name: "",
      tables: [],
      multipleSelection: [],
      pageNum: 1,
      pageSize: 20,
      total: '',
      getList: [
      ],
    };
  },

  created() {
  },
  mounted: function () {
  },
  activated(){
    this.searchDirectory();
    this.planSelect();
  },
  methods: {
    //TODO:方案选择
    planSelect() {
      const querystring = require("querystring");
      Axios.post("/api/designController/planSelect", querystring.stringify({}))
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.planOptions = res.data.result.data.content;
            console.log(this.planOptions);
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
    // TODO: 搜索目录名称
    searchDirectory() {
      var taskName = this.name;
      var pageSize = this.pageSize;
      var pageNum = this.pageNum;
      console.log(taskName);
      const querystring = require("querystring");
      Axios.post(
        "/api/scoreController/directoryList",
        querystring.stringify({
          taskName: taskName,
          pageSize: pageSize,
          pageNum: pageNum,
        })
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.total = res.data.result.data.total;
            console.log(this.total);
            this.getList = res.data.result.data.content;
            console.log(this.getList);
            this.showTable();
          } else if (res.data.result.code === 400) {
            this.$alert("请输入正确的任务名称！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    //TODO: 多选
    handleSelectionChange(val) {
      console.log(val);
      this.multipleSelection = val;
    },
    beginQuality(){
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
              type:'success',
            });
      }else{
        this.dialogFormVisible = true; 
      }
    },
    //TODO:质检
    qualityInspection() {
      this.multiDeleteVisible = false;
      var planId = this.form.planId;
      let checkArr = this.multipleSelection;
      let params = [];
      let self = this;
      checkArr.forEach(function (item) {
        params.push(item.taskId);
      });
      console.log("params************" + params);
      const querystring = require("querystring");
      Axios.post(
        "/api/scoreController/qualityInspection",
        querystring.stringify({
          planId: planId,
          taskIds: params,
        })
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.$alert("质检完成!", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
              type:'success',
            });
            this.dialogFormVisible = false;
          } else if (res.data.result.code === 400) {
            this.$alert("请输入正确的任务名称！", "提示", {
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
      if (this.getList.length > 0) {
        this.getList.forEach((val) => {
          val.flag = false;
        });
      }
      this.tables = this.getList;
    },
    // TODO：更多图标弹出删除图标
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
    // TODO：编辑目录
    handleEdit(index, row) {
      console.log(index, row);
      this.$prompt("原先目录名:" + row.taskName, "请修改目录名", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPlaceholder: "请输入新目录名称",
        center: true,
        inputErrorMessage: "目录名不能为空",
        inputValidator: (value) => {
          // 点击按钮时，对文本框里面的值进行验证
          if (!value) {
            return "输入不能为空";
          }
        },
      })
        .then(({ value }) => {
          const querystring = require("querystring");
          console.log(row.taskId);
          Axios.post(
            "/api/scoreController/updateDirectoryName",
            querystring.stringify({ taskName: value, taskId: row.taskId })
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.searchDirectory();
                this.$alert("修改目录成功!", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              }else if (res.data.result.code === 400) {
            this.$alert("修改目录失败！", "提示", {
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
        });
    },
    // TODO：删除目录
    handleDelete(index, row) {
      this.$confirm("将会删除该目录及目录内所有文件, 确认删除?", "删除", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        iconClass: "icon-warn el-icon-warning",
        customClass: "deleteMessage",
        center: true,
      })
        .then(() => {
          const querystring = require("querystring");
          console.log(row.taskId);
          Axios.post(
            "/api/scoreController/deleteDirectoryName",
            querystring.stringify({ taskId: row.taskId })
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.searchDirectory();
                this.$alert("删除目录成功!", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              }else if(res.data.result.code === 400){
                this.$alert("删除目录失败！",  "提示",{
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
        });
    },
    //TODO:点击当前行传入要跳转模块的id
    overallClick(row, column, cell, event) {
      console.log(column);
      if (column.label=="名称") {
        let that = this;
        that.$router.push({
          path: "/scorefile",
        });
        localStorage.setItem("taskName", row.taskName);
        localStorage.setItem('taskId',row.taskId);
      }
    },
    //TODO: 某一列的样式
    cellStyle({row, column, rowIndex, columnIndex}){
      if (columnIndex == 1){
        return 'cursor:pointer';
      }
    },
    //TODO: 分页
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.pageSize = val;
      this.searchDirectory();
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.pageNum = val;
      this.searchDirectory();
    },
  },
};
</script>
<style scoped>
.scoredirectory {
  width: 100%;
  height: 100%;
}
.header-container {
  width: 100%;
  height: 80px;
}
.main-container {
  /* position: relative; */
  width: 100%;
  height: calc(100% - 80px);
  /* background: #f0f0f0; */
  /* bottom: 0; */
}
.el-row {
  padding-top: 25px;
}
.file-title {
  position: relative;
  left: 2.5%;
  margin-top: 20px;
  display: inline-block;
  color: #666666;
}
.file-name {
  position: relative;
  left: 2.5%;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-time {
  position: absolute;
  margin-left: 525px;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.input {
  position: relative;
  left: 2.8%;
  width: 237px;
}
.input-icon {
  cursor: pointer;
}
.button {
  margin-top: 0px;
  position: absolute;
  right: 2.2%;
  background: #ffffff;
  color: #333333;
  width: 100px;
  border-radius: 8px;
}
.directory-style {
  top: 10px;
  width: calc(100% - 50px);
  left: 20px;
  right: 30px;
  background: #f6f6f6;
}
.icon-folder {
  background: #f3bbc8;
  width: 22px;
  height: 22px;
  text-align: center;
  display: table-cell;
  vertical-align: middle;
  border-radius: 50%;
  margin: 0;
}
.icon-delete {
   background: #ffb100;
  width: 22px;
  height: 22px;
  text-align: center;
  display: table-cell;
  vertical-align: middle;
  border-radius: 50%;
  /* color: black; */
  margin: 0;
  cursor: pointer;
}
</style>
<style>
.icon-warn.el-icon-warning {
  color: #ff6868;
}
.deleteMessage .el-message-box__btns button:nth-child(2) {
  background: #ff6868;
}
/* 输入框样式 */
.input .el-input__inner {
  background: #ececec !important;
  border: 1px solid #e0e0e0;
  border-radius: 24px;
}
/* 表格样式 */
.directory-style tr {
  background: #f6f6f7;
}
.directory-style th.gutter{
  background: #f6f6f7;
}
</style>