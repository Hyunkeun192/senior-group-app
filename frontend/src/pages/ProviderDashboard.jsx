// src/pages/ProviderDashboard.jsx
import React, { useEffect, useState } from "react";
import { format } from "date-fns";
import {
  getMyActivities,
  updateDeadline,
  confirmActivity,
  cancelActivity
} from "../api/provider";
import { motion } from "framer-motion";

// ✅ 상단에 환경 변수에서 API 주소 불러오기 추가
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const ProviderDashboard = () => {
  const [activities, setActivities] = useState([]);
  const [providerId, setProviderId] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const userInfo = JSON.parse(localStorage.getItem("provider"));
    if (token && userInfo?.id) {
      setProviderId(userInfo.id);
      fetchActivities(userInfo.id, token);
    }
  }, []);

  const fetchActivities = async (id, token) => {
    const res = await getMyActivities(id, token);
    setActivities(res);
  };

  const handleDeadlineChange = async (activityId, newDate) => {
    const today = new Date().toISOString().split("T")[0];
    if (newDate < today) {
      alert("오늘 이전 날짜는 선택할 수 없습니다.");
      return;
    }
    const token = localStorage.getItem("access_token");
    await updateDeadline(activityId, newDate, token);
    alert("마감일이 수정되었습니다.");
    fetchActivities(providerId, token);
  };

  const handleConfirmActivity = async (activityId) => {
    const token = localStorage.getItem("access_token");
    try {
      await confirmActivity(activityId, token);
      alert("활동이 확정되었습니다.");
      fetchActivities(providerId, token);
    } catch (error) {
      let message = "활동 확정에 실패했습니다.";
      if (error instanceof Response) {
        const data = await error.json();
        if (data.detail) message = data.detail;
      }
      alert(message);
    }
  };

  const handleCancel = async (activityId) => {
    const token = localStorage.getItem("access_token");
    try {
      await cancelActivity(activityId, token);
      alert("활동이 취소되었습니다.");
      fetchActivities(providerId, token);
    } catch (error) {
      alert("활동 취소에 실패했습니다.");
      console.error(error);
    }
  };

  const handleDeleteProvider = async () => {
    if (!window.confirm("정말로 탈퇴하시겠습니까?")) return;

    try {
      const token = localStorage.getItem("access_token");
      await fetch(`${API_BASE_URL}/providers/me`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      alert("탈퇴가 완료되었습니다.");
      localStorage.removeItem("access_token");
      localStorage.removeItem("provider");
      window.location.href = "/provider-login";
    } catch (err) {
      alert("탈퇴 중 오류가 발생했습니다.");
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="min-h-screen bg-[#FAF9F6] text-gray-800 font-sans px-6 py-12"
    >
      <div className="max-w-4xl mx-auto">
        <h2 className="text-2xl font-semibold mb-6 text-center">나의 활동 관리</h2>

        <div className="space-y-6">
          {activities
            .filter((activity) => activity.status !== "cancelled")
            .map((activity) => (
              <div key={activity.activity_id} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold mb-2">{activity.title}</h3>
                <p className="text-sm text-gray-700 mb-1">
                  👥 모집 인원: {activity.current_participants}
                  {activity.min_participants ? ` / ${activity.min_participants}` : ""}
                </p>
                <p className="text-sm text-gray-700 mb-1">
                  📅 마감일: {activity.deadline ? activity.deadline.slice(0, 10) : "미정"}
                </p>

                <div className="flex flex-wrap gap-3 mt-4 items-center">
                  <label className="text-sm">
                    마감일 변경:
                    <input
                      type="date"
                      defaultValue={activity.deadline ? activity.deadline.slice(0, 10) : ""}
                      onChange={(e) => handleDeadlineChange(activity.activity_id, e.target.value)}
                      className="ml-2 border border-gray-300 rounded px-2 py-1 text-sm"
                      min={new Date().toISOString().split("T")[0]}
                    />
                  </label>

                  {activity.status === "recruiting" && (
                    <button
                      onClick={() => handleConfirmActivity(activity.activity_id)}
                      className="text-sm border border-green-500 text-green-600 px-3 py-1 rounded hover:bg-green-50"
                    >
                      활동 확정
                    </button>
                  )}

                  <button
                    onClick={() => handleCancel(activity.activity_id)}
                    className="text-sm border border-red-500 text-red-600 px-3 py-1 rounded hover:bg-red-50"
                  >
                    활동 취소
                  </button>
                </div>
              </div>
            ))}
        </div>

        {/* 업체 탈퇴 */}
        <div className="mt-10 text-center">
          <button
            onClick={handleDeleteProvider}
            className="text-sm text-red-600 border border-red-500 px-4 py-2 rounded hover:bg-red-50"
          >
            업체 탈퇴
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default ProviderDashboard;
