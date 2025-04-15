// ✅ 업체 관련 API 함수
const BASE_URL = import.meta.env.VITE_API_BASE_URL; // 환경변수로 변경됨!

// ✅ 활동 목록 + 참여자 수 포함된 API 호출
export const getMyActivities = async (providerId, token) => {
  const response = await fetch(`${BASE_URL}/providers/${providerId}/activities/with-counts`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return await response.json();
};

// ✅ 마감일 수정
export const updateDeadline = async (activityId, newDate, token) => {
  await fetch(`${BASE_URL}/activities/${activityId}/deadline`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ new_deadline: new Date(newDate).toISOString() }),
  });
};

// ✅ 활동 확정
export const confirmActivity = async (activityId, token) => {
  const response = await fetch(`${BASE_URL}/activities/${activityId}/confirm`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "활동 확정 중 오류");
  }
};

// ✅ 활동 취소
export const cancelActivity = async (activityId, token) => {
  await fetch(`${BASE_URL}/activities/${activityId}/cancel`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
};
