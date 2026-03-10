<template>
  <div class="search-page">
    <!-- 返回按钮 -->
    <router-link to="/Home" class="arrow-button">返回</router-link>

    <!-- 搜索框 -->
    <div class="search-container">
      <form @submit.prevent="handleSearch" class="search-form">
        <div class="search-input-group">
          <input
            type="text"
            v-model="searchKeyword"
            class="search-input"
            placeholder="没有想要的结果？请再次搜索商品名称、品牌或型号..."
            autocomplete="off"
            aria-label="商品搜索"
          />
          <button type="submit" class="search-button">
            <svg class="search-icon" viewBox="0 0 24 24">
              <path
                d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 0 0 1.48-5.34c-.47-2.78-2.79-5-5.59-5.34a6.505 6.505 0 0 0-7.27 7.27c.34 2.8 2.56 5.12 5.34 5.59a6.5 6.5 0 0 0 5.34-1.48l.27.28v.79l4.25 4.25c.41.41 1.08.41 1.49 0 .41-.41.41-1.08 0-1.49L15.5 14zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
              />
            </svg>
          </button>
        </div>
      </form>
    </div>

    <!-- 搜索结果 -->
    <h2 v-if="searchKeyword" style="margin-left: 15px">
      关于"{{ searchKeyword }}"的搜索结果：
    </h2>
    <h2 v-else style="margin-left: 15px">请输入搜索关键词</h2>

    <div class="tab-container">
      <div class="tab-content">
        <div class="tab-pane active">
          <!-- 加载状态 -->
          <div v-if="loading" class="loading">加载中...</div>

          <!-- 搜索结果 -->
          <div v-else-if="products.length > 0" class="product-grid">
            <div
              v-for="product in products"
              :key="product.id"
              class="product-item"
            >
              <router-link
                :to="{ name: 'ProductDetail', params: { id: product.id } }"
                class="product-link"
              >
                <img
                  :src="product.image"
                  :alt="product.name"
                  class="product-image"
                />
                <h3>{{ product.name }}</h3>
                <p class="price">¥{{ product.price }}</p>
                <p class="stock">库存: {{ product.stock }}</p>
              </router-link>
            </div>
          </div>

          <!-- 无结果提示 -->
          <div v-else class="no-results">
            <h1>暂无结果，请更换搜索内容</h1>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchPage",
  data() {
    return {
      searchKeyword: "",
      products: [],
      loading: true,
    };
  },
  created() {
    this.fetchSearchResults();
  },
  methods: {
    // 处理搜索提交
    handleSearch() {
      this.fetchSearchResults();
    },

    // 获取搜索结果
    async fetchSearchResults() {
      this.searchKeyword = sessionStorage.getItem("searchKeyword");
      const user_id = sessionStorage.getItem("user_id");
      const formData = new URLSearchParams();
      formData.append("searchKeyword", this.searchKeyword);
      formData.append("user_id", user_id);
      const response = await fetch(
        "http://localhost:8000/Backend_Store/api/search",
        {
          method: "POST",
          credentials: "include", // 必须
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            //"X-CSRFToken": this.getCookie("csrftoken") || "",
          },
          body: formData,
        }
      );
      const data = await response.json();
      console.log(data);
      if (data.status == "success") {
        console.log("搜索商品数据成功");
        this.loading = false;
        this.products = data.products;
      } else {
        this.operateMessage("搜索商品数据失败", "error");
      }
    },
    operateMessage(message, type) {
      this.$message({
        message: message,
        type: type,
      });
    },
  },
};
</script>
<style src="../assets/css/Search.css" scoped></style>