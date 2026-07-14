"""URL routes for reports."""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('create/', views.CreateReportView.as_view(), name='create-report'),
    path('admin/all/', views.AdminReportListView.as_view(), name='admin-reports'),
    path('admin/<int:pk>/action/', views.AdminReportActionView.as_view(), name='admin-report-action'),
]
