<template>
  <div>
    <!-- 购物车卡片 -->
    <div id="cartModal" class="modal">
      <div class="modal-content">
        <span class="close">&times;</span>
        <template v-if="Carts && Carts.length">
          <h2>您的购物车：</h2>
          <ul class="rank-list">
            <li class="rank-item" v-for="(Cart, index) in Carts" :key="Cart.id">
              <span class="rank-num">{{ index + 1 }}</span>
              <span class="rank-name">{{ Cart.product.name }}</span>
              <span class="rank-name" @click="closeCart"
                >×{{ Cart.quantity }}</span
              >
              <span class="rank-price"
                >总价：{{ Cart.quantity * Cart.product.price }}</span
              >
            </li>
          </ul>
          <div id="cartItems"></div>
          <div class="cart-total">
            <p>
              合计为: <span id="totalPrice">{{ totalCartValue }}</span
              >元
            </p>
          </div>
          <div class="confirmBox">
            <button class="confirm-button" id="confirm" @click="checkout">
              结算
            </button>
          </div>
        </template>
        <template v-else>
          <h2>购物车中空空如也</h2>
          <button class="confirm-button" id="cancel" @click="closeCart()">
            返回
          </button>
        </template>
      </div>
    </div>

    <!-- 导航栏 -->
    <div class="top-navigation">
      <button class="button-brand" @click="refresh()">3C—淘好货</button>
      <button class="button-normal" @click="openCart()">购物车</button>
      <button class="button-normal" @click="order()">订单中心</button>
      <button class="button-normal" @click="collection()">我的收藏</button>
      <button class="button-normal" @click="help()">帮助中心</button>
      <button class="button-normal" @click="analysis()">数据分析(离线)</button>
      <button class="button-normal" @click="realtime_analysis()">
        数据分析(实时)
      </button>
      <div class="search-box">
        <div>
          <input
            type="text"
            placeholder="热卖商品..."
            class="search-input"
            id="searchInput"
            name="keyWord"
            value=""
          />
          <input
            type="button"
            class="search-button"
            value="🔍"
            @click="search()"
          />
        </div>
      </div>

      <template v-if="current_user.status === 'success'">
        <button class="button-login" @click="user_profile()">
          {{ current_user.username }}
        </button>
      </template>
      <template v-else>
        <button class="button-login" @click="login()">登录</button>
      </template>
    </div>

    <!-- 轮播图区域 -->
    <div class="promote-block">
      <div class="left-card">
        <h3>🔥 热销TOP5</h3>
        <ul class="rank-list">
          <li class="rank-item">
            <span class="rank-num">1</span>
            <span class="rank-name">iPhone 15 Pro</span>
            <span class="rank-price">¥8999</span>
          </li>
          <li class="rank-item">
            <span class="rank-num">2</span>
            <span class="rank-name">AirPods Pro 2</span>
            <span class="rank-price">¥1899</span>
          </li>
          <li class="rank-item">
            <span class="rank-num">3</span>
            <span class="rank-name">华为Mate 60 Pro</span>
            <span class="rank-price">¥6999</span>
          </li>
          <li class="rank-item">
            <span class="rank-num">4</span>
            <span class="rank-name">石头G20扫拖一体机器人</span>
            <span class="rank-price">¥3999</span>
          </li>
          <li class="rank-item">
            <span class="rank-num">5</span>
            <span class="rank-name">微软 Surface Pro 9</span>
            <span class="rank-price">¥6999</span>
          </li>
        </ul>
      </div>
      <div class="carousel">
        <div class="carousel-container">
          <!-- 实际最后一张的克隆（视觉上放在最前面） -->
          <div class="carousel-slide">
            <img src="https://picsum.photos/800/500?random=4" alt="图片4" />
          </div>
          <!-- 原始图片 -->
          <div class="carousel-slide">
            <img src="https://picsum.photos/800/500?random=1" alt="图片1" />
          </div>
          <div class="carousel-slide">
            <img src="https://picsum.photos/800/500?random=2" alt="图片2" />
          </div>
          <div class="carousel-slide">
            <img src="https://picsum.photos/800/500?random=3" alt="图片3" />
          </div>
          <div class="carousel-slide">
            <img src="https://picsum.photos/800/500?random=4" alt="图片4" />
          </div>
          <!-- 实际第一张的克隆（视觉上放在最后面） -->
          <div class="carousel-slide">
            <img src="https://picsum.photos/800/500?random=1" alt="图片1" />
          </div>
        </div>

        <button class="carousel-btn" id="prevBtn">❮</button>
        <button class="carousel-btn" id="nextBtn">❯</button>

        <div class="carousel-indicators">
          <div class="indicator active"></div>
          <div class="indicator"></div>
          <div class="indicator"></div>
          <div class="indicator"></div>
        </div>
      </div>
      <div class="right-card">
        <div class="flip-container">
          <div class="flip-front">
            <img
              src="https://tse4-mm.cn.bing.net/th/id/OIP-C.o2dNmPwG-KUcKoisvtQvEgHaNK?w=187/&h=333/&c=7/&r=0/&o=5/&dpr=1.3/&pid=1.7"
              alt="产品图片"
            />
          </div>
          <div class="flip-back">
            <div class="flip-content">
              <h3>产品详情</h3>
              <p>xxl,iPhonex</p>
              <p>价格: ¥999</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 商品区域 -->
    <div class="tab-container">
      <h2 style="margin-left: 15px">热销商品</h2>
      <div class="tab-nav">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'tab1' }"
          @click="activeTab = 'tab1'"
        >
          手机
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'tab2' }"
          @click="activeTab = 'tab2'"
        >
          电脑
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'tab3' }"
          @click="activeTab = 'tab3'"
        >
          电器
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'tab4' }"
          @click="activeTab = 'tab4'"
        >
          配件
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'tab5' }"
          @click="activeTab = 'tab5'"
        >
          猜你喜欢
        </button>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Phone Products -->
        <div
          class="tab-pane"
          :class="{ active: activeTab === 'tab1' }"
          id="tab1"
        >
          <div class="product-item" v-for="product in phones" :key="product.id">
            <img
              :src="product.image"
              :alt="product.name"
              class="product-image"
              @click="productDetail(product.id)"
            />
            <h3>{{ product.name }}</h3>
            <p class="price">${{ product.price }}</p>
            <p class="stock">库存: {{ product.stock }}</p>
          </div>
        </div>

        <!-- Computer Products -->
        <div
          class="tab-pane"
          :class="{ active: activeTab === 'tab2' }"
          id="tab2"
        >
          <div
            class="product-item"
            v-for="product in computers"
            :key="product.id"
          >
            <img
              :src="product.image"
              :alt="product.name"
              class="product-image"
              @click="productDetail(product.id)"
            />
            <h3>{{ product.name }}</h3>
            <p class="price">${{ product.price }}</p>
            <p class="stock">库存: {{ product.stock }}</p>
          </div>
        </div>

        <!-- Appliance Products -->
        <div
          class="tab-pane"
          :class="{ active: activeTab === 'tab3' }"
          id="tab3"
        >
          <div
            class="product-item"
            v-for="product in appliances"
            :key="product.id"
          >
            <img
              :src="product.image"
              :alt="product.name"
              class="product-image"
              @click="productDetail(product.id)"
            />
            <h3>{{ product.name }}</h3>
            <p class="price">${{ product.price }}</p>
            <p class="stock">库存: {{ product.stock }}</p>
          </div>
        </div>

        <!-- Component Products -->
        <div
          class="tab-pane"
          :class="{ active: activeTab === 'tab4' }"
          id="tab4"
        >
          <div
            class="product-item"
            v-for="product in components"
            :key="product.id"
          >
            <img
              :src="product.image"
              :alt="product.name"
              class="product-image"
              @click="productDetail(product.id)"
            />
            <h3>{{ product.name }}</h3>
            <p class="price">${{ product.price }}</p>
            <p class="stock">库存: {{ product.stock }}</p>
          </div>
        </div>

        <!-- Recommended Products -->
        <div
          class="tab-pane"
          :class="{ active: activeTab === 'tab5' }"
          id="tab5"
        >
          <div
            class="recomend-item"
            v-for="track in track_data"
            :key="track.id"
          >
            <img
              :src="track.image"
              :alt="track.name"
              class="product-image"
              @click="productDetail(track.id)"
            />
            <h3>{{ track.name }}</h3>
            <p class="price">${{ track.price }}</p>
            <p class="stock">库存: {{ track.stock }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 新闻区域 -->
    <div class="news-column">
      <footer class="footer-news">
        <div class="news-container">
          <h3 class="news-title">最新动态</h3>
          <div class="news-grid">
            <div
              class="news-row"
              v-for="(newsItem, index) in news"
              :key="index"
            >
              <article class="news-card">
                <time class="news-date">{{ newsItem.date }}</time>
                <h4 class="news-headline">
                  <a href="#">{{ newsItem.headline }}</a>
                </h4>
                <p class="news-excerpt">{{ newsItem.excerpt }}</p>
              </article>
            </div>
          </div>
        </div>
      </footer>
    </div>

    <!-- 版权区域 -->
    <div class="inf-web">
      <footer class="site-footer">
        <div class="footer-container">
          <!-- 第一行：主要信息 -->
          <div class="footer-main">
            <!-- 公司信息 -->
            <div class="footer-col">
              <h4 class="footer-title">科技电子</h4>
              <p class="footer-about">致力于提供最前沿的电子产品与解决方案</p>
              <div class="footer-contact">
                <p><i class="icon icon-phone"></i> 400-888-8888</p>
                <p><i class="icon icon-email"></i> info@tech-electronics.com</p>
              </div>
            </div>

            <!-- 快速链接 -->
            <div class="footer-col">
              <h4 class="footer-title">快速链接</h4>
              <ul class="footer-links">
                <li><a href="/">首页</a></li>
                <li><a href="/products">产品中心</a></li>
                <li><a href="/solutions">解决方案</a></li>
                <li><a href="/support">技术支持</a></li>
              </ul>
            </div>

            <!-- 服务支持 -->
            <div class="footer-col">
              <h4 class="footer-title">服务支持</h4>
              <ul class="footer-links">
                <li><a href="/warranty">保修政策</a></li>
                <li><a href="/faq">常见问题</a></li>
                <li><a href="/downloads">驱动下载</a></li>
                <li><a href="/contact">联系我们</a></li>
              </ul>
            </div>

            <!-- 社交媒体 -->
            <div class="footer-col">
              <h4 class="footer-title">关注我们</h4>
              <div class="social-links">
                <a href="#"><i class="icon icon-wechat"></i></a>
                <a href="#"><i class="icon icon-weibo"></i></a>
                <a href="#"><i class="icon icon-douyin"></i></a>
                <a href="#"><i class="icon icon-bilibili"></i></a>
              </div>
              <div class="qr-code">
                <img src="qrcode-wechat.png" alt="微信公众号" />
                <p>扫码关注公众号</p>
              </div>
            </div>
          </div>

          <!-- 版权信息 -->
          <div class="footer-bottom">
            <div class="copyright">
              © 2023 科技电子有限公司 版权所有
              <span class="divider">|</span>
              <a href="/privacy">隐私政策</a>
              <span class="divider">|</span>
              <a href="/terms">服务条款</a>
              <span class="divider">|</span>
              <a href="/sitemap">网站地图</a>
            </div>
            <div class="certification">
              <img src="icp-logo.png" alt="ICP备案" />
              <span>京ICP备12345678号</span>
              <img src="security-logo.png" alt="安全认证" />
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<style src="../assets/css/Home.css" scoped></style>

<script>
import request from "@/utils/request";
import { Message } from "element-ui";

export default {
  data() {
    return {
      msg: "我的主页",
      activeTab: "tab1",
      Carts: [],
      phones: [],
      computers: [],
      appliances: [],
      components: [],
      track_data: [],
      news: [],
      current_user: {},
      modal: "",
    };
  },
  computed: {
    totalCartValue() {
      return this.Carts.reduce((total, Cart) => {
        return total + Cart.quantity * Cart.product.price;
      }, 0);
    },
  },
  methods: {
    pageInit() {
      document.addEventListener("DOMContentLoaded", function () {
        const categoryButtons = document.querySelectorAll(".category-button");

        categoryButtons.forEach((button) => {
          button.addEventListener("mouseover", function () {
            const categories = JSON.parse(
              button.getAttribute("data-categories")
            );
            const detailsDiv = document.createElement("div");
            detailsDiv.className = "category-details";

            categories.forEach((category) => {
              const link = document.createElement("a");
              link.href = "#"; // 你可以根据需要修改链接
              link.textContent = category;
              detailsDiv.appendChild(link);
            });

            button.appendChild(detailsDiv);
          });
          button.addEventListener("mouseout", function () {
            const detailsDiv = button.querySelector(".category-details");
            if (detailsDiv) {
              detailsDiv.remove();
            }
          });
        });
      });

      this.modal = document.getElementById("cartModal");
      const closeBtn = document.querySelector(".close");
      const cancel = document.getElementById("cancel");
      const helpBtn = document.getElementById("helpBtn");

      // 关闭弹窗（带动画）
      closeBtn.addEventListener("click", () => {
        this.modal.classList.remove("active");
      });
      cancel.addEventListener("click", () => {
        this.modal.classList.remove("active");
      });

      // 点击遮罩层关闭
      window.addEventListener("click", (e) => {
        if (e.target === this.modal) {
          this.modal.classList.remove("active");
        }
      });

      //轮播图控制
      document.addEventListener("DOMContentLoaded", function () {
        const container = document.querySelector(".carousel-container");
        const slides = document.querySelectorAll(".carousel-slide");
        const prevBtn = document.getElementById("prevBtn");
        const nextBtn = document.getElementById("nextBtn");
        const indicators = document.querySelectorAll(".indicator");

        let currentIndex = 1; // 从原始第一张开始
        const totalSlides = slides.length;
        const realSlidesCount = 4; // 实际图片数量
        prevBtn.style.display = "none";
        nextBtn.style.display = "none";

        // 更新轮播图位置和指示器状态
        function updateCarousel() {
          container.style.transform = `translateX(-${currentIndex * 100}%)`;

          // 更新指示器
          let realIndex = getRealIndex();
          indicators.forEach((indicator, index) => {
            indicator.classList.toggle("active", index === realIndex);
          });
        }

        // 获取实际索引（排除克隆的幻灯片）
        function getRealIndex() {
          if (currentIndex === 0) return realSlidesCount - 1;
          if (currentIndex === totalSlides - 1) return 0;
          return currentIndex - 1;
        }

        // 下一张（无缝循环）
        function nextSlide() {
          currentIndex++;
          container.style.transition = "transform 0.5s ease";
          updateCarousel();

          // 如果到达克隆的最后一张，无动画跳转到真实的第一张
          if (currentIndex === totalSlides - 1) {
            setTimeout(() => {
              container.style.transition = "none";
              currentIndex = 1;
              container.style.transform = `translateX(-${currentIndex * 100}%)`;
            }, 500);
          }
        }

        // 上一张（无缝循环）
        function prevSlide() {
          currentIndex--;
          container.style.transition = "transform 0.5s ease";
          updateCarousel();

          // 如果到达克隆的第一张，无动画跳转到真实的最后一张
          if (currentIndex === 0) {
            setTimeout(() => {
              container.style.transition = "none";
              currentIndex = realSlidesCount;
              container.style.transform = `translateX(-${currentIndex * 100}%)`;
            }, 500);
          }
        }

        // 按钮点击事件
        nextBtn.addEventListener("click", nextSlide);
        prevBtn.addEventListener("click", prevSlide);

        // 指示器点击事件
        indicators.forEach((indicator, index) => {
          indicator.addEventListener("click", () => {
            currentIndex = index + 1;
            container.style.transition = "transform 0.5s ease";
            updateCarousel();
          });
        });

        // 自动轮播
        let autoPlay = setInterval(nextSlide, 3000);

        // 鼠标悬停时暂停自动轮播
        document
          .querySelector(".carousel")
          .addEventListener("mouseenter", () => {
            clearInterval(autoPlay);
            prevBtn.style.display = "block";
            nextBtn.style.display = "block";
          });

        // 鼠标离开时恢复自动轮播
        document
          .querySelector(".carousel")
          .addEventListener("mouseleave", () => {
            autoPlay = setInterval(nextSlide, 3000);
            prevBtn.style.display = "none";
            nextBtn.style.display = "none";
          });
      });
    },
    checkout() {},
    user_profile() {
      this.$router.push("/UserProfile");
    },
    login() {
      this.$router.push("/Login");
    },
    category(fixed_value) {
      window.location.href = `/category?fixed_value=${fixed_value}`;
    },
    recomend() {
      window.location.href = recomendUrl;
    },
    async checkout() {
      if (this.current_user.status != "success") {
        this.operateMessage("当前账号异常!!!");
        return;
      }
      try {
        const formData = new URLSearchParams();
        formData.append("user_id", this.current_user.user_id);
        //console.log(this.product.id, this.user_id, this.quantity);
        const response = await fetch(
          "http://localhost:8000/Backend_Store/api/checkout",
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
        this.operateMessage("结算成功，请前往购物车查看", "success");
        this.Carts = {};
      } catch (error) {
        console.error("购买流程错误:", error);
        this.operateMessage("结算失败", "error");
      }
    },
    help() {
      alert("暂未开发");
    },
    openCart() {
      if (this.current_user.status !== "success") {
        this.operateMessage("尚未登录,请先登录", "warning");
        return;
      }
      this.fetchCartData();
      this.modal.classList.add("active");
    },
    order() {
      if (this.current_user.status !== "success") {
        this.operateMessage("尚未登录,请先登录", "warning");
        return;
      }
      this.$router.push("/Order");
    },
    refresh() {
      window.location.reload();
    },
    collection() {
      this.$router.push("/Collection");
    },
    analysis() {
      this.$router.push("/Analysis");
    },
    realtime_analysis() {
      this.$router.push("/Realtime_Analysis");
    },
    search() {
      if (this.current_user.status != "success") {
        this.operateMessage("请先登录", "warning");
        return;
      }
      const keyword = document.querySelector(".search-input").value;
      sessionStorage.setItem("searchKeyword", keyword);
      sessionStorage.setItem("user_id", this.current_user.user_id);
      this.$router.push("/Search");
    },
    showSlides() {
      const slides = document.querySelectorAll(".slides img");
      for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
      }
      slideIndex++;
      if (slideIndex > slides.length) {
        slideIndex = 1;
      }
      slides[slideIndex - 1].style.display = "block";
      setTimeout(showSlides, 3000); // 每3秒切换一次图片
    },
    plusSlides(n) {
      showSlides((slideIndex += n));
    },
    // 动态生成轮播图图片
    generateCarouselImages() {
      const slidesContainer = document.getElementById("carousel-slides");
      carouselImages.forEach((imageSrc) => {
        const imgElement = document.createElement("img");
        imgElement.src = imageSrc;
        imgElement.style.display = "none";
        slidesContainer.appendChild(imgElement);
      });
      showSlides(); // 初始化显示第一张图片
    },
    async fetchCartData() {
      if (this.current_user.status === "success") {
        const user_id = this.current_user.user_id + "";
        try {
          const response = await request.get(
            "http://localhost:8000/Backend_Store/api/carts/" + user_id
          );
          this.Carts = response.data;
          console.log("获取用户id：" + user_id + "的购物车数据");
        } catch (error) {
          console.error("Error fetching cart data:", error);
        }
      }
    },
    async fetchProductData() {
      try {
        const [phonesRes, computersRes, appliancesRes, componentsRes] =
          await Promise.all([
            request.get(
              "http://localhost:8000/Backend_Store/api/products/phone"
            ),
            request.get(
              "http://localhost:8000/Backend_Store/api/products/computer"
            ),
            request.get(
              "http://localhost:8000/Backend_Store/api/products/appliances"
            ),
            request.get(
              "http://localhost:8000/Backend_Store/api/products/component"
            ), //track_data
          ]);

        // 直接获取data字段（axios自动处理）
        this.phones = phonesRes.data;
        this.computers = computersRes.data;
        this.appliances = appliancesRes.data;
        this.components = componentsRes.data;
        //console.log(this.phones);
      } catch (error) {
        console.error("Error fetching product data:", error);
        // 可选：显示错误提示
        this.$message.error("商品数据加载失败");
      }
    },
    async fetchNewsData() {
      try {
        const response = await request.get(
          "http://localhost:8000/Backend_Store/api/news"
        );
        this.news = response.data;
        //console.log(this.news);
      } catch (error) {
        console.error("Error fetching news data:", error);
      }
    },
    async fetchRecommendData() {
      try {
        const formData = new URLSearchParams();
        formData.append("user_id", this.current_user.user_id);
        //console.log(this.product.id, this.user_id, this.quantity);
        const response = await fetch(
          "http://localhost:8000/Backend_Store/api/recommend",
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
        const responseData = await response.json();
        if (responseData.status == "success") {
          this.track_data = responseData.data;
          console.log("获取用户推荐商品数据成功");
          console.log(this.track_data);
        } else {
          this.operateMessage("获取用户商品数据失败", "warning");
        }
      } catch (error) {
        //console.error("异常！获取用户商品数据失败", error);
        this.operateMessage("异常！获取用户商品数据失败", "error");
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
          this.fetchRecommendData();
          return;
        }
        console.log("用户未登录", response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
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
    closeCart() {
      this.modal.classList.remove("active");
    },
  },
  mounted() {
    // Fetch data from your Flask backend
    //this.fetchCartData();
    this.pageInit();
    this.fetchProductData();
    //this.fetchCartData();
    this.fetchNewsData();
    this.fetchUserData();
  },
};
</script>