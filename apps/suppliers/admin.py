# ==================== apps/suppliers/admin.py ====================
from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'prix', 'devise', 'is_active', 'created_at']
    list_filter = ['country', 'city', 'devise', 'is_active', 'created_at']
    search_fields = ['name', 'country', 'city', 'whatsapp']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['country', 'city', 'name']