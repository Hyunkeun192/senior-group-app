// src/pages/AdminLogin.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

function AdminLogin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || "로그인 실패");
      }

      const data = await res.json();
      localStorage.setItem("admin_token", data.access_token);
      alert("관리자 로그인 성공!");
      navigate("/admin");
    } catch (err) {
      alert("오류: " + err.message);
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
        <h2 className="text-xl font-semibold text-center mb-6">관리자 로그인</h2>

        <label className="block text-sm mb-1">이메일</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-4 p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
          required
        />

        <label className="block text-sm mb-1">비밀번호</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-6 p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
          required
        />

        <button
          type="submit"
          className="w-full border border-gray-400 text-sm py-2 rounded hover:bg-gray-100 transition"
        >
          로그인
        </button>
      </form>
    </motion.div>
  );
}

export default AdminLogin;
