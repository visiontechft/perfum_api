from django.db import models
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField

class CategoryImage(models.Model):
    """Images par défaut pour chaque catégorie"""
    CATEGORY_CHOICES = [
        ('Hommes', 'Hommes'),
        ('Femmes', 'Femmes'),
    ]
    
    categorie = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES,
        unique=True,
        verbose_name="Catégorie"
    )
    image = CloudinaryField(
        'image',
        folder='parfums/categories',
        transformation={
            'quality': 'auto',
            'fetch_format': 'auto'
        },
        help_text="Image par défaut pour tous les produits de cette catégorie"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Image de Catégorie'
        verbose_name_plural = 'Images de Catégories'
    
    def __str__(self):
        return f"Image par défaut - {self.categorie}"
    
    @property
    def image_url(self):
        """Retourne l'URL complète de l'image"""
        if self.image:
            return self.image.url
        return None


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Hommes', 'Hommes'),
        ('Femmes', 'Femmes'),
    ]
    
    code = models.CharField(max_length=10, unique=True, db_index=True)
    nom_parfum = models.CharField(max_length=200)
    nom_etiquette = models.CharField(max_length=100)
    categorie = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    prix = models.FloatField(validators=[MinValueValidator(0)])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Image spécifique au produit (optionnelle)
    image = CloudinaryField(
        'image',
        blank=True,
        null=True,
        folder='parfums/products',
        transformation={
            'quality': 'auto',
            'fetch_format': 'auto'
        },
        help_text="Image spécifique à ce produit (laissez vide pour utiliser l'image par défaut de la catégorie)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
    
    def __str__(self):
        return f"{self.code} - {self.nom_parfum}"
    
    @property
    def image_url(self):
        """
        Retourne l'URL de l'image du produit.
        Si le produit n'a pas d'image spécifique, retourne l'image par défaut de sa catégorie.
        """
        try:
            # Si le produit a une image spécifique, l'utiliser
            if self.image and hasattr(self.image, 'url'):
                return self.image.url
        except Exception:
            pass
        
        # Sinon, chercher l'image par défaut de la catégorie
        try:
            category_image = CategoryImage.objects.get(categorie=self.categorie)
            if category_image.image and hasattr(category_image.image, 'url'):
                return category_image.image.url
        except (CategoryImage.DoesNotExist, Exception):
            pass
        
        return None
    
    def get_image_source(self):
        """Indique si l'image vient du produit ou de la catégorie"""
        try:
            if self.image and hasattr(self.image, 'url'):
                return "Produit"
        except Exception:
            pass
        
        try:
            category_image = CategoryImage.objects.get(categorie=self.categorie)
            if category_image.image and hasattr(category_image.image, 'url'):
                return "Catégorie"
        except (CategoryImage.DoesNotExist, Exception):
            pass
        
        return "Aucune"