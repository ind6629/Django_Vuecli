<template>
  <div class="analysis-container">
    <button @click="backHome" class="arrow-button">返回</button>
    <!-- 标签导航 -->
    <h2 style="margin-left: 15px">数据分析(离线)</h2>
    <div class="tab-nav">
      <button
        id="defaultBtn"
        class="tab-btn"
        :class="{ active: activeTab === 'ClickData' }"
        @click="changeTab('ClickData')"
      >
        点击数据
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'SearchData' }"
        @click="changeTab('SearchData')"
      >
        搜索数据
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'CartData' }"
        @click="changeTab('CartData')"
      >
        购物车数据
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'OrderData' }"
        @click="changeTab('OrderData')"
      >
        订单数据
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'OtherData' }"
        @click="changeTab('OtherData')"
      >
        其它数据
      </button>
    </div>

    <!-- 动态组件容器 -->
    <div class="content-box">
      <component :is="activeComponent" />
    </div>
  </div>
</template>

<script>
// 导入子组件
import ClickData from "./analysis/ClickData.vue";
import SearchData from "./analysis/SearchData.vue";
import CartData from "./analysis/CartData.vue";
import OrderData from "./analysis/OrderData.vue";
import OtherData from "./analysis/OtherData.vue";

export default {
  name: "DataAnalysis",
  components: {
    ClickData,
    SearchData,
    CartData,
    OrderData,
    OtherData,
  },
  data() {
    return {
      activeTab: "ClickData", // 默认激活的标签页
    };
  },
  computed: {
    activeComponent() {
      return this.activeTab; // 直接返回组件名
    },
  },
  methods: {
    changeTab(tabName) {
      this.activeTab = tabName;
      // 这里可以添加标签切换时的额外逻辑
      // 例如：加载数据、重置状态等
    },
    backHome() {
      this.$router.push("/Home");
      setTimeout(() => window.location.reload(), 100);
    },
  },
  mounted() {
    // 初始化默认标签页
    this.changeTab("ClickData");
  },
};
</script>

<style src="../assets/css/Analysis.css" scoped></style>