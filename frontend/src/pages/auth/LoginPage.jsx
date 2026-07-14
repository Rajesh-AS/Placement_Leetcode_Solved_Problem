import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { useGoogleLogin } from '@react-oauth/google';
import { api } from '@/services/api';
import { Building2, Sparkles, ShieldCheck } from 'lucide-react';

export function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const from = location.state?.from?.pathname || '/';

  const onSubmit = async (data) => {
    try {
      setIsLoading(true);
      setError('');
      const user = await login(data);
      
      // Redirect based on role if no specific return url
      if (from === '/') {
        if (user.role === 'admin') navigate('/admin/dashboard');
        else if (user.role === 'owner') navigate('/owner/dashboard');
        else navigate('/');
      } else {
        navigate(from, { replace: true });
      }
    } catch (err) {
      setError(err.response?.data?.non_field_errors?.[0] || err.response?.data?.error || 'Failed to login. Please check credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  const googleLogin = useGoogleLogin({
    onSuccess: async (codeResponse) => {
      try {
        setIsLoading(true);
        const res = await api.post('/auth/google/', { token: codeResponse.access_token });
        localStorage.setItem('access_token', res.data.tokens.access);
        localStorage.setItem('refresh_token', res.data.tokens.refresh);
        window.location.href = '/'; 
      } catch (err) {
        setError('Google login failed.');
        setIsLoading(false);
      }
    },
    onError: () => setError('Google login failed.')
  });

  return (
    <div className="min-h-[calc(100vh-4rem)] flex">
      {/* Left side - Image/Branding (hidden on mobile) */}
      <div className="hidden lg:flex w-1/2 bg-[var(--primary)] relative overflow-hidden flex-col justify-center px-12 text-white">
        <div className="absolute inset-0">
           <img 
             src="https://images.unsplash.com/photo-1541888081622-19e4fbbf77b2?q=80&w=1950&auto=format&fit=crop" 
             alt="Coimbatore architecture" 
             className="w-full h-full object-cover opacity-20 mix-blend-overlay"
           />
           <div className="hero-gradient absolute inset-0" />
        </div>
        
        <div className="relative z-10 max-w-lg">
          <Link to="/" className="flex items-center gap-2 mb-12">
            <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center backdrop-blur-sm border border-white/20">
              <Building2 className="h-6 w-6 text-[var(--gold)]" />
            </div>
            <div>
              <span className="font-extrabold text-2xl tracking-tight text-white">StayFinder</span>
              <span className="block text-[10px] font-bold text-[var(--gold)] tracking-widest mt-0.5">COIMBATORE</span>
            </div>
          </Link>

          <h1 className="text-4xl font-extrabold leading-tight mb-6">
            Find your perfect stay <br/>in <span className="text-[var(--gold)]">Coimbatore</span>
          </h1>
          <p className="text-white/80 text-lg mb-10 leading-relaxed">
            Join thousands of students and professionals who have found their ideal hostels and PGs through our verified platform.
          </p>

          <div className="space-y-4">
            <div className="flex items-center gap-3 text-white/90">
              <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center shrink-0">
                <ShieldCheck className="w-4 h-4 text-[var(--gold)]" />
              </div>
              <span>100% Verified properties & real owner contacts</span>
            </div>
            <div className="flex items-center gap-3 text-white/90">
              <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center shrink-0">
                <Sparkles className="w-4 h-4 text-[var(--gold)]" />
              </div>
              <span>Smart search tailored for Coimbatore colleges & areas</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12 bg-[var(--background)]">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="flex lg:hidden justify-center mb-8">
             <Link to="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-[var(--primary)] flex items-center justify-center">
                <Building2 className="h-6 w-6 text-white" />
              </div>
              <div>
                <span className="font-extrabold text-2xl tracking-tight text-[var(--foreground)]">StayFinder</span>
                <span className="block text-[10px] font-bold text-[var(--primary)] tracking-widest mt-0.5">COIMBATORE</span>
              </div>
            </Link>
          </div>

          <div className="text-center lg:text-left mb-8">
            <h2 className="text-2xl font-bold text-[var(--foreground)]">Welcome back</h2>
            <p className="text-[var(--muted-foreground)] mt-2 text-sm">Enter your credentials to access your account</p>
          </div>

          {error && (
            <div className="mb-6 rounded-lg bg-[var(--destructive)]/10 p-4 text-sm text-[var(--destructive)] border border-[var(--destructive)]/20 flex items-start gap-3">
              <div className="shrink-0 mt-0.5">⚠️</div>
              <p>{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <div>
              <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">Email or Username</label>
              <Input
                type="text"
                placeholder="name@example.com"
                {...register('email', { required: 'Email or username is required' })}
                error={errors.email?.message}
                className="h-11"
              />
            </div>
            
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-sm font-semibold text-[var(--foreground)]">Password</label>
                <Link to="/forgot-password" className="text-xs text-[var(--primary)] font-semibold hover:underline">
                  Forgot password?
                </Link>
              </div>
              <Input
                type="password"
                placeholder="••••••••"
                {...register('password', { required: 'Password is required' })}
                error={errors.password?.message}
                className="h-11"
              />
            </div>

            <Button type="submit" className="w-full h-11 text-base font-semibold shadow-md" disabled={isLoading}>
              {isLoading ? 'Signing in...' : 'Sign in'}
            </Button>
          </form>

          <div className="relative my-8">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t border-[var(--border)]" />
            </div>
            <div className="relative flex justify-center text-xs font-semibold uppercase tracking-wider">
              <span className="bg-[var(--background)] px-4 text-[var(--muted-foreground)]">Or continue with</span>
            </div>
          </div>

          <Button variant="outline" className="w-full h-11 font-medium bg-[var(--card)]" onClick={() => googleLogin()} disabled={isLoading}>
            <svg className="mr-3 h-5 w-5" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
            </svg>
            Sign in with Google
          </Button>

          <p className="text-center text-sm text-[var(--muted-foreground)] mt-8">
            Don't have an account?{' '}
            <Link to="/register" className="font-bold text-[var(--primary)] hover:underline">
              Sign up for free
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
