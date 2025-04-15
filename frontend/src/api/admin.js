// 관리자용 API 함수들

import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
});

// 관리자 JWT 토큰 설정
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 🔹 승인 대기 업체 목록 조회
export const fetchPendingProviders = () => API.get('/admin/pending-providers');

// 🔹 업체 승인 처리
export const approveProvider = (providerId) =>
  API.patch(`/admin/providers/${providerId}/approve`);
