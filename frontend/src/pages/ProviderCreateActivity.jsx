import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { interestOptions, regions } from "../utils/constants";
import { motion } from "framer-motion";

const BASE_URL = "http://localhost:8000";

const ProviderCreateActivity = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    interest_category: "",
    interest_subcategory: "",
    min_participants: 1,
    deadline: "",
    price_per_person: 0,
  });

  const [regionCategory, setRegionCategory] = useState("");
  const [regionSub, setRegionSub] = useState("");

  const regionCategories = Object.keys(regions);
  const regionSubs = regionCategory ? regions[regionCategory] : [];

  const token = localStorage.getItem("access_token");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const providerRaw = localStorage.getItem("provider");
    if (!providerRaw) {
      alert("인증 정보가 만료되었습니다. 다시 로그인해주세요.");
      navigate("/provider-login");
      return;
    }

    const provider = JSON.parse(providerRaw);

    const activityData = {
      ...formData,
      provider_id: provider.id,
      region: regionCategory && regionSub ? `${regionCategory} ${regionSub}` : null,
      min_participants: parseInt(formData.min_participants, 10),
      price_per_person: parseFloat(formData.price_per_person),
    };

    try {
      const res = await fetch(`${BASE_URL}/activities`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(activityData),
      });

      if (res.ok) {
        alert("활동이 등록되었습니다!");
        navigate("/provider/dashboard");
      } else if (res.status === 403) {
        alert("권한이 없습니다. 다시 로그인해주세요.");
        navigate("/provider-login");
      } else {
        const error = await res.json();
        alert("등록 실패: " + (error.detail || "에러 발생"));
      }
    } catch (err) {
      alert("서버 연결 오류");
    }
  };

  const subcategories = interestOptions[formData.interest_category] || [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="min-h-screen bg-[#FAF9F6] text-gray-800 font-sans px-6 py-12"
    >
      <div className="max-w-2xl mx-auto bg-white border border-gray-200 rounded-lg p-8 shadow-sm">
        <h2 className="text-xl font-semibold mb-6 text-center">📌 활동 등록</h2>
        <form onSubmit={handleSubmit} className="space-y-4 text-sm">
          <div>
            <label className="block mb-1 font-medium">활동 제목</label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded p-2"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">활동 설명</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={3}
              className="w-full border border-gray-300 rounded p-2"
              required
            />
          </div>

          {/* ✅ 지역 선택 */}
          <div>
            <label className="block mb-1 font-medium">활동 지역 (도/광역시)</label>
            <select
              value={regionCategory}
              onChange={(e) => {
                setRegionCategory(e.target.value);
                setRegionSub("");
              }}
              className="w-full border border-gray-300 rounded p-2"
              required
            >
              <option value="">도/광역시 선택</option>
              {regionCategories.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          {regionCategory && (
            <div>
              <label className="block mb-1 font-medium">활동 지역 (시/군/구)</label>
              <select
                value={regionSub}
                onChange={(e) => setRegionSub(e.target.value)}
                className="w-full border border-gray-300 rounded p-2"
                required
              >
                <option value="">시/군/구 선택</option>
                {regionSubs.map((sub) => (
                  <option key={sub} value={sub}>{sub}</option>
                ))}
              </select>
            </div>
          )}

          <div>
            <label className="block mb-1 font-medium">관심사 대분류</label>
            <select
              name="interest_category"
              value={formData.interest_category}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded p-2"
              required
            >
              <option value="">선택하세요</option>
              {Object.keys(interestOptions).map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-1 font-medium">관심사 소분류</label>
            <select
              name="interest_subcategory"
              value={formData.interest_subcategory}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded p-2"
              disabled={!formData.interest_category}
              required
            >
              <option value="">선택하세요</option>
              {subcategories.map((sub) => (
                <option key={sub} value={sub}>{sub}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block mb-1 font-medium">최소 참여 인원</label>
            <input
              type="number"
              name="min_participants"
              value={formData.min_participants}
              onChange={handleChange}
              min={1}
              className="w-full border border-gray-300 rounded p-2"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">마감일</label>
            <input
              type="date"
              name="deadline"
              value={formData.deadline}
              onChange={handleChange}
              min={new Date().toISOString().split("T")[0]}
              className="w-full border border-gray-300 rounded p-2"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">인당 비용 (₩)</label>
            <input
              type="number"
              name="price_per_person"
              value={formData.price_per_person}
              onChange={handleChange}
              min={0}
              className="w-full border border-gray-300 rounded p-2"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full border border-gray-400 text-sm py-2 rounded hover:bg-gray-100 transition"
          >
            활동 등록하기
          </button>
        </form>
      </div>
    </motion.div>
  );
};

export default ProviderCreateActivity;
