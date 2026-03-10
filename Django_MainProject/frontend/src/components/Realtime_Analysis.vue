<template>
  <div class="analysis-container">
    <button @click="backHome" class="arrow-button">返回</button>
    <!-- 标签导航 -->
    <h2 style="margin-left: 15px">数据分析(实时)</h2>
    <div class="tab-nav">
      <button
        id="defaultBtn"
        class="tab-btn"
        :class="{ active: activeTab === 'Realtime_ClickData' }"
        @click="changeTab('Realtime_ClickData')"
      >
        点击数据
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'Realtime_SearchData' }"
        @click="changeTab('Realtime_SearchData')"
      >
        搜索数据
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'Realtime_CartData' }"
        @click="changeTab('Realtime_CartData')"
      >
        购物车数据
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'Realtime_OrderData' }"
        @click="changeTab('Realtime_OrderData')"
      >
        订单数据
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'Realtime_OtherData' }"
        @click="changeTab('Realtime_OtherData')"
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
import Realtime_ClickData from "./realtime_analysis/Realtime_ClickData.vue";
import Realtime_SearchData from "./realtime_analysis/Realtime_SearchData.vue";
import Realtime_CartData from "./realtime_analysis/Realtime_CartData.vue";
import Realtime_OrderData from "./realtime_analysis/Realtime_OrderData.vue";
import Realtime_OtherData from "./realtime_analysis/Realtime_OtherData.vue";

export default {
  name: "DataAnalysis",
  components: {
    Realtime_ClickData,
    Realtime_SearchData,
    Realtime_CartData,
    Realtime_OrderData,
    Realtime_OtherData,
  },
  data() {
    return {
      activeTab: "Realtime_ClickData", // 默认激活的标签页
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
    this.changeTab("Realtime_ClickData");
  },
};
</script>

<style src="../assets/css/Realtime_Analysis.css" scoped></style>