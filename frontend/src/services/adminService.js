import { api } from './api';

export const adminService = {
  getDashboardStats: () =>
    api.get('/auth/admin/dashboard/').then(r => r.data),

  getUsers: (params = {}) =>
    api.get('/auth/admin/users/', { params }).then(r => r.data),

  userAction: (userId, action) =>
    api.post(`/auth/admin/users/${userId}/action/`, { action }).then(r => r.data),

  getAllProperties: (params = {}) =>
    api.get('/properties/admin/all/', { params }).then(r => r.data),

  propertyAction: (propertyId, action, reason = '') =>
    api.post(`/properties/admin/${propertyId}/action/`, { action, reason }).then(r => r.data),
};
