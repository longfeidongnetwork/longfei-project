<template>
  <div class="scorefile">
    <div class="header-container">
      <div class="el-row">
        <el-breadcrumb class="file-title" separator-class="el-icon-arrow-right">
          <el-breadcrumb-item :to="{ path: '/scoredirectory' }">质检评分</el-breadcrumb-item>
          <el-breadcrumb-item>{{
            taskName
          }}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-input placeholder="请输入文件名搜索" class="input" v-model="recordName" @keyup.enter.native="searchFile">
          <i
            slot="suffix"
            @click="searchFile"
            class="input-icon el-input__icon el-icon-search"
          ></i>
        </el-input>
        <el-button
          class="button"
          @click="beginQuality()"
          >质检</el-button
        >

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

        <el-button
          size=""
          type="primary"
          class="delete-button"
          @click="exportScoreFile()"
          >导出</el-button
        >
      </div>
    </div>
    <div class="main-container">
      <div style="position: relative; height: calc(100% - 115px)">
      <el-table
        id="out-table"
        :data="tables"
        class="scorefile-table"
        :header-cell-style="{ 'background-color': '#f0f0f0', 'font-size':'13px','text-align':'center' }"
        @selection-change="handleSelectionChange"
        ref="multipleTable"
        max-height="100%"
        height="438px"
        @cell-click="overallClick"
        :cell-style="cellStyle"
      >
        <el-table-column type="selection" width="55" align="center"> </el-table-column>
        <el-table-column label="音频名" width="320">
          <template slot-scope="scope">
            <div style="display: inline; text-align: center">
              <i class="icon-folder el-icon-document"></i>
            </div>
            <div style="display: inline">
              <span style="margin-left: 10px; text-align: center;cursor:pointer">{{
                scope.row.recordName
              }}</span>
            </div>
          </template>
        </el-table-column>
        <!-- <el-table-column label="组别" width="" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.group }}</span>
          </template>
        </el-table-column> -->
        <el-table-column label="key1" width="" align="center">
          <template slot-scope="scope">
            <div style="display: inline; text-align: center">
              <i class="icon-folder el-icon-thumb"></i>
            </div>
            <span style="margin-left: 5px">{{ scope.row.key1 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="key2" width=""  align="center">
          <template slot-scope="scope">
            <div style="display: inline; text-align: center">
              <i class="icon-folder el-icon-thumb"></i>
            </div>
            <span style="margin-left: 5px">{{ scope.row.key2 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="key3" width="" align="center">
          <template slot-scope="scope">
            <div style="display: inline; text-align: center">
              <i class="icon-folder el-icon-thumb"></i>
            </div>
            <span style="margin-left: 5px">{{ scope.row.key3 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="质检方案" width="" align="center">
          <template slot-scope="scope">
            <div style="display: inline; text-align: center">
              <i class="icon-folder el-icon-folder-checked"></i>
            </div>
            <span style="margin-left: 5px">{{ scope.row.planName }}</span>
          </template>
        </el-table-column>
        <el-table-column label="得分" align="center">
          <template slot-scope="scope">
            <div style="display: inline; text-align: center">
              <i class="icon-folder el-icon-star-off"></i>
            </div>
            <span style="margin-left: 5px">{{ scope.row.score }}</span>
          </template>
        </el-table-column>
        <el-table-column align="right">
          <template slot-scope="scope">
             <div style="display: inline; text-align: center; margin-right:10px;" v-show="scope.row.flag" @click.stop="handleDelete(scope.$index, scope.row)">
              <i class="icon-delete el-icon-delete"></i>
            </div>
            <div style="display: inline; text-align: center"  @click.stop="more(scope.$index, scope.row)">
              <i class="icon-more el-icon-more"></i>
            </div>
          </template>
        </el-table-column>
      </el-table>
      </div>
           <el-pagination
      style="margin-left:20px;bottom:40px; position:absolute"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      v-if="getList.length > 0"
      :current-page="pageNum"
      :page-sizes="[8, 20, 50, 100]"
      :page-size="pageSize"
      background
      layout="total, sizes, prev, pager, next, jumper"
      :total="total">
    </el-pagination>
    </div>
  </div>
</template>

<script>
import FileSaver from "file-saver";
import XLSX from "xlsx";
import Axios from '../../js/Axios'
export default {
  inject: ['reload'],
  name: "scorefile",
  data() {
    return {
      dialogFormVisible: false,
      formLabelWidth: "120px",
      multipleSelection: [],
      // 选择框
      planOptions:[],
      form: {
        planId: "",
      },
      changeStatus: false,
      recordName: "",
      taskName: "",
      tables: [],
      pageNum:1,
      pageSize:20,
      total: 0,
      getList: [
      ],
    };
  },

  created() {
  },
  mounted() {},
  activated() {
    this.getRouterData();
    this.searchFile();
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
    //TODO：搜索录音
    searchFile() {
      var taskId = this.taskId;
      var recordName = this.recordName;
      var pageSize = this.pageSize;
      var pageNum = this.pageNum;
      const querystring = require("querystring");
      Axios.post(
        "/api/fileController/resultList",
        querystring.stringify({
          taskId: taskId,
          recordName: recordName,
          pageSize: pageSize,
          pageNum: pageNum,
        })
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.total = res.data.result.data.total;
            this.getList = res.data.result.data.content;
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
    // TODO：删除
    handleDelete(index, row) {
      this.$confirm("将会删除这个文件, 确认删除?", "删除", {
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
            "/api/fileController/deleteResult",
            querystring.stringify({ resultId: row.resultId, taskId:this.taskId})
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.searchFile();
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
      if (column.label=="音频名") {
        let that = this;
        that.$router.push({
          name: "qualitydetail",
          query:{
            planName: row.planName,
            totalScore: row.score,
          }
        });
        let recordName = row.recordName;
        let recordId = row.recordId;
        localStorage.setItem("recordId",recordId);
        localStorage.setItem('recordName',recordName);
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
        // console.log(`每页 ${val} 条`);
        this.pageSize = val;
        this.searchFile();
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.pageNum = val;
        this.searchFile();
      },
    //TODO:路由取值
    getRouterData() {
      this.taskName = localStorage.getItem("taskName");
      this.taskId = localStorage.getItem("taskId");
      console.log(this.taskName);
    },
    //TODO:导出评分列表
    exportScoreFile() {
      let taskName = this.taskName;
      var now = new Date();
      let localTime = now.toLocaleDateString();
      var wb = XLSX.utils.table_to_book(document.querySelector('#out-table'))
      var wbout = XLSX.write(wb,{bookType: 'xlsx', bookSST: true, type: 'array'})
      try {
        FileSaver.saveAs(new Blob([wbout], {type:'appliction/octet-stream'}), name+ '_' + localTime +'.xlsx')
      }catch(e){
        if (typeof console !== 'undefined')
        console.log(e, wbout)
      }
      return wbout
      //请求时需要设置responseType
      // let checkArr = this.multipleSelection;
      // let params = [];
      // let self = this;
      // checkArr.forEach(function (item) {
      //   params.push(item.id);
      // });
      // axios({
      //   method: "post",
      //   url: "http://127.0.0.1:8000/api/test",
      //   params: params,
      //   responseType: "blob",
      // }).then((response) => {
      //   window.location.href = window.URL.createObjectURL(
      //     new Blob([response.data], { type: "application/vnd.ms-excel" })
      //   );
      // });
    },
    //TODO: 多选
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    //TODO：是否选中文件
    beginQuality(){
      let checkArr = this.multipleSelection;
      let params = [];
      let self = this;
      checkArr.forEach(function (item) {
        params.push(item.id);
      });
      if (params.length === 0){
        self.$alert("请先选择文件!", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
      }else{
        this.dialogFormVisible = true;
      }
    },
    //TODO:质检
    qualityInspection() {
      let taskId = this.taskId;
      let planId = this.form.planId;
      let checkArr = this.multipleSelection;
      let params = [];
      let self = this;
      checkArr.forEach(function (item) {
        params.push(item.recordId);
      });
      console.log("params************"+params);
      const querystring = require("querystring");
      Axios.post(
        "/api/scoreController/qualityInspection",
        querystring.stringify({
          planId: planId,
          params: params,
          taskIds: taskId,
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
            this.searchFile();
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
  },
};
</script>
<style scoped>
.scorefile{
  height: 100%;
}
.header-container{
  width: 100%;
  height: 80px;
  background: #f0f0f0;
}
.el-row {
  padding-top: 8px;
}
.file-title {
  position: relative;
  left: 2.5%;
  margin-top: 20px;
  display: inline-block;
  color: #666666;
  font-size: 16px;
}
.file-all {
  position: relative;
  left: 2.5%;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-name {
  position: relative;
  margin-left: 60px;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-group {
  position: relative;
  margin-left: 280px;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-top {
  position: relative;
  margin-left: 40px;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-duration {
  position: relative;
  margin-left: 100px;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-time {
  position: relative;
  margin-left: 70px;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.input {
  position: relative;
  left: 18.2%;
  width: 237px;
}
.input-icon {
  cursor: pointer;
}
.button {
  position: relative;
  margin-right: 33px;
  margin-top: 10px;
  float: right;
  background: #ffffff;
  color: #333333;
  border-radius: 8px;
}
.delete-button {
  position: relative;
  float: right;
  margin-right: 20px;
  border-radius: 8px;
  color: #333333;
  background: #ffffff;
  margin-top: 10px;
  border: none;
}

.main-container {
  position: relative;
  top: -10px;
  width: 100%;
  height: calc(100% - 80px);
  background: #f0f0f0;
}
.scorefile-table {
  margin-top: 10px;
  position: relative;
  width: auto;
  max-height: 430.4px;
  left: 20px;
  margin-right: 50px;
  background: #f0f0f0;
}
.icon-folder {
  background: #f3bbc8;
  width: 22px;
  height: 22px;
  text-align: center;
  display: table-cell;
  vertical-align: middle;
  border-radius: 50%;
  color: #ffffff;
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
  color: #ffffff;
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
.scorefile-table tr {
  background: #f0f0f0;
}
.scorefile-table th.gutter{
  background: #f0f0f0;
}
/* 更多图标样式 */
.icon-more {
  cursor: pointer;
}
</style>