# 🌸 Parfum API - Django REST Framework

API REST professionnelle pour la gestion de produits de parfums et fournisseurs avec Docker, PostgreSQL et Swagger.

## 🚀 Fonctionnalités

- ✅ Gestion complète des produits (CRUD)
- ✅ Gestion des fournisseurs avec prix et devises
- ✅ Upload d'images pour les produits
- ✅ Documentation API automatique avec Swagger/ReDoc
- ✅ Filtres et recherche avancés
- ✅ Pagination intégrée
- ✅ Docker pour développement et production
- ✅ PostgreSQL comme base de données
- ✅ Prêt pour déploiement sur Render

## 📋 Prérequis

- Python 3.11+
- Docker & Docker Compose
- Git

## 🛠️ Installation

### 1. Cloner le repository

```bash
git clone <votre-repo>
cd parfum_api
```

### 2. Configuration des variables d'environnement

```bash
cp .env.example .env
```

Éditez le fichier `.env` avec vos configurations.

### 3. Démarrage avec Docker

```bash
# Build et démarrer les conteneurs
docker-compose up --build

# En arrière-plan
docker-compose up -d
```

### 4. Exécuter les migrations

```bash
docker-compose exec web python manage.py migrate
```

### 5. Créer un superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Accéder à l'application

- **API Root**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## 📚 Documentation API

### Endpoints Produits

```
GET    /api/products/              - Liste des produits
POST   /api/products/              - Créer un produit
GET    /api/products/{id}/         - Détail d'un produit
PUT    /api/products/{id}/         - Modifier un produit
PATCH  /api/products/{id}/         - Modification partielle
DELETE /api/products/{id}/         - Supprimer un produit
POST   /api/products/{id}/upload_image/ - Upload image
```

### Endpoints Fournisseurs

```
GET    /api/suppliers/             - Liste des fournisseurs
POST   /api/suppliers/             - Créer un fournisseur
GET    /api/suppliers/{id}/        - Détail d'un fournisseur
PUT    /api/suppliers/{id}/        - Modifier un fournisseur
DELETE /api/suppliers/{id}/        - Supprimer un fournisseur
GET    /api/suppliers/countries/   - Liste des pays
GET    /api/suppliers/cities/?country=X - Villes par pays
```

## 🔍 Exemples d'utilisation

### Créer un produit

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "code": "PARFUM001",
    "nom_parfum": "Chanel No 5",
    "nom_etiquette": "Chanel",
    "categorie": "Femmes",
    "description": "Parfum classique et élégant",
    "prix": 150.00,
    "stock": 25
  }'
```

### Upload d'une image

```bash
curl -X POST http://localhost:8000/api/products/1/upload_image/ \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/path/to/image.jpg"
```

### Filtrer les produits

```bash
# Par catégorie
GET /api/products/?categorie=Femmes

# Recherche
GET /api/products/?search=Chanel

# Combiné
GET /api/products/?categorie=Hommes&search=sport
```

## 🐳 Commandes Docker utiles

```bash
# Voir les logs
docker-compose logs -f

# Arrêter les conteneurs
docker-compose down

# Reconstruire après changements
docker-compose up --build

# Exécuter des commandes Django
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Accéder au shell Django
docker-compose exec web python manage.py shell

# Accéder à PostgreSQL
docker-compose exec db psql -U parfum_user -d parfum_db
```

## 🌐 Déploiement sur Render

### 1. Préparer le repository

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Sur Render.com

1. Créer un nouveau **Web Service**
2. Connecter votre repository GitHub
3. Configurer :
   - **Build Command**: (Render détectera Dockerfile automatiquement)
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

### 3. Ajouter PostgreSQL

1. Créer une **PostgreSQL Database** sur Render
2. Copier l'URL de connexion interne

### 4. Variables d'environnement sur Render

```
DEBUG=False
SECRET_KEY=<générer-une-clé-secrète>
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<url-postgres-render>
DJANGO_SETTINGS_MODULE=config.settings.production
```

### 5. Après le déploiement

```bash
# Se connecter via le shell Render et exécuter
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 📁 Structure du projet

```
parfum_api/
├── apps/
│   ├── products/       # App gestion produits
│   └── suppliers/      # App gestion fournisseurs
├── config/
│   ├── settings/       # Settings (base, local, production)
│   ├── urls.py         # URLs principales
│   └── wsgi.py
├── media/              # Fichiers uploadés
├── staticfiles/        # Fichiers statiques collectés
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## 🧪 Tests

```bash
# Lancer tous les tests
docker-compose exec web python manage.py test

# Tests d'une app spécifique
docker-compose exec web python manage.py test apps.products
```

## 🔒 Sécurité

- Variables sensibles dans `.env`
- CORS configuré
- Validation des données avec serializers
- Protection CSRF activée
- Headers de sécurité en production

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT.

## 👨‍💻 Auteur

 [VISIONTECH](https://visiontech.vision)

## 🙏 Remerciements

- Django REST Framework
- Docker
- PostgreSQL
- Render.com