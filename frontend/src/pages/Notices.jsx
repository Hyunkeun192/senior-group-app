// src/pages/Notices.jsx
import React from 'react';
import { motion } from 'framer-motion';

const Notices = () => {
  const notices = [
    {
      title: '시니어 활동 추천 시스템 도입',
      content: 'AI 기반 맞춤 추천 시스템이 이번 달부터 정식 적용됩니다. 나에게 맞는 활동을 자동으로 찾아보세요!'
    },
    {
      title: '5월 신규 클래스 오픈',
      content: '요가, 그림, 사진 클래스 등 5월 신규 프로그램이 개설되었습니다. 지금 확인하고 참여해보세요.'
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="flex flex-col min-h-screen bg-[#FAF9F6] text-gray-800 font-sans"
    >
      {/* Header */}
      <header className="sticky top-0 z-10 bg-white border-b border-gray-200 px-6 py-3">
        <div className="flex justify-end gap-4">
          <button onClick={() => window.location.href = '/'} className="text-sm hover:underline">홈</button>
          <button onClick={() => window.location.href = '/about'} className="text-sm hover:underline">회사 소개</button>
          <button onClick={() => window.location.href = '/notices'} className="text-sm hover:underline">공지사항</button>
          <button onClick={() => window.location.href = '/entry'} className="text-sm hover:underline">로그인</button>
        </div>
      </header>

      {/* Main */}
      <main className="flex-grow px-6 py-16 max-w-3xl mx-auto">
        <h1 className="text-2xl md:text-3xl font-semibold text-center mb-10">공지사항</h1>
        <div className="flex flex-col gap-6">
          {notices.map((notice, index) => (
            <div key={index} className="bg-white border border-gray-200 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-2">{notice.title}</h2>
              <p className="text-gray-700 leading-relaxed text-base">{notice.content}</p>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-6">
        © 2025 Senior Group. All rights reserved.
      </footer>
    </motion.div>
  );
};

export default Notices;
