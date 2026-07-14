"""Views for reporting content and admin moderation."""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType

from .models import Report
from .serializers import ReportSerializer, ReportCreateSerializer
from apps.users.permissions import IsAdmin

class CreateReportView(generics.CreateAPIView):
    """Submit a report."""
    serializer_class = ReportCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
        # Notify admins could be added here

class AdminReportListView(generics.ListAPIView):
    """List all reports for admin review."""
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        queryset = Report.objects.all().select_related('reporter')
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

class AdminReportActionView(APIView):
    """Admin update report status."""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({'error': 'Report not found.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        notes = request.data.get('admin_notes', '')

        if action in ['review', 'resolve', 'dismiss']:
            if action == 'review':
                report.status = Report.Status.REVIEWED
            elif action == 'resolve':
                report.status = Report.Status.RESOLVED
            elif action == 'dismiss':
                report.status = Report.Status.DISMISSED
            
            if notes:
                report.admin_notes = notes
                
            report.save(update_fields=['status', 'admin_notes'])
            return Response({'message': f'Report {action}ed.'})
            
        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
