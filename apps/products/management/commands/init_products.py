from django.core.management.base import BaseCommand
from apps.products.models import Product

# Prix unique pour tous les parfums
PRIX_STANDARD = 3500

# Données des produits
PRODUCTS_HOMMES = [
    {"code": "001", "nom_parfum": "Bleu de Chanel", "nom_etiquette": "B. Chnl"},
    {"code": "002", "nom_parfum": "Allure Sport Chanel", "nom_etiquette": "Alr. Spr"},
    {"code": "004", "nom_parfum": "Dior Homme Sauvage", "nom_etiquette": "Sge"},
    {"code": "022", "nom_parfum": "Dior Homme Intense", "nom_etiquette": "D. Yor Intse"},
    {"code": "014", "nom_parfum": "Pi de Givenchy", "nom_etiquette": "P. Gvc"},
    {"code": "008", "nom_parfum": "Invictus de Paco Rabanne", "nom_etiquette": "Ivts."},
    {"code": "030", "nom_parfum": "Black Orchid de Tom Ford", "nom_etiquette": "Blk. Or chd"},
    {"code": "031", "nom_parfum": "Scandal Homme de JP Gaultier", "nom_etiquette": "Scl. Hme"},
    {"code": "010", "nom_parfum": "Black XS l'Exces de P Rabanne", "nom_etiquette": "Blk. Exs."},
    {"code": "021", "nom_parfum": "The One For Men de Dolce Gabana", "nom_etiquette": "The 1. For Man"},
    {"code": "024", "nom_parfum": "La Nuit de l'Homme de Y S Laurent", "nom_etiquette": "Noui. D. Lom."},
    {"code": "020", "nom_parfum": "Boss Bottled de Hugo Boss", "nom_etiquette": "Bos Boted"},
    {"code": "017", "nom_parfum": "Terre d'Hermès de Hermès", "nom_etiquette": "Ter. Derms"},
    {"code": "007", "nom_parfum": "One Million de Paco Rabanne", "nom_etiquette": "1M."},
    {"code": "012", "nom_parfum": "Acqua Di Gio de Giorgio Armani", "nom_etiquette": "Aqa. D. G."},
]

PRODUCTS_FEMMES = [
    {"code": "111", "nom_parfum": "J'adore de Dior", "nom_etiquette": "Jdr."},
    {"code": "127", "nom_parfum": "My Way de Giorgio Armani", "nom_etiquette": "Myway"},
    {"code": "120", "nom_parfum": "La Vie Est Belle de Lancome", "nom_etiquette": "La V. et Bel"},
    {"code": "102", "nom_parfum": "Black Opium de Yves St Laurent", "nom_etiquette": "Blk. Opm"},
    {"code": "106", "nom_parfum": "Scandale Femme de JP Gaultier", "nom_etiquette": "Scl"},
    {"code": "112", "nom_parfum": "L'Interdit de Givenchy", "nom_etiquette": "Intd."},
    {"code": "109", "nom_parfum": "Evidence de Yves Rocher", "nom_etiquette": "Evce."},
    {"code": "132", "nom_parfum": "Hypnotic Poison de Dior", "nom_etiquette": "Hpno Pwazon"},
    {"code": "107", "nom_parfum": "Libre de Yves Saint Laurent", "nom_etiquette": "Lbr."},
    {"code": "113", "nom_parfum": "Miss Dior Cherie de Dior", "nom_etiquette": "Ms. Dr. Chr."},
    {"code": "116", "nom_parfum": "Coco Mademoiselle de Chanel", "nom_etiquette": "Cc. Mlle."},
    {"code": "126", "nom_parfum": "Hugo Women de Hugo Boss", "nom_etiquette": "Higo Wmn"},
    {"code": "131", "nom_parfum": "NINA de Nina Ricci", "nom_etiquette": "Ni. Na."},
    {"code": "125", "nom_parfum": "Gucci Guilty de Gucci", "nom_etiquette": "Gci. Glty"},
    {"code": "105", "nom_parfum": "Nuit Blanche de Yves S Laurent", "nom_etiquette": "Nt. Blch."},
]


class Command(BaseCommand):
    help = 'Initialise les produits dans la base de données'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprimer tous les produits existants avant l\'initialisation',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🚀 Initialisation des produits...'))
        
        # Vérifier si des produits existent déjà
        existing_count = Product.objects.count()
        
        if existing_count > 0:
            self.stdout.write(
                self.style.WARNING(f'⚠️  {existing_count} produits existent déjà dans la base de données.')
            )
            
            if options['clear']:
                Product.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('✅ Base de données nettoyée.'))
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Utilisez --clear pour supprimer les données existantes.')
                )
                return
        
        try:
            # Créer les produits hommes
            products_created = 0
            products_updated = 0
            
            for product_data in PRODUCTS_HOMMES:
                product, created = Product.objects.update_or_create(
                    code=product_data['code'],
                    defaults={
                        'nom_parfum': product_data['nom_parfum'],
                        'nom_etiquette': product_data['nom_etiquette'],
                        'prix': PRIX_STANDARD,
                        'categorie': 'Hommes',
                        'stock': 10,
                        'description': f"Parfum {product_data['nom_parfum']} pour homme"
                    }
                )
                if created:
                    products_created += 1
                else:
                    products_updated += 1
            
            # Créer les produits femmes
            for product_data in PRODUCTS_FEMMES:
                product, created = Product.objects.update_or_create(
                    code=product_data['code'],
                    defaults={
                        'nom_parfum': product_data['nom_parfum'],
                        'nom_etiquette': product_data['nom_etiquette'],
                        'prix': PRIX_STANDARD,
                        'categorie': 'Femmes',
                        'stock': 10,
                        'description': f"Parfum {product_data['nom_parfum']} pour femme"
                    }
                )
                if created:
                    products_created += 1
                else:
                    products_updated += 1
            
            total = len(PRODUCTS_HOMMES) + len(PRODUCTS_FEMMES)
            
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(self.style.SUCCESS('✅ Initialisation terminée avec succès!'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(f'📊 Statistiques:')
            self.stdout.write(f'   • Produits créés: {products_created}')
            self.stdout.write(f'   • Produits mis à jour: {products_updated}')
            self.stdout.write(f'   • Total dans la base: {total}')
            self.stdout.write(f'   • Parfums hommes: {len(PRODUCTS_HOMMES)}')
            self.stdout.write(f'   • Parfums femmes: {len(PRODUCTS_FEMMES)}')
            self.stdout.write(f'   • Prix standard: {PRIX_STANDARD} FCFA')
            self.stdout.write(self.style.SUCCESS('=' * 60))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de l\'initialisation: {str(e)}')
            )
            raise