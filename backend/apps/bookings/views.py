"""
Views for booking management — create, list, status updates.
"""
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer, BookingStatusUpdateSerializer
from apps.users.permissions import IsStudent, IsOwner, IsAdmin, IsNotSuspended


class StudentBookingListView(generics.ListAPIView):
    """List bookings for the authenticated student."""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotSuspended]

    def get_queryset(self):
        queryset = Booking.objects.filter(
            user=self.request.user
        ).select_related('property', 'property__owner', 'room')
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class StudentBookingCreateView(generics.CreateAPIView):
    """Student creates a visit booking."""
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        booking = serializer.save()
        # Notify the property owner
        from apps.notifications.models import Notification
        Notification.objects.create(
            user=booking.property.owner,
            notification_type='booking',
            title='New Visit Request',
            message=f'{booking.user.get_full_name()} wants to visit "{booking.property.name}" on {booking.visit_date} at {booking.visit_time}.',
            related_object_id=booking.id,
        )


class StudentBookingCancelView(APIView):
    """Student cancels their booking."""
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status in ['cancelled', 'completed']:
            return Response({'error': 'Cannot cancel this booking.'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=['status'])

        from apps.notifications.models import Notification
        Notification.objects.create(
            user=booking.property.owner,
            notification_type='booking',
            title='Booking Cancelled',
            message=f'{booking.user.get_full_name()} cancelled their visit to "{booking.property.name}".',
            related_object_id=booking.id,
        )
        return Response({'message': 'Booking cancelled.'})


class OwnerBookingListView(generics.ListAPIView):
    """List bookings for the owner's properties."""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = Booking.objects.filter(
            property__owner=self.request.user
        ).select_related('user', 'property', 'room')
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class OwnerBookingActionView(APIView):
    """Owner approves, rejects, or reschedules a booking."""
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, property__owner=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']
        from apps.notifications.models import Notification

        if action == 'approve':
            booking.status = Booking.Status.APPROVED
            booking.owner_notes = serializer.validated_data.get('owner_notes', '')
            booking.save(update_fields=['status', 'owner_notes'])
            Notification.objects.create(
                user=booking.user,
                notification_type='booking',
                title='Visit Approved!',
                message=f'Your visit to "{booking.property.name}" on {booking.visit_date} has been approved.',
                related_object_id=booking.id,
            )
        elif action == 'reject':
            booking.status = Booking.Status.REJECTED
            booking.owner_notes = serializer.validated_data.get('owner_notes', '')
            booking.save(update_fields=['status', 'owner_notes'])
            Notification.objects.create(
                user=booking.user,
                notification_type='booking',
                title='Visit Rejected',
                message=f'Your visit to "{booking.property.name}" was not approved. {booking.owner_notes}',
                related_object_id=booking.id,
            )
        elif action == 'reschedule':
            booking.status = Booking.Status.RESCHEDULED
            booking.rescheduled_date = serializer.validated_data['rescheduled_date']
            booking.rescheduled_time = serializer.validated_data['rescheduled_time']
            booking.reschedule_reason = serializer.validated_data.get('reschedule_reason', '')
            booking.owner_notes = serializer.validated_data.get('owner_notes', '')
            booking.save()
            Notification.objects.create(
                user=booking.user,
                notification_type='booking',
                title='Visit Rescheduled',
                message=f'Your visit to "{booking.property.name}" has been rescheduled to {booking.rescheduled_date} at {booking.rescheduled_time}.',
                related_object_id=booking.id,
            )
        elif action == 'complete':
            booking.status = Booking.Status.COMPLETED
            booking.save(update_fields=['status'])
            Notification.objects.create(
                user=booking.user,
                notification_type='booking',
                title='Visit Completed',
                message=f'Your visit to "{booking.property.name}" has been marked as completed. Please leave a review!',
                related_object_id=booking.id,
            )

        return Response(BookingSerializer(booking).data)

from .models import Payment

class CreateMockPaymentView(APIView):
    """Creates a mock payment intent (simulating Razorpay order creation)."""
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        amount = request.data.get('amount', 500.00) # e.g. booking fee
        
        # Create mock order
        import uuid
        mock_order_id = f"order_{uuid.uuid4().hex[:14]}"
        
        payment = Payment.objects.create(
            booking=booking,
            user=request.user,
            amount=amount,
            order_id=mock_order_id,
            status=Payment.Status.PENDING
        )

        return Response({
            'payment_id': payment.id,
            'order_id': mock_order_id,
            'amount': amount,
            'currency': 'INR',
            'key': 'rzp_test_mockkey' # For frontend to simulate
        })


class VerifyMockPaymentView(APIView):
    """Verifies a mock payment (simulating Razorpay signature verification)."""
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        payment_id = request.data.get('payment_id')
        transaction_id = request.data.get('transaction_id')
        
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)

        payment.status = Payment.Status.SUCCESS
        payment.transaction_id = transaction_id or f"pay_{import_uuid().hex[:14]}"
        payment.save()
        
        # Update booking status or notes if needed
        # e.g., booking.is_paid = True (if we added it)
        
        from apps.notifications.models import Notification
        Notification.objects.create(
            user=payment.booking.property.owner,
            notification_type='payment',
            title='Payment Received!',
            message=f'{request.user.get_full_name()} paid ₹{payment.amount} for booking #{payment.booking.id}.',
            related_object_id=payment.booking.id,
        )

        return Response({'message': 'Payment successful', 'status': 'success'})

def import_uuid():
    import uuid
    return uuid.uuid4()
