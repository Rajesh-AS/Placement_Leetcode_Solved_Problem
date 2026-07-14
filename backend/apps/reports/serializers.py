"""Serializers for reports."""
from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    reporter_name = serializers.CharField(source='reporter.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'reporter', 'reporter_name', 'report_type', 'target_id',
            'reason', 'description', 'status', 'status_display', 'admin_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reporter', 'status', 'admin_notes', 'created_at', 'updated_at']

class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['report_type', 'target_id', 'reason', 'description']
