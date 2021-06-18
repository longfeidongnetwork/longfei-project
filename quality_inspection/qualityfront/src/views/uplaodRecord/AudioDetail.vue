<template>
  <div class="audiodetail">
    <div class="header-container">
      <div class="el-row">
        <!-- <div class="file-title" @click="back()">全部录音/{{audioDirectoryName}}/..bacK.</div> -->
        <el-breadcrumb class="file-title" separator-class="el-icon-arrow-right">
          <el-breadcrumb-item :to="{ path: '/uploadaudio' }"
            >全部录音</el-breadcrumb-item
          >
          <el-breadcrumb-item>{{ taskName }}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-input
          placeholder="请输入文件名搜索"
          class="input"
          v-model="name"
          @keyup.enter.native="searchAudio()"
        >
          <i
            slot="suffix"
            @click="searchAudio()"
            class="search-icon el-input__icon el-icon-search"
          ></i>
        </el-input>
        <el-upload
          style="display: inline-block; right: 0; position: absolute"
          action=""
          multiple
          :http-request="uploadFile"
          :show-file-list="false"
          :file-list="fileList"
        >
          <el-button class="button"
            >上传<i class="el-icon-upload el-icon--right"></i
          ></el-button>
        </el-upload>
        <el-button
          type="primary"
          class="delete-button"
          @click="beforeBatchDelete()"
          >批量删除</el-button
        >
        <el-dialog :visible.sync="multiDeleteVisible" title="提示" width="30%">
          <span>确定删除吗?</span>
          <span slot="footer">
            <el-button title="primary" @click="batchDeleteAudio"
              >确定</el-button
            >
            <el-button @click="multiDeleteVisible = false">取消</el-button>
          </span>
        </el-dialog>
      </div>
    </div>
    <div class="main-container">
      <div style="position: relative; height: calc(100% - 115px)">
        <el-table
          :data="tables"
          class="audio-detail-table"
          @selection-change="handleSelectionChange"
          ref="multipleTable"
          :header-cell-style="{
            'background-color': '#f6f6f7',
            'font-size': '12px',
            color: '#cccccc',
          }"
          tooltip-effect="dark"
          max-height="100%"
          height="438px"
        >
          <el-table-column type="selection" width="55" align="center">
          </el-table-column>
          <el-table-column label="音频名称" width="400" align="center">
            <template slot-scope="scope">
              <div style="display: inline; text-align: center">
                <i class="icon-folder el-icon-document"></i>
              </div>
              <div style="display: inline">
                <span style="margin-left: 10px; text-align: center">{{
                  scope.row.recordName
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="音频大小"  align="center">
            <template slot-scope="scope">
              <div style="display: inline; text-align: center">
                <i class="icon-folder el-icon-tickets"></i>
              </div>
              <span style="margin-left: 10px">{{ scope.row.size }}</span>
            </template>
          </el-table-column>
          <el-table-column label="音频时长(秒)"  align="center">
            <template slot-scope="scope">
              <div style="display: inline; text-align: center">
                <i class="icon-folder el-icon-time"></i>
              </div>
              <span style="margin-left: 10px">{{ scope.row.duration }}</span>
            </template>
          </el-table-column>
          <el-table-column label="上传日期" align="center">
            <template slot-scope="scope">
              <div style="display: inline; text-align: center">
                <i class="icon-folder el-icon-date"></i>
              </div>
              <span style="margin-left: 10px">{{ scope.row.uploadTime }}</span>
            </template>
          </el-table-column>
          <el-table-column align="right">
            <template slot-scope="scope">
              <div
                style="display: inline; text-align: center; margin-right: 10px"
                v-show="scope.row.flag"
                @click.stop="handleDelete(scope.$index, scope.row)"
              >
                <i class="icon-delete el-icon-delete"></i>
              </div>
              <div
                style="display: inline; text-align: center; cursor: pointer"
                @click.stop="more(scope.$index, scope.row)"
              >
                <i class="el-icon-more"></i>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination
        style="margin-left: 20px; bottom: 40px; position:absolute;"
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
    <!-- 上传文件弹出框 -->
    <div>
      <el-dialog
        v-el-drag-dialog
        :visible.sync="showProgress"
        :show-close="false"
        width="35%"
      >
        <div slot="title" class="clearfix">
          <span>文件上传成功</span>
          <el-button
            style="float: right; padding: 3px 0"
            type="text"
            @click="closeCard()"
            >关闭</el-button
          >
        </div>
        <el-table
          :data="fileList"
          max-height="350px"
          :show-header="false"
          class="file-table"
        >
          <el-table-column width="285px" text-align="left">
            <template slot-scope="scope">{{ scope.row.name }} </template>
          </el-table-column>
          <el-table-column width="183px" text-align="left">
            <template slot-scope="scope">
              <MyProgressBar
                :percentage="scope.row.progress"
                :strokeWidth="7"
                :reload="progressReload"
              />
            </template>
          </el-table-column>
        </el-table>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import elDragDialog from "@/js/directive";
import Axios from "../../js/Axios";
export default {
  directives: { elDragDialog },
  inject: ["reload"],
  name: "audiodetail",
  components: {
    MyProgressBar, // 自定义进度条
  },
  data() {
    return {
      taskId:"",
      taskName: "",
      fileList: [],
      multiDeleteVisible: false,
      multipleSelection: [],
      showProgress: false,
      progressReload: false,
      changeStatus: false,
      name: "",
      tables: [],
      pageNum: 1,
      pageSize: 20,
      total: "",
      getList: [],
    };
  },
  created() {
  },
  mounted: function () {},
  activated() {
    this.taskName = localStorage.getItem("taskName");
    this.taskId = localStorage.getItem('taskId');
    this.searchAudio();
  },
  methods: {
    // TODO: 搜索文件
    searchAudio() {
      let recordName = this.name;
      var pageSize = this.pageSize;
      var pageNum = this.pageNum;
      var taskId = this.taskId;
      console.log(recordName);
      const querystring = require("querystring");
      Axios.post(
        "/api/detailController/recordList",
        querystring.stringify({
          recordName: recordName,
          pageSize: pageSize,
          pageNum: pageNum,
          taskId: taskId,
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
            this.$alert("请输入正确的音频名！", "提示", {
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
    //TODO: 删除录音
    handleDelete(index, row) {
      this.$confirm("是否确认删除该录音文件?", "删除", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        iconClass: "icon-warn el-icon-warning",
        customClass: "deleteMessage",
        center: true,
      })
        .then(() => {
          const querystring = require("querystring");
          var taskName = this.taskName;
          Axios.post(
            "/api/detailController/deleteAudio",
            querystring.stringify({
              recordId: row.recordId,
              recordName: row.recordName,
              taskName: taskName
            })
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.searchAudio();
                this.$alert("音频删除成功！", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              } else if (res.data.result.code === 400) {
                this.$alert("音频删除失败！", "提示", {
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
    //TODO: 上传文件
    uploadFile: function (item) {
      this.showProgress = true;
      var userId = localStorage.getItem("userId");
      var taskName = this.taskName;
      let file = item.file;
      this.fileList.push(file);
      let form = new FormData();
      form.append("file", file);
      form.append("taskName", taskName);
      form.append("userId",userId);
      let cancelToken = axios.CancelToken;
      file.source = cancelToken.source();
      uploadFileRequest("/api/audioController/uploadFile", form, file.source, (progress) => {
        this.updateProgress(file, parseInt(progress));
      })
        .then((data) => {
          console.log(data);
          this.searchAudio();
        })
        .catch((error) => {
          console.log(error);
          // this.showProgress = false;
        });
    },
    // 更新进度条
    updateProgress: function (file, progress) {
      this.$set(
        this.fileList.filter((f) => f.uid === file.uid)[0],
        "progress",
        progress
      );
      this.progressReload = !this.progressReload; // 让 MyProgressBar 组件重新加载
    },
    // 取消上传
    // cancelUpload: function (uid) {
    //   let index = -1;
    //   for (index = 0; index < this.fileList.length; index++) {
    //     if (this.fileList[index].uid === uid) {
    //       break;
    //     }
    //   }
    //   let file = this.fileList[index];
    //   if (file.source) {
    //     file.source.cancel();
    //     this.fileList.splice(index, 1);
    //     if (this.fileList.length === 0) {
    //       this.showProgress = false;
    //     }
    //   }
    // },
    // 关闭卡片
    closeCard() {
      this.showProgress = false;
      this.fileList = [];
    },
    //TODO: 返回
    back() {
      let that = this;
      that.$router.push({
        path: "/uploadaudio",
      });
      that.reload();
    },
    //TODO: 分页
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`);
      this.pageSize = val;
      this.searchAudio();
    },
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`);
      this.pageNum = val;
      this.searchAudio();
    },
    //TODO: 批量删除音频
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
        params.push(item.recordId);
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
    //TODO：批量删除录音方法
    batchDeleteAudio() {
      this.multiDeleteVisible = false;
      var taskName = this.taskName;
      let checkArr = this.multipleSelection;
      let params = [];
      let self = this;
      checkArr.forEach(function (item) {
        params.push(item.recordId);
      });
      const querystring = require("querystring");
      Axios.post(
        "/api/detailController/batchDeleteAudio",
        querystring.stringify({
          recordIds: params,
          taskName: taskName
        })
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.searchAudio();
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
  },
};
// 上传文件方法
import MyProgressBar from "@/components/MyProgressBar";
import axios from "axios";
axios.defaults.timeout = 10000; // 单位：ms（-1 表示无限制）
export const uploadFileRequest = (url, params, source, callback) => {
  return axios({
    method: "post",
    url: url,
    data: params,
    headers: {
      "Content-Type": "multipart/form-data",
    },
    cancelToken: source.token,
    onUploadProgress(progressEvent) {
      if (progressEvent.lengthComputable) {
        let progress = parseInt(
          (progressEvent.loaded / progressEvent.total) * 100
        ).toFixed(0);
        callback(progress);
      }
    },
  });
};
</script>
<style scoped>
.audiodetail {
  width: 100%;
  height: 100%;
}
.header-container {
  height: 80px;
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
.file-size {
  position: relative;
  margin-left: 400px;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-duration {
  position: relative;
  margin-left: 180px;
  margin-top: 20px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-time {
  position: relative;
  margin-left: 170px;
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
.search-icon {
  cursor: pointer;
}
.button {
  position: relative;
  margin-right: 33px;
  margin-top: 11px;
  float: right;
  border-radius: 8px;
  height: 37px;
}
.delete-button {
  position: relative;
  float: right;
  margin-right: 150px;
  border-radius: 8px;
  color: #333333;
  background: #ffffff;
  margin-top: 10px;
  border: none;
}

.main-container {
  width: 100%;
  height: calc(100% - 80px);
}
.audio-detail-table {
  margin-top: 0px;
  position: relative;
  width: auto;
  left: 20px;
  margin-right: 60px;
  background: #f6f6f6;
}
.icon-folder {
  background: #90daca;
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
.file-table {
  background: #ffffff;
}
/* 表格最下面边框删除 */
/* el-table__row>td {
  border: none;
} */
.el-table::before {
  height: 0px;
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
.audio-detail-table tr {
  background: #f6f6f7;
}
.audio-detail-table th.gutter {
  background: #f6f6f7;
  display: table-cell !important;
}
/* 上传文件弹框 */
.box-card {
  position: fixed;
  margin-left: 00px;
}
</style>