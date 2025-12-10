# ==================== apps/suppliers/views.py ====================
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Supplier
from .serializers import (
    SupplierSerializer,
    SupplierCreateSerializer,
    SupplierUpdateSerializer
)

class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les fournisseurs
    
    list: Récupérer tous les fournisseurs
    create: Créer un nouveau fournisseur
    retrieve: Récupérer un fournisseur spécifique
    update: Mettre à jour un fournisseur
    partial_update: Mise à jour partielle
    destroy: Supprimer un fournisseur
    countries: Liste des pays disponibles
    cities: Liste des villes par pays
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'city', 'localisation', 'is_active', 'devise']
    search_fields = ['name', 'country', 'city', 'localisation', 'whatsapp']
    ordering_fields = ['prix', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SupplierCreateSerializer
        if self.action in ['update', 'partial_update']:
            return SupplierUpdateSerializer
        return SupplierSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset
    
    @swagger_auto_schema(
        operation_description="Récupérer la liste des pays disponibles",
        responses={200: openapi.Response('Liste des pays', schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ))}
    )
    @action(detail=False, methods=['get'])
    def countries(self, request):
        """Récupérer la liste des pays uniques"""
        countries = Supplier.objects.values_list('country', flat=True).distinct().order_by('country')
        return Response(list(countries))
    
    @swagger_auto_schema(
        operation_description="Récupérer les villes d'un pays spécifique",
        manual_parameters=[
            openapi.Parameter('country', openapi.IN_QUERY, 
                            description="Nom du pays", 
                            type=openapi.TYPE_STRING,
                            required=True)
        ],
        responses={200: openapi.Response('Liste des villes', schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ))}
    )
    @action(detail=False, methods=['get'])
    def cities(self, request):
        """Récupérer les villes d'un pays"""
        country = request.query_params.get('country')
        if not country:
            return Response(
                {'error': 'Le paramètre country est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Inclut la localisation dans la récupération des villes
        cities = Supplier.objects.filter(country=country).values_list('city', 'localisation').distinct()
        # Formatage : "ville - localisation" si localisation existante
        formatted_cities = [
            f"{city} - {localisation}" if localisation else city
            for city, localisation in cities
        ]
        return Response(formatted_cities)
