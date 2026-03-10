<template>
  <div class="login-page">
    <button @click="backHome()" class="arrow-button">返回</button>
    <div class="container">
      <div class="auth-container">
        <div class="auth-header">
          <h2 id="form-title">登录/Login</h2>
        </div>
        <div id="loginBox">
          <!-- 登录表单 -->
          <form
            class="auth-form"
            @submit.prevent="handleLogin"
            autocomplete="off"
          >
            <div class="mb-3">
              <label for="login-account" class="form-label">账号</label>
              <input
                type="text"
                autocomplete="current-username"
                class="form-control"
                id="username"
                v-model="username"
                readonly
                @focus="removeReadonly('username')"
                required
              />
            </div>
            <div class="mb-3">
              <label for="login-password" class="form-label">密码</label>
              <input
                type="password"
                autocomplete="current-password"
                class="form-control"
                id="password"
                v-model="password"
                readonly
                @focus="removeReadonly('password')"
                required
              />
            </div>
            <button type="submit" class="btn btn-primary w-100">登录</button>
            <div class="toggle-btn" @click="goToRegister">注册账号</div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      registerUrl: "/auth/register",
    };
  },
  methods: {
    removeReadonly(fieldId) {
      document.getElementById(fieldId).removeAttribute("readonly");
    },
    async handleLogin() {
      try {
        const formData = new URLSearchParams();
        formData.append("username", this.username);
        formData.append("password", this.password);

        // 1. 先获取CSRF Token
        await fetch("http://localhost:8000/Backend_Store/api/csrf_token/", {
          method: "GET",
          credentials: "include",
        });

        // 2. 执行登录
        const loginResponse = await fetch(
          "http://localhost:8000/Backend_Store/api/login",
          {
            method: "POST",
            credentials: "include", // 必须
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
              "X-CSRFToken": this.getCookie("csrftoken") || "",
            },
            body: formData,
          }
        );

        const loginData = await loginResponse.json();
        console.log("登录响应:", loginData);

        if (loginData.status === "success") {
          // 3. 立即验证登录状态
          const checkResponse = await fetch(
            "http://localhost:8000/Backend_Store/api/checkLogin",
            {
              method: "GET",
              credentials: "include",
            }
          );

          const checkData = await checkResponse.json();
          console.log("登录状态检查:", checkData);

          if (checkData.status === "success") {
            this.backHome();
          }
        } else {
          this.operateMessage("登录失败，账号信息有误", "error");
        }
      } catch (error) {
        console.error("登录流程错误:", error);
      }
    },
    goToRegister() {
      this.$router.push("/Register");
    },
    backHome() {
      this.$router.push("/Home");
      setTimeout(() => window.location.reload(), 100);
    },
    async testLogin() {
      try {
        // 注意URL改为/api开头的路径
        const response = await request.get(
          "http://localhost:8000/Backend_Store/api/checkLogin"
        );
        console.log("登录状态:", response.data);
      } catch (error) {
        console.error("请求失败:", error);
      }
    },
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
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
    operateMessage(message, type) {
      this.$message({
        message: message,
        type: type,
      });
    },
  },
};
</script>

<style src="../assets/css/Login.css" scoped></style>