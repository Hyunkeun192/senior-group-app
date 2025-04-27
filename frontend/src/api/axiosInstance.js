// 이 코드는 Axios 인스턴스를 생성하고 모든 요청에 JWT 토큰을 자동 첨부하기 위한 설정입니다.
import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000", // ✅ 환경변수 기반 서버 URL
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: false, // ✅ 쿠키 인증 대신 JWT 토큰을 헤더로 처리
});

// ✅ 요청 보내기 전 Authorization 헤더 자동 첨부
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token") || localStorage.getItem("admin_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default API;
