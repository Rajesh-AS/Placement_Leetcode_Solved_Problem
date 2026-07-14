import { Suspense, lazy } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';

// Lazy loaded pages
const HomePage = lazy(() => import('@/pages/home/HomePage').then(module => ({ default: module.HomePage })));
const SearchPage = lazy(() => import('@/pages/search/SearchPage').then(module => ({ default: module.SearchPage })));
const PropertyDetail = lazy(() => import('@/pages/property/PropertyDetail').then(module => ({ default: module.PropertyDetail })));
const LoginPage = lazy(() => import('@/pages/auth/LoginPage').then(module => ({ default: module.LoginPage })));
const RegisterPage = lazy(() => import('@/pages/auth/RegisterPage').then(module => ({ default: module.RegisterPage })));
const WishlistPage = lazy(() => import('@/pages/student/WishlistPage').then(module => ({ default: module.WishlistPage })));
const BookingsPage = lazy(() => import('@/pages/student/BookingsPage').then(module => ({ default: module.BookingsPage })));
const AdminDashboard = lazy(() => import('@/pages/admin/AdminDashboard').then(module => ({ default: module.AdminDashboard })));
const OwnerDashboard = lazy(() => import('@/pages/owner/OwnerDashboard').then(module => ({ default: module.OwnerDashboard })));
const ManageProperties = lazy(() => import('@/pages/owner/ManageProperties').then(module => ({ default: module.ManageProperties })));
const AddProperty = lazy(() => import('@/pages/owner/AddProperty').then(module => ({ default: module.AddProperty })));
const OwnerBookings = lazy(() => import('@/pages/owner/OwnerBookings').then(module => ({ default: module.OwnerBookings })));
const ChatPage = lazy(() => import('@/pages/chat/ChatPage').then(module => ({ default: module.ChatPage })));

function ProtectedRoute({ children, allowedRoles }) {
  const { user, loading } = useAuth();
  const location = useLocation();
  
  if (loading) return <div className="flex justify-center p-20"><div className="w-10 h-10 border-4 border-[var(--primary)] border-t-transparent rounded-full animate-spin"></div></div>;
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />;
  if (allowedRoles && !allowedRoles.includes(user.role)) return <Navigate to="/" replace />;
  
  return children;
}

export function AppRoutes() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--primary)]"></div></div>}>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/property/:id" element={<PropertyDetail />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Student Routes */}
        <Route path="/wishlists" element={<ProtectedRoute allowedRoles={['student']}><WishlistPage /></ProtectedRoute>} />
        <Route path="/bookings" element={<ProtectedRoute allowedRoles={['student']}><BookingsPage /></ProtectedRoute>} />
        
        {/* Owner Routes */}
        <Route path="/owner/dashboard" element={<ProtectedRoute allowedRoles={['owner']}><OwnerDashboard /></ProtectedRoute>} />
        <Route path="/owner/properties" element={<ProtectedRoute allowedRoles={['owner']}><ManageProperties /></ProtectedRoute>} />
        <Route path="/owner/properties/new" element={<ProtectedRoute allowedRoles={['owner']}><AddProperty /></ProtectedRoute>} />
        <Route path="/owner/bookings" element={<ProtectedRoute allowedRoles={['owner']}><OwnerBookings /></ProtectedRoute>} />
        
        {/* Admin Routes */}
        <Route path="/admin/dashboard" element={<ProtectedRoute allowedRoles={['admin']}><AdminDashboard /></ProtectedRoute>} />
        
        {/* Chat (Shared) */}
        <Route path="/chat" element={<ProtectedRoute allowedRoles={['student', 'owner']}><ChatPage /></ProtectedRoute>} />

        {/* 404 Route */}
        <Route path="*" element={
          <div className="p-8 text-center mt-20">
            <h1 className="text-4xl font-bold text-[var(--foreground)] mb-4">404 - Not Found</h1>
            <p className="text-[var(--muted-foreground)]">The page you are looking for does not exist.</p>
          </div>
        } />
      </Routes>
    </Suspense>
  );
}
