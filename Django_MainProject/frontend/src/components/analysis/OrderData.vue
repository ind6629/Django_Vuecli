<template>
  <div class="order-analysis">
    <h2>订单数据分析</h2>
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
  name: "OrderAnalysis",
  data() {
    return {
      orders: [],
      loading: false,
      dateRange: [
        new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // 默认最近30天
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
        useDirtyRect: true,
        passive: true,
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
          "http://localhost:8000/Backend_Store/api/orderData"
        );
        this.orders = res.data.data;
        console.log(this.orders);
        this.updateChart();
      } catch (error) {
        console.error("获取订单数据失败:", error);
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
      if (!this.myChart || !this.orders.length) return;

      const dates = [...new Set(this.orders.map((o) => o.date))].sort();
      const categories = [...new Set(this.orders.map((o) => o.category))];

      // 按日期和类别组织数据
      const seriesData = categories.map((category) => {
        return {
          name: category,
          type: "line",
          data: dates.map((date) => {
            const order = this.orders.find(
              (o) => o.date === date && o.category === category
            );
            return order
              ? {
                  value: order.count,
                  label: {
                    show: true,
                    formatter: category,
                    position: "top",
                  },
                }
              : 0;
          }),
          smooth: true,
          symbolSize: 8,
          lineStyle: {
            width: 3,
          },
        };
      });

      const option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
          },
        },
        legend: {
          data: categories,
          top: "bottom",
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "15%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          data: dates,
          axisLabel: {
            rotate: 30,
          },
        },
        yAxis: {
          type: "value",
          name: "订单数量",
        },
        series: seriesData,
      };

      this.myChart.setOption(option);
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

<style src="../../assets/css/OrderData.css" scoped></style>