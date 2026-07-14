"""URL routes for booking management."""
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Student endpoints
    path('my/', views.StudentBookingListView.as_view(), name='student-bookings'),
    path('create/', views.StudentBookingCreateView.as_view(), name='create-booking'),
    path('<int:pk>/cancel/', views.StudentBookingCancelView.as_view(), name='cancel-booking'),

    # Owner endpoints
    path('owner/', views.OwnerBookingListView.as_view(), name='owner-bookings'),
    path('owner/<int:pk>/action/', views.OwnerBookingActionView.as_view(), name='owner-booking-action'),

    # Payment endpoints
    path('<int:pk>/pay/', views.CreateMockPaymentView.as_view(), name='create-payment'),
    path('payment/verify/', views.VerifyMockPaymentView.as_view(), name='verify-payment'),
]
