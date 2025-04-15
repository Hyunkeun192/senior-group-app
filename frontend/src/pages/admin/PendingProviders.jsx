// src/pages/admin/PendingProviders.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

const PendingProviders = () => {
  const [pending, setPending] = useState([]);
  const [rejectingId, setRejectingId] = useState(null);
  const [rejectReason, setRejectReason] = useState("");

  const token = localStorage.getItem("admin_token");

  const fetchPending = async () => {
    try {
      const res = await axios.get("http://localhost:8000/admin/pending-providers", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setPending(res.data);
    } catch (err) {
      alert("업체 목록 불러오기 실패");
    }
  };

  const approve = async (id) => {
    try {
      await axios.patch(`http://localhost:8000/admin/providers/${id}/approve`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("승인 완료!");
      fetchPending();
    } catch (err) {
      alert("승인 실패");
    }
  };

  const reject = async () => {
    try {
      await axios.post(`http://localhost:8000/admin/providers/${rejectingId}/reject`, {
        reason: rejectReason,
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("거절 완료!");
      setRejectingId(null);
      setRejectReason("");
      fetchPending();
    } catch (err) {
      alert("거절 실패");
    }
  };

  useEffect(() => {
    fetchPending();
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="min-h-screen bg-[#FAF9F6] px-6 py-12 text-gray-800 font-sans"
    >
      <div className="max-w-3xl mx-auto">
        <h2 className="text-2xl font-semibold mb-6 text-center">승인 대기 업체</h2>

        {pending.length === 0 ? (
          <p className="text-sm text-center text-gray-500">승인 대기 중인 업체가 없습니다.</p>
        ) : (
          <ul className="space-y-6">
            {pending.map((p) => (
              <li key={p.id} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm text-sm">
                <p className="font-semibold mb-1">{p.name}</p>
                <p>대표자: {p.representative}</p>
                <p>이메일: {p.email}</p>
                <p>연락처: {p.phone}</p>
                <p>서비스 지역: {p.service_area}</p>

                <div className="flex gap-3 mt-4 flex-wrap">
                  <button
                    onClick={() => approve(p.id)}
                    className="px-4 py-1 border border-green-600 text-green-600 rounded hover:bg-green-50"
                  >
                    승인
                  </button>
                  <button
                    onClick={() => setRejectingId(p.id)}
                    className="px-4 py-1 border border-red-600 text-red-600 rounded hover:bg-red-50"
                  >
                    거절
                  </button>
                </div>

                {rejectingId === p.id && (
                  <div className="mt-4">
                    <label className="block text-sm mb-1">거절 사유 입력</label>
                    <input
                      value={rejectReason}
                      onChange={(e) => setRejectReason(e.target.value)}
                      className="w-full border border-gray-300 rounded p-2 mb-2"
                      placeholder="예: 정보 미비, 연락처 불분명 등"
                    />
                    <button
                      onClick={reject}
                      className="text-sm px-3 py-1 border border-red-500 text-red-600 rounded hover:bg-red-50"
                    >
                      사유 전송 및 거절 확정
                    </button>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </motion.div>
  );
};

export default PendingProviders;
