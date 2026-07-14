from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_type', 'target_id', 'reporter', 'status', 'created_at')
    list_filter = ('report_type', 'status')
    search_fields = ('reporter__username', 'reason', 'description')
