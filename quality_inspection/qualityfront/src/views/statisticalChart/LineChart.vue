<template>
  <div :class="className" :style="{ height: height, width: width }"></div>
</template>

<script>
const echarts = require("echarts/lib/echarts");
require("echarts/lib/component/title");
require("echarts/lib/component/toolbox");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/grid");
require("echarts/lib/component/legend");
require("echarts/lib/chart/line");
require("echarts/lib/component/markLine");
require("echarts/lib/component/markPoint");
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
      default: "100%",
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
      var chartDom = document.getElementById("lineChart");
      var myChart = echarts.init(chartDom);
      var option;

      option = {
        title: {
          text: "30天均分展示",
          textStyle: {
            fontSize: 14, //大小
            align: "center", //水平对齐
          },
        },
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            magicType: { type: ["line", "bar"] },
            restore: {},
            saveAsImage: {},
          },
        },
        legend: {
          data: ["平均分"],
        },
        grid: {
          height: "50%",
        },
        xAxis: {
          type: "category",
          data: [
            "04-11",
            "04-12",
            "04-13",
            "04-14",
            "04-15",
            "04-16",
            "04-17",
            "04-18",
            "04-19",
            "04-20",
            "04-21",
            "04-22",
            "04-23",
            "04-24",
            "04-25",
            "04-26",
            "04-27",
            "04-28",
            "04-29",
            "04-30",
            "05-01",
            "05-02",
            "05-03",
            "05-04",
            "05-05",
            "05-06",
            "05-07",
            "05-08",
            "05-09",
            "05-10",
            "05-11",
          ],
        },
        yAxis: {
          type: "value",
          min: "70",
          max: "90",
          splitNumber: 2,
        },
        series: [
          {
            data: [
              80,
              81,
              78,
              89,
              88,
              87,
              88,
              89,
              88,
              87,
              88,
              89,
              88,
              87,
              88,
              75,
              73,
              76,
              77,
              75,
              73,
              75,
              76,
              75,
              73,
              78,
              78,
              79,
              75,
              74,
              78,
              74,
              75,
              77,
            ],
            type: "line",
            name: "平均分",
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
