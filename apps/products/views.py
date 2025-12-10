# ==================== apps/products/views.py ====================
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import (
    ProductSerializer, 
    ProductCreateSerializer, 
    ProductUpdateSerializer,
    ImageUploadSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les produits
    
    list: Récupérer tous les produits
    create: Créer un nouveau produit
    retrieve: Récupérer un produit spécifique
    update: Mettre à jour un produit
    partial_update: Mise à jour partielle d'un produit
    destroy: Supprimer un produit
    upload_image: Télécharger une image pour un produit
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie', 'code']
    search_fields = ['nom_parfum', 'nom_etiquette', 'code', 'description']
    ordering_fields = ['prix', 'stock', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        if self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        if self.action == 'upload_image':
            return ImageUploadSerializer
        return ProductSerializer
    
    @swagger_auto_schema(
        operation_description="Récupérer la liste des produits avec filtres optionnels",
        manual_parameters=[
            openapi.Parameter('categorie', openapi.IN_QUERY, 
                            description="Filtrer par catégorie (Hommes/Femmes)", 
                            type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, 
                            description="Rechercher dans nom, code, description", 
                            type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Créer un nouveau produit",
        request_body=ProductCreateSerializer
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(
            ProductSerializer(product, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    
    @swagger_auto_schema(
        operation_description="Télécharger une image pour un produit",
        manual_parameters=[
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='Image du produit',
                required=True
            )
        ],
        responses={200: ProductSerializer}
    )
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        """Télécharger une image pour un produit"""
        product = self.get_object()
        serializer = ImageUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            product.image = serializer.validated_data['image']
            product.save()
            return Response(
                ProductSerializer(product, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)