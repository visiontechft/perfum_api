# ==================== apps/suppliers/models.py ====================
from django.db import models
from django.core.validators import MinValueValidator

class Supplier(models.Model):
    # Définition des devises par pays
    COUNTRY_CURRENCY = {
        'Maroc': 'MAD',
        'Côte D’Ivoire': 'FCFA',
        'Sénégal': 'FCFA',
        'Mali': 'FCFA',
        'Burkina Faso': 'FCFA',
        'Niger': 'FCFA',
        'Togo': 'FCFA',
        'Mauritanie': 'MRU',
        'Guinée Conakry': 'GNF',
        'Ghana': 'GHS',
        'Cameroun': 'FCFA',
        'Gabon': 'XAF',
        'RDC': 'CDF',
    }

    DEVISE_CHOICES = [
        ('FCFA', 'FCFA'),
        ('MAD', 'MAD'),
        ('EUR', 'EUR'),
        ('USD', 'USD'),
        ('MRU', 'MRU'),
        ('GNF', 'GNF'),
        ('GHS', 'GHS'),
        ('XAF', 'XAF'),
        ('CDF', 'CDF'),
    ]
    
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    localisation = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Ex: quartier, rue ou détails supplémentaires de la ville"
    )
    whatsapp = models.CharField(max_length=200, help_text="Numéros multiples possibles séparés par /")
    prix = models.FloatField(validators=[MinValueValidator(0)])
    devise = models.CharField(
        max_length=10, 
        choices=DEVISE_CHOICES, 
        blank=True, 
        null=True,
        help_text="Devise optionnelle selon le pays"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['country', 'city', 'name']
        verbose_name = 'Fournisseur'
        verbose_name_plural = 'Fournisseurs'
    
    def __str__(self):
        loc = f", {self.localisation}" if self.localisation else ""
        return f"{self.name} - {self.city}{loc}, {self.country}"
    
    # Méthode pour remplir la devise automatiquement selon le pays
    def save(self, *args, **kwargs):
        if not self.devise and self.country in self.COUNTRY_CURRENCY:
            self.devise = self.COUNTRY_CURRENCY[self.country]
        super().save(*args, **kwargs)
