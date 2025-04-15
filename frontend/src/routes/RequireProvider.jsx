// src/routes/RequireProvider.jsx
import { Navigate } from "react-router-dom";

const RequireProvider = ({ children }) => {
  const token = localStorage.getItem("access_token");
  const isAdmin = !!localStorage.getItem("admin_token");
  const provider = localStorage.getItem("provider");

  console.log("🔒 RequireProvider 실행됨");
  console.log("access_token:", token);
  console.log("admin_token:", isAdmin);
  console.log("provider:", provider);

  if (!token || isAdmin || !provider) {
    console.log("🚫 조건 불충족 → /provider-login 리디렉션");
    return <Navigate to="/provider-login" replace />;
  }

  console.log("✅ 접근 허용 (provider)");
  return children;
};

export default RequireProvider;
