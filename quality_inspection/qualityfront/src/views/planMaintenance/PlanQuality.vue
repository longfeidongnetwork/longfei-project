<template>
  <div class="planquality">
    <div class="header-container">
      <div class="el-row">
        <el-input placeholder="请输入方案名搜索" class="input" v-model="name" @keyup.enter.native="searchPlan()">
          <i
            slot="suffix"
            @click="searchPlan()"
            class="search-icon el-input__icon el-icon-search"
          ></i>
        </el-input>
      </div>
    </div>
    <div style="height:60px">
      <div class="file-name">名称</div>
      <div class="file-time">更新日期</div>
      <div class="file-total">总分</div>
      <div style="float: right; display: inline-block">
        <i class="file-icon el-icon-s-operation"></i>
      </div>
    </div>
    <div class="divider">
      <el-divider direction="horizontal"> </el-divider>
    </div>
    <div class="main-container">
      <div style="position: relative; height: calc(100% - 115px)">
      <el-table
        :data="tables"
        class="quality-table"
        :show-header="false"
        max-height="100%"
        height="390.4px"
        @cell-click="overallClick"
        :cell-style="cellStyle"
      >
        <el-table-column label="名称" width="420">
          <template slot-scope="scope">
            <div style="display: inline; text-align: center">
              <i class="icon-folder el-icon-document"></i>
            </div>
            <div style="display: inline">
              <span style="margin-left: 10px; text-align: center; cursor:pointer">{{
                scope.row.planName
              }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="更新日期" width="420">
          <template slot-scope="scope">
            <div style="display: inline; text-align: center">
              <i class="icon-folder el-icon-time"></i>
            </div>
            <span style="margin-left: 10px">{{ scope.row.lastTime }}</span>
          </template>
        </el-table-column>
        <el-table-column label="总分" width="">
          <template slot-scope="scope">
            <div style="display: inline; text-align: center">
              <i class="icon-folder el-icon-star-on"></i>
            </div>
            <div style="display: inline">
              <span style="margin-left: 10px; text-align: center">{{
                scope.row.totalScore
              }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column align="right">
          <template slot-scope="scope">
                    <div style="display: inline; text-align: center; margin-right:10px;" v-show="scope.row.flag" @click.stop="handleEdit(scope.$index, scope.row)">
              <i class="icon-edit el-icon-edit-outline"></i>
            </div>
            <div style="display: inline; text-align: center; cursor:pointer"  @click.stop="more(scope.$index, scope.row)">
              <i class="el-icon-more"></i>
            </div>
          </template>
        </el-table-column>
      </el-table>
      </div>
      <el-pagination
        style="left:20px;bottom:40px; position:absolute;"
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
import Axios from "../../js/Axios";
export default {
  inject: ['reload'],
  name: "uplaodaudio",
  data() {
    return {
      changeStatus: false,
      name: "",
      tables: [],
      pageNum: 1,
      pageSize: 20,
      total: '',
      getList: [],
    };
  },

  created() {
  },
  mounted: function () {},
  activated(){
    this.searchPlan();
  },

  methods: {
    //TODO: 搜索方案名
    searchPlan() {
      let planName = this.name;
      var pageSize = this.pageSize;
      var pageNum = this.pageNum;
      const querystring = require("querystring");
      Axios.post(
        "/api/planController/planList",
        querystring.stringify({
          planName: planName,
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
    //TODO: 是否修改方案名
    handleEdit(index, row) {
      console.log(index, row);
      this.$prompt("原先方案名:" + row.planName, "请修改方案名", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPlaceholder: "请输入新方案名称",
        center: true,
        inputErrorMessage: "方案名不能为空",
        inputValidator: (value) => {
          // 点击按钮时，对文本框里面的值进行验证
          if (!value) {
            return "输入不能为空";
          }
        },
      })
        .then(({ value }) => {
          const querystring = require("querystring");
          console.log(row.planId);
          Axios.post(
            "/api/planController/EditPlan",
            querystring.stringify({ planName: value, planId: row.planId })
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.searchPlan();
                this.$alert("修改方案名成功!", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              }else if(res.data.result.code === 400){
                this.$alert("修改方案名失败！",  "提示",{
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
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
    },
    //TODO:点击当前行传入要跳转模块的id
    overallClick(row, column, cell, event) {
      console.log(column);
      if (column.label=="名称") {
        let that = this;
        that.$router.push({
          path: "/plandesign",
        });
        localStorage.setItem("planName", row.planName);
        localStorage.setItem("planId", row.planId);
      }
    },
    //TODO: 某一列的样式
    cellStyle({row, column, rowIndex, columnIndex}){
      if (columnIndex == 0){
        return 'cursor:pointer';
      }
    },
    //TODO: 分页
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
    },
  },
};
</script>
<style scoped>
.planquality{
  width: 100%;
  height: 100%;
}
.header-container{
  height: 65px;
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
}
/* 名称 */
.file-name {
  position: relative;
  left: 4%;
  margin-top: 40px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
/* 更新日期 */
.file-time {
  position: absolute;
  margin-left: 445px;
  margin-top: 40px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
/* 总分 */
.file-total {
  position: absolute;
  margin-left: 850px;
  margin-top: 40px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-icon {
  margin-right: 50px;
  margin-top: 40px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.input {

  margin-left:36px;
  margin-top:17px;
  width: 237px;
}
.search-icon {
  cursor: pointer;
}
.button {
  margin-top: 14px;
  position: absolute;
  right: 2.2%;
  background: #ffffff;
  color: #333333;
  border-radius: 8px;
}
.main-container {
  position: relative;
  width: 100%;
  height: calc(100% - 146px);
}
.quality-table {
  margin-top: 0px;
  position: relative;
  width: auto;
  left: 20px;
  margin-right: 60px;
  background: #f6f6f6;
}
.icon-folder {
  background: #7cd3ff;
  width: 22px;
  height: 22px;
  text-align: center;
  display: table-cell;
  vertical-align: middle;
  border-radius: 50%;
  /* display:inline-block; */
  margin: 0;
}
.icon-edit {
  background: #ffb100;
  width: 22px;
  height: 22px;
  text-align: center;
  display: table-cell;
  vertical-align: middle;
  border-radius: 50%;
  margin: 0;
  cursor:pointer;
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
.quality-table tr {
  background: #f6f6f7;
}
.divider .el-divider--horizontal{
  margin:10px 0;
}
</style>