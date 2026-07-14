"""
URL routes for property management and search.
"""
from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # Public endpoints
    path('', views.PropertyListView.as_view(), name='property-list'),
    path('<int:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
    path('featured/', views.FeaturedPropertiesView.as_view(), name='featured'),
    path('popular/', views.PopularPropertiesView.as_view(), name='popular'),
    path('nearby/', views.NearbyPropertiesView.as_view(), name='nearby'),
    path('suggest/', views.AutoSuggestView.as_view(), name='auto-suggest'),
    path('amenities/', views.AmenityListView.as_view(), name='amenities'),
    path('smart-search/', views.SmartSearchView.as_view(), name='smart-search'),

    # Owner endpoints
    path('my/', views.OwnerPropertyListView.as_view(), name='owner-properties'),
    path('create/', views.OwnerPropertyCreateView.as_view(), name='create-property'),
    path('<int:pk>/update/', views.OwnerPropertyUpdateView.as_view(), name='update-property'),
    path('<int:pk>/delete/', views.OwnerPropertyDeleteView.as_view(), name='delete-property'),
    path('<int:property_id>/upload-images/', views.PropertyImageUploadView.as_view(), name='upload-images'),

    # Admin endpoints
    path('admin/all/', views.AdminPropertyListView.as_view(), name='admin-property-list'),
    path('admin/<int:pk>/action/', views.AdminPropertyActionView.as_view(), name='admin-property-action'),
]
