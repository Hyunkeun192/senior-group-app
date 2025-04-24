// 이 코드는 공통 axios 인스턴스를 생성해 API 호출에 사용할 수 있도록 설정합니다.
import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // 인증이 필요한 요청에 쿠키를 포함하기 위해 사용됩니다.
});

export default API;
