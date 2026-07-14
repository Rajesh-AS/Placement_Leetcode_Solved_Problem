"""URL patterns for reviews."""
from django.urls import path
from . import views

urlpatterns = [
    path('property/<int:property_id>/', views.PropertyReviewsView.as_view(), name='property-reviews'),
    path('create/', views.CreateReviewView.as_view(), name='create-review'),
    path('my/', views.UserReviewsView.as_view(), name='user-reviews'),
    path('admin/', views.AdminReviewListView.as_view(), name='admin-reviews'),
    path('admin/<int:pk>/action/', views.AdminReviewActionView.as_view(), name='admin-review-action'),
]
