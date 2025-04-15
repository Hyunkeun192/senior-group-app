// src/pages/AdminDashboard.jsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer,
  LineChart, Line, Legend
} from "recharts";
import { motion } from "framer-motion";

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [regionData, setRegionData] = useState([]);
  const [registrationData, setRegistrationData] = useState([]);
  const [showRegionChart, setShowRegionChart] = useState(false);
  const [showDateChart, setShowDateChart] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("admin_token");
    if (!token) {
      alert("로그인이 필요합니다.");
      navigate("/admin-login");
      return;
    }

    fetch("http://localhost:8000/admin/stats/summary", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("통계 로딩 오류", err));
  }, []);

  const fetchRegionStats = async () => {
    const token = localStorage.getItem("admin_token");
    try {
      const res = await fetch("http://localhost:8000/admin/stats/users-by-region", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setRegionData(data);
      setShowRegionChart(true);
      setShowDateChart(false);
    } catch (err) {
      alert("지역별 통계 불러오기 실패: " + err.message);
    }
  };

  const fetchRegistrationStats = async () => {
    const token = localStorage.getItem("admin_token");
    try {
      const res = await fetch("http://localhost:8000/admin/stats/registrations-by-date", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setRegistrationData(data);
      setShowDateChart(true);
      setShowRegionChart(false);
    } catch (err) {
      alert("날짜별 통계 불러오기 실패: " + err.message);
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
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-semibold text-center mb-10">👋 관리자님 환영합니다!</h1>

        {stats ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
            <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm text-center">
              <p className="text-sm text-gray-500 mb-2">전체 사용자</p>
              <p className="text-2xl font-bold">{stats.total_users}</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm text-center">
              <p className="text-sm text-gray-500 mb-2">전체 업체</p>
              <p className="text-2xl font-bold">{stats.total_providers}</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm text-center">
              <p className="text-sm text-gray-500 mb-2">관리자 수</p>
              <p className="text-2xl font-bold">{stats.total_admins}</p>
            </div>
          </div>
        ) : (
          <p className="text-sm text-gray-500 text-center">통계 데이터를 불러오는 중...</p>
        )}

        <div className="flex flex-wrap gap-4 justify-center mb-10">
          <button
            onClick={fetchRegionStats}
            className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 text-sm"
          >
            📍 지역별 사용자 통계
          </button>
          <button
            onClick={fetchRegistrationStats}
            className="px-4 py-2 border border-green-600 text-green-600 rounded hover:bg-green-50 text-sm"
          >
            📅 날짜별 가입 통계
          </button>
          <button
            onClick={() => navigate("/admin/interests")}
            className="px-4 py-2 border border-purple-600 text-purple-600 rounded hover:bg-purple-50 text-sm"
          >
            🔀 관심사 통합 승인
          </button>
          <button
            onClick={() => navigate("/admin/users")}
            className="px-4 py-2 border border-sky-600 text-sky-600 rounded hover:bg-sky-50 text-sm"
          >
            👤 사용자 관리
          </button>
          <button
            onClick={() => navigate("/admin/providers")}
            className="px-4 py-2 border border-amber-600 text-amber-600 rounded hover:bg-amber-50 text-sm"
          >
            🏢 업체 관리
          </button>
        </div>

        {showRegionChart && (
          <div className="bg-white border border-gray-200 p-6 rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold mb-4">📊 지역별 사용자 분포</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={regionData} layout="vertical" margin={{ left: 60 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="region" type="category" />
                <Tooltip />
                <Bar dataKey="count" fill="#60A5FA" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {showDateChart && (
          <div className="bg-white border border-gray-200 p-6 rounded-lg shadow-sm mt-10">
            <h2 className="text-lg font-semibold mb-4">📈 날짜별 가입자 수</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={registrationData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="user_count" stroke="#60A5FA" name="사용자" />
                <Line type="monotone" dataKey="provider_count" stroke="#34D399" name="업체" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </motion.div>
  );
}

export default AdminDashboard;
