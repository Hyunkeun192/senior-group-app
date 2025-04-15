// src/pages/About.jsx
import React from 'react';
import { motion } from 'framer-motion';

const About = () => {
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
          <button onClick={() => window.location.href = '/'} className="text-sm hover:underline">홈</button>
          <button onClick={() => window.location.href = '/about'} className="text-sm hover:underline">회사 소개</button>
          <button onClick={() => window.location.href = '/notices'} className="text-sm hover:underline">공지사항</button>
          <button onClick={() => window.location.href = '/entry'} className="text-sm hover:underline">로그인</button>
        </div>
      </header>

      <main className="flex-grow flex flex-col items-center justify-center px-6 py-16 text-center">
        <h1 className="text-2xl md:text-3xl font-semibold leading-relaxed">
          함께하는 즐거운 취미생활,<br className="hidden md:block" />
          지금 시작해보세요.
        </h1>
      </main>

      <footer className="text-center text-xs text-gray-400 py-6">
        © 2025 Senior Group. All rights reserved.
      </footer>
    </motion.div>
  );
};

export default About;
