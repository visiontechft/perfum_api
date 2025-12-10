# ==================== apps/products/serializers.py ====================
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'code', 'nom_parfum', 'nom_etiquette', 
            'categorie', 'description', 'prix', 'stock', 
            'image', 'image_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    
    def validate_code(self, value):
        if self.instance:
            if Product.objects.exclude(pk=self.instance.pk).filter(code=value).exists():
                raise serializers.ValidationError("Ce code produit existe déjà.")
        else:
            if Product.objects.filter(code=value).exists():
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