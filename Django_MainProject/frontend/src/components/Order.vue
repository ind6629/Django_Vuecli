<template>
  <div class="order-page">
    <button @click="backHome" class="arrow-button">返回</button>
    <div class="order-list-container">
      <h2 class="order-list-title">我的订单</h2>

      <div v-if="orders && orders.length">
        <div class="order-list-header">
          <div class="header-checkbox">
            <input
              type="checkbox"
              id="select-all"
              class="order-checkbox"
              v-model="selectAll"
              @change="toggleSelectAll"
            />
            <label for="select-all">全选</label>
          </div>
          <div class="header-product">商品</div>
          <div class="header-quantity">数量</div>
          <div class="header-price">总价</div>
        </div>

        <div class="order-items">
          <div
            class="order-item"
            v-for="order in orders"
            :key="order.id"
            :data-order_id="order.id"
          >
            <div class="item-checkbox">
              <input
                type="checkbox"
                :id="'order-' + order.id"
                class="order-checkbox"
                v-model="selectedOrders"
                :value="order.id"
              />
              <label :for="'order-' + order.id"></label>
            </div>
            <div class="item-product">
              <img
                :src="order.product.image"
                alt="商品图片"
                class="product-image"
              />
              <div class="product-info">
                <h3 class="product-name">{{ order.product.name }}</h3>
                <p class="product-spec">{{ order.product.description }}</p>
              </div>
            </div>
            <div class="item-quantity">
              <span class="quantity-value">{{ order.quantity }}</span>
            </div>
            <div class="item-price">
              <span class="price-value">{{ order.total_price }}</span>
            </div>
          </div>
        </div>

        <div class="order-list-footer">
          <div class="footer-left">
            <input
              type="checkbox"
              id="footer-select-all"
              class="order-checkbox"
              v-model="selectAll"
              @change="toggleSelectAll"
            />
            <label for="footer-select-all">全选</label>
            <button class="delete-selected" @click="deleteSelected">
              删除选中
            </button>
          </div>
          <div class="footer-right">
            <span class="total-text"
              >已选
              <span class="selected-count">{{ selectedOrders.length }}</span>
              件商品，合计：</span
            >
            <span class="total-price">{{ calculateTotalPrice() }}</span>
            <button
              class="checkout-btn"
              v-show="selectedOrders.length > 0"
              @click="settleOrders"
            >
              去结算
            </button>
          </div>
        </div>
      </div>

      <h1 v-else>当前未有订单</h1>
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";

export default {
  name: "OrderPage",
  data() {
    return {
      orders: [], // Will be populated from API
      selectedOrders: [],
      selectAll: false,
      ordersUrl: "http://localhost:8000/Backend_Store/api/orders/",
      settleOrderUrl: "http://localhost:8000/Backend_Store/api/orders/24",
      current_user: {},
    };
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    async fetchOrders() {
      // Replace with your actual API call
      if (this.current_user.status != "success") {
        alert("登录状态异常!!!");
        return;
      }
      try {
        const response = await request.get(
          this.ordersUrl + this.current_user.user_id
        );
        this.orders = response.data;
        console.log(this.orders);
      } catch (error) {
        console.error("Error fetching cart data:", error);
      }
    },
    toggleSelectAll() {
      if (this.selectAll) {
        this.selectedOrders = this.orders.map((order) => order.id);
      } else {
        this.selectedOrders = [];
      }
    },
    deleteSelected() {
      if (this.selectedOrders.length === 0) return;

      if (confirm("确定要删除选中的订单吗？")) {
        axios
          .post(this.cancelOrderUrl, { orderIds: this.selectedOrders })
          .then(() => {
            this.orders = this.orders.filter(
              (order) => !this.selectedOrders.includes(order.id)
            );
            this.selectedOrders = [];
            this.selectAll = false;
          })
          .catch((error) => {
            console.error("Error deleting orders:", error);
          });
      }
    },
    settleOrders() {
      axios
        .post(this.settleOrderUrl, { orderIds: this.selectedOrders })
        .then((response) => {
          // Handle successful settlement
          this.$router.push("/checkout");
        })
        .catch((error) => {
          console.error("Error settling orders:", error);
        });
    },
    calculateTotalPrice() {
      return this.orders
        .filter((order) => this.selectedOrders.includes(order.id))
        .reduce((total, order) => total + parseFloat(order.total_price), 0)
        .toFixed(2);
    },
    backHome() {
      this.$router.push("/Home");
      setTimeout(() => window.location.reload(), 100);
    },
    async fetchUserData() {
      try {
        const response = await request.get(
          "http://localhost:8000/Backend_Store/api/checkLogin"
        );
        console.log("response:" + response.data);
        if (response.data.user_id != "-1") {
          this.current_user = response.data;
          console.log("用户已登录", this.current_user);
          this.fetchOrders();
          return;
        }
        console.log("用户未登录", response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
  },
  watch: {
    selectedOrders(newVal) {
      this.selectAll =
        newVal.length === this.orders.length && this.orders.length > 0;
    },
  },
};
</script>
<style src="../assets/css/Order.css" scoped></style>