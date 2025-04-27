// 이 코드는 업체(Provider) 관련 API 요청을 axiosInstance를 이용해 깔끔하게 정리한 파일입니다.
import API from "./axiosInstance";

// ✅ 활동 목록 + 참여자 수 포함 조회
export const getMyActivities = async (providerId) => {
  const response = await API.get(`/providers/${providerId}/activities/with-counts`);
  return response.data;
};

// ✅ 마감일 수정
export const updateDeadline = async (activityId, newDate) => {
  const response = await API.patch(`/activities/${activityId}/deadline`, {
    new_deadline: new Date(newDate).toISOString(),
  });
  return response.data;
};

// ✅ 활동 확정
export const confirmActivity = async (activityId) => {
  const response = await API.patch(`/activities/${activityId}/confirm`);
  return response.data;
};

// ✅ 활동 취소
export const cancelActivity = async (activityId) => {
  const response = await API.patch(`/activities/${activityId}/cancel`);
  return response.data;
};
