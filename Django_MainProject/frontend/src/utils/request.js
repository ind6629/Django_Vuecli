import axios from 'axios'

const service = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  withCredentials: true, // 允许携带cookie
})

// 请求拦截器自动添加CSRF Token
service.interceptors.request.use(config => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  const csrfToken = match ? match[1] : null;
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken
  }
  return config
})

export default service