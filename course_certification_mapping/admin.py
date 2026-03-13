from django.contrib import admin
from .models import CourseCertificationMapping

@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'certification', 'primary_mapping', 'is_active']
    list_filter = ['primary_mapping', 'is_active']
    search_fields = ['course__name', 'certification__name']
    readonly_fields = ['created_at', 'updated_at']
