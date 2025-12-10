#!/bin/bash
# ============================================================================
# 🌸 GUIDE DE DÉMARRAGE RAPIDE - PARFUM API
# ============================================================================
# Ce script contient toutes les commandes nécessaires pour créer et démarrer
# le projet Django REST Framework avec Docker et PostgreSQL
# ============================================================================

# ============================================================================
# ÉTAPE 1 : CRÉATION DE LA STRUCTURE DE BASE
# ============================================================================

echo "📁 Création de la structure du projet..."

# Créer le répertoire principal
mkdir parfum_api
cd parfum_api

# Créer tous les répertoires
mkdir -p config/settings
mkdir -p apps/products
mkdir -p apps/suppliers
mkdir -p core
mkdir -p media/products
mkdir -p staticfiles

# Créer les fichiers __init__.py
touch config/__init__.py
touch config/settings/__init__.py
touch apps/__init__.py
touch apps/products/__init__.py
touch apps/suppliers/__init__.py
touch core/__init__.py

echo "✅ Structure créée"

# ============================================================================
# ÉTAPE 2 : CRÉER LES FICHIERS DE CONFIGURATION
# ============================================================================

echo "📝 Création des fichiers de configuration..."

# --- requirements.txt ---
cat > requirements.txt << 'EOF'
Django==5.0
djangorestframework==3.14.0
django-environ==0.11.2
psycopg2-binary==2.9.9
Pillow==10.1.0
drf-yasg==1.21.7
django-cors-headers==4.3.1
django-filter==23.5
gunicorn==21.2.0
whitenoise==6.6.0
EOF

# --- .env.example ---
cat > .env.example << 'EOF'
DEBUG=True
SECRET_KEY=django-insecure-change-this-key-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DATABASE_URL=postgresql://parfum_user:parfum_pass@db:5432/parfum_db
EOF

# --- .env ---
cp .env.example .env

# --- .gitignore ---
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
venv/
env/
*.log
db.sqlite3
/media/
/staticfiles/
.env
.vscode/
.idea/
.DS_Store
EOF

# --- Dockerfile ---
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/media /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
EOF

# --- docker-compose.yml ---
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: parfum_db
      POSTGRES_USER: parfum_user
      POSTGRES_PASSWORD: parfum_pass
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U parfum_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --reload"
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
  static_volume:
  media_volume:
EOF

echo "✅ Fichiers de configuration créés"

# ============================================================================
# ÉTAPE 3 : INSTALLER DJANGO ET CRÉER LE PROJET
# ============================================================================

echo "🐍 Installation de Django..."

# Option A : Avec environnement virtuel (développement local)
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install django djangorestframework

# Créer le projet Django
django-admin startproject config .

# Créer les apps
python manage.py startapp products apps/products
python manage.py startapp suppliers apps/suppliers

echo "✅ Projet Django créé"

# ============================================================================
# ÉTAPE 4 : AJOUTER LES FICHIERS PYTHON
# ============================================================================

echo "📄 À faire manuellement : Copiez les fichiers suivants..."

cat << 'FILELIST'

Copiez les fichiers Python dans les répertoires appropriés :

1. config/settings/base.py       (settings de base)
2. config/settings/local.py      (settings développement)
3. config/settings/production.py (settings production)
4. config/urls.py                (URLs principales avec Swagger)

5. apps/products/models.py
6. apps/products/serializers.py
7. apps/products/views.py
8. apps/products/urls.py
9. apps/products/admin.py
10. apps/products/apps.py

11. apps/suppliers/models.py
12. apps/suppliers/serializers.py
13. apps/suppliers/views.py
14. apps/suppliers/urls.py
15. apps/suppliers/admin.py
16. apps/suppliers/apps.py

FILELIST

# ============================================================================
# ÉTAPE 5 : DÉMARRER AVEC DOCKER
# ============================================================================

echo ""
echo "🐳 Pour démarrer avec Docker, exécutez :"
echo ""
echo "docker-compose up --build"
echo ""

# ============================================================================
# COMMANDES DOCKER ESSENTIELLES
# ============================================================================

cat << 'DOCKERCOMMANDS'

# ====================================
# 📋 COMMANDES DOCKER ESSENTIELLES
# ====================================

# Démarrer les conteneurs (première fois)
docker-compose up --build

# Démarrer en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f
docker-compose logs -f web  # Logs du service web uniquement

# Arrêter les conteneurs
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Reconstruire après modifications
docker-compose up --build


# ====================================
# 🗄️ COMMANDES DATABASE
# ====================================

# Créer les migrations
docker-compose exec web python manage.py makemigrations

# Appliquer les migrations
docker-compose exec web python manage.py migrate

# Vérifier l'état des migrations
docker-compose exec web python manage.py showmigrations

# Accéder au shell de la base de données
docker-compose exec db psql -U parfum_user -d parfum_db

# Créer un backup de la base
docker-compose exec db pg_dump -U parfum_user parfum_db > backup.sql

# Restaurer un backup
docker-compose exec -T db psql -U parfum_user parfum_db < backup.sql


# ====================================
# 👤 GESTION DES UTILISATEURS
# ====================================

# Créer un superuser
docker-compose exec web python manage.py createsuperuser

# Changer le mot de passe d'un user
docker-compose exec web python manage.py changepassword username


# ====================================
# 🔧 COMMANDES DJANGO UTILES
# ====================================

# Shell Django
docker-compose exec web python manage.py shell

# Shell Python avancé (IPython si installé)
docker-compose exec web python manage.py shell_plus

# Collecter les fichiers statiques
docker-compose exec web python manage.py collectstatic --noinput

# Vérifier les problèmes
docker-compose exec web python manage.py check

# Lancer les tests
docker-compose exec web python manage.py test

# Tests avec coverage
docker-compose exec web python manage.py test --verbosity=2


# ====================================
# 📊 MONITORING & DEBUG
# ====================================

# Voir les conteneurs en cours
docker-compose ps

# Voir l'utilisation des ressources
docker stats

# Inspecter un conteneur
docker-compose exec web env

# Redémarrer un service
docker-compose restart web

# Voir les logs en temps réel avec filtre
docker-compose logs -f --tail=100 web


# ====================================
# 🧹 NETTOYAGE
# ====================================

# Nettoyer les conteneurs arrêtés
docker-compose down

# Supprimer les images inutilisées
docker image prune

# Nettoyage complet du système Docker
docker system prune -a

# Supprimer tous les volumes
docker volume prune

DOCKERCOMMANDS


# ============================================================================
# URLS ET ACCÈS
# ============================================================================

cat << 'URLS'

# ====================================
# 🌐 URLS DE L'APPLICATION
# ====================================

Une fois l'application démarrée, accédez à :

✅ API Root:          http://localhost:8000/api/
✅ Products API:      http://localhost:8000/api/products/
✅ Suppliers API:     http://localhost:8000/api/suppliers/
✅ Admin Django:      http://localhost:8000/admin/
✅ Swagger UI:        http://localhost:8000/swagger/
✅ ReDoc:             http://localhost:8000/redoc/

URLS


# ============================================================================
# TESTS DE L'API
# ============================================================================

cat << 'TESTS'

# ====================================
# 🧪 TESTER L'API
# ====================================

# Test simple
curl http://localhost:8000/api/products/

# Créer un produit
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "code": "TEST001",
    "nom_parfum": "Test Parfum",
    "nom_etiquette": "Test",
    "categorie": "Hommes",
    "prix": 50.00,
    "stock": 10
  }'

# Créer un fournisseur
curl -X POST http://localhost:8000/api/suppliers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Supplier",
    "country": "Cameroun",
    "city": "Douala",
    "whatsapp": "+237600000000",
    "prix": 1000.00,
    "devise": "FCFA"
  }'

TESTS


# ============================================================================
# GIT
# ============================================================================

cat << 'GIT'

# ====================================
# 📦 VERSIONNER AVEC GIT
# ====================================

# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit: Django REST API with Docker"

# Ajouter un remote
git remote add origin https://github.com/votre-username/parfum-api.git

# Push vers GitHub
git branch -M main
git push -u origin main

GIT


# ============================================================================
# DÉPLOIEMENT SUR RENDER
# ============================================================================

cat << 'RENDER'

# ====================================
# 🚀 DÉPLOYER SUR RENDER
# ====================================

1. Créer une base PostgreSQL sur Render :
   - New + → PostgreSQL
   - Nom: parfum-db
   - Plan: Free
   - Copier l'Internal Database URL

2. Créer un Web Service :
   - New + → Web Service
   - Connecter votre repo GitHub
   - Runtime: Docker
   - Plan: Free

3. Variables d'environnement sur Render :
   DEBUG=False
   SECRET_KEY=<générer-une-clé-forte>
   DJANGO_SETTINGS_MODULE=config.settings.production
   ALLOWED_HOSTS=.onrender.com
   DATABASE_URL=<url-postgres-de-render>

4. Après déploiement, dans le Shell Render :
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput

RENDER


# ============================================================================
# RÉSUMÉ DES ÉTAPES
# ============================================================================

cat << 'SUMMARY'

# ═══════════════════════════════════════════════════════════════
# 📋 RÉSUMÉ DES ÉTAPES
# ═══════════════════════════════════════════════════════════════

✅ 1. Créer la structure du projet
✅ 2. Ajouter les fichiers de configuration
✅ 3. Créer le projet Django
✅ 4. Ajouter les fichiers Python (models, views, etc.)
✅ 5. Lancer Docker: docker-compose up --build
✅ 6. Migrations: docker-compose exec web python manage.py migrate
✅ 7. Superuser: docker-compose exec web python manage.py createsuperuser
✅ 8. Tester l'API sur http://localhost:8000/swagger/

# ═══════════════════════════════════════════════════════════════
# 🎉 VOTRE API EST PRÊTE !
# ═══════════════════════════════════════════════════════════════

SUMMARY

echo ""
echo "✨ Setup terminé ! Consultez les sections ci-dessus pour les commandes."
echo ""