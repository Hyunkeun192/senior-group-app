// src/utils/recommendUtils.js

import { interestOptions } from './interestOptions';

// 날씨 및 미세먼지 기반 추천 알고리즘
export function recommendActivitiesBasedOnWeather(weatherData) {
    const { current, air, daily } = weatherData;
    const weather = current.weather.toLowerCase();
    const pm10 = air.pm10;

    let recommendations = [];

    // 🛑 Step 1: 미세먼지가 매우 나쁨일 경우 (무조건 실내 활동 추천)
    if (pm10 > 150) {
        recommendations = [
            "실내 요가 클래스", "독서 모임", "온라인 강의",
            "플라워 클래스", "공예 소품 만들기", "도예 체험"
        ];
        return enrichRecommendations(recommendations);
    }

    // 🛑 Step 2: 날씨 상태별 추천
    if (weather.includes("rain") || weather.includes("drizzle")) {
        // 비 오는 경우
        recommendations = [
            "플라워 클래스", "요리 체험", "도예 체험",
            "실내 요가", "공방 체험", "책 출판하기"
        ];
    } else if (weather.includes("snow")) {
        // 눈 오는 경우
        recommendations = [
            "홈트레이닝", "디지털 사진 편집", "영상 편집 배우기",
            "독서 모임", "자서전 쓰기"
        ];
    } else if (weather.includes("clouds")) {
        if (pm10 > 80) {
            // 흐리고 미세먼지도 나쁘면
            recommendations = [
                "공예 소품 만들기", "도서관 북토크", "플라워 클래스"
            ];
        } else {
            // 흐리지만 미세먼지는 괜찮으면
            recommendations = [
                "걷기 모임", "사진 촬영", "카페 투어"
            ];
        }
    } else if (weather.includes("clear")) {
        if (pm10 > 80) {
            // 맑지만 미세먼지가 나쁨
            recommendations = [
                "실내 요가", "플로리스트 클래스", "DIY 공예"
            ];
        } else {
            // 맑고 공기 좋으면
            recommendations = [
                "동네 걷기 모임", "야외 자전거 타기", "등산 모임",
                "야외 사진 촬영회", "텃밭 가꾸기", "반려견 산책 모임"
            ];
        }
    } else {
        // 그 외 날씨
        recommendations = [
            "카페 독서", "공방 체험", "실내 수공예"
        ];
    }

    // 🛑 Step 3: 주간 예보에 비 소식이 있으면 추가 안내
    const rainComing = daily.some(d => d.weather.toLowerCase().includes("rain"));
    if (rainComing) {
        recommendations.push("※ 이번 주 비 소식 있음, 실내 활동 추천");
    }

    return enrichRecommendations(recommendations);
}

// 카테고리와 서브카테고리 맵핑해서 반환
function enrichRecommendations(recommendations) {
    const enriched = [];

    for (const rec of recommendations) {
        let found = false;
        for (const option of interestOptions) {
            if (option.subcategories.some(sub => rec.includes(sub) || rec.includes(sub.replace(/\s/g, '')))) {
                enriched.push({
                    title: rec,
                    category: option.category
                });
                found = true;
                break;
            }
        }
        if (!found) {
            enriched.push({ title: rec, category: "기타" });
        }
    }

    return enriched;
}
