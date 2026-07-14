import { api } from './api';

export const bookingService = {
  getMyBookings: () =>
    api.get('/bookings/my/').then(r => r.data),

  createBooking: (data) =>
    api.post('/bookings/create/', data).then(r => r.data),

  cancelBooking: (id) =>
    api.post(`/bookings/${id}/cancel/`).then(r => r.data),

  // Owner endpoints
  getPropertyBookings: () =>
    api.get('/bookings/owner/').then(r => r.data),

  updateBookingStatus: (id, data) =>
    api.patch(`/bookings/${id}/status/`, data).then(r => r.data),
};
