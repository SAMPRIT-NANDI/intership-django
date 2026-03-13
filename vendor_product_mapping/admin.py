from django.contrib import admin
from .models import VendorProductMapping

@admin.register(VendorProductMapping)
class VendorProductMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'product', 'primary_mapping', 'is_active']
    list_filter = ['primary_mapping', 'is_active']
    search_fields = ['vendor__name', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
