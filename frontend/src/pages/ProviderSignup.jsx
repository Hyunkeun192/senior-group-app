// src/pages/ProviderSignup.jsx
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { regions as REGIONS } from "../utils/constants";
import { motion } from "framer-motion";

const ProviderSignup = () => {
  const [form, setForm] = useState({
    name: "",
    email: "",
    service_name: "",
    phone: "",
    password: "",
    service_area: "",
    is_business: 1,
    business_registration_number: ""
  });

  const [selectedDo, setSelectedDo] = useState("");
  const [selectedSiGun, setSelectedSiGun] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleRadioChange = (e) => {
    const value = parseInt(e.target.value);
    setForm((prev) => ({
      ...prev,
      is_business: value,
      business_registration_number: value === 1 ? prev.business_registration_number : ""
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const fullRegion = `${selectedDo} ${selectedSiGun}`;
    const dataToSend = { ...form, service_area: fullRegion };

    try {
      await axios.post("http://localhost:8000/providers", dataToSend);
      alert("회원가입 성공! 로그인 페이지로 이동합니다.");
      navigate("/provider-login");
    } catch (err) {
      alert("회원가입 실패! 입력 정보를 확인해주세요.");
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="flex items-center justify-center min-h-screen bg-[#FAF9F6] text-gray-800 font-sans"
    >
      <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-lg p-8 w-full max-w-3xl">
        <h2 className="text-xl font-semibold text-center mb-6">업체 회원가입</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm">대표자명</label>
            <input type="text" name="name" value={form.name} onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded" required />
          </div>

          <div>
            <label className="text-sm">이메일</label>
            <input type="email" name="email" value={form.email} onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded" required />
          </div>

          <div>
            <label className="text-sm">업체명 (서비스명)</label>
            <input type="text" name="service_name" value={form.service_name} onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded" required />
          </div>

          <div>
            <label className="text-sm">연락처</label>
            <input type="text" name="phone" value={form.phone} onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded" required />
          </div>

          <div>
            <label className="text-sm">서비스 지역 (도)</label>
            <select value={selectedDo} onChange={(e) => { setSelectedDo(e.target.value); setSelectedSiGun(""); }}
              className="w-full p-2 border border-gray-300 rounded" required>
              <option value="">선택</option>
              {Object.keys(REGIONS).map((doName) => (
                <option key={doName} value={doName}>{doName}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm">서비스 지역 (시/군/구)</label>
            <select value={selectedSiGun} onChange={(e) => setSelectedSiGun(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded" required disabled={!selectedDo}>
              <option value="">선택</option>
              {selectedDo && REGIONS[selectedDo].map((siGun) => (
                <option key={siGun} value={siGun}>{siGun}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm">비밀번호</label>
            <input type="password" name="password" value={form.password} onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded" required />
          </div>

          <div className="col-span-2">
            <label className="text-sm block mb-1">사업자 구분</label>
            <div className="flex gap-4">
              <label className="text-sm">
                <input type="radio" name="is_business" value={1} checked={form.is_business === 1} onChange={handleRadioChange} />
                <span className="ml-1">사업자</span>
              </label>
              <label className="text-sm">
                <input type="radio" name="is_business" value={0} checked={form.is_business === 0} onChange={handleRadioChange} />
                <span className="ml-1">개인</span>
              </label>
            </div>
          </div>

          {form.is_business === 1 && (
            <div className="col-span-2">
              <label className="text-sm">사업자등록번호</label>
              <input type="text" name="business_registration_number"
                value={form.business_registration_number}
                onChange={handleChange}
                className="w-full p-2 border border-gray-300 rounded" />
            </div>
          )}
        </div>

        <button type="submit"
          className="mt-6 w-full border border-gray-400 text-sm py-2 rounded hover:bg-gray-100 transition">
          회원가입
        </button>
      </form>
    </motion.div>
  );
};

export default ProviderSignup;
