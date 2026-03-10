<template>
  <div class="product-detail">
    <div class="main_box">
      <div class="left_box">
        <div class="main-image-container">
          <img
            id="mainImage"
            class="main-image"
            :src="product.image"
            :alt="product.name"
          />
        </div>
        <div class="thumbnail-container">
          <img
            class="thumbnail active"
            :src="product.image"
            @click="changeImage(product.image)"
          />

          <img class="thumbnail" src="#" @click="changeImage('#')" />

          <img class="thumbnail" src="#" @click="changeImage('#')" />

          <img class="thumbnail" src="#" @click="changeImage('#')" />
        </div>
      </div>
      <div class="right_box">
        <h1>{{ product.name }}</h1>
        <div
          class="product-description"
          :data-product_id="product.id"
          :data-product_price="product.price"
        >
          <p>商品描述：</p>
          <div class="description">{{ product.description }}</div>
        </div>
        <div class="product-price">
          <p>价格：${{ product.price }}</p>
        </div>
        <div class="product-stock">
          <p>库存：{{ product.stock }}</p>
        </div>
        <form @submit.prevent="addToCart" class="add-to-cart">
          <label for="quantity" class="add-to-cart-quantity">数量:</label>
          <input
            type="button"
            class="quantity-minus"
            value="-"
            @click="decreaseQuantity"
          />
          <input
            type="number"
            name="quantity"
            class="add-to-cart-number"
            id="quantity-input"
            min="1"
            :max="product.stock"
            v-model="quantity"
            required
          />
          <input
            type="button"
            class="quantity-plus"
            value="+"
            @click="increaseQuantity"
          /><br />
          <button
            type="button"
            class="cart-button"
            id="addOrder"
            @click="addToOrder"
          >
            立即购买
          </button>
          <input
            type="submit"
            class="cart-button"
            value="添加到购物车"
            id="submitBtn"
            :data-id="product.id"
            :data-category="product.category"
          />
          <button type="button" class="cart-button" @click="collect">
            <span class="star-text">
              {{ is_collected ? "已收藏" : "收藏" }}
            </span>
          </button>
          <!-- <button
            id="collect-btn"
            :class="['star-btn', { collected: is_collected }]"
          >
            <svg class="star-icon" viewBox="0 0 24 24">
              <path
                d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
              />
            </svg>
            <span class="star-text">
              {{ is_collected ? "已收藏" : "收藏" }}
            </span>
          </button> -->
        </form>
      </div>
    </div>
    <div id="message">{{ message }}</div>
    <button class="cart-button" id="backbtn" @click="backHome()">
      退出详情页
    </button>
    <hr />
    <div class="comments">
      <h2>用户评论</h2>
      <!-- <form @submit.prevent="submitComment">
        <label for="rating">评分:</label>
        <select id="rating" name="rating" v-model="commentRating" required>
          <option value="1">1星</option>
          <option value="2">2星</option>
          <option value="3">3星</option>
          <option value="4">4星</option>
          <option value="5">5星</option>
        </select>
        <label for="comment" class="comments-text">发表评论:</label>
        <textarea
          id="comment"
          name="comment"
          rows="4"
          cols="50"
          v-model="commentContent"
          required
        ></textarea>
        <button type="submit">提交评论</button>
      </form> -->

      <h3>已有评论</h3>
      <template v-if="current_user && current_user.is_authenticated">
        <div
          class="comment"
          v-for="comment in product.comments"
          :key="comment.id"
        >
          <p>
            <strong>{{ comment.user.username }}</strong> ({{
              formatDate(comment.created_at)
            }}):
          </p>
          <p>{{ comment.content }}</p>
          <p>评分: {{ comment.rating }} 星</p>
        </div>
      </template>
      <template v-else>
        <p>请先登录以查看评论。</p>
      </template>
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";
import { Message } from "element-ui";
export default {
  name: "ProductDetail",
  data() {
    return {
      product: {
        id: null,
        name: "",
        image: "",
        description: "",
        price: 0,
        stock: 0,
        category: "",
        comments: [],
      },
      current_user: {},
      is_collected: false,
      user_id: null,
      quantity: 1,
      message: "",
      commentRating: "5",
      commentContent: "",
      orderUrl: "/api/order/add",
    };
  },
  created() {
    this.fetchProductData();
    this.fetchUserData();
    //this.checkQuantityParam();
    //this.trackProductClicks();
  },
  methods: {
    async fetchProductData() {
      try {
        const product_id = this.$route.query.product_id;
        const response = await request.get(
          "http://localhost:8000/Backend_Store/api/productDetail/" + product_id
        );
        this.product = response.data[0];
        console.log(this.product);
        //this.current_user = data.current_user || { is_authenticated: false };
        //this.is_collected = data.is_collected || false;
        //this.is_collected = false;
        //this.user_id = data.user_id || null;
      } catch (error) {
        console.error("Error fetching cart data:", error);
      }
    },
    checkQuantityParam() {
      const quantity = this.$route.query.quantity;
      if (quantity) {
        this.message = `此次加入购物车成功，请注意数量：${quantity}件`;
        document.getElementById("submitBtn").style.backgroundColor = "orange";
      }
    },
    trackProductClicks() {
      document.querySelectorAll(".product-link").forEach((link) => {
        link.addEventListener("click", (event) => {
          event.preventDefault();
          const user = JSON.parse(localStorage.getItem("user"));
          const userId = user ? user.id : null;
          const productId = link.getAttribute("data-id");
          const category = link.getAttribute("data-category");

          fetch("/api/tracking", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              event_id: productId,
              event_type: "product_click",
              user_id: userId,
              category: category,
            }),
          })
            .then((response) => response.json())
            .then((data) => {
              console.log("Success:", data);
              window.location.href = link.href;
            })
            .catch((error) => {
              console.error("Error:", error);
              window.location.href = link.href;
            });
        });
      });
    },
    changeImage(newSrc) {
      document.getElementById("mainImage").src = newSrc;
      document.querySelectorAll(".thumbnail").forEach((img) => {
        img.classList.remove("active");
      });
      event.target.classList.add("active");
    },
    decreaseQuantity() {
      if (this.quantity > 1) {
        this.quantity--;
      }
    },
    increaseQuantity() {
      if (this.quantity < this.product.stock) {
        this.quantity++;
      }
    },
    backHome() {
      this.$router.push("/Home");
      setTimeout(() => window.location.reload(), 100);
    },
    async addToOrder() {
      if (this.current_user.status != "success") {
        this.operateMessage("请先登录", "warning");
        return;
      }
      try {
        const formData = new URLSearchParams();
        formData.append("product_id", this.product.id);
        formData.append("user_id", this.user_id);
        formData.append("quantity", this.quantity);
        //console.log(this.product.id, this.user_id, this.quantity);
        const addToCartResponse = await fetch(
          "http://localhost:8000/Backend_Store/api/add_to_order",
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
        console.log(addToCartResponse);
        this.operateMessage("购买成功", "success");
      } catch (error) {
        console.error("购买流程错误:", error);
        this.operateMessage("购买失败", "error");
      }
    },
    async addToCart() {
      //api/add_to_cart
      // This should be replaced with actual form submission or API call
      if (this.current_user.status != "success") {
        this.operateMessage("请先登录", "warning");
        return;
      }
      try {
        const formData = new URLSearchParams();
        formData.append("product_id", this.product.id);
        formData.append("user_id", this.user_id);
        formData.append("quantity", this.quantity);
        //console.log(this.product.id, this.user_id, this.quantity);
        const addToCartResponse = await fetch(
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
        console.log(addToCartResponse);
        this.operateMessage("加入购物车成功", "success");
      } catch (error) {
        console.error("购买流程错误:", error);
        this.operateMessage("加入购物车失败", "error");
      }
    },
    submitComment() {
      // This should be replaced with actual form submission
      fetch(`/api/comments/add?product_id=${this.product.id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          rating: this.commentRating,
          content: this.commentContent,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          this.product.comments.unshift(data.comment);
          this.commentRating = "5";
          this.commentContent = "";
        });
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString("zh-CN", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
    },
    async fetchUserData() {
      try {
        const response = await request.get(
          "http://localhost:8000/Backend_Store/api/checkLogin"
        );
        if (response.data.user_id != "-1") {
          this.current_user = response.data;
          this.user_id = this.current_user.user_id;
          console.log("用户已登录", this.current_user);
          this.checkCollect();
          return;
        }
        console.log("用户未登录", response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
    async checkCollect() {
      this.is_collected = false;
      try {
        const formData = new URLSearchParams();
        formData.append("product_id", this.product.id);
        formData.append("user_id", this.user_id);
        //console.log(this.product.id, this.user_id, this.quantity);
        const response = await fetch(
          "http://localhost:8000/Backend_Store/api/checkCollect",
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
        if (data.status === "success") {
          this.is_collected = true;
          console.log("商品收藏");
        } else {
          console.log("商品未收藏");
        }
      } catch (error) {
        console.error("购买流程错误:", error);
        this.operateMessage("判断商品收藏状态失败", "error");
      }
    },
    operateMessage(message, type) {
      this.$message({
        message: message,
        type: type,
      });
    },
    async collect() {
      if (this.is_collected) {
        try {
          const formData = new URLSearchParams();
          formData.append("product_id", this.product.id);
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
          const data = await response.json();
          console.log(data.status);
          if (data.status == "success") {
            this.operateMessage("已取消收藏", "success");
            this.is_collected = false;
          }
        } catch (error) {
          console.error("移除操作失败:", error);
        }
        return;
      } else {
        try {
          const formData = new URLSearchParams();
          formData.append("product_id", this.product.id);
          formData.append("user_id", this.current_user.user_id);
          const response = await fetch(
            "http://localhost:8000/Backend_Store/api/collect",
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
          console.log(data.status);
          if (data.status == "success") {
            this.operateMessage("已收藏", "success");
            this.is_collected = true;
          }
        } catch (error) {
          console.error("收藏操作失败:", error);
        }
      }
    },
  },
};
</script>

<style src="../assets/css/ProductDetail.css" scoped></style>