<template>
  <div class="click-data-analysis">
    <h2>点击数据分析</h2>
    <div class="toolbar">
      <!-- <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="fetchData"
      /> -->
      <el-button type="primary" :loading="loading" @click="fetchData">
        刷新数据
      </el-button>
    </div>
    <div class="chart-container" ref="chartDom"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import request from "@/utils/request";
export default {
  name: "ClickDataAnalysis",
  data() {
    return {
      myChart: null,
      products: [],
      loading: false,
      dateRange: [new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), new Date()], // 默认最近7天
    };
  },
  mounted() {
    this.initChart();
    this.fetchData();
    window.addEventListener("resize", this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
    if (this.myChart) {
      this.myChart.dispose();
    }
  },
  methods: {
    initChart() {
      this.myChart = echarts.init(this.$refs.chartDom);
      this.myChart.showLoading(); // 显示加载动画
    },
    async fetchData() {
      try {
        this.loading = true;
        // const params = {
        //   start_date: this.formatDate(this.dateRange[0]),
        //   end_date: this.formatDate(this.dateRange[1]),
        // };

        const res = await request.get(
          "http://localhost:8000/Backend_Store/api/clickData"
        );
        this.products = res.data;
        this.updateChart();
      } catch (error) {
        console.error("获取数据失败:", error);
        this.$message.error("数据加载失败");
      }
      {
        this.loading = false;
        if (this.myChart) {
          this.myChart.hideLoading();
        }
      }
    },
    formatDate(date) {
      return date.toISOString().split("T")[0]; // 格式化为YYYY-MM-DD
    },
    updateChart() {
      if (!this.myChart) return;

      console.log("updateChart", this.products.data);
      const datax = this.products.data.map((p) => p.name);
      const datay = this.products.data.map((p) => p.interaction_count);

      const option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
          formatter: (params) => {
            const data = params[0].data;
            return `
              <div style="font-weight:bold">${params[0].name}</div>
              <div>点击量: ${data}</div>
            `;
          },
        },
        xAxis: {
          type: "category",
          data: datax,
          axisLabel: {
            interval: 0,
            rotate: 30,
            fontSize: 12,
          },
        },
        yAxis: {
          type: "value",
          name: "点击次数",
        },
        series: [
          {
            name: "点击量",
            type: "bar",
            data: datay,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: "#83bff6" },
                { offset: 1, color: "#188df0" },
              ]),
            },
            emphasis: {
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: "#2378f7" },
                  { offset: 1, color: "#093d9b" },
                ]),
              },
            },
          },
        ],
        dataZoom: [
          {
            type: "slider",
            show: true,
            xAxisIndex: 0,
            start: 0,
            end: datax.length > 10 ? 50 : 100, // 数据多时默认显示50%
          },
        ],
      };

      this.myChart.setOption(option, true);
      this.handleResize();
    },
    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    },
  },
};
</script>

<style src="../../assets/css/ClickData.css" scoped></style>