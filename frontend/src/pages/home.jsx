import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { interestOptions } from '../utils/constants';
import bannerImage1 from '../assets/image1.png';
import bannerImage2 from '../assets/image2.png';
import bannerImage3 from '../assets/image3.png';
import bannerImage4 from '../assets/image4.png';
import bannerImage5 from '../assets/image5.png';
import API from '../api/axiosInstance'; // ✅ axios 인스턴스 불러오기

const images = [bannerImage1, bannerImage2, bannerImage3, bannerImage4, bannerImage5];

const Home = () => {
  const navigate = useNavigate();
  const [currentImage, setCurrentImage] = useState(0);
  const [activities, setActivities] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const isLoggedIn = !!localStorage.getItem("access_token");

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % images.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // ✅ API 호출 부분 수정
  useEffect(() => {
    API.get('/activities')
      .then(res => {
        console.log("✅ 활동 데이터:", res.data);
        alert(`✅ 활동 ${res.data.length}건 불러옴`);
        setActivities(res.data);
      })
      .catch(err => {
        console.error("❌ 활동 API 호출 실패:", err);
        alert("❌ API 호출 실패: " + err.message);
      });
  }, []);

  const filteredActivities = activities.filter((a) => {
    const matchCategory = selectedCategory ? a.interest_category === selectedCategory : true;
    const matchSearch = searchKeyword ? a.title.includes(searchKeyword) || a.description.includes(searchKeyword) : true;
    return matchCategory && matchSearch;
  });

  const handleActivityClick = (activityId) => {
    if (!isLoggedIn) {
      navigate('/login');
    } else {
      navigate(`/activities/${activityId}`);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="flex flex-col min-h-screen bg-[#FAF9F6] text-gray-800 font-sans"
    >
      <div className="w-full max-w-xl mx-auto mt-20 px-4">

        {/* 🔍 검색 바 */}
        <div className="flex items-center w-full border border-gray-300 rounded-full px-4 py-2 shadow-sm mb-6">
          <span className="text-gray-400 mr-2">🔍</span>
          <input
            type="text"
            value={searchKeyword}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') setSearchKeyword(searchQuery); }}
            placeholder="나의 주변에 어떤 활동들이 있는지 찾아보세요"
            className="flex-1 outline-none text-sm bg-transparent"
          />
          <button onClick={() => setSearchKeyword(searchQuery)} className="ml-2 px-3 py-1 text-sm border rounded-full bg-white hover:bg-gray-100">검색</button>
        </div>

        {/* 🖼 이미지 슬라이드 */}
        <div className="relative rounded-lg overflow-hidden shadow-md mb-8">
          <img
            src={images[currentImage]}
            alt="배너"
            className="w-full object-cover h-[153.6px] sm:h-[192px] md:h-[230.4px] lg:h-[276px] xl:h-[307.2px] transition-opacity duration-500 ease-in-out"
          />
          <div className="absolute inset-0 bg-black bg-opacity-30 flex flex-col justify-center items-center text-white text-center px-4">
            {!isLoggedIn && (<h2 className="text-lg md:text-xl font-semibold mb-2 drop-shadow">지금 내 주변에서 어떤 활동이 열리고 있을까요?</h2>)}
            {!isLoggedIn && (<button onClick={() => navigate('/activities')} className="mt-2 px-4 py-2 bg-white text-gray-800 rounded-full text-sm shadow hover:bg-gray-100 transition">활동 둘러보기</button>)}
          </div>
        </div>

        {/* 🎨 관심사 카드 */}
        <section className="w-full grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2 py-4">
          {["전체", ...Object.keys(interestOptions)].map((category, idx) => (
            <motion.div
              key={idx}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setSelectedCategory(category === selectedCategory ? null : (category === "전체" ? null : category))}
              className={`cursor-pointer p-4 rounded-xl border border-gray-300 shadow-sm text-center text-sm transition ${
                selectedCategory === category ? 'bg-blue-100 border-blue-400' : 'bg-white hover:bg-pink-50'
              }`}
            >
              <div className="text-2xl mb-2">
                {(() => {
                  switch (category) {
                    case "운동/스포츠": return "🏃";
                    case "예술/취미": return "🎨";
                    case "음악/공연": return "🎵";
                    case "건강/웰빙": return "🧘";
                    case "여행/산책/나들이": return "🧳";
                    case "봉사/사회참여": return "🤝";
                    case "교육/자기계발": return "📘";
                    case "요리/식생활": return "🍳";
                    case "반려동물/가드닝": return "🌿";
                    case "커뮤니티/친목": return "👥";
                    case "생활기술": return "🛠";
                    default: return "🎯";
                }})()}
              </div>
              <p className="font-medium truncate">{category}</p>
            </motion.div>
          ))}
        </section>

        {/* 📦 활동 목록 */}
        <section className="w-full py-6">
          <h2 className="text-lg font-semibold mb-4">{selectedCategory ? `선택한 관심사: ${selectedCategory}` : '진행 중인 활동'}</h2>
          
          {filteredActivities.length === 0 ? (
            <p className="text-sm text-center text-gray-400">표시할 활동이 없습니다.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {filteredActivities.map((a) => (
                <div
                  key={a.id}
                  onClick={() => handleActivityClick(a.id)}
                  className="bg-white border border-gray-400 rounded-xl p-4 shadow-sm hover:shadow-md hover:bg-green-50 transition cursor-pointer"
                >
                  <h3 className="text-base font-semibold mb-2 truncate">{a.title}</h3>
                  <p className="text-sm text-gray-500 mb-1">지역: {a.region}</p>
                  <p className="text-sm text-gray-500">참여비: {a.price_per_person?.toLocaleString()}원</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </motion.div>
  );
};

export default Home;
