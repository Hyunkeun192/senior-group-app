import React, { useState, useEffect } from 'react';
import ActivityPopupModal from './ActivityPopupModal'; // ✅ 모달 컴포넌트
import { recommendActivitiesBasedOnWeather } from '../utils/recommendUtils'; // ✅ 추천 로직 import

function WeatherBox({ weatherData, activities }) {
    const [selectedActivity, setSelectedActivity] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [recommendations, setRecommendations] = useState([]);

    useEffect(() => {
        if (weatherData) {
            const recs = recommendActivitiesBasedOnWeather(weatherData);
            setRecommendations(recs);
        }
    }, [weatherData]);

    if (!weatherData) return null;

    const { city, current, hourly, air } = weatherData;

    const openModal = (activityName) => {
        setSelectedActivity(activityName);
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedActivity(null);
    };

    const getActivityCount = (activityName) => {
        return activities?.filter(a =>
            a.title.replace(/\s/g, '').toLowerCase().includes(activityName.replace(/\s/g, '').toLowerCase())
        ).length || 0;
    };

    const getDustLevel = (value) => {
        if (value <= 30) return { emoji: "😊", level: "좋음" };
        if (value <= 80) return { emoji: "🙂", level: "보통" };
        if (value <= 150) return { emoji: "😷", level: "나쁨" };
        return { emoji: "🥵", level: "매우 나쁨" };
    };

    const pm10Info = getDustLevel(air.pm10);

    return (
        <div className="bg-gradient-to-b from-blue-50 to-white p-4 rounded-2xl shadow-md text-gray-700 text-xs space-y-4 w-full">

            {/* 현재 날씨 */}
            <div className="text-center space-y-1">
                <h3 className="text-sm font-bold">📍 {city}</h3>
                <p className="text-lg font-semibold">{current.temperature.toFixed(1)}℃, {current.weather}</p>
            </div>

            {/* 간단한 시간별 예보 */}
            <div className="flex justify-around text-center">
                {hourly.slice(0, 2).map((h, idx) => (
                    <div key={idx} className="flex flex-col items-center space-y-1">
                        <p className="text-xs">{h.time}</p>
                        <div className="text-lg">
                            {h.weather.includes('구름') ? '☁️' : h.weather.includes('비') ? '🌧️' : '☀️'}
                        </div>
                        <p className="text-xs">{h.temp}℃</p>
                    </div>
                ))}
            </div>

            {/* 미세먼지 */}
            <div className="flex items-center justify-center space-x-2">
                <span className="text-base">{pm10Info.emoji}</span>
                <span>미세먼지 ({pm10Info.level})</span>
            </div>

            {/* 추천 활동 */}
            <div className="space-y-2">
                <h4 className="font-semibold text-xs">🔥 추천 활동</h4>
                <div className="grid grid-cols-1 gap-2">
                    {recommendations.map((r, idx) => {
                        const count = getActivityCount(r.title);
                        return (
                            <button
                                key={idx}
                                onClick={() => openModal(r.title)}
                                className="relative bg-white p-2 rounded-xl shadow-sm text-center text-xs font-medium hover:bg-pink-50 transition"
                            >
                                {r.title}
                                {/* 모집 수 뱃지 */}
                                <span className={`absolute top-1 right-2 text-white text-[10px] px-2 py-0.5 rounded-full ${count > 0 ? 'bg-blue-500' : 'bg-gray-300'}`}>
                                    {count}
                                </span>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* 모달 */}
            {isModalOpen && (
                <ActivityPopupModal
                    activityName={selectedActivity}
                    activities={activities}
                    onClose={closeModal}
                />
            )}
        </div>
    );
}

export default WeatherBox;
