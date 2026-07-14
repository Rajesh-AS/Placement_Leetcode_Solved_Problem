import { useState } from 'react';
import { api } from '@/services/api';
import { Button } from '@/components/common/Button';
import { X, CreditCard, Lock, CheckCircle2 } from 'lucide-react';

export function PaymentCheckoutModal({ booking, onClose, onSuccess }) {
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1);
  const [paymentDetails, setPaymentDetails] = useState(null);

  const handleInitiatePayment = async () => {
    setLoading(true);
    try {
      const res = await api.post(`/bookings/${booking.id}/pay/`, {
        amount: 500.00 // standard advance booking fee
      });
      setPaymentDetails(res.data);
      setStep(2);
    } catch (err) {
      console.error('Failed to initiate payment', err);
      alert('Failed to initiate payment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateSuccess = async () => {
    setLoading(true);
    try {
      await api.post('/bookings/payment/verify/', {
        payment_id: paymentDetails.payment_id,
        transaction_id: `mock_tx_${Date.now()}`
      });
      setStep(3);
      setTimeout(() => {
        onSuccess();
      }, 2000);
    } catch (err) {
      console.error('Failed to verify payment', err);
      alert('Payment verification failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-card w-full max-w-md rounded-2xl shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="p-4 border-b border-border flex justify-between items-center bg-secondary/30">
          <h2 className="font-bold text-lg flex items-center gap-2">
            <CreditCard className="w-5 h-5 text-primary" />
            Payment Checkout
          </h2>
          {step !== 3 && (
            <button onClick={onClose} className="p-1 hover:bg-muted rounded-full transition-colors">
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Content */}
        <div className="p-6">
          {step === 1 && (
            <div className="space-y-6">
              <div className="text-center">
                <h3 className="text-xl font-bold mb-2">Advance Booking Fee</h3>
                <p className="text-muted-foreground text-sm">Pay the advance fee to confirm your booking for {booking.property.name}.</p>
              </div>
              
              <div className="bg-secondary/50 rounded-xl p-4 space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Property</span>
                  <span className="font-medium">{booking.property.name}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Date</span>
                  <span className="font-medium">{new Date(booking.visit_date).toLocaleDateString()}</span>
                </div>
                <div className="border-t border-border pt-3 flex justify-between font-bold text-lg">
                  <span>Total Amount</span>
                  <span className="text-primary">₹500.00</span>
                </div>
              </div>

              <div className="flex items-center gap-2 text-xs text-muted-foreground justify-center">
                <Lock className="w-3 h-3" /> Secure Payment Gateway (Mock)
              </div>

              <Button onClick={handleInitiatePayment} disabled={loading} className="w-full h-12 text-lg font-bold">
                {loading ? 'Processing...' : 'Proceed to Pay ₹500'}
              </Button>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6 text-center py-4">
              <h3 className="text-lg font-bold">Razorpay Mock Gateway</h3>
              <p className="text-sm text-muted-foreground">Order ID: {paymentDetails.order_id}</p>
              
              <div className="grid grid-cols-2 gap-4 mt-6">
                <Button variant="outline" onClick={onClose} className="border-red-200 text-red-600 hover:bg-red-50">
                  Simulate Failure
                </Button>
                <Button onClick={handleSimulateSuccess} disabled={loading} className="bg-green-600 hover:bg-green-700">
                  {loading ? 'Verifying...' : 'Simulate Success'}
                </Button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4 text-center py-8">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
                <CheckCircle2 className="w-10 h-10 text-green-600" />
              </div>
              <h3 className="text-2xl font-bold text-green-700">Payment Successful!</h3>
              <p className="text-muted-foreground text-sm">Your booking has been confirmed.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
