import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { regions, interestOptions } from "../utils/constants";

const steps = ["기본 정보", "연락처 및 지역", "관심사"];

function Signup() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    phone: "",
    age: "",
    region: "",
    district: "",
    selectedCategories: [],
    selectedSubcategories: [],
    customInterest: "",
  });
  const [phoneValid, setPhoneValid] = useState(true);

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleCategorySelect = (category) => {
    if (!form.selectedCategories.includes(category) && form.selectedCategories.length < 5) {
      handleChange("selectedCategories", [...form.selectedCategories, category]);
    }
  };

  const handleSubcategorySelect = (subcategory) => {
    if (!form.selectedSubcategories.includes(subcategory) && form.selectedSubcategories.length < 5) {
      handleChange("selectedSubcategories", [...form.selectedSubcategories, subcategory]);
    }
  };

  const handleSubmit = async () => {
    const requestData = {
      name: form.name,
      email: form.email,
      password: form.password,
      phone: form.phone,
      age: parseInt(form.age),
      location: `${form.region} ${form.district}`,
      interests: form.selectedSubcategories.join(", "),
    };

    const res = await fetch("http://localhost:8000/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestData),
    });

    if (res.ok) {
      alert("회원가입 성공! 로그인 페이지로 이동합니다.");
      window.location.href = "/login";
    } else {
      alert("회원가입 실패");
    }
  };

  const isValidPhone = (value) => /^\d{3}-\d{4}-\d{4}$/.test(value);

  return (
    <div className="min-h-screen bg-[#FAF9F6] flex items-center justify-center">
      <div className="w-full max-w-2xl bg-white border rounded-lg p-6">
        {/* 단계 인디케이터 */}
        <div className="flex justify-center gap-4 mb-6">
          {steps.map((label, index) => (
            <div
              key={index}
              className={`text-sm font-medium px-3 py-1 rounded-full ${
                step === index ? "bg-green-600 text-white" : "bg-gray-200"
              }`}
            >
              {index + 1}. {label}
            </div>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {step === 0 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.3 }}
              className="flex flex-col gap-4"
            >
              <input placeholder="이름" className="p-2 border rounded" value={form.name} onChange={(e) => handleChange("name", e.target.value)} />
              <input placeholder="이메일" className="p-2 border rounded" value={form.email} onChange={(e) => handleChange("email", e.target.value)} />
              <input type="password" placeholder="비밀번호" className="p-2 border rounded" value={form.password} onChange={(e) => handleChange("password", e.target.value)} />
            </motion.div>
          )}

          {step === 1 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.3 }}
              className="flex flex-col gap-4"
            >
              <input
                placeholder="전화번호 (000-0000-0000)"
                className="p-2 border rounded"
                value={form.phone}
                onChange={(e) => {
                  handleChange("phone", e.target.value);
                  setPhoneValid(isValidPhone(e.target.value));
                }}
              />
              {!phoneValid && <p className="text-sm text-red-500">전화번호 형식이 올바르지 않습니다. 000-0000-0000 형식으로 입력해 주세요.</p>}
              <input placeholder="나이" className="p-2 border rounded" value={form.age} onChange={(e) => handleChange("age", e.target.value)} />
              <select className="p-2 border rounded" value={form.region} onChange={(e) => handleChange("region", e.target.value)}>
                <option value="">도/광역시 선택</option>
                {Object.keys(regions).map((r) => <option key={r}>{r}</option>)}
              </select>
              {form.region && (
                <select className="p-2 border rounded" value={form.district} onChange={(e) => handleChange("district", e.target.value)}>
                  <option value="">시/군/구 선택</option>
                  {regions[form.region].map((d) => <option key={d}>{d}</option>)}
                </select>
              )}
            </motion.div>
          )}

          {step === 2 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.3 }}
            >
              <div className="mb-4">
                <label className="block mb-1 font-medium">관심사 대분류 (최대 5개)</label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  {Object.keys(interestOptions).map((cat) => (
                    <button
                      key={cat}
                      onClick={() => handleCategorySelect(cat)}
                      className={`p-4 rounded-xl border text-center text-sm shadow-sm ${
                        form.selectedCategories.includes(cat) ? "bg-green-200 border-green-400" : "bg-white hover:bg-gray-50"
                      }`}
                    >
                      <div className="text-2xl mb-2">{categoryToEmoji(cat)}</div>
                      <div className="font-semibold">{cat}</div>
                    </button>
                  ))}
                </div>
              </div>

              {form.selectedCategories.length > 0 && (
                <div className="mb-4">
                  <label className="block mb-1 font-medium">관심사 소분류 (최대 5개)</label>
                  <div className="space-y-4">
                    {form.selectedCategories.map((cat) => (
                      <div key={cat}>
                        <div className="text-sm font-semibold text-gray-600 border-b pb-1 mb-2">{cat}</div>
                        <div className="flex flex-wrap gap-2">
                          {interestOptions[cat].map((sub) => (
                            <button
                              key={sub}
                              onClick={() => handleSubcategorySelect(sub)}
                              className={`px-3 py-1 text-sm rounded border ${
                                form.selectedSubcategories.includes(sub)
                                  ? "bg-green-200 border-green-400"
                                  : "bg-white hover:bg-gray-100"
                              }`}
                            >
                              {sub}
                            </button>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* 하단 버튼 */}
        <div className="mt-8 text-center">
          {step > 0 && (
            <button onClick={() => setStep(step - 1)} className="mr-2 px-4 py-2 border rounded">이전</button>
          )}
          {step < 2 ? (
            <button
              onClick={() => {
                if (step === 1 && !isValidPhone(form.phone)) {
                  alert("전화번호를 000-0000-0000 형식으로 입력해 주세요.");
                  return;
                }
                setStep(step + 1);
              }}
              className="px-4 py-2 border rounded bg-[#66bb6a] text-white"
            >
              다음
            </button>
          ) : (
            <button onClick={handleSubmit} className="px-4 py-2 border rounded bg-[#43a047] text-white">회원가입 완료</button>
          )}
        </div>
      </div>
    </div>
  );
}

function categoryToEmoji(category) {
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
  }
}

export default Signup;
