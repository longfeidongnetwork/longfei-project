<template>
  <div class="qualitydetail">
    <div class="el-row" style="width: 100%; height: 60px">
      <el-row>
        <div class="header-left">
          <div class="back-button" @click="back">
            <i class="el-icon-arrow-left" aria-hidden="true"></i>
          </div>
          <div class="left" @click="leftAudio">
            <i class="el-icon-caret-left" aria-hidden="true"></i>
          </div>
          <div class="audio-name">{{ recordName }}</div>
          <div class="right" @click="rightAudio">
            <i class="el-icon-caret-right" aria-hidden="true"></i>
          </div>
        </div>
        <el-button
          @click="detailResult()"
          type="primary"
          class="button"
          size="small"
          >完成并评分</el-button
        >
      </el-row>
    </div>
    <div class="right-container">
      <div class="left-content">
        <div style="text-align: center">{{ recordName }}</div>
        <div class="detail">
          <audio
            class="audio"
            ref="player"
            id="audio"
            :src="audio_url"
            controls
            autoplay
          ></audio>
          <div class="wrapper">
            <div class="bottom_fade_reverse"></div>
            <ul ref="ul" class="content">
              <li
                v-for="(item, index) in oLRC.ms"
                :key="item.index"
                :data-index="index"
                ref="c"
              >
                {{ item.c }}
              </li>
            </ul>
            <div class="bottom_fade"></div>
          </div>
        </div>
      </div>
      <div class="divider">
        <el-divider direction="vertical"> </el-divider>
      </div>
      <div class="right-content">
        <div>
          <div style="margin-left: 15px; margin-top: 5px; position: absolute">
            质检方案
          </div>
          <el-tag
            size="medium"
            style="
              margin-left: 90px;
              background: #ececec;
              font-size: 14px;
              text-align: center;
              color: #666666;
              width: 120px;
            "
            >{{ planName }}</el-tag
          >
          <div
            style="
              margin-top: 0;
              margin-right: 30px;
              float: right;
              font-size: 28px;
              color: green;
            "
          >
            {{ totalScore }}
          </div>
          <div
            style="
              margin-top: 5px;
              margin-right: 10px;
              postiion: absolute;
              float: right;
            "
          >
            评分：
          </div>
          <el-divider></el-divider>
        </div>
        <div style="width: 100%; height: 40%">
          <div>
            <el-table
              :data="tableData"
              size="mini"
              :show-header="false"
              class="table-style"
              :row-key="getRowKeys"
              @expand-change="expandChange"
              :expand-row-keys="expands"
            >
              <el-table-column type="expand">
                <template slot-scope="props">
                  <el-form
                    label-position="left"
                    inline
                    class="demo-table-expand"
                  >
                    <el-tag
                      v-for="item in props.row.keyword"
                      :key="item.label"
                      :type="'info'"
                      effect="dark"
                      size="small"
                      @click.native="searchKeyWord(item.label)"
                    >
                      {{ item.label }}
                    </el-tag>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column prop="id" width="100px"> </el-table-column>
              <el-table-column prop="totalScore">
                <template slot-scope="scope">
                  <span style="margin-right: 20px">总分</span>
                  {{ scope.row.totalScore }}
                </template>
              </el-table-column>
              <el-table-column
                align="right"
                style="float: left"
                prop="score"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span style="margin-right: 20px">打分</span>
                  <el-input
                    v-model="scope.row.score"
                    class="textarea"
                    @change="handleEdit(scope.$index, scope.row)"
                    maxlength="2"
                    oninput="if(value<0)value=0"
                    @keyup.native="
                      scope.row.score = scope.row.score.replace(/[^\d.]/g, '')
                    "
                  ></el-input>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>
import Axios from "../../js/Axios";
export default {
  name: "qualitydetail",
  data() {
    return {
      recordName: "",
      planName: "",
      score: "",
      audio_url: "",
      expands: [],
      lrcData: "",
      totalScore: 0,
      tableData: [],
      // 歌词与音频
      oLRC: {
        ti: "", //歌曲名
        ar: "", //演唱者
        al: "", //专辑名
        by: "", //歌词制作人
        ms: [], //歌词数组{t:时间,c:歌词}
      },
      lineNo: 0, //当前行
      Cpos: 3, //C位
      offset: -32, //滚动距离（应等于行高）
      lineNumber: 0, //页面展示为多行
      time: "",
      clickKeyWord: false, //点击关键词
      keywordInfo: "", //关键词信息
    };
  },
  created() {},
  activated() {
    this.getAudio();
    this.getRouterData();
    this.detailResult();
  },
  mounted() {
    this.getLrcFile();
    const music = this.$refs.player; // 音频所在对象
    music.addEventListener("timeupdate", () => {
      if (this.lineNo == this.oLRC.ms.length) return;
      const curTime = music.currentTime; //播放器时间
      if (this.time > curTime) {
        for (var i = 1; i < this.oLRC.ms.length; i++) {
          if (parseFloat(this.oLRC.ms[i].t) >= curTime) {
            while (this.lineNo >= i) {
              this.changeLine();
              --this.lineNo;
            }
          }
        }
      }
      if (parseFloat(this.oLRC.ms[this.lineNo].t) <= curTime) {
        this.time = curTime;
        this.lineHigh(); //高亮当前行
        this.lineNo++;
      }
      if (this.clickKeyWord == true) {
        this.keywordHigh();
      }
    });

    music.addEventListener("ended", () => {
      this.goback(); //回滚歌词
      music.play();
    });
  },
  methods: {
    //TODO：每一行点击按钮
    getRowKeys(row) {
      return row.id;
    },
    expandChange(row, expandedRows) {
      var that = this;
      if (expandedRows.length) {
        that.expands = [];
        if (row) {
          that.expands.push(row.id); // 每次push进去的是每行的ID
        }
      } else {
        that.expands = []; // 默认不展开
      }
    },
    //TODO:路由取值
    getRouterData() {
      this.recordName = localStorage.getItem("recordName");
    },
    // TODO: 返回上一级
    back() {
      let that = this;
      that.$router.push({
        path: "/scorefile",
      });
    },
    //TODO: 上一条音频
    leftAudio() {
      let recordId = localStorage.getItem("recordId");
      let taskId = localStorage.getItem("taskId");
      const querystring = require("querystring");
      Axios.post(
        "api/qualityController/lastResult",
        querystring.stringify({
          taskId: taskId,
          recordId: recordId,
        })
      )
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 201) {
            this.$alert("没有上一条啦!", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
              type: "success",
            });
          } else if (res.data.result.code === 200) {
            // console.log(res.data.result.data.content);
            this.recordId = res.data.result.data.content.recordId;
            this.recordName = res.data.result.data.content.recordName;
            //音频和日志
            this.lrcData = [];
            localStorage.setItem("recordId", this.recordId);
            localStorage.setItem("recordName", this.recordName);
            this.detailResult();
          }
        })
        .catch(function (err) {
          // console.log(err);
        });
    },
    //TODO：下一条音频
    rightAudio() {
      let recordId = localStorage.getItem("recordId");
      let taskId = localStorage.getItem("taskId");
      const querystring = require("querystring");
      Axios.post(
        "api/qualityController/nextResult",
        querystring.stringify({
          taskId: taskId,
          recordId: recordId,
        })
      )
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 201) {
            this.$alert("没有下一条啦!", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
              type: "success",
            });
          } else if (res.data.result.code === 200) {
            this.recordId = res.data.result.data.content.recordId;
            this.recordName = res.data.result.data.content.recordName;
            //音频和日志
            this.lrcData = [];
            localStorage.setItem("recordId", this.recordId);
            localStorage.setItem("recordName", this.recordName);
            this.detailResult();
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    //TODO:初始化评分结果
    detailResult() {
      let recordId = localStorage.getItem("recordId");
      const querystring = require("querystring");
      Axios.post(
        "api/qualityController/detailResult",
        querystring.stringify({
          recordId: recordId,
        })
      )
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 200) {
            this.tableData = res.data.result.data.content;
            this.planName = res.data.result.data.planName;
            this.totalScore = res.data.result.data.score;
            // 默认展开第一行
            this.expands = [];
            this.expands.push(this.tableData[0].id);
          } else if (res.data.result.code === 201) {
            this.planName = res.data.result.data.planName;
            this.totalScore = res.data.result.data.score;
            this.$alert("该方案没有质检结果！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          } else if (res.data.result.code === 400) {
            this.$alert("评分结果展示失败！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    //TODO:关键词可点击
    searchKeyWord(label) {
      // console.log(label);
      let recordId = localStorage.getItem("recordId");
      const querystring = require("querystring");
      Axios.post(
        "api/qualityController/keywordTimeResult",
        querystring.stringify({
          keyword: label,
          recordId: recordId,
        })
      )
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 200) {
            var keywordTime = res.data.result.data.keywordTime;
            var s = keywordTime.split(":"); //分离:前后文字
            var t = (parseFloat(s[0]) * 60 + parseFloat(s[1])).toFixed(3);
            // 设置当前时间进行播放
            const music = this.$refs.player;
            music.currentTime = parseFloat(t);
            this.keywordInfo = label;
            this.clickKeyWord = true;
          } else if (res.data.result.code === 400) {
            this.$alert("点击关键词跳转失败！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    //TODO: 人工打分
    handleEdit(index, row) {
      if (row.score > this.tableData[index].totalScore) {
        this.$alert("输入的值大于该组别总分,请重新输入！", "提示", {
          confirmButtonText: "确定",
          callback: (action) => {},
        });
      } else {
        let recordId = localStorage.getItem("recordId");
        const querystring = require("querystring");
        Axios.post(
          "api/qualityController/editResult",
          querystring.stringify({
            recordId: recordId,
            series: row.id,
            score: row.score,
          })
        )
          .then((res) => {
            // console.log(res);
            if (res.data.result.code === 200) {
              this.$alert("人工打分成功！", "提示", {
                confirmButtonText: "确定",
                callback: (action) => {},
              });
            } else if (res.data.result.code === 400) {
              this.$alert("人工打分失败！", "提示", {
                confirmButtonText: "确定",
                callback: (action) => {},
              });
            }
          })
          .catch(function (err) {
            console.log(err);
          });
      }
    },
    //TODO:获取音频
    getAudio() {
      let recordId = localStorage.getItem("recordId");
      let taskId = localStorage.getItem("taskId");
      const querystring = require("querystring");
      Axios.post(
        "api/qualityController/getRecordFile",
        querystring.stringify({
          recordId: recordId,
          taskId: taskId,
        })
      )
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 200) {
            this.audio_url = "/static/15895133275-8004-1618237764.wav";
            // this.audio_url = res.data.result.data.recordFile;
          } else if (res.data.result.code === 400) {
            this.$alert("评分结果展示失败！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    // TODO: 获取歌词
    getLrcFile() {
      let recordId = localStorage.getItem("recordId");
      let taskId = localStorage.getItem("taskId");
      const querystring = require("querystring");
      Axios.post(
        "api/qualityController/getLrcFile",
        querystring.stringify({
          recordId: recordId,
          taskId: taskId,
        })
      )
        .then((res) => {
          // console.log(res);
          if (res.data.result.code === 200) {
            var lrc = res.data.result.data.lrcFile;
            this.createLrcObj(lrc);
          } else if (res.data.result.code === 400) {
            this.$alert("评分结果展示失败！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    //TODO：解析歌词
    createLrcObj(lrc) {
      let oLRC = this.oLRC;
      if (lrc.length == 0) return;
      var lrcs = lrc.split("\n"); //用回车拆分成数组
      for (var i in lrcs) {
        //遍历歌词数组
        lrcs[i] = lrcs[i].replace(/(^\s*)|(\s*$)/g, ""); //去除前后空格
        var t = lrcs[i].substring(
          lrcs[i].indexOf("[") + 1,
          lrcs[i].indexOf("]")
        ); //取[]间的内容
        var s = t.split(":"); //分离:前后文字
        if (isNaN(parseInt(s[0]))) {
          //不是数值
          for (var i in oLRC) {
            if (i != "ms" && i == s[0].toLowerCase()) {
              oLRC[i] = s[1];
            }
          }
        } else {
          //是数值
          var arr = lrcs[i].match(/\[(\d+:.+?)\]/g); //提取时间字段，可能有多个
          var start = 0;
          for (var k in arr) {
            start += arr[k].length; //计算歌词位置
          }
          var content = lrcs[i].substring(start); //获取歌词内容
          for (var k in arr) {
            var t = arr[k].substring(1, arr[k].length - 1); //取[]间的内容
            var s = t.split(":"); //分离:前后文字
            oLRC.ms.push({
              //对象{t:时间,c:歌词}加入ms数组
              t: (parseFloat(s[0]) * 60 + parseFloat(s[1])).toFixed(3),
              c: content,
            });
          }
        }
      }
      oLRC.ms.sort(function (a, b) {
        //按时间顺序排序
        return a.t - b.t;
      });
    },
    //TODO:高亮歌词滚动事件
    lineHigh() {
      const ulist = this.$refs.ul;
      const list = ulist.getElementsByTagName("li");
      var height = { top: list[this.lineNo].offsetHeight };
      var lineCount = height.top / 32;
      this.lineNumber += lineCount - 1;
      if (this.lineNo > 0) {
        list[this.lineNo - 1].removeAttribute("class"); //去掉当前行的高亮样式
      }
      list[this.lineNo].className = "lineHigh"; //高亮显示上一行

      //文字滚动
      if (this.lineNo > this.Cpos) {
        ulist.style.transform =
          "translateY(" +
          (this.lineNumber + this.lineNo - this.Cpos) * this.offset +
          "px)"; //整体向上滚动一行高度
      }
    },
    //TODO:关键词高亮显示
    keywordHigh() {
      const ulist = this.$refs.ul;
      const list = ulist.getElementsByTagName("li");
      console.log(list)
      // 匹配关键字正则
      let replaceReg = new RegExp(this.keywordInfo, "g");
      // 高亮替换v-html值
      let replaceString =
        '<span style="color:red">' + this.keywordInfo + "</span>";
      console.log(list[this.lineNo-1])
      console.log(list[this.lineNo-1].innerHTML);
      list[this.lineNo-1].innerHTML = list[this.lineNo-1].innerHTML.replace(replaceReg,replaceString);      
    },
    //TODO:切换进度条时间
    changeLine() {
      const ulist = this.$refs.ul;
      const list = ulist.getElementsByTagName("li");
      list[this.lineNo].removeAttribute("class");
      list[this.lineNo - 1].className = "lineHigh";
      var height = { top: list[this.lineNo].offsetHeight };
      var lineCount = height.top / 32;
      this.lineNumber -= lineCount - 1;
      //文字滚动
      if (this.lineNo > 2) {
        ulist.style.transform =
          "translateY(" +
          (this.lineNumber + this.lineNo - this.Cpos) * this.offset +
          "px)"; //整体向上滚动一行高度
      }
    },
    //TODO: 重新播放是歌词重置事件
    goback() {
      const ulist = this.$refs.ul;
      document.querySelector(".lineHigh").removeAttribute("class");
      ulist.style.transform = "translateY(0)";
      this.lineNo = 0; //lineNo清零，重新播放
      this.lineNumber = 0;
    },
  },
};
</script>
<style scoped>
.qualitydetail {
  /* position: relative; */
  height: 100%;
}
.right-container {
  position: relative;
  margin-top: 20px;
  margin-left: 2.5%;
  margin-right: 2.2%;
  height: calc(100% - 110px);
  background: #ffffff;
  border-radius: 18px;
}
.home {
  width: 100%;
  height: 100%;
}
.back-button {
  position: absolute;
  margin-top: 2%;
  margin-left: 3.8%;
  font-size: 24px;
  cursor: pointer;
}
.left {
  margin-top: 2.4%;
  color: hsl(0, 0%, 60%);
  float: left;
  margin-left: 100px;
  cursor: pointer;
}
.audio-name {
  margin-top: 2.4%;
  margin-left: 20px;
  float: left;
  cursor: pointer;
}
.right {
  margin-top: 2.4%;
  margin-left: 20px;
  color: hsl(0, 0%, 60%);
  float: left;
  cursor: pointer;
}
.el-row .el-button {
  margin-top: 1.6%;
  margin-right: 2.2%;
  float: right;
  background: #1276d9;
  color: #ffffff;
  border-radius: 8px;
}
.left-content {
  display: block;
  position: absolute;
  height: 465px;
  width: 638px;
  background: #ffffff;
  margin-left: 30px;
  margin-top: 20px;
}
.el-divider--vertical {
  position: relative;
  left: 668px;
  margin-top: 25px;
  height: 440px;
  float: left;
}
.right-content {
  position: absolute;
  height: 445px;
  left: 680px;
  width: calc(100% - 685px);
  background: #ffffff;
  margin-top: 20px;
}
.audio {
  margin-top: 26px;
  margin-left: 14px;
  width: 595px;
  height: 42px;
  border-radius: 8px;
  /* background: #555555; */
  color: #555555;
  background-size: cover;
}
.text-content {
  margin-top: 42px;
  margin-left: 30px;
  width: 557px;
  height: 359px;
  background: #ffffff;
  text-align: center;
  font-size: 16px;
}
.el-divider--horizontal {
  margin-top: 15px;
  margin-left: 15px;
  margin-right: 30px;
  width: auto;
}
.el-tag {
  margin-left: 10px;
  margin-top: 3px;
  background: #ffffff;
  border-radius: 18px;
  font-family: NotoSansHans-Regular;
  font-size: 6px;
  color: #666666;
  text-align: center;
  cursor: pointer;
}
.test {
  padding: 0;
}
/* 歌词和音频开始 */
.detail {
  /* position: absolute; */
  height: 445px;
  left: 0;
  right: 0;
  text-align: center;
  /* color: #26a2ff; */
  /* color: black; */
  font-family: KaiTi;
  font-weight: bold;
}
.p {
  width: 100%;
  line-height: 0.8rem;
  font-size: 18px;
  color: #ffd700;
  margin-top: 0.1rem;
  text-align: center;
  /* background-color: #fff; */
}
.wrapper {
  overflow: hidden;
  margin-top: 10px;
  /* padding-top: 10px; */
  right: 0;
  left: 0;
  height: 335px;
  z-index: 1;
  /* background-color: yellow; */
}
.content {
  margin-top: -96px;
  margin-right: 60px;
  margin-left: 30px;
  /* width: 200px; */

  /* display: inline-block; */
}
.bottom_fade_reverse {
  display: inline-block;
  width: 100%;
  height: 130px;
  z-index: 99;
  position: relative;
  /* bottom: 310px; */
  background: url("../../assets/images/bottom-fade-reverse.png") bottom center
    no-repeat;
}
.bottom_fade {
  /* display: inline-block; */
  width: 100%;
  height: 100px;
  z-index: 99;
  position: absolute;
  bottom: 0px;
  background: url("../../assets/images/bottom-fade.png") bottom center no-repeat;
}
.ul {
  width: 100%;
  padding-bottom: 1rem;
}
.li {
  font-size: 14px;
  transition-duration: 600ms;
}
ul,
li {
  list-style: none;
  line-height: 32px;
  font-size: 14px;
}
.lineHigh {
  color: #3af029;
  font-size: 18px;
}
.keywordHigh {
  color: red;
}
</style>

<style>
.table-style {
  margin-top: 10px;
  position: absolute;
  width: auto;
  left: 20px;
  right: 30px;
}
.demo-table-expand {
  padding: 10px;
  height: 60px;
}
.demo-table-expand label {
  width: 50px;
  color: #99a9bf;
}
.table-style th {
  border: none;
}
.table-style td,
.table-style th.is-leaf {
  border: none;
}
.el-table--border,
.el-table--group {
  border: none;
}
.el-table--border::after,
.el-table--group::after {
  width: 0;
}
.table-style::before {
  width: 0;
}
.table-style .el-table__fixed-right::before,
.el-table__fixed::before {
  width: 0;
}
.table-style,
.el-table__expanded-cell {
  background: #ececec;
  padding: 0 !important;
}
/* 表格悬停颜色 */
.table-style tr {
  background: #f9f9f9;
}
/* 悬停备用，供选择 */
.table-style tr:hover > td {
  background-color: #ececec !important;
}
.button,
.button::after {
  border: none;
  margin: 0;
  padding: none;
}
.textarea {
  width: 50px;
}
.textarea > .el-input__inner {
  width: 50px;
  height: 28px;
  font-size: 14px !important;
  color: #000000 !important;
  font-family: cursive !important;
}
</style>