import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { regionMap } from "../utils/regionMap";
import { interestMap } from "../utils/interestMap";

const steps = [
  "서비스 이용 동의", "이름 입력", "이메일 입력", "비밀번호 입력",
  "전화번호 입력", "관심사 선택", "가입 완료"
];

function Signup() {
  const [step, setStep] = useState(0);
  const [agreed, setAgreed] = useState(false);
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    phone: "",
    interests: []
  });
  const [birthYear, setBirthYear] = useState("");
  const [birthMonth, setBirthMonth] = useState("");

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    setStep((prev) => prev + 1);
  };

  const handlePrev = () => {
    setStep((prev) => prev - 1);
  };

  const handleSubmit = async () => {
    const requestData = {
      ...form,
      birth: `${birthYear}-${String(birthMonth).padStart(2, "0")}`,
      interests: form.interests.join(", "),
    };

    const res = await fetch("http://localhost:8000/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestData),
    });

    if (res.ok) {
      handleNext();
    } else {
      alert("회원가입 실패");
    }
  };

  const beige = "#EAD7C2";
  const beigeHover = "#d9c2a7";

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{ duration: 0.4 }}
      className="min-h-screen bg-[#FAF9F6] flex items-center justify-center"
    >
      <div className="w-full max-w-md bg-white border border-gray-200 rounded-lg p-8 text-center">
        {/* 상단 타이틀 */}
        <h2 className="text-xl font-semibold mb-6">{steps[step]}</h2>

        <AnimatePresence mode="wait">
          {step === 0 && (
            <motion.div
              key="step0"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -16 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col gap-4"
            >
              <p className="text-gray-600 mb-4">서비스 이용약관에 동의해주세요.</p>

              <div className="flex items-center justify-center gap-2">
                <input
                  type="checkbox"
                  id="agree"
                  checked={agreed}
                  onChange={(e) => setAgreed(e.target.checked)}
                />
                <label htmlFor="agree" className="text-sm text-gray-700">
                  전체 약관에 동의합니다.
                </label>
              </div>
            </motion.div>
          )}

          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -16 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col gap-4"
            >
              <input
                type="text"
                placeholder="이름을 입력하세요"
                value={form.name}
                onChange={(e) => handleChange("name", e.target.value)}
                className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
              />
            </motion.div>
          )}

          {step === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -16 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col gap-4"
            >
              <input
                type="email"
                placeholder="이메일을 입력하세요"
                value={form.email}
                onChange={(e) => handleChange("email", e.target.value)}
                className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
              />
            </motion.div>
          )}

          {step === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -16 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col gap-4"
            >
              <input
                type="password"
                placeholder="비밀번호를 입력하세요"
                value={form.password}
                onChange={(e) => handleChange("password", e.target.value)}
                className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
              />
            </motion.div>
          )}

          {step === 4 && (
            <motion.div
              key="step4"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -16 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col gap-4"
            >
              <input
                type="text"
                placeholder="전화번호 (000-0000-0000)"
                value={form.phone}
                onChange={(e) => handleChange("phone", e.target.value)}
                className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-gray-400"
              />
            </motion.div>
          )}

          {step === 5 && (
            <motion.div
              key="step5"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -16 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col gap-4"
            >
              <div className="text-sm mb-2 text-gray-600">관심사를 선택하세요 (최대 5개)</div>
              <div className="grid grid-cols-2 gap-3">
                {Array.from(interestMap.keys()).map((cat) => (
                  <button
                    key={cat}
                    onClick={() => {
                      if (!form.interests.includes(cat) && form.interests.length < 5) {
                        handleChange("interests", [...form.interests, cat]);
                      }
                    }}
                    className={`p-2 border rounded text-sm ${form.interests.includes(cat)
                        ? "bg-green-200 border-green-400"
                        : "bg-white hover:bg-gray-50"
                      }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </motion.div>
          )}

          {step === 6 && (
            <motion.div
              key="step6"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -16 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col gap-4 items-center justify-center"
            >
              <p className="text-green-600 text-lg font-semibold mb-4">
                🎉 가입이 완료되었습니다!
              </p>
              <p className="text-gray-600 text-sm">환영합니다. 이제 서비스를 시작할 수 있어요!</p>
              <button
                onClick={() => window.location.href = "/login"}
                className="mt-6 w-40 py-2 rounded bg-[#EAD7C2] hover:bg-[#d9c2a7] text-gray-800 font-semibold transition"
              >
                로그인하러 가기
              </button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* 하단 버튼 (이전/다음) */}
        <div className="flex justify-between mt-8">
          {step > 0 && step < 6 && (
            <button
              onClick={handlePrev}
              className="w-32 border border-gray-400 text-sm py-2 rounded hover:bg-gray-100 transition"
            >
              이전
            </button>
          )}
          <div className="flex-1" />
          {step < 5 && (
            <button
              onClick={handleNext}
              disabled={step === 0 && !agreed}
              style={{
                backgroundColor: agreed || step > 0 ? "#EAD7C2" : "#eee",
                color: "#555",
              }}
              className="w-32 text-sm py-2 rounded hover:bg-[#d9c2a7] transition"
            >
              다음
            </button>
          )}
          {step === 5 && (
            <button
              onClick={handleSubmit}
              className="w-32 text-sm py-2 rounded bg-[#EAD7C2] hover:bg-[#d9c2a7] transition"
            >
              회원가입 완료
            </button>
          )}
        </div>
      </div>
    </motion.div>
  );
}

export default Signup;

