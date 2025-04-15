// src/pages/admin/InterestMerge.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

const InterestMerge = () => {
  const [interests, setInterests] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [mainCategory, setMainCategory] = useState("");
  const [subCategory, setSubCategory] = useState("");
  const token = localStorage.getItem("admin_token");

  const fetchCustomInterests = async () => {
    try {
      const res = await axios.get("http://localhost:8000/admin/custom-interests", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setInterests(res.data);
    } catch (err) {
      alert("관심사 목록 불러오기 실패");
    }
  };

  const handleToggle = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const handleMerge = async () => {
    if (!mainCategory || !subCategory || selectedIds.length === 0) {
      alert("대분류/소분류를 입력하고 관심사를 선택해주세요.");
      return;
    }
    try {
      await axios.post(
        "http://localhost:8000/admin/group-interests",
        {
          interest_ids: selectedIds,
          category: mainCategory,
          subcategory: subCategory,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      alert("관심사 통합이 완료되었습니다.");
      setSelectedIds([]);
      fetchCustomInterests();
    } catch (err) {
      alert("관심사 통합 실패");
    }
  };

  useEffect(() => {
    fetchCustomInterests();
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="min-h-screen bg-[#FAF9F6] px-6 py-12 text-gray-800 font-sans"
    >
      <div className="max-w-2xl mx-auto bg-white border border-gray-200 rounded-lg p-8 shadow-sm">
        <h2 className="text-xl font-semibold mb-6 text-center">🔀 관심사 통합 승인</h2>

        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-sm mb-1 font-medium">대분류</label>
            <input
              value={mainCategory}
              onChange={(e) => setMainCategory(e.target.value)}
              className="w-full border border-gray-300 rounded p-2 text-sm"
              placeholder="예: 문화, 운동, 예술"
            />
          </div>
          <div>
            <label className="block text-sm mb-1 font-medium">소분류</label>
            <input
              value={subCategory}
              onChange={(e) => setSubCategory(e.target.value)}
              className="w-full border border-gray-300 rounded p-2 text-sm"
              placeholder="예: 요가, 사진, 서예"
            />
          </div>
        </div>

        <h3 className="text-sm font-semibold mb-2">📌 주관식 관심사 목록</h3>
        <ul className="space-y-2 mb-6 max-h-64 overflow-y-auto">
          {interests.map((item) => (
            <li key={item.id} className="border border-gray-200 rounded px-3 py-2 flex items-center text-sm">
              <input
                type="checkbox"
                checked={selectedIds.includes(item.id)}
                onChange={() => handleToggle(item.id)}
                className="mr-2"
              />
              <span>{item.name} ({item.count})</span>
            </li>
          ))}
        </ul>

        <button
          onClick={handleMerge}
          className="w-full border border-blue-600 text-blue-600 py-2 rounded hover:bg-blue-50 text-sm"
        >
          선택 항목 통합 승인
        </button>
      </div>
    </motion.div>
  );
};

export default InterestMerge;
