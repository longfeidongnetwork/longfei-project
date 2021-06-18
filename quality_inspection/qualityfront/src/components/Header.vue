<template>
  <div class="header">
    <div :class="isCollapse?'header-left':'not-header-left'">
        <transition name="sidebarLogoFade">
          <div
            v-if="isCollapse"
            key="iscollapse"
          >
            <img  :src="logo1" class="sidebar-logo1" />
              <i class="el-icon-s-unfold expandBtn" @click="collapseMethod"></i>
          </div>
          <router-link v-else key="expand" to="">
            <img :src="logo" class="sidebar-logo" />
              <h1 style="display: inline-block" class="sidebar-title">
                {{ title }}
              </h1>
              <i class="el-icon-s-fold shrinkBtn" @click="collapseMethod"></i>
          </router-link>
        </transition>
    </div>
    <div class="header-right">
      <img class="avatarImg" :src="avatarImg" alt />
      <span class="avatarName">Evan You</span>
      <span class="loginOut" @click="centerDialogVisible = true">
        <i style="margin-right: 20px" class="el-icon-switch-button"></i>
      </span>
    </div>
    <el-dialog
      title="提示"
      :visible.sync="centerDialogVisible"
      width="30%"
      center
    >
      <span>是否确认退出系统？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="loginOut">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import avatarImg from "../assets/images/boy.png";
import Axios from "../js/Axios";
import logo from "../assets/images/logo.png";
import logo1 from "@/assets/images/logo1.png";
export default {
  name: "Header",
  data() {
    return {
      avatarImg,
      centerDialogVisible: false,
      logo,
      logo1,
      isCollapse: false,
      title: "语音质检系统",
    };
  },
  created() {
    this.account = this.$route.query.account;
    this.password = this.$route.query.password;
  },
  mounted() {},
  methods: {
    // TODO:折叠展开
    collapseMethod() {
      this.isCollapse = !this.isCollapse;
      this.$emit("fatherMethod", this.isCollapse);
    },
    //退出接口
    loginOut() {
      //发送请求
      Axios.post("/api/loginController/loginOut")
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.$message({
              title: "成功",
              message: "恭喜，退出成功！",
              duration: 3000,
              type: "success",
            });
            setTimeout(() => {
              this.$router.push({
                name: "Login",
              });
            }, 500);
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
.header {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
}
.header-left {
  width: 82px;
  background: #1a2638;
  transition: 0.5s width ease-in-out, 0.5s padding-left ease-in-out,
    0.5s padding-right ease-in-out;
}
.not-header-left {
  width: 256px;
  background: #1a2638;
  transition: 0.5s width ease-in-out, 0.5s padding-left ease-in-out,
    0.5s padding-right ease-in-out;
}
.header-right {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  text-align: right;
  background: linear-gradient(to right, rgb(26, 39, 56), rgb(52, 152, 219));
}
.avatarImg {
  border-radius: 50%;
  height: 30px;
  width: 30px;
}
.avatarName {
  margin-left: 10px;
  margin-right: 10px;
  color: #fff;
}
.avatarName:hover {
  color: #4bb0ff;
}
.header-right span {
  color: #fff;
  cursor: pointer;
}
.header-right .loginOut:active {
  box-shadow: 0 0 3px #333;
}

.sidebarLogoFade-enter-active {
  transition: opacity 1.5s;
}

.sidebarLogoFade-enter,
.sidebarLogoFade-leave-to {
  opacity: 0;
}

.sidebar-logo-container {
  width: 256px;
  height: 80px;
}
.sidebar-logo {
  margin-left: 20px;
  width: 112px;
  height: 32px;
  margin-right: 124px;
  margin-top: 15px;
}
.sidebar-logo1 {
  width: 32px;
  height: 32px;
  margin-right: 30px;
  margin-left: 20px;
  padding-top: 15px;
}

.sidebar-title {
  margin-left: 20px;
  /* margin: 0; */
  color: #fff;
  font-weight: 600;
  font-size: 18px;
  margin-top: 5px;
  margin-right: 105px;
}

.collapse .sidebar-logo {
  margin-left: 0px;
}
/* 菜单折叠 */

.shrinkBtn {
  background: #1a2638;
  border: none;
  outline: none;
  color: #999999;
  cursor: pointer;
  font-size: 20px;
  position: fixed;
  margin-top: 10px;
}
.expandBtn {
  padding-top: 10px;
  margin-left: 22px;
  background: #1a2638;
  border: none;
  color: #999999;
  outline: none;
  cursor: pointer;
  font-size: 20px;
  display: block;
}
</style>