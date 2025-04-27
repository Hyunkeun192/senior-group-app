// src/pages/ActivityDetail.jsx
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import API from '../api/axiosInstance'; // ✅ axiosInstance import
import { motion } from 'framer-motion';

const ActivityDetail = () => {
  const { id } = useParams();
  const [activity, setActivity] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchActivity = async () => {
      try {
        const res = await API.get(`/activities/${id}`);
        setActivity(res.data);
      } catch (err) {
        console.error("활동 정보를 불러오지 못했습니다.", err);
      }
    };

    fetchActivity();
  }, [id]);

  const handleParticipate = async () => {
    try {
      await API.post('/subscriptions', { activity_id: id });
      alert("참여 신청이 완료되었습니다!");
      navigate('/mypage');
    } catch (err) {
      alert("참여 신청에 실패했습니다.");
      console.error(err);
    }
  };

  if (!activity) return <div className="p-8">로딩 중...</div>;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="min-h-screen bg-[#FAF9F6] text-gray-800 font-sans px-6 py-12"
    >
      <div className="max-w-2xl mx-auto bg-white border border-gray-200 rounded-lg p-8 shadow-sm">
        <h2 className="text-2xl font-semibold mb-6">{activity.title}</h2>

        <ul className="space-y-3 text-sm text-gray-700">
          <li><strong>설명:</strong> {activity.description}</li>
          <li><strong>지역:</strong> {activity.region}</li>
          <li><strong>관심사:</strong> {activity.interest_category} / {activity.interest_subcategory}</li>
          <li><strong>참여비:</strong> {activity.price_per_person.toLocaleString()}원</li>
          <li><strong>모집 인원:</strong> {activity.current_participants} / {activity.min_participants}</li>
          <li><strong>마감일:</strong> {activity.deadline ? activity.deadline.slice(0, 10) : "정보 없음"}</li>
        </ul>

        <button
          onClick={handleParticipate}
          className="mt-6 w-full border border-gray-400 py-2 rounded hover:bg-gray-100 transition text-sm"
        >
          참여 신청
        </button>
      </div>
    </motion.div>
  );
};

export default ActivityDetail;
