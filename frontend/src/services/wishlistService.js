import { api } from './api';

export const wishlistService = {
  getWishlists: () =>
    api.get('/wishlists/').then(r => r.data),

  addToWishlist: (propertyId) =>
    api.post('/wishlists/toggle/', { property_id: propertyId }).then(r => r.data),

  removeFromWishlist: (propertyId) =>
    api.delete(`/wishlists/${propertyId}/`).then(r => r.data),

  checkWishlisted: (propertyId) =>
    api.get(`/wishlists/check/${propertyId}/`).then(r => r.data),
};
