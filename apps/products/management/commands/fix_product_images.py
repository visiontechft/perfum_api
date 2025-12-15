# apps/products/management/commands/fix_product_images.py

from django.core.management.base import BaseCommand
from apps.products.models import Product
from django.db import connection

class Command(BaseCommand):
    help = 'Nettoie les images des produits de manière sécurisée'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categorie',
            type=str,
            help='Catégorie à nettoyer (Hommes ou Femmes)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Nettoyer toutes les catégories',
        )

    def handle(self, *args, **options):
        categorie = options.get('categorie')
        all_categories = options.get('all')

        if not categorie and not all_categories:
            self.stdout.write(self.style.ERROR(
                'Vous devez spécifier --categorie=Femmes ou --all'
            ))
            return

        # Déterminer les catégories à traiter
        categories_to_process = []
        if all_categories:
            categories_to_process = ['Hommes', 'Femmes']
        else:
            categories_to_process = [categorie]

        total_updated = 0
        total_errors = 0

        for cat in categories_to_process:
            self.stdout.write(f"\n📦 Traitement catégorie: {cat}")
            
            products = Product.objects.filter(categorie=cat)
            count = 0
            errors = 0

            for product in products:
                try:
                    # Utiliser une requête SQL directe pour éviter les problèmes Cloudinary
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE products_product SET image = NULL WHERE id = %s",
                            [product.id]
                        )
                    count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ {product.code} - {product.nom_parfum}")
                    )
                except Exception as e:
                    errors += 1
                    self.stdout.write(
                        self.style.ERROR(f"✗ Erreur {product.code}: {str(e)}")
                    )

            total_updated += count
            total_errors += errors

            self.stdout.write(f"\n--- Résumé {cat} ---")
            self.stdout.write(f"Images supprimées : {count}")
            self.stdout.write(f"Erreurs : {errors}")
            self.stdout.write(f"Total produits : {products.count()}")

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ TERMINÉ - Total : {total_updated} mis à jour, {total_errors} erreurs"
        ))


# UTILISATION :
# python manage.py fix_product_images --categorie=Femmes
# python manage.py fix_product_images --categorie=Hommes
# python manage.py fix_product_images --all