import { useState, useEffect } from 'react';
import { bookingService } from '@/services/bookingService';
import { Button } from '@/components/common/Button';
import { Calendar, MapPin, Clock, ArrowLeft, CheckCircle2, XCircle, Clock4, CreditCard } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import { PaymentCheckoutModal } from '@/components/payment/PaymentCheckoutModal';

export function BookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [payingBooking, setPayingBooking] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const res = await bookingService.getMyBookings();
      setBookings(res.results || res || []);
    } catch (err) {
      console.error('Failed to fetch bookings', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentSuccess = () => {
    setPayingBooking(null);
    fetchBookings(); // Refresh bookings to update any status
  };

  const getStatusBadge = (status) => {
    switch(status.toLowerCase()) {
      case 'approved':
      case 'completed':
        return <span className="flex items-center gap-1 bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-semibold"><CheckCircle2 className="w-3 h-3" /> {status.charAt(0).toUpperCase() + status.slice(1)}</span>;
      case 'rejected':
      case 'cancelled':
        return <span className="flex items-center gap-1 bg-red-100 text-red-700 px-3 py-1 rounded-full text-xs font-semibold"><XCircle className="w-3 h-3" /> {status.charAt(0).toUpperCase() + status.slice(1)}</span>;
      case 'rescheduled':
        return <span className="flex items-center gap-1 bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-semibold"><Clock4 className="w-3 h-3" /> Rescheduled</span>;
      default:
        return <span className="flex items-center gap-1 bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-xs font-semibold"><Clock4 className="w-3 h-3" /> Pending</span>;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] mb-6 cursor-pointer transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back
      </button>

      <div className="flex items-center gap-3 mb-8">
        <div className="w-12 h-12 rounded-xl bg-[var(--primary)]/10 flex items-center justify-center">
          <Calendar className="w-6 h-6 text-[var(--primary)]" />
        </div>
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-[var(--foreground)]">My Scheduled Visits</h1>
          <p className="text-sm text-[var(--muted-foreground)] mt-1">
            {loading ? 'Loading...' : `You have ${bookings.length} scheduled visits`}
          </p>
        </div>
      </div>

      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map(i => <div key={i} className="shimmer h-32 rounded-2xl w-full max-w-3xl" />)}
        </div>
      ) : bookings.length === 0 ? (
        <div className="text-center py-24 rounded-2xl border border-[var(--border)] bg-[var(--card)] mt-8 max-w-3xl">
          <div className="w-16 h-16 rounded-full bg-[var(--secondary)] flex items-center justify-center mx-auto mb-4">
            <Calendar className="w-8 h-8 text-[var(--muted-foreground)]" />
          </div>
          <h3 className="text-xl font-semibold text-[var(--foreground)] mb-2">No visits scheduled</h3>
          <p className="text-[var(--muted-foreground)] mb-6 max-w-sm mx-auto">
            You haven't scheduled any property visits yet. Find a property you like and book a visit!
          </p>
          <Button onClick={() => navigate('/search')}>Explore Properties</Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {bookings.map(booking => (
            <div key={booking.id} className="bg-[var(--card)] border border-[var(--border)] rounded-2xl overflow-hidden hover:shadow-md transition-shadow flex flex-col">
              <div className="p-5 border-b border-[var(--border)]">
                <div className="flex justify-between items-start mb-3">
                  {getStatusBadge(booking.status || 'pending')}
                  <span className="text-xs text-[var(--muted-foreground)]">ID: #{booking.id}</span>
                </div>
                <Link to={`/property/${booking.property.id || booking.property}`} className="font-bold text-lg text-[var(--foreground)] hover:text-[var(--primary)] line-clamp-1 mb-1">
                  {booking.property.name || booking.property_name}
                </Link>
                <div className="flex items-center text-sm text-[var(--muted-foreground)]">
                  <MapPin className="w-4 h-4 mr-1 shrink-0" />
                  <span className="truncate">{booking.property.area || booking.property_city}, Coimbatore</span>
                </div>
              </div>
              
              <div className="p-5 bg-[var(--secondary)] flex-grow space-y-3">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-[var(--muted-foreground)] flex items-center gap-2"><Calendar className="w-4 h-4" /> Date</span>
                  <span className="font-medium text-[var(--foreground)]">
                    {new Date(booking.visit_date || booking.start_date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-[var(--muted-foreground)] flex items-center gap-2"><Clock className="w-4 h-4" /> Time</span>
                  <span className="font-medium text-[var(--foreground)]">{booking.visit_time || '10:00 AM - 12:00 PM'}</span>
                </div>
              </div>

              <div className="p-4 flex gap-2 border-t border-border mt-auto">
                <Button variant="outline" className="flex-1" onClick={() => navigate('/chat')}>Message</Button>
                
                {booking.status === 'approved' && (
                  <Button className="flex-1 bg-green-600 hover:bg-green-700 flex items-center gap-1" onClick={() => setPayingBooking(booking)}>
                    <CreditCard className="w-4 h-4" /> Pay Advance
                  </Button>
                )}

                {(!booking.status || booking.status === 'pending') && (
                  <Button variant="destructive" className="flex-1">Cancel</Button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {payingBooking && (
        <PaymentCheckoutModal 
          booking={payingBooking} 
          onClose={() => setPayingBooking(null)} 
          onSuccess={handlePaymentSuccess} 
        />
      )}
    </div>
  );
}
