# ==================== apps/suppliers/serializers.py ====================
from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'country', 'city', 'whatsapp',
            'prix', 'devise', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class SupplierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'country', 'city', 'whatsapp', 'prix', 'devise']

class SupplierUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'country', 'city', 'whatsapp', 'prix', 'devise', 'is_active']