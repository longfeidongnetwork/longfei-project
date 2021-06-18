<template>
  <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
const echarts = require("echarts/lib/echarts");
require("echarts/lib/component/title");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/legend");
require("echarts/lib/chart/pie");
export default {
  //import引入的组件
  components: {},
  props: {
    className: {
      type: String,
      defualt: "chart",
    },
    width: {
      type: String,
      default: "100%",
    },
    height: {
      type: String,
      default: "300px",
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  activated() {
    // this.drawLine();
  },
  //方法集合
  methods: {
    drawLine() {
      var chartDom = document.getElementById("pieChart");
      var myChart = echarts.init(chartDom);
      var option;
      option = {
        title: {
          text: "扣分占比分析",
          textStyle: {
            fontSize: 14, //大小
            align: "center", //水平对齐
          },
          left: "right",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        color: [
          "#7a81f0",
          "#44cef6",
          "#f0a786",
          "#6ebaf0",
          "#177cb0",
          "#f0d156",
          "#62f0df",
          "#8da4da",
          "#ffa400",
          "#4b5cc4",
          "#fffbf0",
          "#f47983"
          
        ],
        series: [
          {
            name: "访问来源",
            type: "pie",
            radius: "60%",
            center: ["65%", "50%"],
            data: [
              { value: 1048, name: "稍后评价" },
              { value: 735, name: "结束语" },
              { value: 580, name: "开场白" },
              { value: 484, name: "无应答" },
              { value: 300, name: "吸烟调查" },
              { value: 345, name: "禁用语句" },
              { value: 548, name: "声音小" },
              { value: 124, name: "明显搪塞、应付、推诿" },
              { value: 678, name: "敬语" },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };

      option && myChart.setOption(option);
    },
  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    this.drawLine();
  },
};
</script>
<style >
</style>