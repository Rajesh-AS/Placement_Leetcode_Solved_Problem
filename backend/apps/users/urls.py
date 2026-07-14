"""
URL routes for user authentication and profile management.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('google/', views.GoogleAuthView.as_view(), name='google-auth'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/upload-picture/', views.UploadProfilePictureView.as_view(), name='upload-picture'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),

    # Admin
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:user_id>/action/', views.AdminUserActionView.as_view(), name='admin-user-action'),
    path('admin/dashboard/', views.AdminDashboardStatsView.as_view(), name='admin-dashboard'),
]
