<template>
  <div class="cart-analysis">
    <h2>购物车商品分析</h2>
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
  name: "Realtime_CartData",
  data() {
    return {
      carts: [],
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
        useDirtyRect: true,
        passive: true,
      });
      this.myChart.showLoading();
    },

    async fetchData() {
      try {
        this.loading = true;
        const res = await await request.get(
          "http://localhost:8000/Backend_Store/api/realtime_cartData"
        );
        this.carts = res.data.data;
        this.updateChart();
        console.log(this.carts);
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
      if (!this.myChart || !this.carts.length) return;

      const listData = this.carts.map((cart) => ({
        name: cart.category,
        value: cart.times,
      }));

      const option = {
        title: {
          text: "购物车中商品分析",
          subtext: "商品类别占比",
          left: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: (params) => {
            return `
              <div style="font-weight:bold">${params.name}</div>
              <div>数量: ${params.value}</div>
              <div>占比: ${params.percent}%</div>
            `;
          },
        },
        legend: {
          orient: "vertical",
          left: "left",
          data: listData.map((item) => item.name),
        },
        series: [
          {
            name: "具体数量",
            type: "pie",
            radius: ["40%", "70%"], // 环形饼图
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: true,
              formatter: "{b}: {c} ({d}%)",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: "18",
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: true,
            },
            data: listData,
          },
        ],
        graphic: [
          {
            type: "text",
            left: "center",
            top: "40%",
            style: {
              text: "总商品数",
              textAlign: "center",
              fill: "#333",
              fontSize: 20,
            },
          },
          {
            type: "text",
            left: "center",
            top: "50%",
            style: {
              text: listData.reduce((sum, item) => sum + item.value, 0),
              textAlign: "center",
              fill: "#1890ff",
              fontSize: 28,
              fontWeight: "bold",
            },
          },
        ],
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

<style src="../../assets/css/Realtime_CartData.css" scoped></style>