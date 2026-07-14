import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { Button } from '@/components/common/Button';
import { Calendar, MapPin, CheckCircle2, XCircle, Clock4, User } from 'lucide-react';
import { Link } from 'react-router-dom';

export function OwnerBookings() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const res = await api.get('/bookings/owner/');
      setBookings(res.data.results || res.data || []);
    } catch (err) {
      console.error('Failed to fetch bookings', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (id, action) => {
    try {
      await api.post(`/bookings/owner/${id}/action/`, { action, notes: '' });
      // Update local state
      setBookings(bookings.map(b => 
        b.id === id ? { ...b, status: action } : b
      ));
    } catch (err) {
      alert('Failed to update booking status.');
      console.error(err);
    }
  };

  const getStatusBadge = (status) => {
    switch(status.toLowerCase()) {
      case 'approved':
      case 'completed':
        return <span className="flex items-center gap-1 bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-semibold"><CheckCircle2 className="w-3 h-3" /> {status.charAt(0).toUpperCase() + status.slice(1)}</span>;
      case 'rejected':
      case 'cancelled':
        return <span className="flex items-center gap-1 bg-red-100 text-red-700 px-3 py-1 rounded-full text-xs font-semibold"><XCircle className="w-3 h-3" /> {status.charAt(0).toUpperCase() + status.slice(1)}</span>;
      default:
        return <span className="flex items-center gap-1 bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-xs font-semibold"><Clock4 className="w-3 h-3" /> Pending</span>;
    }
  };

  if (loading) return <div className="p-8 text-center text-muted-foreground">Loading...</div>;

  return (
    <div className="max-w-7xl mx-auto p-6 mt-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Manage Booking Requests</h1>
      </div>

      {bookings.length === 0 ? (
        <div className="text-center p-12 border-2 border-dashed rounded-xl bg-muted/20">
          <Calendar className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-xl font-medium mb-2">No booking requests yet</h3>
          <p className="text-muted-foreground mb-6">When students request a visit to your properties, they will appear here.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {bookings.map(booking => (
            <div key={booking.id} className="bg-card rounded-xl border shadow-sm p-6 flex flex-col md:flex-row justify-between gap-6">
              <div className="flex-1 space-y-3">
                <div className="flex justify-between items-start">
                  <h3 className="text-lg font-bold text-foreground">
                    {booking.property.name}
                  </h3>
                  {getStatusBadge(booking.status)}
                </div>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-primary" />
                    <span className="font-medium text-foreground">{booking.user.first_name} {booking.user.last_name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-primary" />
                    <span>{new Date(booking.visit_date).toLocaleDateString()} at {booking.visit_time}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-primary" />
                    <span>{booking.property.area}</span>
                  </div>
                </div>

                {booking.message && (
                  <div className="mt-4 p-3 bg-muted rounded-lg text-sm italic">
                    "{booking.message}"
                  </div>
                )}
              </div>
              
              <div className="flex flex-col gap-2 justify-center border-t md:border-t-0 md:border-l md:pl-6 pt-4 md:pt-0">
                {booking.status === 'pending' ? (
                  <>
                    <Button onClick={() => handleAction(booking.id, 'approved')} className="w-full bg-green-600 hover:bg-green-700">Approve Request</Button>
                    <Button onClick={() => handleAction(booking.id, 'rejected')} variant="outline" className="w-full text-red-600 hover:text-red-700 hover:bg-red-50">Reject</Button>
                  </>
                ) : (
                  <Button variant="outline" className="w-full" disabled>Processed</Button>
                )}
                <Button variant="outline" className="w-full">Message Student</Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
