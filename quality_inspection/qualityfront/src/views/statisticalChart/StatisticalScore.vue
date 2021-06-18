<template>
  <div class="statisticalscore">
    <el-row :gutter="32" class="panel-group">
      <el-col :xs="24" :sm="24" :lg="10" class="card-panel-col">
        <div class="header-left">总平均分：{{ 80.36 }}</div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="14" class="card-panel-col">
        <div class="header-right">
        <el-date-picker
            v-model="time"
            size="mini"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          >
          </el-date-picker>
        <el-button type="primary" size="mini" icon="el-icon-search" round @click="search" style="display:inline-block;margin-left:20px;">查询</el-button>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="32" class="panel-group">
      <el-col :xs="24" :sm="24" :lg="10">
        <div id="barChart" class="chart-wrapper-bar">
          <bar-chart />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="14">
        <div id="pieChart" class="chart-wrapper">
          <pie-chart />
        </div>
        <div id="lineChart" class="chart-wrapper">
          <line-chart />
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="32" class="panel-group">
      <el-col :xs="24" :sm="24" :lg="24" style="margin-bottom:8px">  
      <div id="histogram" class="chart-wrapper-histogram">
        <Histogram />
      </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import LineChart from '../statisticalChart/LineChart'
import PieChart from '../statisticalChart/PieChart'
import BarChart from '@/views/statisticalChart/BarChart'
import Histogram from '../statisticalChart/Histogram'
import Axios from '../../js/Axios'
export default {
  name: 'statusticalscore',
  //import引入的组件
  components: {
    BarChart,
    PieChart,
    LineChart,
    Histogram
  },
  data() {
    return {
      time:'',
    };
  },
  //方法集合
  methods: {
    search(){
      let time = this.time;
      const querystring = require("querystring");
      Axios.post(
        "/api/planController/planList",
        querystring.stringify({
          time: time,
        })
      )
        .then((res) => {
          console.log(res);
          if (res.data.result.code === 200) {
            this.total = res.data.result.data.total;
            console.log(this.total);
            this.getList = res.data.result.data.content;
            console.log(this.getList);
            this.showTable();
          } else if (res.data.result.code === 400) {
            this.$alert("请输入正确的任务名称！", "提示", {
              confirmButtonText: "确定",
              callback: (action) => {},
            });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    }
  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {},
};
</script>
<style lang="scss" scoped>
.statisticalscore {
  padding: 32px;
  position: relative;
  .panel-group {
    position: relative;
    box-sizing: border-box;
    margin-left: -16px;
    margin-right: -16px;
    .card-panel-col{
      margin-bottom: 32px;
    }
  }
  .header-left {
    background: #fff;
    padding: 16px 0 16px 0;
    text-align: center;
    vertical-align: middle;
    font-size:21px;
    font-weight:700
  }
  .header-right {
    background: rgb(255, 255, 255);
    padding: 16px 0 16px 0;
    text-align: center;
  }
  .chart-wrapper-bar {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
    height: 400px;
  }
  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
    height: 176px;
  }
  .chart-wrapper-histogram{
    background: #fff;
    padding: 16px 16px 0;
    height: 200px;
  }
}
@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>