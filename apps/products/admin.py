from django.contrib import admin
from django.utils.html import format_html
from .models import Product, CategoryImage

@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ['categorie', 'image_preview', 'created_at', 'updated_at']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    
    def image_preview(self, obj):
        """Affiche un aperçu de l'image avec gestion d'erreur"""
        try:
            if obj.image and hasattr(obj.image, 'url'):
                return format_html(
                    '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                    obj.image.url
                )
        except Exception as e:
            return format_html('<span style="color: red;">Erreur: {}</span>', str(e))
        return "Aucune image"
    image_preview.short_description = 'Aperçu'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom_parfum', 'categorie', 'prix', 'stock', 'image_preview', 'image_source', 'created_at']
    list_filter = ['categorie', 'created_at']
    search_fields = ['code', 'nom_parfum', 'nom_etiquette']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('code', 'nom_parfum', 'nom_etiquette', 'categorie')
        }),
        ('Détails', {
            'fields': ('description', 'prix', 'stock')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Téléchargez une image spécifique pour ce produit, ou laissez vide pour utiliser l\'image par défaut de la catégorie.'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        """Affiche un aperçu de l'image avec gestion d'erreur robuste"""
        try:
            image_url = obj.image_url
            if image_url:
                source = obj.get_image_source()
                color = '#28a745' if source == 'Produit' else '#007bff'
                return format_html(
                    '<div style="text-align: center;">'
                    '<img src="{}" style="max-height: 80px; max-width: 80px; border: 2px solid {}; border-radius: 4px;" onerror="this.style.display=\'none\'" />'
                    '<br><small style="color: {};">{}</small>'
                    '</div>',
                    image_url, color, color, source
                )
        except Exception as e:
            return format_html('<span style="color: #dc3545;">Erreur: {}</span>', str(e))
        
        return format_html('<span style="color: #6c757d;">Aucune image</span>')
    image_preview.short_description = 'Image'
    
    def image_source(self, obj):
        """Indique la source de l'image avec gestion d'erreur"""
        try:
            source = obj.get_image_source()
            if source == "Produit":
                return format_html('<span style="color: #28a745; font-weight: bold;">✓ Spécifique</span>')
            elif source == "Catégorie":
                return format_html('<span style="color: #007bff;">→ Catégorie</span>')
            else:
                return format_html('<span style="color: #dc3545;">✗ Aucune</span>')
        except Exception as e:
            return format_html('<span style="color: #dc3545;">Erreur</span>')
    image_source.short_description = 'Source Image'