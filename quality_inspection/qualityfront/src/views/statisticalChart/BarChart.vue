<template>
  <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
const echarts = require("echarts/lib/echarts");
require("echarts/lib/component/title");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/grid");
require("echarts/lib/component/legend");
require("echarts/lib/chart/bar");

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
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    this.drawLine();
  },
  //方法集合
  methods: {
    drawLine() {
      var chartDom = document.getElementById("barChart");
      var myChart = echarts.init(chartDom);
      var option;
      option = {
        title: {
          text: "平均分排行榜",
          textStyle: {
            fontSize: 14, //大小
            align: "center", //水平对齐
          },
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        color: "#3490de",
        legend: {
          data: ["姓名"],
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "value",
          boundaryGap: [0, 0.01],
        },
        yAxis: {
          type: "category",
          data: [
            "居凤霞",
            "陈冬",
            "刘路",
            "许杰",
            "张晗",
            "倪港香",
            "冉嫣然",
            "李晶",
            "李俊杰",
            "王玉淑",
            "谢雨婷",
            "朱玲",
          ],
        },
        series: [
          {
            name: "姓名",
            type: "bar",
            data: [
              18203,
              23489,
              29034,
              34970,
              35970,
              43970,
              44567,
              47780,
              58790,
              63340,
              66780,
              70000,
            ],
            // itemStyle: {
            //   normal: {
            //     color: function (params) {
            //       var colorList = ["#3490de"];
            //       return colorList[params.dataIndex % colorList.length];
            //     },
            //   },
            // },
          },
          //   {
          //     name: "2012年",
          //     type: "bar",
          //     data: [19325, 23438, 31000, 121594, 134141, 681807],
          //   },
        ],
      };

      option && myChart.setOption(option);
    },
  },
};
</script>