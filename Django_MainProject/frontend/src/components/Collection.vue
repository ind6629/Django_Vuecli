<template>
  <div class="collection-page">
    <button @click="backHome" class="arrow-button">返回</button>
    <div class="collection-container">
      <h1 class="collection-title">我的收藏</h1>
      <div v-if="collections.length" class="collection-grid">
        <div
          v-for="item in collections"
          :key="item.product.id"
          class="collection-item"
          :data-product-id="item.product.id"
        >
          <div class="item-image-container">
            <img
              :src="item.product.image"
              :alt="item.product.name"
              class="item-image"
            />
            <button
              class="remove-collection-btn"
              title="取消收藏"
              @click.stop="removeCollection(item.product.id)"
            >
              <i class="fas fa-heart"></i>
            </button>
          </div>

          <div class="item-info">
            <h3 class="item-name">{{ item.product.name }}</h3>
            <div class="item-price-stock">
              <span class="item-price"
                >¥{{ item.product.price.toFixed(2) }}</span
              >
              <span
                class="item-stock"
                :class="{ 'out-of-stock': item.product.stock <= 0 }"
              >
                {{
                  item.product.stock > 0
                    ? `库存: ${item.product.stock}件`
                    : "已售罄"
                }}
              </span>
            </div>
          </div>

          <div class="item-actions">
            <button
              class="add-to-cart-btn"
              :disabled="item.product.stock <= 0"
              @click="addToCart(item.product.id)"
            >
              加入购物车
            </button>
            <button
              class="view-detail-btn"
              @click="productDetail(item.product.id)"
            >
              查看详情
            </button>
          </div>
        </div>
      </div>
      <div v-else class="empty-collection">
        <img src="#" alt="空收藏" />
        <p>您还没有收藏任何商品</p>
      </div>
    </div>
    <div class="cartBox">
      <button class="animated-arrow-btn" @click="enterCart">
        <span>前往购物车</span>
        <div class="arrow">
          <span></span>
          <span></span>
        </div>
      </button>
    </div>

    <div v-if="toast.show" :class="['toast', toast.type]">
      {{ toast.message }}
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";

export default {
  name: "CollectionPage",
  data() {
    return {
      collections: [],
      removeCollectionUrl: "/collect/remove",
      toast: {
        show: false,
        message: "",
        type: "success",
      },
      collectUrl: "/cart",
      current_user: {},
    };
  },
  created() {
    this.fetchUserData();
  },
  methods: {
    async fetchCollections() {
      try {
        const response = await request.get(
          "http://localhost:8000/Backend_Store/api/collections/" +
            this.current_user.user_id
        );
        this.collections = response.data;
      } catch (error) {
        console.error("Error fetching collection data:", error);
      }
    },
    async fetchUserData() {
      try {
        const response = await request.get(
          "http://localhost:8000/Backend_Store/api/checkLogin"
        );
        if (response.data.user_id != "-1") {
          this.current_user = response.data;
          console.log("用户已登录", this.current_user);
          this.fetchCollections();
          return;
        }
        console.log("用户未登录", response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
    async removeCollection(productId) {
      if (confirm("确定要从收藏中移除该商品吗？")) {
        try {
          const formData = new URLSearchParams();
          formData.append("product_id", productId);
          formData.append("user_id", this.current_user.user_id);
          const response = await fetch(
            "http://localhost:8000/Backend_Store/api/removeCollection",
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
          //response.data
          const data = await response.json();
          this.fetchCollections();
          console.log(data.status);
        } catch (error) {
          console.error("移除操作失败:", error);
        }
      }
    },
    async addToCart(product_id) {
      //api/add_to_cart
      // This should be replaced with actual form submission or API call
      if (this.current_user.status != "success") {
        this.operateMessage("请先登录", "warning");
        return;
      }
      try {
        const formData = new URLSearchParams();
        formData.append("product_id", product_id);
        formData.append("user_id", this.current_user.user_id);
        formData.append("quantity", 1);
        //console.log(this.product.id, this.user_id, this.quantity);
        const response = await fetch(
          "http://localhost:8000/Backend_Store/api/add_to_cart",
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
        console.log(response);
        this.operateMessage("加入购物车成功", "success");
      } catch (error) {
        console.error("购买流程错误:", error);
        this.operateMessage("加入购物车失败", "fail");
      }
    },
    enterCart() {
      window.location.href = this.collectUrl;
    },
    showToast(message, type = "success") {
      this.toast = { show: true, message, type };
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    },
    updateCartCount(count) {
      const cartCountEl = document.querySelector(".cart-count");
      if (cartCountEl) {
        cartCountEl.textContent = count;
        cartCountEl.classList.add("updated");
        setTimeout(() => {
          cartCountEl.classList.remove("updated");
        }, 500);
      }
    },
    getCSRFToken() {
      const cookieValue = document.cookie.match(
        "(^|;)\\s*csrftoken\\s*=\\s*([^;]+)"
      );
      return cookieValue ? cookieValue.pop() : "";
    },
    backHome() {
      this.$router.push("/Home");
      setTimeout(() => window.location.reload(), 100);
    },
    productDetail(product_id) {
      this.$router.push({
        path: "/ProductDetail",
        query: { product_id: product_id },
      });
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

<style src="../assets/css/Collection.css" scoped></style>