import React from 'react';

function ActivityPopupModal({ activityName, activities, onClose }) {
    // ✅ 안전한 필터링
    const filteredActivities = (activities || []).filter(a =>
        a.title.replace(/\s/g, '').toLowerCase().includes(activityName.replace(/\s/g, '').toLowerCase())
    );

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
            <div className="bg-white p-6 rounded-2xl shadow-lg w-80 max-h-[90vh] overflow-y-auto space-y-4">

                {/* 헤더 */}
                <div className="flex justify-between items-center mb-2">
                    <h2 className="text-lg font-bold">{activityName}</h2>
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-800">✖️</button>
                </div>

                {/* 활동 리스트 */}
                {filteredActivities.length > 0 ? (
                    filteredActivities.map((activity) => (
                        <div key={activity.id} className="p-3 border rounded-lg space-y-1">
                            <div className="text-sm font-semibold">{activity.title}</div>
                            <div className="text-xs text-gray-500">{activity.region} · {activity.deadline.split('T')[0]}</div>
                            <button className="mt-2 w-full bg-blue-500 hover:bg-blue-600 text-white py-1 rounded text-xs">
                                신청하기
                            </button>
                        </div>
                    ))
                ) : (
                    <div className="text-sm text-gray-500 text-center py-6">
                        모집 중인 활동이 없습니다.
                    </div>
                )}

                {/* 닫기 버튼 */}
                <button onClick={onClose} className="w-full mt-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-xs font-medium">
                    닫기
                </button>

            </div>
        </div>
    );
}

export default ActivityPopupModal;
