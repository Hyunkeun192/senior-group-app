// src/pages/Login.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.removeItem("admin_token");
        localStorage.removeItem("provider");
        localStorage.setItem("access_token", data.access_token);
        alert("로그인 성공!");
        navigate("/");
      } else {
        alert(`로그인 실패: ${data.detail || "오류 발생"}`);
      }
    } catch (error) {
      alert("로그인 중 오류가 발생했습니다.");
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
      <div className="bg-white border border-gray-200 rounded-lg p-8 w-full max-w-md">
        <h2 className="text-xl font-semibold text-center mb-6">내 계정으로 들어가기</h2>

        <label className="block text-sm mb-1">이메일</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="이메일을 입력하세요"
          className="w-full mb-4 p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
          required
        />

        <label className="block text-sm mb-1">비밀번호</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="비밀번호를 입력하세요"
          className="w-full mb-6 p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
          required
        />

        <button
          onClick={handleLogin}
          className="w-full border border-gray-400 text-sm py-2 rounded hover:bg-gray-100 transition"
        >
          로그인
        </button>

        {/* ✅ 추가된 회원가입 유도 문구 */}
        <p className="mt-4 text-center text-sm">
          처음 이용하시나요?{" "}
          <Link to="/signup" className="text-blue-600 hover:underline">
          회원가입하고 시작하기기
          </Link>
        </p>
      </div>
    </motion.div>
  );
}

export default Login;
