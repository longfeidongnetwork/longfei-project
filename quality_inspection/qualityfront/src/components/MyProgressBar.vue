<template>
  <el-progress :percentage="percentage" :stroke-width="strokeWidth" >
  </el-progress>
</template>

<script>
export default {
  name: 'MyProgressBar',
  props: ['reload', 'percentage', 'strokeWidth'],
  watch: {
    reload: function (val) {
      this.$forceUpdate()	// 强制刷新
    }
  }
}
</script>

<style scoped>
</style>
