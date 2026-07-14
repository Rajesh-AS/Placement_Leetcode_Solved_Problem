import { api } from './api';

export const reviewService = {
  getPropertyReviews: (propertyId) =>
    api.get(`/reviews/property/${propertyId}/`).then(r => r.data),

  createReview: (data) =>
    api.post('/reviews/create/', data).then(r => r.data),

  updateReview: (id, data) =>
    api.patch(`/reviews/${id}/update/`, data).then(r => r.data),

  deleteReview: (id) =>
    api.delete(`/reviews/${id}/delete/`).then(r => r.data),
};
