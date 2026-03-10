<template>
  <div class="search-data-analysis">
    <h2>搜索数据分析</h2>
    <div class="toolbar">
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
  name: "SearchDataAnalysis",
  data() {
    return {
      records: [],
      loading: false,
      dateRange: [
        new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 默认最近7天
        new Date(),
      ],
      myChart: null,
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
      this.myChart = echarts.init(this.$refs.chartDom, null, {
        renderer: "canvas",
        useDirtyRect: true, // 启用脏矩形渲染优化性能
        passive: true, // 解决wheel事件警告
      });
      this.myChart.showLoading();
    },

    async fetchData() {
      try {
        this.loading = true;
        // const params = {
        //   start_date: this.formatDate(this.dateRange[0]),
        //   end_date: this.formatDate(this.dateRange[1]),
        // };

        const res = await await request.get(
          "http://localhost:8000/Backend_Store/api/searchData"
        );
        this.records = res.data.data;
        this.updateChart();
        //console.log(this.records);
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
      return date.toISOString().split("T")[0]; // YYYY-MM-DD
    },

    updateChart() {
      if (!this.myChart || !this.records.length) return;

      // 准备数据 - 按搜索量降序排序
      const sortedRecords = [...this.records].sort(
        (a, b) => b.search_count - a.search_count
      );
      const categories = sortedRecords.map((r) => r.category);
      const counts = sortedRecords.map((r) => r.search_count);

      const option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
          formatter: (params) => {
            const data = params[0];
            return `
              <div style="font-weight:bold">${data.name}</div>
              <div>搜索次数: ${data.value}</div>
            `;
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        yAxis: {
          type: "category",
          data: categories,
          axisLabel: {
            interval: 0,
            rotate: 0,
          },
        },
        xAxis: {
          type: "value",
          name: "搜索次数",
        },
        series: [
          {
            name: "搜索量",
            type: "bar",
            data: counts,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: "#83bff6" },
                { offset: 1, color: "#188df0" },
              ]),
            },
            label: {
              show: true,
              position: "right",
            },
          },
        ],
        dataZoom: [
          {
            type: "slider",
            yAxisIndex: 0,
            filterMode: "filter",
            start: 0,
            end: 100,
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

<style src="../../assets/css/SearchData.css" scoped></style>