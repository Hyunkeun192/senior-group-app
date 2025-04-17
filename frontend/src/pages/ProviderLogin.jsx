// src/pages/ProviderLogin.jsx
import React, { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const ProviderLogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);

      const res = await axios.post(`${API_BASE_URL}/providers/login`, params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      const token = res.data.access_token;
      const providerInfo = res.data.provider;

      localStorage.removeItem("admin_token");
      localStorage.setItem("access_token", token);
      localStorage.setItem("provider", JSON.stringify(providerInfo));
      alert("로그인 성공!");
      navigate("/provider/dashboard");
    } catch (err) {
      alert("로그인 실패! 이메일 또는 비밀번호를 확인해주세요.");
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
      <form onSubmit={handleLogin} className="bg-white border border-gray-200 rounded-lg p-8 w-full max-w-md">
        <h2 className="text-xl font-semibold text-center mb-6">업체 로그인</h2>

        <label className="block text-sm mb-1">이메일</label>
        <input
          type="email"
          className="w-full mb-4 p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label className="block text-sm mb-1">비밀번호</label>
        <input
          type="password"
          className="w-full mb-6 p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          className="w-full border border-gray-400 text-sm py-2 rounded hover:bg-gray-100 transition"
        >
          로그인
        </button>

        <p className="mt-4 text-center text-sm">
          아직 가입하지 않으셨나요?{" "}
          <Link to="/provider-signup" className="text-blue-600 hover:underline">
            업체 회원가입
          </Link>
        </p>
      </form>
    </motion.div>
  );
};

export default ProviderLogin;
