<template>
  <div class="sider">
    <div style="font-size: 0">
      <el-menu
        :default-active="routerPath"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
        :collapse="isCollapse"
        @select="handleSelect"
      >
        <el-menu-item index="/uploadaudio" @click="jump('/uploadaudio')">
          <i class="el-icon-mic"></i>
          <span slot="title">录音上传</span>
        </el-menu-item>
        <el-menu-item index="/scoredirectory" @click="jump('/scoredirectory')">
          <i class="el-icon-star-off"></i>
          <span slot="title">质检评分</span>
        </el-menu-item>
        <el-menu-item index="/planquality" @click="jump('/planquality')">
          <i class="el-icon-setting"></i>
          <span slot="title">质检方案</span>
        </el-menu-item>
        <el-menu-item index="/statisticalscore" @click="jump('/statisticalscore')">
          <i class="el-icon-pie-chart"></i>
          <span slot="title">质检图表</span>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>
<script>
import logo from "../assets/images/logo.png";
import logo1 from "@/assets/images/logo1.png";
export default {
  name: "Sider",
  props: {
    isCollapse: {
      type: Boolean,
      required: true,
      default(){
        return false
      }
    },
  },
  data() {
    return {
      logo,
      logo1,
      activeIndex: "",
      // isCollapse:true
    };
  },
  mounted(){
    console.log(this.isCollapse)
  },
  watch: {
    $route() {
      this.handleSelect(this.activeIndex);
    },
  },
  computed: {
    routerPath() {
      return this.$route.meta.guidePath
        ? this.$route.meta.jumpPath
        : this.$route.path;
    },
  },
  methods: {
    // TODO:路由跳转
    jump(url) {
      this.$router.push({
        path: url,
      });
    },
    // TODO:菜单收起
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    handleSelect(index) {
      this.activeIndex = index;
    },
  },
};
</script>
<style >
.sider {
  height: calc(100% - 80px);
}
.aside-logo {
  position: relative;
  width: 102.5px;
  height: 38px;
  padding-top: 10px;
  padding-left: 20px;
}
.el-menu {
  background: #1a2638;
  width: 100%;
  height: 150px;
}
.el-menu-vertical-demo {
  background-color: #1a2638;
  width: 82px;
  margin-top: 20px;
  border-right: 0;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 256px;
  height: 100%;
  position: relative;
}

.horizontal-collapse-transition {
  transition: 0.5s width ease-in-out, 0.5s padding-left ease-in-out,
    0.5s padding-right ease-in-out;
}
.el-submenu {
  font: 5px;
  color: #ffffff;
}
.el-submenu span {
  font: 5px sans-serif;
  color: #ffffff;
}
.el-menu-item {
  font: 5px;
  color: #ffffff;
  background: #1a2638;
  padding-left: 23px;
}
.el-menu-item:focus,
.el-menu-item:hover {
  background: #1a2638;
}
.el-message-box {
  border-radius: 16px;
}
.el-dialog {
  border-radius: 16px;
}
/* //滚动条的宽度 */
::-webkit-scrollbar {
  width: 0px;
  height: 10px;
}
/* //滚动条的滑块 */
::-webkit-scrollbar-thumb {
  background-color: #a1a3a9;
  border-radius: 3px;
}
</style>