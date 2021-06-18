<template>
  <div class="uplaodaudio">
    <div class="header-container">
      <div class="el-row" style="padding-top: 8px">
        <div class="file-title">全部录音/...</div>
        <el-input
          placeholder="请输入名称搜索"
          class="input"
          v-model="name"
          @keyup.enter.native="search()"
        >
          <i
            slot="suffix"
            @click="search()"
            class="input-icon el-input__icon el-icon-search"
          ></i>
        </el-input>
        <el-button class="button" @click="newDirectory">新建任务名称</el-button>
        <!-- 录音上传弹框 -->
        <el-dialog
          title="录音上传"
          :visible.sync="uploadDialogForm"
          center
          width="30%"
          top="30vh"
          height="300px"
        >
          <el-upload
            class="upload-demo"
            ref="upload"
            action=""
            :file-list="fileList"
            :on-change="onChangeFile"
            :http-request="uploadFile"
            multiple
            :show-file-list="false"
            :auto-upload="false"
          >
            <el-button type="primary" slot="trigger"
              >上传<i class="el-icon-upload el-icon--right"></i
            ></el-button>
            <div slot="tip" class="el-upload__tip">
              支持wav,mp3,v3音频文件,支持多选文件且不超过10MB！
            </div>
          </el-upload>
          <!-- 上传显示进度条 -->
          <div
            v-show="beforeUploadVerify"
            slot="footer"
            class="dialog-footer"
            align="center"
            style="color: red"
          >
            文件已存在！
          </div>
        </el-dialog>
        <el-dialog
          v-el-drag-dialog
          :visible.sync="dialogTableVisible"
          :show-close="false"
        >
          <span slot="title">
            <div v-show="!uplaodSuccess" style="display: inline-block">
              文件上传中...
            </div>
            <div v-show="uplaodSuccess" style="display: inline-block">
              文件上传成功
            </div>
            <el-button
              v-show="!uplaodSuccess"
              @click="submitUpload()"
              style="
                display: inline-block;
                float: right;
                border-radius: 16px;
                width: 120px;
              "
              >开始上传</el-button
            >
            <el-button
              v-show="uplaodSuccess"
              @click="closeUpoad()"
              style="
                display: inline-block;
                float: right;
                border-radius: 16px;
                width: 120px;
              "
              >上传完成</el-button
            >
          </span>
          <el-table
            :data="fileList"
            height="377px"
            max-height="377px"
            class="file-table"
          >
            <el-table-column label="音频名称" width="350" text-align="left">
              <template slot-scope="scope">{{ scope.row.name }} </template>
            </el-table-column>
            <el-table-column width="280" align="left" label="进度条">
              <!--进度条-->
              <template slot-scope="scope">
                <MyProgressBar
                  :percentage="scope.row.progress"
                  :strokeWidth="7"
                  :reload="progressReload"
                />
              </template>
            </el-table-column>
            <el-table-column width="" align="right" label="操作">
              <template slot-scope="scope">
                <el-button
                  circle
                  type="text"
                  style="float: right; padding: 3px 3px; margin-left: 10px"
                  @click="cancelUpload(scope.row.uid)"
                  ><i class="el-icon-close" style="float: left"></i
                ></el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-dialog>
      </div>
    </div>
    <div style="height: 60px">
      <div class="file-name">名称</div>
      <div class="file-time">更新日期</div>
      <div style="display: inline-block; float: right">
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
          class="upload-audio-style"
          :show-header="false"
          max-height="100%"
          height="390.4px"
          @cell-click="overallClick"
          :cell-style="cellStyle"
        >
          <el-table-column label="名称" width="520">
            <template slot-scope="scope">
              <div style="display: inline; text-align: center; cursor: pointer">
                <i class="icon-folder el-icon-folder"></i>
              </div>
              <div style="display: inline">
                <span
                  style="margin-left: 10px; text-align: center; cursor: pointer"
                  >{{ scope.row.taskName }}</span
                >
              </div>
            </template>
          </el-table-column>
          <el-table-column label="日期">
            <template slot-scope="scope">
              <div style="display: inline; text-align: center">
                <i class="icon-folder el-icon-time"></i>
              </div>
              <span style="margin-left: 10px">{{ scope.row.lastTime }}</span>
            </template>
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
        style="left: 20px; bottom: 40px; position: absolute"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        v-if="tables.length > 0"
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
import elDragDialog from "@/js/directive";
// 上传文件方法
import MyProgressBar from "@/components/MyProgressBar";
export default {
  directives: { elDragDialog },
  inject: ["reload"],
  name: "uplaodaudio",
  components: {
    MyProgressBar, // 自定义进度条
  },
  data() {
    return {
      uploadDialogForm: false,
      changeStatus: false,
      dialogTableVisible: false,
      // uploadButton: false,
      // selectButton: true,
      fileExist: false,
      beforeUploadVerify: false,
      uplaodSuccess: false,
      userId:'',
      pageNum: 1,
      pageSize: 20,
      name: "",
      tables: [],
      total: 0,
      getList: [],
      fileList: [], //存储多文件
      progressReload: false,
      progressFlag: false, //进度条初始值隐藏
      progressPercent: 0, //进度条初始值
      customColor: [
        { color: "#f56c6c", percentage: 20 },
        { color: "#e6a23c", percentage: 40 },
        { color: "#5cb87a", percentage: 60 },
        { color: "#1989fa", percentage: 80 },
        { color: "#6f7ad3", percentage: 100 },
      ],
      newDirectoryName:"", //新建的任务名称
    };
  },

  created() {
    localStorage.clear();
    this.search();
  },
  mounted: function () {
    var userId=getCookie("userId");
    localStorage.setItem("userId",userId);
  },
  activated(){
  },
  methods: {
    //TODO:点击当前行传入要跳转模块的id
    overallClick(row, column, cell, event) {
      console.log(column);
      if (column.label == "名称") {
        let that = this;
        that.$router.push({
          path: "/audiodetail",
        });
        localStorage.setItem("taskName", row.taskName);
        localStorage.setItem("taskId",row.taskId);
      }
    },
    //TODO: 某一列的样式
    cellStyle({ row, column, rowIndex, columnIndex }) {
      if (columnIndex == 0) {
        return "cursor:pointer";
      }
    },
    // TODO: 搜索目录名
    search() {
      var name = this.name;
      var pageSize = this.pageSize;
      var pageNum = this.pageNum;
      console.log(name);
      const querystring = require("querystring");
      Axios.post(
        "api/audioController/taskList",
        querystring.stringify({
          name: name,
          pageSize: pageSize,
          pageNum: pageNum,
        })
      )
        .then((res) => {
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
    // TODO: 新建任务名称
    newDirectory() {
      this.$prompt("目录名最多不超过40个字符，可以是中文字符", "新建任务名称", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPlaceholder: "请输入目录名称",
        inputErrorMessage: "输入不能为空",
        center: true,
        inputValidator: (value) => {
          // 点击按钮时，对文本框里面的值进行验证
          if (!value) {
            return "输入不能为空";
          }
        },
      })
        .then(({ value }) => {
          this.mkdirDirectory(value);
          //新建的任务名称
          this.newDirectoryName = value;
          //上传录音弹框
          this.uploadDialogForm = true;
          this.fileList = [];
        })
        .catch(() => {
        });
    },
    //TODO: 新建任务名
    mkdirDirectory(value) {
      let taskName = value;
      const querystring = require("querystring");
      let userId = localStorage.getItem("userId");
      Axios.post(
        "/api/audioController/createTask",
        querystring.stringify({ userId: userId,  taskName: taskName})
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.search();
            this.message = res.data.result.data;
            console.log(this.message);
            this.$alert(this.message, "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }else if(res.data.result.code === 400){
            this.message = res.data.result.data;
            this.$alert(this.message, "提示", {
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
    //TODO: 分页
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`);
      this.pageSize = val;
      this.search();
    },
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`);
      this.pageNum = val;
      this.search();
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
    //TODO: 删除按钮
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
            "/api/audioController/deleteTaskName",
            querystring.stringify({ taskId: row.taskId, taskName: row.taskName })
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.search();
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
    //TODO: 编辑按钮
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
          Axios.post(
            "/api/audioController/editTaskName",
            querystring.stringify({ taskName: value, taskId: row.taskId, oldTaskName: row.taskName })
          )
            .then((res) => {
              console.log(res);
              if (res.data.result.code === 200) {
                this.search();
                this.$alert("修改目录成功!", "提示", {
                  confirmButtonText: "确定",
                  callback: (action) => {},
                });
              }else if(res.data.result.code === 400){
                this.$alert("修改目录失败！",  "提示",{
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
    //TODO: 文件上传时
    onChangeFile(file, fileList) {
      console.log(file, this.fileList);
      this.dialogTableVisible = true;
      this.uplaodSuccess = false;
      this.fileList = fileList;
    },
    submitUpload() {
      this.$refs.upload.submit();
    },
    //TODO: 上传文件
    uploadFile(item) {
      var taskName = this.newDirectoryName;
      var userId = localStorage.getItem("userId");
      let file = item.file;
      let form = new FormData();
      form.append("file", file);
      form.append("taskName",taskName);
      form.append("userId",userId);
      let cancelToken = axios.CancelToken;
      file.source = cancelToken.source();
      console.log(file.source);
      uploadFileRequest(
        "/api/audioController/uploadFile",
        form,
        file.source,
        (progress) => {
          this.updateProgress(file, parseInt(progress));
        }
      ).then((data) => {
          console.log(data);
          setTimeout(() => {
            this.uplaodSuccess = true;
          }, 1500);
          this.$refs["upload"].clearFiles();
          console.log(this.$refs);
          this.beforeUploadVerify = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // 文件上传前
    // beforeUpload(file) {
    //   if (file) {
    //     console.log("文件上传前：" + file.name);
    //     console.log("文件列表：" + this.fileList);
    //   }
    //   this.fileExist = false;
    //   var fileList = this.fileList;
    //   var result = fileList.some((item) => {
    //     if (item.name == file.name) {
    //       return true;
    //     }
    //   });
    //   if (result) {
    //     console.log("文件已存在");
    //     this.fileExist = true;
    //   }
    // },
    //TODO:录音上传
    // submitUpl(file) {
    //   var that = this;
    //   // that.$refs.upload.submit();
    //   if (that.fileList.length == 0) {
    //     that.$message({
    //       message: "请选择导入的文件",
    //       type: "warning",
    //       duration: "2000",
    //     });
    //   } else {
    //     let paramFormData = new FormData();
    //     that.fileList.forEach((file) => {
    //       paramFormData.append("files", file.raw);
    //       paramFormData.append("fileNames", file.name);
    //     });
    //     that.progressFlag = true;
    //     console.log(paramFormData.getAll("files"));
    //     that
    //       .$axios({
    //         url: "http://127.0.0.1:8000/api/test",
    //         method: "post",
    //         data: paramFormData,
    //         headers: { "Content-Type": "multipart/form-data" },
    //         onUploadProgress: (progressEvent) => {
    //           that.progressPercent =
    //             ((progressEvent.loaded / progressEvent.total) * 100) | 0;
    //         },
    //       })
    //       .then((res) => {
    //         // if(res.data == "success" && that.progressPercent === 100){
    //         if (that.progressPercent === 100) {

    //           that.updateProgress(file, parseInt(that.progressPercent));
    //           setTimeout(function () {
    //             that.$alert("文件上传成功，请继续!", "提示", {
    //               confirmButtonText: "确定",
    //               callback: (action) => {},
    //             });
    //             that.progressFlag = false;
    //             that.progressPercent = 0;
    //             that.$refs["upload"].clearFiles();
    //             // that.uploadDialogForm = false;
    //           }, 1000);
    //         }
    //       })
    //       .catch((error) => {
    //         that.progressFlag = false;
    //         that.progressPercent = 0;
    //         that.$refs.upload.clearFiles();
    //         that.$alert("上传失败，请重新上传!", "提示", {
    //           confirmButtonText: "确定",
    //           callback: (action) => {},
    //         });
    //       });
    //   }
    // },
    // 更新进度条
    updateProgress(file, progress) {
      this.$set(
        this.fileList.filter((f) => f.uid === file.uid)[0],
        "progress",
        progress
      );
      this.progressReload = !this.progressReload; // 让 MyProgressBar 组件重新加载
    },
    // 取消上传
    cancelUpload: function (uid) {
      let index = -1;
      for (index = 0; index < this.fileList.length; index++) {
        if (this.fileList[index].uid === uid) {
          break;
        }
      }
      let file = this.fileList[index];
      if (file.source) {
        file.source.cancel();
        this.fileList.splice(index, 1);
        if (this.fileList.length === 0) {
          this.showProgress = false;
        }
      }
    },
    closeUpoad() {
      this.$refs["upload"].clearFiles();
      this.dialogTableVisible = false;
      this.uploadDialogForm = false;
    },
    //TODO: 文件状态改变时的钩子，添加文件上传文件和上传失败都会被调用
    // onChange(file, fileList) {
    //   this.fileList = fileList;
    // },
    // handleRemove(file, fileList) {
    //   this.fileList = fileList;
    // },
  },
};
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

//获取cookie
function getCookie(name) {
	var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
 
	if (arr = document.cookie.match(reg))
 
		return unescape(arr[2]);
	else
		return null;
}
</script>
<style scoped>
.uplaodaudio {
  width: 100%;
  height: 100%;
}
.header-container {
  height: 65px;
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
  left: 4%;
  margin-top: 40px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-time {
  position: absolute;
  margin-left: 545px;
  margin-top: 40px;
  display: inline-block;
  color: #cccccc;
  font-size: 12px;
}
.file-icon {
  margin-right: 60px;
  right: 50px;
  margin-top: 40px;
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
.upload-demo {
  text-align: center;
}
.upload-audio-style {
  margin-top: 0px;
  position: relative;
  width: auto;
  left: 20px;
  margin-right: 60px;
  background: #f6f6f7;
}
.icon-folder {
  background: #90daca;
  width: 22px;
  height: 22px;
  text-align: center;
  display: table-cell;
  vertical-align: middle;
  border-radius: 50%;
  /* display:inline-block; */
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
.upload-audio-style tr {
  background: #f6f6f7;
}
/* 分割线样式 */
.divider .el-divider--horizontal {
  margin: 10px 0;
}
</style>