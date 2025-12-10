# ==================== apps/suppliers/models.py ====================
from django.db import models
from django.core.validators import MinValueValidator

class Supplier(models.Model):
    DEVISE_CHOICES = [
        ('FCFA', 'FCFA'),
        ('MAD', 'MAD'),
        ('EUR', 'EUR'),
        ('USD', 'USD'),
    ]
    
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    whatsapp = models.CharField(max_length=20)
    prix = models.FloatField(validators=[MinValueValidator(0)])
    devise = models.CharField(max_length=10, choices=DEVISE_CHOICES, default='FCFA')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['country', 'city', 'name']
        verbose_name = 'Fournisseur'
        verbose_name_plural = 'Fournisseurs'
    
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"