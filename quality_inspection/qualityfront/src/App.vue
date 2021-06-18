<template>
  <div id="app">
    <!-- <img src="./assets/input-bg.png" height="50px" width="12000px"> -->
    <router-view v-if="isRouterAlive"></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  provide() {
    return {
      reload: this.reload,
    };
  },
  data() {
    return {
      isRouterAlive: true,
    };
  },
  methods: {
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(function () {
        this.isRouterAlive = true;
      });
    },
  },
};
</script>

<style>
/* html,
body {
  margin: 0;
  width: 100vw;
  height: 100%;
  overflow: hidden;
} */
html {
  overflow-x: hidden;
  overflow-y: auto;
}
body {
  margin: 0;
  width: 100vw;
  overflow: hidden;
  padding-left: calc(100vw - 100%);
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}
</style>
