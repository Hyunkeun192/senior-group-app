// src/App.jsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';

import Signup from './pages/Signup';
import Login from './pages/Login';
import Mypage from './pages/Mypage';
import Activities from './pages/Activities';
import Navbar from './components/Navbar';
import ActivityDetail from './pages/ActivityDetail';

import ProviderLogin from "./pages/ProviderLogin";
import ProviderSignup from "./pages/ProviderSignup";
import ProviderDashboard from "./pages/ProviderDashboard";
import ProviderCreateActivity from "./pages/ProviderCreateActivity";

import AdminLogin from "./pages/AdminLogin";
import AdminSignup from "./pages/AdminSignup";
import AdminDashboard from "./pages/AdminDashboard";
import PendingProviders from './pages/admin/PendingProviders';
import InterestMerge from './pages/admin/InterestMerge';
import UserManagement from "./pages/admin/UserManagement";
import ProviderManagement from "./pages/admin/ProviderManagement";

import RequireUser from './routes/RequireUser';
import RequireProvider from './routes/RequireProvider';
import RequireAdmin from './routes/RequireAdmin';

import Home from './pages/home';
import About from './pages/About';
import Notices from './pages/Notices';
import Entry from './pages/Entry';

function Layout() {
  const location = useLocation();

  return (
    <div>
      <Navbar /> {/* ✅ 항상 Navbar 표시 */}

      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          {/* ✅ 사용자 전용 */}
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/mypage" element={
            <RequireUser>
              <Mypage />
            </RequireUser>
          } />
          <Route path="/activities" element={
            <RequireUser>
              <Activities />
            </RequireUser>
          } />
          <Route path="/activities/:id" element={
            <RequireUser>
              <ActivityDetail />
            </RequireUser>
          } />

          {/* ✅ 업체 전용 */}
          <Route path="/provider-login" element={<ProviderLogin />} />
          <Route path="/provider-signup" element={<ProviderSignup />} />
          <Route path="/provider/dashboard" element={
            <RequireProvider>
              <ProviderDashboard />
            </RequireProvider>
          } />
          <Route path="/provider/create-activity" element={
            <RequireProvider>
              <ProviderCreateActivity />
            </RequireProvider>
          } />

          {/* ✅ 관리자 전용 */}
          <Route path="/admin-login" element={<AdminLogin />} />
          <Route path="/admin-signup" element={<AdminSignup />} />
          <Route path="/admin" element={
            <RequireAdmin>
              <AdminDashboard />
            </RequireAdmin>
          } />
          <Route path="/admin/pending-providers" element={
            <RequireAdmin>
              <PendingProviders />
            </RequireAdmin>
          } />
          <Route path="/admin/interests" element={
            <RequireAdmin>
              <InterestMerge />
            </RequireAdmin>
          } />
          <Route path="/admin/users" element={
            <RequireAdmin>
              <UserManagement />
            </RequireAdmin>
          } />
          <Route path="/admin/providers" element={
            <RequireAdmin>
              <ProviderManagement />
            </RequireAdmin>
          } />

          {/* ✅ 일반 공개 페이지 */}
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/notices" element={<Notices />} />
          <Route path="/entry" element={<Entry />} />
        </Routes>
      </AnimatePresence>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Layout />
    </Router>
  );
}

export default App;
