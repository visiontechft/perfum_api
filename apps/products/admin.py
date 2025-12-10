from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom_parfum', 'categorie', 'prix', 'stock', 'created_at']
    list_filter = ['categorie', 'created_at']
    search_fields = ['code', 'nom_parfum', 'nom_etiquette']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']