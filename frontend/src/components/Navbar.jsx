import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const [isAdmin, setIsAdmin] = useState(false);
  const [isProvider, setIsProvider] = useState(false);
  const [isUser, setIsUser] = useState(false);

  useEffect(() => {
    const accessToken = localStorage.getItem("access_token");
    const adminToken = localStorage.getItem("admin_token");
    const providerInfo = localStorage.getItem("provider");

    setIsAdmin(!!adminToken);
    setIsProvider(!!accessToken && !adminToken && !!providerInfo);
    setIsUser(!!accessToken && !adminToken && !providerInfo);
  }, [location.key]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("provider");
    setIsProvider(false);
    setIsUser(false);
    alert("로그아웃 되었습니다.");
    navigate("/");
  };

  const handleAdminLogout = () => {
    localStorage.removeItem("admin_token");
    setIsAdmin(false);
    alert("관리자 로그아웃 되었습니다.");
    navigate("/admin-login");
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-200 px-6 py-2 shadow-sm">
      <div className="flex justify-center items-center gap-8">
        {isAdmin ? (
          <>
            <NavItem to="/admin" icon="📊" label="대시보드" />
            <NavItem to="/admin/pending-providers" icon="✅" label="업체 승인" />
            <NavItem to="/admin/users" icon="👤" label="사용자" />
            <NavItem to="/admin/providers" icon="🏢" label="업체" />
            <LogoutButton onClick={handleAdminLogout} />
          </>
        ) : isProvider ? (
          <>
            <NavItem to="/provider/dashboard" icon="📂" label="내 활동" />
            <NavItem to="/provider/create-activity" icon="➕" label="활동 등록" />
            <NavItem to="/provider/notifications" icon="🔔" label="알림" />
            <LogoutButton onClick={handleLogout} />
          </>
        ) : isUser ? (
          <>
            <NavItem to="/" icon="🏠" label="홈" />
            <NavItem to="/mypage" icon="📂" label="나의 활동" />
            <LogoutButton onClick={handleLogout} />
          </>
        ) : (
          <>
            <NavItem to="/" icon="🏠" label="홈" />
            <NavItem to="/login" icon="📂" label="나의 활동" />
            <NavItem to="/login" icon="🔑" label="로그인" />
          </>
        )}
      </div>
    </nav>
  );
}

function NavItem({ to, icon, label }) {
  return (
    <button
      onClick={() => window.location.href = to}
      className="flex flex-col items-center text-sm text-gray-700 hover:text-blue-500"
    >
      <span className="text-base">{icon}</span>
      <span className="text-xs mt-1">{label}</span>
    </button>
  );
}

function LogoutButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="flex flex-col items-center text-sm text-gray-700 hover:text-blue-500"
    >
      <span className="text-base">🚪</span>
      <span className="text-xs mt-1">로그아웃</span>
    </button>
  );
}

export default Navbar;
