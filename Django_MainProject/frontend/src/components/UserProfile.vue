<template>
  <div class="user-profile">
    <div class="mainBox">
      <h1>欢迎您，{{ user.username }}</h1>
      <img :src="avatarUrl" class="avatar" />
      <!-- <img src="../assets/images/defaultAvatar.png" /> -->
      <form
        @submit.prevent="updateProfile"
        class="profile-form"
        enctype="multipart/form-data"
      >
        <div class="form-card">
          <h2 class="form-title">编辑个人资料</h2>
          <div class="contentBox">
            <div class="form-group">
              <label for="username" class="form-label">用户名</label>
              <input
                type="text"
                id="username"
                v-model="user.username"
                class="form-input"
                required
              />
            </div>

            <div class="form-group">
              <label for="email" class="form-label">邮箱</label>
              <input
                type="email"
                id="email"
                v-model="user.email"
                class="form-input"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="avatar" class="form-label">头像</label>
            <div class="file-upload">
              <label for="avatar" class="file-upload-label">
                <span class="file-upload-text">选择文件</span>
                <span class="file-upload-name">{{
                  selectedFileName || "未选择文件"
                }}</span>
              </label>
              <input
                type="file"
                id="avatar"
                ref="avatarInput"
                @change="handleFileChange"
                class="file-upload-input"
              />
            </div>
          </div>

          <button type="submit" class="refine-btn" id="submit">保存更改</button>
        </div>
      </form>

      <div class="bottomBox">
        <button @click="backHome" class="refine-btn" id="backHome">
          返回主页
        </button>
        <button @click="logout" class="refine-btn" id="logout">退出登录</button>
      </div>
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";
import axios from "axios";

export default {
  name: "UserProfile",
  data() {
    return {
      user: {
        username: "",
        email: "",
        avatar: null,
      },
      selectedFile: null,
      selectedFileName: "",
    };
  },
  computed: {
    avatarUrl() {
      if (this.user.avatar && this.user.avatar !== "null") {
        return require(`@/assets/images/${this.user.avatar}`);
      }
      return require("@/assets/images/defaultAvatar.png");
    },
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.selectedFileName = this.selectedFile ? this.selectedFile.name : "";
    },
    updateProfile() {
      const formData = new FormData();
      formData.append("username", this.user.username);
      formData.append("email", this.user.email);
      formData.append("user_id", this.user.user_id);
      formData.append("avatar", this.selectedFileName);
      if (this.selectedFile) {
        formData.append("avatar", this.selectedFile);
      }

      axios
        .post(
          "http://localhost:8000/Backend_Store/api/update_profile",
          formData
        )
        .then((response) => {
          // 处理成功响应
          if (response.data.status == "success") {
            console.log("更新用户数据成功", response);
          } else {
            console.log("用户数据更新失败：", response);
          }
        })
        .catch((error) => {
          console.log("catch用户数据更新失败：", response);
        });
    },
    backHome() {
      this.$router.push("/Home");
      setTimeout(() => window.location.reload(), 100);
    },
    async logout() {
      try {
        const response = await request.get(
          "http://localhost:8000/Backend_Store/api/logout"
        );
        if (response.data.status == "success") {
          console.log("成功注销");
          this.backHome();
          return;
        }
        console.log("注销失败", response.data.message);
      } catch (error) {
        console.log("回应异常", response.data.message);
        console.error("Error fetching user data:", error);
      }
    },
    async fetchUserData() {
      try {
        const response = await request.get(
          "http://localhost:8000/Backend_Store/api/checkLogin"
        );
        if (response.data.user_id != "-1") {
          this.user = response.data;
          this.selectedFileName = this.user.avatar;
          console.log("用户已登录", this.user);
          return;
        }
        console.log("用户未登录", response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
  },
  mounted() {
    this.fetchUserData();
  },
};
</script>

<style src="../assets/css/UserProfile.css" scoped></style>