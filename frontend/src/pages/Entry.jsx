// src/pages/Entry.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const Entry = () => {
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="flex flex-col min-h-screen bg-[#FAF9F6] text-gray-800 font-sans"
    >
      <header className="sticky top-0 z-10 bg-white border-b border-gray-200 px-6 py-3">
        <div className="flex justify-end gap-4">
          <button onClick={() => navigate('/')} className="text-sm hover:underline">홈</button>
          <button onClick={() => navigate('/about')} className="text-sm hover:underline">회사 소개</button>
          <button onClick={() => navigate('/notices')} className="text-sm hover:underline">공지사항</button>
          <button onClick={() => navigate('/entry')} className="text-sm hover:underline">로그인</button>
        </div>
      </header>

      <main className="flex-grow flex flex-col items-center justify-center px-6 py-16 text-center gap-6">
        <h1 className="text-2xl md:text-3xl font-semibold">로그인 유형을 선택해주세요</h1>
        <div className="flex flex-col md:flex-row gap-4">
          <button
            onClick={() => navigate('/login')}
            className="px-6 py-3 border border-gray-300 rounded-md text-sm hover:bg-gray-100 transition"
          >
            나의 활동 시작하기
          </button>
          <button
            onClick={() => navigate('/provider-login')}
            className="px-6 py-3 border border-gray-300 rounded-md text-sm hover:bg-gray-100 transition"
          >
            활동 준비하시는 분
          </button>
        </div>
      </main>

      <footer className="text-center text-xs text-gray-400 py-6">
        © 2025 Senior Group. All rights reserved.
      </footer>
    </motion.div>
  );
};

export default Entry;
