// src/routes/RequireUser.jsx
import { Navigate } from "react-router-dom";

const RequireUser = ({ children }) => {
  const token = localStorage.getItem("access_token");
  const isAdmin = !!localStorage.getItem("admin_token");
  const provider = localStorage.getItem("provider");

  console.log("🔒 RequireUser 실행됨");
  console.log("access_token:", token);
  console.log("admin_token:", isAdmin);
  console.log("provider:", provider);

  if (!token || isAdmin || provider) {
    console.log("🚫 조건 불충족 → /login 리디렉션");
    return <Navigate to="/login" replace />;
  }

  console.log("✅ 접근 허용 (user)");
  return children;
};

export default RequireUser;
