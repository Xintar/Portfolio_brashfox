# 🏛️ API Architecture - BrashFox Portfolio

**Data:** 4 listopada 2025  
**Wersja:** 1.0 (po refactoringu Etap 1-6)  
**Status:** Production-ready

---

## 📐 Architektura warstwowa

API zbudowane jest w architekturze warstwowej (Layered Architecture) z czystym podziałem odpowiedzialności:

```
┌─────────────────────────────────────────────┐
│          HTTP Layer (Views)                 │  ← Routing, HTTP, Permissions
├─────────────────────────────────────────────┤
│       Business Logic (Services)             │  ← Logika biznesowa, walidacje
├─────────────────────────────────────────────┤
│      Data Access (Models/Serializers)       │  ← ORM, serialization
├─────────────────────────────────────────────┤
│           Database (PostgreSQL)             │  ← Persistence
└─────────────────────────────────────────────┘
```

---

## 🎯 Warstwy i odpowiedzialności

### 1. **HTTP Layer** (`api/views/`)

**Odpowiedzialność:**
- Routing requestów HTTP
- Walidacja uprawnień (permissions)
- Rate limiting (throttling)
- Wybór serializera (list vs detail)
- Delegowanie do Services

**NIE należy tutaj:**
- ❌ Logika biznesowa (→ Services)
- ❌ Bezpośrednie zapytania DB (→ Services/Models)
- ❌ Skomplikowana walidacja (→ Validators)

**Przykład:**
```python
class BlogPostViewSet(ModelViewSet):
    """Cienka warstwa HTTP - tylko routing"""
    
    def perform_create(self, serializer):
        # Deleguj do serwisu
        BlogPostService.create_post(
            author=self.request.user,
            validated_data=serializer.validated_data
        )
```

---

### 2. **Business Logic Layer** (`api/services/`)

**Odpowiedzialność:**
- Logika biznesowa aplikacji
- Złożone walidacje
- Transakcje bazodanowe
- Integracje zewnętrzne (email, storage)
- Agregacja danych z wielu modeli

**Tutaj powinno być:**
- ✅ Tworzenie zasobów z walidacją
- ✅ Generowanie slug, unikalność
- ✅ Wysyłanie emaili/notyfikacji
- ✅ Złożone queries (JOIN, agregacja)

**Przykład:**
```python
class BlogPostService:
    @staticmethod
    def create_post(author, validated_data):
        """Kompletna logika tworzenia posta"""
        # Auto-slug z zapewnieniem unikalności
        slug = generate_unique_slug(BlogPost, slugify(title))
        
        # Transakcja
        with transaction.atomic():
            post = BlogPost.objects.create(...)
            
        return post
```

---

### 3. **Data Layer** (`api/models/`, `api/serializers/`)

**Models** - Struktura danych:
- Definicje pól
- Relacje (ForeignKey, ManyToMany)
- Meta opcje (ordering, indexes)
- Proste property/metody

**Serializers** - Transformacja danych:
- Walidacja pól
- Nested serialization
- Read-only/Write-only pola
- Custom fields

**Przykład:**
```python
# Model
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    @property
    def excerpt(self):
        return generate_excerpt(self.post)

# Serializer
class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
```

---

### 4. **Utils Layer** (`api/utils/`)

**Odpowiedzialność:**
- Reusable functions
- Validatory
- Helpery
- Stałe
- Custom exceptions

**Organizacja:**
- `constants.py` - Stałe (ALLOWED_FORMATS, MAX_SIZE, THROTTLE_RATES)
- `validators.py` - Funkcje walidacyjne (validate_image_file, validate_slug)
- `helpers.py` - Funkcje pomocnicze (generate_unique_slug, truncate_text)
- `exceptions.py` - Custom wyjątki (BusinessLogicError, FileTooLargeError)

---

## 🔄 Przepływ requestu

### Przykład: Tworzenie posta blogowego

```
1. POST /api/blog-posts/
   ↓
2. BlogPostViewSet.create()
   - Sprawdza permissions (IsAuthenticated)
   - Sprawdza throttling
   ↓
3. BlogPostDetailSerializer.validate()
   - Walidacja pól (title, post)
   - Validators z utils
   ↓
4. BlogPostViewSet.perform_create()
   - Deleguje do BlogPostService
   ↓
5. BlogPostService.create_post()
   - Generuje slug (helpers.generate_unique_slug)
   - Tworzy post w transakcji
   - Zwraca BlogPost instance
   ↓
6. Serializer.data
   - Transformuje model → JSON
   ↓
7. Response (201 Created)
   - Zwraca JSON z utworzonym postem
```

---

## 📦 Moduły API

### **Models** (5 plików, 253 linie)

```
models/
├── photo.py      # FotoDescription, FotoCategory, FotoTags
├── blog.py       # BlogPost, PostCategory
├── comment.py    # PostComments
├── message.py    # Message
└── __init__.py   # Eksporty
```

**Organizacja:** Po domenach biznesowych (photo, blog, comment, message)

---

### **Serializers** (6 plików, 312 linii)

```
serializers/
├── user.py       # UserSerializer, UserCreateSerializer, GroupSerializer
├── photo.py      # FotoDescription (list/detail), FotoCategory, FotoTags
├── blog.py       # BlogPost (list/detail), PostCategory
├── comment.py    # PostComments (nested blog_post)
├── message.py    # Message
└── __init__.py   # Eksporty
```

**Wzorce:**
- List vs Detail serializers (różne pola)
- Nested serialization (author, category)
- Auto-slug w `create()`
- Read-only computed fields

---

### **Views** (6 plików, 309 linii)

```
views/
├── user.py       # UserViewSet (/users/me/), GroupViewSet
├── photo.py      # FotoCategoryViewSet, FotoDescriptionViewSet, FotoTagsViewSet
├── blog.py       # BlogPostViewSet (slug lookup), PostCategoryViewSet
├── comment.py    # PostCommentsViewSet
├── message.py    # MessageViewSet (throttled contact)
└── __init__.py   # Eksporty
```

**Wzorce:**
- ModelViewSet (CRUD)
- Custom actions (@action decorator)
- Dynamic permissions (get_permissions)
- Dynamic throttling (get_throttles)
- Query optimization (select_related, prefetch_related)

---

### **Services** (5 plików, 481 linii)

```
services/
├── user_service.py     # Rejestracja, update, statystyki
├── blog_service.py     # BlogPost + Comment logic
├── photo_service.py    # Walidacja uploadów, queries
├── message_service.py  # Contact form + email
└── __init__.py         # Eksporty
```

**Wzorce:**
- Static methods (stateless)
- Transaction.atomic dla consistency
- Delegowanie do utils (validators, helpers)
- Error handling (ValidationError, custom exceptions)

---

### **Utils** (5 plików, 676 linii)

```
utils/
├── constants.py    # FileUpload, TextValidation, API, Messages
├── validators.py   # validate_image_file, validate_slug, validate_comment_length
├── helpers.py      # generate_unique_slug, truncate_text, get_client_ip
├── exceptions.py   # BusinessLogicError, ResourceNotFoundError, FileTooLargeError
└── __init__.py     # Eksporty
```

**Wzorce:**
- Single Responsibility
- Pure functions (no side effects)
- Clear naming (validate_*, generate_*, format_*)

---

## 🔐 Security Layers

### 1. **Authentication** (JWT)
- Access token: 1h lifetime
- Refresh token: 7 dni
- Header: `Authorization: Bearer <token>`

### 2. **Permissions** (DRF)
- `IsAuthenticatedOrReadOnly` - Odczyt dla wszystkich, zapis dla zalogowanych
- `IsAuthorOrReadOnly` - Edycja tylko dla autora/admina
- `IsAdminOrReadOnly` - Zapis tylko dla adminów
- `IsOwnerOrAdmin` - Tylko właściciel lub admin

### 3. **Throttling** (Rate Limiting)
- Anonymous: 100/hour
- User: 1000/hour
- Registration: 3/hour
- Contact form: 10/hour

### 4. **Validation**
- Serializer validation (DRF)
- Custom validators (utils/validators.py)
- Model validation (Model.clean())
- Business logic validation (Services)

---

## 📊 Optymalizacje

### Query Optimization
```python
# Select related (JOIN)
queryset = BlogPost.objects.select_related('author')

# Prefetch related (oddzielne query)
queryset = FotoDescription.objects.prefetch_related('foto_tags')

# Annotate (agregacja)
queryset = User.objects.annotate(
    blog_posts_count=Count('blogpost')
)
```

### Pagination
- Default: 10 items/page
- Max: 100 items/page
- Types: PageNumberPagination

### Caching (planned)
- Redis cache backend
- Cache dla list views (5 min)
- Cache dla statistics (30 min)

---

## 🧪 Testing Strategy

### Unit Tests
- Services (logika biznesowa)
- Validators (edge cases)
- Helpers (pure functions)

### Integration Tests
- API endpoints (permissions, responses)
- Serializers (nested, validation)

### E2E Tests (planned)
- User flows (register → login → create post)
- File uploads

---

## 📈 Scalability Considerations

### Current
- Modular structure (łatwa rozbudowa)
- Services pattern (reusable logic)
- Utils (DRY)
- Permissions (fine-grained)
- Throttling (ochrona zasobów)

### Future
- [ ] Cache layer (Redis)
- [ ] Celery tasks (async email, image processing)
- [ ] CDN dla media files
- [ ] Database read replicas
- [ ] API versioning (v1, v2)

---

## 🛠️ Developer Guide

### Dodawanie nowego endpointu

1. **Model** (`api/models/{domena}.py`)
```python
class NewModel(models.Model):
    field = models.CharField(max_length=100)
```

2. **Serializer** (`api/serializers/{domena}.py`)
```python
class NewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewModel
        fields = '__all__'
```

3. **Service** (`api/services/{domena}_service.py`)
```python
class NewModelService:
    @staticmethod
    def create_resource(validated_data):
        # Business logic here
        pass
```

4. **ViewSet** (`api/views/{domena}.py`)
```python
class NewModelViewSet(ModelViewSet):
    queryset = NewModel.objects.all()
    serializer_class = NewModelSerializer
```

5. **URL** (`api/urls.py`)
```python
router.register(r'new-models', NewModelViewSet)
```

6. **Test** (`tests/test_{domena}.py`)
```python
def test_create_new_model(api_client):
    # Test logic
    pass
```

---

## 📚 Conventions

### Naming
- Models: PascalCase (BlogPost, FotoDescription)
- Serializers: ModelNameSerializer
- ViewSets: ModelNameViewSet
- Services: ModelNameService
- Files: snake_case.py

### Imports
```python
# Standard library
import os
from datetime import datetime

# Django
from django.db import models

# DRF
from rest_framework import serializers

# Local
from brashfox_app.models import BlogPost
from brashfox_app.api.utils import validate_image_file
```

### Docstrings
```python
def function_name(param1, param2):
    """
    Short description.
    
    Args:
        param1: Description
        param2: Description
        
    Returns:
        Description
        
    Raises:
        ExceptionType: When this happens
    """
    pass
```

---

## 🔗 Related Documents

- **STRUCTURE.md** - Ogólna struktura projektu
- **INTEGRATION.md** - Frontend-Backend integration
- **QUICKSTART.md** - Szybki start dla developerów
- **UTILS_GUIDE.md** - (w przygotowaniu) Przewodnik po utils

---

**Projekt:** BrashFox Portfolio  
**Branch:** zadanie_0.1.1  
**Autor dokumentacji:** GitHub Copilot  
**Status:** Production-ready ✅
