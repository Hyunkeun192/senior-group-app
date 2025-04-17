// src/pages/Activities.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { regions, interestOptions } from '../utils/constants';
import { motion } from 'framer-motion';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [regionCategory, setRegionCategory] = useState('');
  const [regionSub, setRegionSub] = useState('');
  const [interestCategory, setInterestCategory] = useState('');
  const [interestSubcategory, setInterestSubcategory] = useState('');
  const navigate = useNavigate();

  const regionCategories = Object.keys(regions);
  const regionSubs = regionCategory ? regions[regionCategory] : [];

  const interestCategories = Object.keys(interestOptions);
  const interestSubs = interestCategory ? interestOptions[interestCategory] : [];

  const fetchActivities = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(`${API_BASE_URL}/activities`, {
        params: {
          region: regionCategory && regionSub ? `${regionCategory} ${regionSub}` : undefined,
          interest: interestSubcategory || undefined
        },
        headers: { Authorization: `Bearer ${token}` }
        
      });
      setActivities(response.data);
    } catch (error) {
      console.error("활동 목록 불러오기 실패:", error);
    }
  };

  useEffect(() => {
    fetchActivities();
  }, []);

  const handleFilter = () => {
    fetchActivities();
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="min-h-screen bg-[#FAF9F6] text-gray-800 font-sans px-6 py-12"
    >
      <h2 className="text-2xl font-semibold mb-6 text-center">전체 활동 목록</h2>

      {/* 🔍 필터 영역 */}
      <div className="mb-8 flex flex-wrap gap-4 items-center justify-center">
        <select
          value={regionCategory}
          onChange={(e) => { setRegionCategory(e.target.value); setRegionSub(''); }}
          className="border border-gray-300 px-4 py-2 rounded"
        >
          <option value="">도/광역시 선택</option>
          {regionCategories.map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>

        {regionCategory && (
          <select
            value={regionSub}
            onChange={(e) => setRegionSub(e.target.value)}
            className="border border-gray-300 px-4 py-2 rounded"
          >
            <option value="">시/군/구 선택</option>
            {regionSubs.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        )}

        <select
          value={interestCategory}
          onChange={(e) => { setInterestCategory(e.target.value); setInterestSubcategory(''); }}
          className="border border-gray-300 px-4 py-2 rounded"
        >
          <option value="">관심사 대분류 선택</option>
          {interestCategories.map((cat) => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>

        {interestCategory && (
          <select
            value={interestSubcategory}
            onChange={(e) => setInterestSubcategory(e.target.value)}
            className="border border-gray-300 px-4 py-2 rounded"
          >
            <option value="">소분류 선택</option>
            {interestSubs.map((sub) => (
              <option key={sub} value={sub}>{sub}</option>
            ))}
          </select>
        )}

        <button
          onClick={handleFilter}
          className="px-4 py-2 border border-gray-400 rounded hover:bg-gray-100 transition text-sm"
        >
          필터 적용
        </button>
      </div>

      {/* 🎨 활동 카드 리스트 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {activities.map((activity) => (
          <div
            key={activity.activity_id}
            className="bg-white border border-gray-200 rounded-lg p-6 cursor-pointer hover:shadow-sm transition"
            onClick={() => navigate(`/activities/${activity.id}`)}

          >
            <h3 className="text-lg font-semibold mb-1">{activity.title}</h3>
            <p className="text-sm text-gray-600">📍 지역: {activity.region}</p>
            <p className="text-sm text-gray-600">🎯 관심사: {activity.interest_category} / {activity.interest_subcategory}</p>
            <p className="text-sm text-gray-600">👥 인원: {activity.current_participants} / {activity.min_participants}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
};

export default Activities;
