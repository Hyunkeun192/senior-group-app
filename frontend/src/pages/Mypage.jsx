// src/pages/Mypage.jsx
import React, { useEffect, useState } from 'react';
import API from '../api/axiosInstance'; // ✅ axiosInstance import
import { motion } from 'framer-motion';

const Mypage = () => {
  const [user, setUser] = useState(null);
  const [myActivities, setMyActivities] = useState([]);
  const [notifications, setNotifications] = useState([]);

  const fetchUser = async () => {
    try {
      const res = await API.get('/auth/me');
      setUser(res.data);
    } catch (err) {
      console.error("사용자 정보 불러오기 실패:", err);
    }
  };

  const fetchActivityDetails = async (activityId) => {
    try {
      const res = await API.get(`/activities/${activityId}`);
      return res.data;
    } catch (err) {
      console.error("🔥 활동 정보 불러오기 실패", err);
      return null;
    }
  };

  const fetchMyActivities = async () => {
    try {
      const res = await API.get('/subscriptions/me');

      const enriched = await Promise.all(
        res.data.map(async (sub) => {
          const activity = await fetchActivityDetails(sub.activity_id);
          return { ...sub, activity };
        })
      );

      setMyActivities(enriched);
    } catch (err) {
      console.error("내 활동 목록 불러오기 실패:", err);
    }
  };

  const fetchNotifications = async () => {
    try {
      const res = await API.get('/notifications/me');
      setNotifications(res.data);
    } catch (err) {
      console.error("알림 목록 불러오기 실패:", err);
    }
  };

  const cancelParticipation = async (subscriptionId) => {
    if (!window.confirm("정말로 참여를 취소하시겠습니까?")) return;
    try {
      await API.delete(`/subscriptions/${subscriptionId}`);
      alert("참여가 취소되었습니다.");
      fetchMyActivities();
    } catch (err) {
      alert("취소에 실패했습니다.");
      console.error(err);
    }
  };

  const handleDeleteAccount = async () => {
    if (!window.confirm("정말로 탈퇴하시겠습니까?")) return;
    try {
      await API.delete('/users/me');
      alert("탈퇴가 완료되었습니다.");
      localStorage.clear();
      window.location.href = "/login";
    } catch (err) {
      alert("탈퇴 중 오류가 발생했습니다.");
      console.error(err);
    }
  };

  const getIcon = (message) => {
    if (message.includes("승인")) return "✅";
    if (message.includes("활동") || message.includes("클래스")) return "📢";
    return "🔔";
  };

  useEffect(() => {
    fetchUser();
    fetchMyActivities();
    fetchNotifications();
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="min-h-screen bg-[#FAF9F6] text-gray-800 font-sans px-6 py-12"
    >
      <div className="max-w-3xl mx-auto space-y-10">
        <h2 className="text-2xl font-semibold text-center">마이페이지</h2>

        {/* 사용자 정보 */}
        {user && (
          <section className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
            <h3 className="text-lg font-semibold mb-4">내 정보</h3>
            <ul className="text-sm space-y-1">
              <li><strong>이름:</strong> {user.username}</li>
              <li><strong>이메일:</strong> {user.email}</li>
              <li><strong>거주 지역:</strong> {user.location}</li>
            </ul>
          </section>
        )}

        {/* 참여한 활동 */}
        <section className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <h3 className="text-lg font-semibold mb-4">참여 중인 활동</h3>
          {myActivities.length === 0 ? (
            <p className="text-sm text-gray-500">참여한 활동이 없습니다.</p>
          ) : (
            <ul className="space-y-4">
              {myActivities.map((item) => (
                <li key={item.id} className="border border-gray-100 rounded p-4 text-sm">
                  <h4 className="font-semibold mb-1">{item.activity?.title || "제목 없음"}</h4>
                  <p>지역: {item.activity?.region}</p>
                  <p>관심사: {item.activity?.interest_category} / {item.activity?.interest_subcategory}</p>
                  <p>참여비: {item.activity?.price_per_person?.toLocaleString()}원</p>
                  <p>마감일: {item.activity?.deadline}</p>
                  <p>상태: {item.activity?.status === "confirmed" ? "확정됨 ✅" : "참여 대기 중 ⏳"}</p>

                  <div className="mt-2 flex flex-wrap gap-2">
                    <button
                      onClick={() => cancelParticipation(item.id)}
                      className="text-sm border border-red-400 text-red-600 px-3 py-1 rounded hover:bg-red-50"
                    >
                      참여 취소
                    </button>

                    {item.activity?.status === "confirmed" && (
                      <button
                        onClick={() => {
                          alert("결제 처리 로직 연결 예정!");
                          // window.location.href = `/payments/pay/${item.id}`;
                        }}
                        className="text-sm border border-green-500 text-green-600 px-3 py-1 rounded hover:bg-green-50"
                      >
                        결제하기
                      </button>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* 알림 목록 */}
        <section className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <h3 className="text-lg font-semibold mb-4">내 알림</h3>
          {notifications.length === 0 ? (
            <p className="text-sm text-gray-500">도착한 알림이 없습니다.</p>
          ) : (
            <ul className="space-y-4 text-sm">
              {notifications.map((n) => (
                <li
                  key={n.id}
                  className={`flex items-start gap-3 border p-4 rounded-lg shadow-sm ${n.status === "unread" ? "bg-yellow-50 border-yellow-300" : "bg-white border-gray-200"
                    }`}
                >
                  <div className="text-lg">{getIcon(n.message)}</div>
                  <div className="flex-1">
                    <p className="font-medium">{n.message}</p>
                    {n.created_at && (
                      <p className="text-xs text-gray-500 mt-1">{new Date(n.created_at).toLocaleString()}</p>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* 탈퇴 */}
        <div className="text-center">
          <button
            onClick={handleDeleteAccount}
            className="text-sm text-red-600 border border-red-500 px-4 py-2 rounded hover:bg-red-50"
          >
            회원 탈퇴
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default Mypage;
