import { regionOptions } from './regions';

// Map 형태 변환
export const regionMap = new Map(
  regionOptions.map(item => [item.province, item.cities])
);

// Object 형태 변환 (선택)
export const regionObject = Object.fromEntries(
  regionOptions.map(item => [item.province, item.cities])
);
