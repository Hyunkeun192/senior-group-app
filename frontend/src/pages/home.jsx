import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { interestMap } from '../utils/interestMap';
import bannerImage1 from '../assets/image1.png';
import bannerImage2 from '../assets/image2.png';
import bannerImage3 from '../assets/image3.png';
import bannerImage4 from '../assets/image4.png';
import bannerImage5 from '../assets/image5.png';
import API from '../api/axiosInstance';
import WeatherBox from '../components/WeatherBox';

const images = [bannerImage1, bannerImage2, bannerImage3, bannerImage4, bannerImage5];

const categoryToEmoji = (category) => {
  switch (category) {
    case "운동/스포츠": return "🏃";
    case "예술/취미/공예": return "🎨";
    case "음악/공연/무용": return "🎵";
    case "건강/힐링/웰빙": return "🧘";
    case "여행/문화탐방": return "🧳";
    case "봉사/사회참여": return "🤝";
    case "교육/디지털역량": return "📱";
    case "요리/식생활/전통음식": return "🍳";
    case "반려동물/가드닝": return "🌿";
    case "커뮤니티/모임/동아리": return "👥";
    case "생활기술/셀프메이킹": return "💖";
    case "사진/영상/디지털 컨텐츠": return "📷";
    case "자서전/구작/출판": return "✍️";
    case "가계/재미/재테크": return "💰";
    case "자기계발/심리/멘탈캠": return "🧠";
    default: return "🎯";
  }
};

const Home = () => {
  const navigate = useNavigate();
  const [currentImage, setCurrentImage] = useState(0);
  const [activities, setActivities] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [weatherData, setWeatherData] = useState(null);
  const [error, setError] = useState(null);
  const [itemsPerPage, setItemsPerPage] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);

  const isLoggedIn = !!localStorage.getItem("access_token");

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % images.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    API.get('/activities/')
      .then(res => {
        setActivities(res.data);
      })
      .catch(err => {
        console.error("❌ 활동 API 호출 실패:", err);
        setError(err.message || "API 호출 실패");
      });
  }, []);

  useEffect(() => {
    API.get('/weather/full?city=Seoul')
      .then(res => {
        setWeatherData(res.data);
      })
      .catch(err => {
        console.error("❌ 날씨 API 호출 실패:", err);
      });
  }, []);

  const filteredActivities = Array.isArray(activities) ? activities.filter((a) => {
    const matchCategory = selectedCategory && selectedCategory !== "전체"
      ? a.interest_category === selectedCategory
      : true;
    const matchSearch = searchKeyword
      ? a.title.includes(searchKeyword) || a.description.includes(searchKeyword)
      : true;
    return matchCategory && matchSearch;
  }) : [];

  const totalPages = Math.ceil(filteredActivities.length / itemsPerPage);

  const currentActivities = filteredActivities.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handleActivityClick = (activityId) => {
    if (!isLoggedIn) {
      navigate('/login');
    } else {
      navigate(`/activities/${activityId}`);
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -16 }} transition={{ duration: 0.4, ease: "easeOut" }} className="flex flex-row min-h-screen bg-[#FAF9F6] text-gray-800 font-sans">

      {/* 좌측 메인 컨텐츠 */}
      <div className="w-3/4 flex flex-col px-4">

        {/* 호가 키워드 검색 방식 */}
        <div className="flex items-center w-full border border-gray-300 rounded-full px-4 py-2 shadow-sm mb-6 mt-20">
          <span className="text-gray-400 mr-2">🔍</span>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') setSearchKeyword(searchQuery); }}
            placeholder="내 주변에 어떤 활동이 있는지 찾아보세요"
            className="flex-1 outline-none text-sm bg-transparent"
          />
          <button onClick={() => setSearchKeyword(searchQuery)} className="ml-2 px-3 py-1 text-sm border rounded-full bg-white hover:bg-gray-100">검색</button>
        </div>

        {/* 배너 슬라이드 */}
        <div className="relative rounded-lg overflow-hidden shadow-md mb-8">
          <img
            src={images[currentImage]}
            alt="배너"
            className="w-full object-cover h-[153.6px] sm:h-[192px] md:h-[230.4px] lg:h-[276px] xl:h-[307.2px] transition-opacity duration-500 ease-in-out"
          />
        </div>

        {/* 관심사 카드 */}
        <section className="w-full grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 py-4">
          {["\uc804\uccb4", ...Array.from(interestMap.keys())].map((category, idx) => (
            <motion.div
              key={idx}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setSelectedCategory(category === selectedCategory ? null : (category === "\uc804\uccb4" ? null : category))}
              className={`cursor-pointer p-4 min-h-[100px] min-w-[96px] flex flex-col justify-center items-center rounded-xl border border-gray-300 shadow-sm text-center text-sm transition ${selectedCategory === category ? 'bg-blue-100 border-blue-400' : 'bg-white hover:bg-pink-50'}`}
            >
              <div className="text-2xl mb-2">{categoryToEmoji(category)}</div>
              <p className="font-medium text-xs leading-tight break-keep">{category}</p>
            </motion.div>
          ))}
        </section>

        {/* 활동 현재 상황 */}
        <section className="w-full py-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">{selectedCategory ? `선택한 관심사: ${selectedCategory}` : '진행 중인 활동'}</h2>
            <select value={itemsPerPage} onChange={(e) => { setItemsPerPage(Number(e.target.value)); setCurrentPage(1); }} className="ml-4 border rounded px-2 py-1 text-sm">
              <option value={10}>10개 보기</option>
              <option value={20}>20개 보기</option>
              <option value={50}>50개 보기</option>
            </select>
          </div>

          {error ? (
            <p className="text-red-500 text-sm text-center">❌ 활동 목록을 불러오는 중 오류가 발생했습니다: {error}</p>
          ) : currentActivities.length === 0 ? (
            <p className="text-sm text-center text-gray-400">표시할 활동이 없습니다.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {currentActivities.map((a) => (
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

          {/* 페이지네이션 */}
          <div className="flex justify-center items-center mt-6 gap-2">
            <button disabled={currentPage === 1} onClick={() => setCurrentPage((p) => Math.max(1, p - 1))} className="px-3 py-1 border rounded disabled:opacity-50">ㅇ전</button>
            <span className="text-sm">{currentPage} / {totalPages}</span>
            <button disabled={currentPage === totalPages} onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))} className="px-3 py-1 border rounded disabled:opacity-50">다음</button>
          </div>

        </section>

      </div>

      {/* 우측 날씨 백스 */}
      <div className="w-1/4 p-4 mt-24">
        <WeatherBox weatherData={weatherData} activities={activities} />
      </div>

    </motion.div>
  );
};

export default Home;
