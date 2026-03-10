<template>
  <div class="register-page">
    <div class="container">
      <div class="auth-container">
        <div class="auth-header">
          <h2 id="form-title">注册/Register</h2>
        </div>
        <div id="registerBox">
          <!-- 注册表单 -->
          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label for="register-username" class="form-label">用户名</label>
              <input
                type="text"
                autocomplete="username"
                class="form-control"
                id="username"
                v-model="form.username"
                required
              />
            </div>
            <div class="mb-3">
              <label for="register-email" class="form-label">邮箱</label>
              <input
                type="email"
                autocomplete="email"
                class="form-control"
                id="email"
                v-model="form.email"
                required
              />
            </div>
            <div class="mb-3">
              <label for="register-password" class="form-label">密码</label>
              <input
                type="password"
                autocomplete="new-password"
                class="form-control"
                id="password"
                v-model="form.password"
                required
              />
            </div>
            <div class="mb-3">
              <label for="register-confirm" class="form-label">确认密码</label>
              <input
                type="password"
                autocomplete="off"
                class="form-control"
                id="confirm_password"
                v-model="form.confirm_password"
                required
              />
              <div class="error-message" id="password-match-error"></div>
            </div>
            <button type="submit" class="btn btn-success w-100">注册</button>
            <div class="toggle-btn" @click="login">已有账号？点击此处登录</div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RegisterPage",
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        confirm_password: "",
      },
    };
  },
  methods: {
    login() {
      this.$router.push("/Login");
    },
    handleRegister() {
      // 这里可以添加表单验证逻辑
      if (this.form.password !== this.form.confirm_password) {
        document.getElementById("password-match-error").textContent =
          "两次输入的密码不一致";
        return;
      }

      // 发送注册请求
      fetch("http://localhost:8000/Backend_Store/api/register", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: JSON.stringify(this.form),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            alert("注册成功!!!");
            this.login();
          } else {
            alert("注册失败：" + data.message);
          }
        })
        .catch((error) => {
          console.error("注册错误:", error);
        });
    },
  },
};
</script>
<style src="../assets/css/Register.css" scoped></style>