import { api } from './api';

export const propertyService = {
  getProperties: (params = {}) =>
    api.get('/properties/', { params }).then(r => r.data),

  getPropertyById: (id) =>
    api.get(`/properties/${id}/`).then(r => r.data),

  getFeatured: () =>
    api.get('/properties/featured/').then(r => r.data),

  getPopular: () =>
    api.get('/properties/popular/').then(r => r.data),

  getNearby: (lat, lng, radius = 5) =>
    api.get('/properties/nearby/', { params: { lat, lng, radius } }).then(r => r.data),

  smartSearch: (query) =>
    api.get('/properties/smart-search/', { params: { q: query } }).then(r => r.data),

  getSuggestions: (query) =>
    api.get('/properties/suggest/', { params: { q: query } }).then(r => r.data),

  getAmenities: () =>
    api.get('/properties/amenities/').then(r => r.data),

  // Owner endpoints
  getMyProperties: () =>
    api.get('/properties/my/').then(r => r.data),

  createProperty: (data) =>
    api.post('/properties/create/', data).then(r => r.data),

  updateProperty: (id, data) =>
    api.patch(`/properties/${id}/update/`, data).then(r => r.data),

  deleteProperty: (id) =>
    api.delete(`/properties/${id}/delete/`).then(r => r.data),

  uploadImages: (propertyId, formData) =>
    api.post(`/properties/${propertyId}/upload-images/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(r => r.data),
};
