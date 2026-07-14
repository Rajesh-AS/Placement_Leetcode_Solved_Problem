"""URL routes for wishlists."""
from django.urls import path
from . import views

app_name = 'wishlists'

urlpatterns = [
    path('', views.WishlistListView.as_view(), name='wishlist-list'),
    path('toggle/<int:property_id>/', views.ToggleWishlistView.as_view(), name='wishlist-toggle'),
    path('check/<int:property_id>/', views.CheckWishlistView.as_view(), name='wishlist-check'),
]
