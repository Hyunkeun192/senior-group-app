// 이 코드는 관리자(Admin) 관련 API 요청을 axiosInstance를 이용해 깔끔하게 정리한 파일입니다.
import API from "./axiosInstance";

// 🔹 승인 대기 업체 목록 조회
export const fetchPendingProviders = async () => {
  const response = await API.get('/admin/pending-providers');
  return response.data;
};

// 🔹 업체 승인 처리
export const approveProvider = async (providerId) => {
  const response = await API.patch(`/admin/providers/${providerId}/approve`);
  return response.data;
};
