<template>
  <div class="Layout">
    <el-container>
      <el-header height="80px">
          <Header @fatherMethod="change($event)"></Header>
        </el-header>
      <el-container>
        <el-aside width='auto'>
        <Sider :isCollapse="isCollapse"></Sider>
      </el-aside>
        <el-main>
          <transition name="fade">
            <keep-alive>
            <router-view></router-view>
          </keep-alive>
          </transition>
          
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<script>
import Sider from "@/components/Sider.vue";
import Header from "@/components/Header.vue";
export default {
  name: "Layout",
  components: {
    Sider,
    Header,
  },
  data() {
    return {
      isCollapse:false,
    };
  },
  methods: {
    change(data){
      this.isCollapse = data;
      console.log(this.isCollapse);
    },
  },
};
</script>
<style scoped>
.Layout {
  width: 100%;
  height: 100vh;
  position: relative;
}
.el-container {
  overflow: hidden;
  height: 100%;
  position: relative;
}
.el-aside {
  background-color: #1a2638;
}
.el-header {
  padding: 0;
  width: 100%;
  /* background: linear-gradient(to right, rgb(26, 39, 56), rgb(52, 152, 219)); */
}
.el-main {
  background-color: #f6f6f6;
  padding: 0;
  overflow-y: scroll;
}
.fade-enter, .fade-leave-to {
  opacity: 0
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s
}
</style>