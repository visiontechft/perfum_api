# ==================== apps/products/models.py ====================
from django.db import models
from django.core.validators import MinValueValidator

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
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
    
    def __str__(self):
        return f"{self.code} - {self.nom_parfum}"