import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { api } from '@/services/api';
import { Building2, ArrowLeft } from 'lucide-react';

const COLLEGES = [
  'PSG Tech', 'PSG College', 'Kumaraguru College', 'Karunya University',
  'Rathinam College', 'Sri Krishna College', 'SNS College', 'NGP College',
  'Hindusthan College', 'CIT', 'Government Arts College', 'Amrita University',
];

export function RegisterPage() {
  const { register, handleSubmit, watch, formState: { errors } } = useForm();
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [step, setStep] = useState(1);
  const selectedRole = watch('role', 'student');

  const onSubmit = async (data) => {
    if (data.password !== data.password_confirm) {
      setError('Passwords do not match');
      return;
    }

    try {
      setIsLoading(true);
      setError('');
      // Always set city to Coimbatore for our scoped app
      data.city = 'Coimbatore';
      
      await api.post('/auth/register/', data);
      navigate('/login', { state: { message: 'Registration successful! Please login.' } });
    } catch (err) {
      const errData = err.response?.data;
      let errMsg = 'Failed to register. Please try again.';
      if (errData) {
        if (typeof errData === 'string') {
          errMsg = errData;
        } else if (errData.email) {
          errMsg = errData.email[0];
        } else if (errData.username) {
          errMsg = errData.username[0];
        } else if (errData.password) {
          errMsg = errData.password[0];
        } else if (errData.password_confirm) {
          errMsg = errData.password_confirm[0];
        } else if (errData.phone) {
          errMsg = errData.phone[0];
        } else if (errData.non_field_errors) {
          errMsg = errData.non_field_errors[0];
        } else {
           const firstKey = Object.keys(errData)[0];
           if (firstKey && Array.isArray(errData[firstKey])) {
             errMsg = errData[firstKey][0];
           }
        }
      }
      setError(errMsg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center p-4 bg-[var(--background)]">
      <div className="w-full max-w-xl bg-[var(--card)] rounded-2xl border border-[var(--border)] shadow-xl overflow-hidden">
        
        {/* Header */}
        <div className="bg-[var(--secondary)] p-6 md:p-8 text-center border-b border-[var(--border)] relative">
           <Link to="/" className="absolute left-6 top-8 text-[var(--muted-foreground)] hover:text-[var(--foreground)]">
              <ArrowLeft className="w-5 h-5" />
           </Link>
           <div className="w-12 h-12 rounded-xl bg-[var(--primary)] flex items-center justify-center mx-auto mb-4 shadow-sm">
             <Building2 className="h-7 w-7 text-white" />
           </div>
           <h2 className="text-2xl font-bold text-[var(--foreground)]">Create your account</h2>
           <p className="text-[var(--muted-foreground)] mt-2 text-sm">Join StayFinder Coimbatore today</p>
        </div>

        {/* Form Container */}
        <div className="p-6 md:p-8">
          {error && (
            <div className="mb-6 rounded-lg bg-[var(--destructive)]/10 p-4 text-sm text-[var(--destructive)] border border-[var(--destructive)]/20 flex items-start gap-3">
              <div className="shrink-0 mt-0.5">⚠️</div>
              <p>{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)}>
            {/* Step 1: Role & Basic Info */}
            {step === 1 && (
              <div className="space-y-5 animate-fade-in">
                <div>
                  <label className="text-sm font-semibold text-[var(--foreground)] mb-3 block">I am a...</label>
                  <div className="grid grid-cols-2 gap-4">
                    <label className={`
                      flex flex-col items-center justify-center p-4 rounded-xl border-2 cursor-pointer transition-all
                      ${selectedRole === 'student' ? 'border-[var(--primary)] bg-[var(--primary)]/5' : 'border-[var(--border)] hover:border-[var(--primary)]/50'}
                    `}>
                      <input type="radio" value="student" {...register('role')} className="sr-only" defaultChecked />
                      <span className="text-2xl mb-2">🎓</span>
                      <span className="font-semibold text-sm">Student / User</span>
                    </label>
                    <label className={`
                      flex flex-col items-center justify-center p-4 rounded-xl border-2 cursor-pointer transition-all
                      ${selectedRole === 'owner' ? 'border-[var(--primary)] bg-[var(--primary)]/5' : 'border-[var(--border)] hover:border-[var(--primary)]/50'}
                    `}>
                      <input type="radio" value="owner" {...register('role')} className="sr-only" />
                      <span className="text-2xl mb-2">🏠</span>
                      <span className="font-semibold text-sm">Property Owner</span>
                    </label>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 pt-2">
                  <div>
                    <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">First Name</label>
                    <Input {...register('first_name', { required: 'Required' })} error={errors.first_name?.message} />
                  </div>
                  <div>
                    <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">Last Name</label>
                    <Input {...register('last_name', { required: 'Required' })} error={errors.last_name?.message} />
                  </div>
                </div>

                <div>
                  <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">Email</label>
                  <Input type="email" {...register('email', { required: 'Required' })} error={errors.email?.message} />
                </div>
                
                <Button type="button" className="w-full h-11 text-base mt-2" onClick={async () => {
                   // Basic validation before next step
                   if (watch('first_name') && watch('last_name') && watch('email')) setStep(2);
                   else setError("Please fill all fields to continue.");
                }}>
                  Continue to next step
                </Button>
              </div>
            )}

            {/* Step 2: Details & Security */}
            {step === 2 && (
              <div className="space-y-5 animate-fade-in">
                <div>
                  <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">Username</label>
                  <Input {...register('username', { required: 'Required', minLength: { value: 3, message: 'Min 3 chars' } })} error={errors.username?.message} />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">Phone Number</label>
                    <Input type="tel" {...register('phone', { required: 'Required' })} error={errors.phone?.message} />
                  </div>
                  <div>
                    <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">Gender</label>
                    <select 
                      {...register('gender')} 
                      className="w-full h-10 rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)] outline-none focus:ring-2 focus:ring-[var(--primary)]/30 focus:border-[var(--primary)]"
                    >
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>

                {selectedRole === 'student' && (
                  <div>
                    <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">College (in Coimbatore)</label>
                    <select 
                      {...register('college')} 
                      className="w-full h-10 rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)] outline-none focus:ring-2 focus:ring-[var(--primary)]/30 focus:border-[var(--primary)]"
                    >
                      <option value="">I am working / Not in college</option>
                      {COLLEGES.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4 pt-2">
                  <div>
                    <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">Password</label>
                    <Input type="password" {...register('password', { required: 'Required', minLength: { value: 8, message: 'Min 8 chars' } })} error={errors.password?.message} />
                  </div>
                  <div>
                    <label className="text-sm font-semibold text-[var(--foreground)] mb-1.5 block">Confirm Password</label>
                    <Input type="password" {...register('password_confirm', { required: 'Required' })} error={errors.password_confirm?.message} />
                  </div>
                </div>

                <div className="flex gap-3 pt-4">
                  <Button type="button" variant="outline" className="w-1/3 h-11" onClick={() => { setStep(1); setError(''); }}>
                    Back
                  </Button>
                  <Button type="submit" className="w-2/3 h-11" disabled={isLoading}>
                    {isLoading ? 'Creating account...' : 'Create Account'}
                  </Button>
                </div>
              </div>
            )}
          </form>

          <p className="text-center text-sm text-[var(--muted-foreground)] mt-8">
            Already have an account?{' '}
            <Link to="/login" className="font-bold text-[var(--primary)] hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
