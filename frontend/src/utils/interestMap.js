// src/utils/interestMap.js
import { interestOptions } from './interestOptions';

// interestOptions를 Map 형태로 변환
export const interestMap = new Map(
  interestOptions.map(item => [item.category, item.subcategories])
);

// 선택사항: Object 형태로 변환 (필요 시)
export const interestObject = Object.fromEntries(
  interestOptions.map(item => [item.category, item.subcategories])
);
