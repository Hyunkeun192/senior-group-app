// src/pages/admin/UserManagement.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState("created_at");
  const [order, setOrder] = useState("desc");

  const token = localStorage.getItem("admin_token");

  const fetchUsers = async () => {
    try {
      const res = await axios.get("http://localhost:8000/admin/users", {
        params: { search, sort, order },
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(res.data);
    } catch (err) {
      console.error("사용자 목록 조회 실패:", err);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [search, sort, order]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="min-h-screen bg-[#FAF9F6] px-6 py-12 text-gray-800 font-sans"
    >
      <div className="max-w-5xl mx-auto">
        <h2 className="text-2xl font-semibold mb-6 text-center">👤 사용자 관리</h2>

        {/* 검색/정렬 */}
        <div className="flex flex-wrap gap-3 items-center justify-center mb-6">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="이름 또는 이메일 검색"
            className="border border-gray-300 rounded px-4 py-2 text-sm"
          />
          <select value={sort} onChange={(e) => setSort(e.target.value)} className="border px-3 py-2 rounded text-sm">
            <option value="created_at">가입일</option>
            <option value="name">이름</option>
            <option value="email">이메일</option>
          </select>
          <select value={order} onChange={(e) => setOrder(e.target.value)} className="border px-3 py-2 rounded text-sm">
            <option value="desc">내림차순</option>
            <option value="asc">오름차순</option>
          </select>
        </div>

        {/* 사용자 테이블 */}
        <div className="overflow-x-auto bg-white border border-gray-200 rounded-lg">
          <table className="min-w-full text-sm text-left">
            <thead className="bg-gray-100 text-gray-600">
              <tr>
                <th className="px-4 py-2 border">이름</th>
                <th className="px-4 py-2 border">이메일</th>
                <th className="px-4 py-2 border">지역</th>
                <th className="px-4 py-2 border">가입일</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id} className="border-t hover:bg-gray-50">
                  <td className="px-4 py-2 border">{user.username}</td>
                  <td className="px-4 py-2 border">{user.email}</td>
                  <td className="px-4 py-2 border">{user.location}</td>
                  <td className="px-4 py-2 border">{user.created_at?.slice(0, 10)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  );
};

export default UserManagement;
