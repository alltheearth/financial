# 🏗️ Estrutura Profissional Django REST Framework

## 📁 Estrutura de Diretórios

```
projeto/
│
├── apps/
│   ├── __init__.py
│   └── users/
│       ├── __init__.py
│       ├── apps.py
│       ├── admin.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── permissions.py
│       ├── managers.py
│       ├── signals.py
│       ├── migrations/
│       │   └── __init__.py
│       └── tests/
│           ├── __init__.py
│           ├── test_models.py
│           ├── test_serializers.py
│           ├── test_views.py
│           └── factories.py
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── production.py
│       └── testing.py
│
├── core/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── permissions.py
│   ├── pagination.py
│   ├── mixins.py
│   └── utils.py
│
├── manage.py
├── pyproject.toml
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 📄 Arquivos de Configuração

### `config/settings/__init__.py`
```python
"""
Carrega configurações baseado no ambiente
"""
import os

ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'testing':
    from .testing import *
else:
    from .development import *
```

### `config/settings/base.py`
```python
"""
Configurações base compartilhadas entre todos os ambientes
"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

# Applications
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

LOCAL_APPS = [
    'apps.users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# CORS
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True
```

### `config/settings/development.py`
```python
"""
Configurações para desenvolvimento
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# BrowsableAPI para desenvolvimento
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]

# Email para console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### `config/settings/production.py`
```python
"""
Configurações para produção
"""
from .base import *

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

---

## 🔐 App Users

### `apps/users/models.py`
```python
"""
Modelos de usuários
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserProfile(models.Model):
    """Perfil estendido do usuário"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - Profile"


# Signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria perfil automaticamente ao criar usuário"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Cria token automaticamente ao criar usuário"""
    if created:
        Token.objects.create(user=instance)
```

### `apps/users/serializers.py`
```python
"""
Serializers para usuários
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil de usuário"""
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'phone', 'birth_date', 'bio', 'avatar',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer completo de usuário"""
    
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_superuser', 'profile'
        ]
        read_only_fields = ['id', 'is_staff', 'is_superuser']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuário"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {"password": "As senhas não coincidem."}
            )
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            raise serializers.ValidationError(
                "Username e password são obrigatórios."
            )
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError(
                "Credenciais inválidas."
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                "Usuário está inativo."
            )
        
        data['user'] = user
        return data
```

### `apps/users/views.py`
```python
"""
Views para usuários
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer,
    UserCreateSerializer, LoginSerializer
)
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para usuários"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Admin vê todos, usuário vê apenas ele mesmo"""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retorna dados do usuário logado"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_profile(self, request, pk=None):
        """Atualiza perfil do usuário"""
        user = self.get_object()
        serializer = UserProfileSerializer(
            user.profile, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Registrar novo usuário"""
    serializer = UserCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Usuário criado com sucesso',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login de usuário"""
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Login realizado com sucesso',
            'token': token.key,
            'user': UserSerializer(user).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout - deleta o token"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Logout realizado com sucesso'})
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
```

### `apps/users/permissions.py`
```python
"""
Permissões customizadas para usuários
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada: apenas o dono pode editar
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj == request.user
```

### `apps/users/urls.py`
```python
"""
URLs do app users
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', include(router.urls)),
]
```

### `apps/users/admin.py`
```python
"""
Admin para usuários
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
```

---

## 🔗 URLs Principal

### `config/urls.py`
```python
"""
URLs principais do projeto
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Painel Administrativo"
admin.site.site_title = "Admin"
admin.site.index_title = "Bem-vindo ao Painel"
```

---

## 🧪 Testes

### `apps/users/tests/factories.py`
```python
"""
Factories para testes
"""
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from apps.users.models import UserProfile


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password('test123')


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile
    
    user = factory.SubFactory(UserFactory)
    phone = factory.Faker('phone_number')
```

---

## 📝 Variáveis de Ambiente

### `.env.example`
```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 🏗️ Criar Estrutura Automaticamente

### Script para criar toda a estrutura de diretórios e arquivos

Crie um arquivo chamado `setup_structure.sh`:

```bash
#!/bin/bash

echo "🏗️  Criando estrutura do projeto Django..."

# Criar diretórios principais
mkdir -p apps/users/{migrations,tests}
mkdir -p config/settings
mkdir -p core
mkdir -p templates
mkdir -p staticfiles
mkdir -p media

# Apps - Users
touch apps/__init__.py
touch apps/users/__init__.py
touch apps/users/apps.py
touch apps/users/admin.py
touch apps/users/models.py
touch apps/users/serializers.py
touch apps/users/views.py
touch apps/users/urls.py
touch apps/users/permissions.py
touch apps/users/managers.py
touch apps/users/signals.py
touch apps/users/migrations/__init__.py

# Tests
touch apps/users/tests/__init__.py
touch apps/users/tests/test_models.py
touch apps/users/tests/test_serializers.py
touch apps/users/tests/test_views.py
touch apps/users/tests/test_permissions.py
touch apps/users/tests/factories.py

# Config
touch config/__init__.py
touch config/asgi.py
touch config/wsgi.py
touch config/urls.py

# Settings
touch config/settings/__init__.py
touch config/settings/base.py
touch config/settings/development.py
touch config/settings/production.py
touch config/settings/testing.py

# Core
touch core/__init__.py
touch core/exceptions.py
touch core/permissions.py
touch core/pagination.py
touch core/mixins.py
touch core/utils.py
touch core/validators.py

# Arquivos raiz
touch manage.py
touch .env
touch .env.example
touch .gitignore
touch README.md
touch pyproject.toml
touch Dockerfile
touch docker-compose.yml
touch pytest.ini
touch conftest.py

echo "✅ Estrutura criada com sucesso!"
echo ""
echo "📁 Estrutura de diretórios:"
tree -L 3 -I '__pycache__|*.pyc'
```

### Como usar:

```bash
# 1. Criar o script
nano setup_structure.sh

# 2. Dar permissão de execução
chmod +x setup_structure.sh

# 3. Executar
./setup_structure.sh
```

### OU use este comando único (copie e cole no terminal):

```bash
mkdir -p apps/users/{migrations,tests} config/settings core templates staticfiles media && \
touch apps/{__init__.py,users/{__init__.py,apps.py,admin.py,models.py,serializers.py,views.py,urls.py,permissions.py,managers.py,signals.py}} && \
touch apps/users/migrations/__init__.py && \
touch apps/users/tests/{__init__.py,test_models.py,test_serializers.py,test_views.py,test_permissions.py,factories.py} && \
touch config/{__init__.py,asgi.py,wsgi.py,urls.py} && \
touch config/settings/{__init__.py,base.py,development.py,production.py,testing.py} && \
touch core/{__init__.py,exceptions.py,permissions.py,pagination.py,mixins.py,utils.py,validators.py} && \
touch manage.py .env .env.example .gitignore README.md pyproject.toml Dockerfile docker-compose.yml pytest.ini conftest.py && \
echo "✅ Estrutura criada com sucesso!"
```

## 🚀 Como Usar

### 1. Instalar dependências
```bash
poetry install
```

### 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

### 3. Rodar migrações
```bash
python manage.py migrate
```

### 4. Criar superusuário
```bash
python manage.py createsuperuser
```

### 5. Rodar servidor
```bash
python manage.py runserver
```

---

## 📚 Endpoints Disponíveis

```
POST   /api/v1/auth/register/        - Registrar usuário
POST   /api/v1/auth/login/           - Login
POST   /api/v1/auth/logout/          - Logout
GET    /api/v1/auth/users/           - Listar usuários
POST   /api/v1/auth/users/           - Criar usuário
GET    /api/v1/auth/users/{id}/      - Detalhes do usuário
PATCH  /api/v1/auth/users/{id}/      - Atualizar usuário
DELETE /api/v1/auth/users/{id}/      - Deletar usuário
GET    /api/v1/auth/users/me/        - Dados do usuário logado
```

---

## ✅ Boas Práticas Implementadas

- ✅ Settings divididos por ambiente
- ✅ Apps organizados em diretório `apps/`
- ✅ Serializers separados por funcionalidade
- ✅ Permissions customizadas
- ✅ Signals para criação automática de perfil e token
- ✅ Testes estruturados com factories
- ✅ Documentação clara
- ✅ Validações robustas
- ✅ Token authentication
- ✅ CORS configurado
- ✅ Admin customizado#   f i n a n c i a l  
 