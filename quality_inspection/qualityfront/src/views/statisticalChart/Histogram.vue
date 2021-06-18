<template>
  <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
const echarts = require("echarts/lib/echarts");
require("echarts/lib/component/dataset");
require("echarts/lib/component/title");
require("echarts/lib/component/grid");
require("echarts/lib/component/dataZoom");
require("echarts/lib/chart/bar");

export default {
  //import引入的组件
  components: {},
  props: {
    className: {
      type: String,
      default: "chart",
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
      var chartDom = document.getElementById("histogram");
      var myChart = echarts.init(chartDom);
      var option;
      option = {
        title: {
          text: "当月通话量",
          textStyle: {
            fontSize: 14, //大小
            align: "center", //水平对齐
          },
          // left: 'center',
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
          data: ["数量"],
        },
        grid: {
          height: "50%",
        },
        dataset: [
          {
            dimensions: ["name", "age", "profession", "score", "date"],
            source: [
              ["蒋梦颖", 41, "Engineer", 1394, "2011-02-12"],
              ["许杰", 20, "Teacher", 1351, "2011-03-01"],
              ["李晶", 52, "Musician", 1287, "2011-02-14"],
              ["冉嫣然", 37, "Teacher", 1219, "2011-02-18"],
              ["李俊杰", 25, "Engineer", 1153, "2011-04-02"],
              ["倪港香", 19, "Teacher", 1123, "2011-01-16"],
              ["谢雨婷", 71, "Engineer", 1065, "2011-03-19"],
              ["张晗", 36, "Musician", 1018, "2011-02-24"],
              ["朱玲", 67, "Engineer", 966, "2011-03-12"],
              ["王玉漱", 41, "Engineer", 914, "2011-02-12"],
              ["王沛", 20, "Teacher", 851, "2011-03-01"],
              ["张茜云", 52, "Musician", 787, "2011-02-14"],
              ["陈东", 37, "Teacher", 719, "2011-02-18"],
              ["苏乔欣", 25, "Engineer", 653, "2011-04-02"],
              ["沈鸿云", 19, "Teacher", 645, "2011-01-16"],
              ["徐洋", 71, "Engineer", 565, "2011-03-19"],
              ["刘路", 36, "Musician", 318, "2011-02-24"],
              ["居风霞", 67, "Engineer", 36, "2011-03-12"],
            ],
          },
        ],
        xAxis: {
          type: "category",
          axisLabel: {
            interval: 0,
            rotate: 30,
          },
        },
        yAxis: {
          min: "0",
          max: "1600",
          splitNumber: 8,
        },
        series: [
          {
            name:"数量",
            type: "bar",
            barWidth : 20,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: "#83bff6" },
                { offset: 0.5, color: "#188df0" },
                { offset: 1, color: "#188df0" },
              ]),
            },
            emphasis: {
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: "#2378f7" },
                  { offset: 0.7, color: "#2378f7" },
                  { offset: 1, color: "#83bff6" },
                ]),
              },
            },
            encode: { x: "name", y: "score" },
            datasetIndex: 0,
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