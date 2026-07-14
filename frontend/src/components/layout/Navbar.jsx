import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { useTheme } from '@/contexts/ThemeContext';
import { Button } from '@/components/common/Button';
import {
  LogOut, User as UserIcon, Heart, MessageSquare, Menu, X,
  Sun, Moon, Home, Search, LayoutDashboard, Shield, Building2
} from 'lucide-react';
import { useState } from 'react';
import { NotificationDropdown } from '@/components/notifications/NotificationDropdown';

export function Navbar() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    setMobileMenuOpen(false);
    navigate('/');
  };

  return (
    <nav className="glass border-b border-[var(--border)] sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center gap-2 group">
              <div className="w-9 h-9 rounded-xl bg-[var(--primary)] flex items-center justify-center group-hover:scale-105 transition-transform">
                <Building2 className="h-5 w-5 text-white" />
              </div>
              <div className="hidden sm:flex flex-col">
                <span className="font-extrabold text-lg leading-none text-[var(--primary)]">
                  StayFinder
                </span>
                <span className="text-[10px] font-medium text-[var(--gold)] leading-none tracking-wider">
                  COIMBATORE
                </span>
              </div>
            </Link>
          </div>

          {/* Desktop Search */}
          <div className="hidden md:flex items-center flex-1 max-w-md mx-8">
            <button
              onClick={() => navigate('/search')}
              className="w-full flex items-center gap-2 px-4 py-2 rounded-full border border-[var(--border)] bg-[var(--card)] text-sm text-[var(--muted-foreground)] hover:border-[var(--primary)] hover:shadow-md transition-all cursor-pointer"
            >
              <Search className="w-4 h-4" />
              <span>Search hostels, PGs, areas...</span>
            </button>
          </div>

          {/* Desktop Menu */}
          <div className="hidden sm:flex sm:items-center sm:gap-1">
            {/* Theme Toggle */}
            <Button variant="ghost" size="icon" onClick={toggleTheme} title="Toggle theme">
              {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </Button>

            {!user ? (
              <>
                <Link to="/login">
                  <Button variant="ghost">Log in</Button>
                </Link>
                <Link to="/register">
                  <Button>Sign up</Button>
                </Link>
              </>
            ) : (
              <>
                <NotificationDropdown />
                
                {user.role === 'student' && (
                  <>
                    <Link to="/wishlists">
                      <Button variant="ghost" size="icon" title="Wishlists">
                        <Heart className="h-5 w-5" />
                      </Button>
                    </Link>
                    <Link to="/chat">
                      <Button variant="ghost" size="icon" title="Messages">
                        <MessageSquare className="h-5 w-5" />
                      </Button>
                    </Link>
                    <Link to="/bookings">
                      <Button variant="ghost" size="sm">My Visits</Button>
                    </Link>
                  </>
                )}
                {user.role === 'owner' && (
                  <Link to="/owner/dashboard">
                    <Button variant="ghost" size="sm">
                      <LayoutDashboard className="h-4 w-4 mr-1.5" />Dashboard
                    </Button>
                  </Link>
                )}
                {user.role === 'admin' && (
                  <Link to="/admin/dashboard">
                    <Button variant="ghost" size="sm">
                      <Shield className="h-4 w-4 mr-1.5" />Admin
                    </Button>
                  </Link>
                )}

                {/* User menu */}
                <div className="relative ml-2 flex items-center gap-2 border-l border-[var(--border)] pl-3">
                  <div className="w-8 h-8 rounded-full bg-[var(--primary)]/10 border-2 border-[var(--primary)]/30 flex items-center justify-center overflow-hidden">
                    {user.profile_picture ? (
                      <img src={user.profile_picture} alt="Avatar" className="w-full h-full object-cover" />
                    ) : (
                      <UserIcon className="h-4 w-4 text-[var(--primary)]" />
                    )}
                  </div>
                  <span className="text-sm font-medium text-[var(--foreground)]">
                    {user.first_name}
                  </span>
                  <Button variant="ghost" size="icon" onClick={handleLogout} title="Logout">
                    <LogOut className="h-4 w-4" />
                  </Button>
                </div>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center gap-1 sm:hidden">
            <Button variant="ghost" size="icon" onClick={toggleTheme}>
              {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </Button>
            <Button variant="ghost" size="icon" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="sm:hidden border-t border-[var(--border)] animate-slide-down">
          <div className="p-4 space-y-2 bg-[var(--card)]">
            {/* Mobile Search */}
            <button
              onClick={() => { navigate('/search'); setMobileMenuOpen(false); }}
              className="w-full flex items-center gap-2 px-4 py-3 rounded-xl border border-[var(--border)] text-sm text-[var(--muted-foreground)] mb-3"
            >
              <Search className="w-4 h-4" />
              Search hostels, PGs...
            </button>

            {!user ? (
              <>
                <Link to="/login" className="block" onClick={() => setMobileMenuOpen(false)}>
                  <Button variant="outline" className="w-full justify-start">Log in</Button>
                </Link>
                <Link to="/register" className="block" onClick={() => setMobileMenuOpen(false)}>
                  <Button className="w-full justify-start">Sign up</Button>
                </Link>
              </>
            ) : (
              <>
                <div className="flex items-center gap-3 px-4 py-3 bg-[var(--secondary)] rounded-xl mb-2">
                  <div className="w-10 h-10 rounded-full bg-[var(--primary)]/10 flex items-center justify-center">
                    {user.profile_picture ? (
                      <img src={user.profile_picture} alt="" className="w-full h-full rounded-full object-cover" />
                    ) : (
                      <UserIcon className="h-5 w-5 text-[var(--primary)]" />
                    )}
                  </div>
                  <div>
                    <p className="font-semibold text-sm">{user.first_name} {user.last_name}</p>
                    <p className="text-xs text-[var(--muted-foreground)] capitalize">{user.role}</p>
                  </div>
                </div>

                <Link to="/" className="block" onClick={() => setMobileMenuOpen(false)}>
                  <Button variant="ghost" className="w-full justify-start"><Home className="w-4 h-4 mr-2" />Home</Button>
                </Link>

                {user.role === 'student' && (
                  <>
                    <Link to="/wishlists" className="block" onClick={() => setMobileMenuOpen(false)}>
                      <Button variant="ghost" className="w-full justify-start"><Heart className="w-4 h-4 mr-2" />Wishlists</Button>
                    </Link>
                    <Link to="/bookings" className="block" onClick={() => setMobileMenuOpen(false)}>
                      <Button variant="ghost" className="w-full justify-start">My Visits</Button>
                    </Link>
                    <Link to="/chat" className="block" onClick={() => setMobileMenuOpen(false)}>
                      <Button variant="ghost" className="w-full justify-start"><MessageSquare className="w-4 h-4 mr-2" />Messages</Button>
                    </Link>
                  </>
                )}
                {user.role === 'owner' && (
                  <Link to="/owner/dashboard" className="block" onClick={() => setMobileMenuOpen(false)}>
                    <Button variant="ghost" className="w-full justify-start"><LayoutDashboard className="w-4 h-4 mr-2" />Dashboard</Button>
                  </Link>
                )}
                {user.role === 'admin' && (
                  <Link to="/admin/dashboard" className="block" onClick={() => setMobileMenuOpen(false)}>
                    <Button variant="ghost" className="w-full justify-start"><Shield className="w-4 h-4 mr-2" />Admin Panel</Button>
                  </Link>
                )}

                <hr className="border-[var(--border)]" />
                <Button
                  variant="ghost"
                  className="w-full justify-start text-[var(--destructive)] hover:bg-[var(--destructive)]/10"
                  onClick={handleLogout}
                >
                  <LogOut className="w-4 h-4 mr-2" />Log out
                </Button>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
