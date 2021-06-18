<template>
  <div class="main">
    <img :src="loginPicture" class="background-picture" alt />
    <div class="login">
      <div class="left">
        <div class="el-row">
          <img :src="logo1" style="width: 100px; height: 32px" alt />
        </div>
        <div>
          <img :src="loginElement" class="login-element" alt />
        </div>
      </div>
      <div class="right">
        <h3 style="text-align: left; margin-top: 30px">质检语音分析系统</h3>
        <el-form ref="form" :model="form" style="margin-top: 35px">
          <el-form-item>
            <el-input
             id="login_name"
              prefix-icon="el-icon-user"
              v-model="login_name"
              placeholder="请输入用户名"
              class="input-style"
            />
          </el-form-item>
          <el-form-item>
            <el-input
              id="login_pwd"
              type="password"
              prefix-icon="el-icon-lock"
              v-model="login_pwd"
              placeholder="请输入密码"
              class="input-style"
              @keyup.enter.native="login()"
            />
          </el-form-item>
          <!-- <el-form-item>
            <label class="inline">
              <input type="checkbox" class="ace" id="remb_me" />
              <span class="lbl"> 记住我</span>
            </label> 
          </el-form-item> -->
          <el-form-item>
            <el-button
              style="width: 200px; margin-top: 30px"
              type="primary"
              @click="login()"
              >登 录</el-button
            >
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import Axios from "../js/Axios";
import loginPicture from "../assets/images/login.png";
import loginElement from "../assets/images/loginelement.png";
import logo1 from "../assets/images/logo-01.png";
export default {
  name: "login",
  data() {
    return {
      logo1,
      loginPicture,
      loginElement,
      login_name: "",
      login_pwd: "",
      repeat: "",
      form: {},
    };
  },
  methods: {
    login() {
      console.log("执行登录");
      var username = this.login_name;
      var password = this.login_pwd;
      if (username && password) {
        //发送请求
        const querystring = require("querystring");
        Axios.post(
          "/api/loginController/myLogin",
          querystring.stringify({
            username: username,
            password: password
          })
        )
          .then((res) => {
            console.log(res);
            if (res.data.code === 200) {
              this.$message({
                title: "成功",
                message: "恭喜，登陆成功！",
                duration: 3000,
                type: "success"
              });
              setTimeout(() => {
                this.$router.push({
                  name: "uploadaudio"
                });
              }, 500);
            } else if (res.data.result.code === 400) {
              this.$message({
                title: "登陆失败",
                message: "请重新输入用户名和密码！",
                type: "error"
              });
            }
          })
          .catch(function (err) {
            console.log(err);
          });
      }
    },
  },
};
</script>
 
<style scoped>
.main {
  width: 100vw;
  height: 100vh;
}
.background-picture {
  width: 100vw;
  height: 100vh;
}
.login {
  width: 722px;
  height: 358px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  box-shadow: 0 2px 8px 0;
  border-radius: 10px;
}
.left {
  width: 445px;
  height: 100%;
  display: inline-block;
}
.el-row {
  height: 30px;
  padding-left: 40px;
  margin-top: 25px;
}
.login-element {
  width: 400px;
  height: 277px;
  margin-left: 42px;
  margin-top: 5px;
}
.right {
  left: 445px;
  margin-left: 30px;
  width: 277px;
  height: 100%;
  display: inline-block;
  position: absolute;
}
.input-style {
  width: 200px;
  border: none;
  outline: none;
  margin-top: 22px;
}
.input-style .el-input__inner {
  background: #ffffff !important;
}
.el-form .el-form-item{
  margin-bottom: 0;
}
</style>