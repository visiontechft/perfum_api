# ==================== apps/products/serializers.py ====================
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_source = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'code',
            'nom_parfum',
            'nom_etiquette',
            'categorie',
            'description',
            'prix',
            'stock',
            'image',
            'image_url',
            'image_source',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        """
        Retourne l'image du produit ou celle de la catégorie (fallback)
        """
        url = obj.image_url
        request = self.context.get('request')

        if url and request:
            return request.build_absolute_uri(url)

        return url

    def get_image_source(self, obj):
        """
        Indique la source de l'image : Produit / Catégorie / Aucune
        """
        return obj.get_image_source()

    def validate_code(self, value):
        queryset = Product.objects.filter(code=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Ce code produit existe déjà.")

        return value


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['code', 'nom_parfum', 'nom_etiquette', 'categorie', 
                  'description', 'prix', 'stock']

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['nom_parfum', 'nom_etiquette', 'categorie', 
                  'description', 'prix', 'stock', 'image']
        
class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()