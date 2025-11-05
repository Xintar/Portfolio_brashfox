# 🛠️ Utils Guide - BrashFox Portfolio API

**Data:** 4 listopada 2025  
**Wersja:** 1.0  
**Lokalizacja:** `backend/brashfox_app/api/utils/`

---

## 📚 Wprowadzenie

Moduł `utils` zawiera reusable funkcje, validatory, stałe i wyjątki używane w całej aplikacji. Celem jest **eliminacja duplikacji kodu** i **centralizacja wspólnych wartości**.

---

## 📂 Struktura

```
utils/
├── __init__.py        # Eksport wszystkich utils
├── constants.py       # Stałe aplikacji
├── validators.py      # Custom validatory
├── helpers.py         # Funkcje pomocnicze
└── exceptions.py      # Custom wyjątki
```

---

## 🔢 Constants (`constants.py`)

### Kiedy używać?
- ✅ Wartości używane w wielu miejscach
- ✅ Limity (rozmiar, długość)
- ✅ Formaty plików
- ✅ Komunikaty użytkownika
- ✅ Konfiguracja API (throttling, cache)

### Klasy stałych

#### **FileUpload** - Pliki

```python
from brashfox_app.api.utils import FileUpload

# Formaty
FileUpload.ALLOWED_IMAGE_FORMATS  # ['jpg', 'jpeg', 'png', 'gif', 'webp']

# Limity rozmiaru
FileUpload.MAX_IMAGE_SIZE        # 10 * 1024 * 1024 (10MB)
FileUpload.MAX_AVATAR_SIZE       # 2 * 1024 * 1024 (2MB)

# Wymiary
FileUpload.MAX_IMAGE_WIDTH       # 4000
FileUpload.MAX_IMAGE_HEIGHT      # 4000
FileUpload.THUMBNAIL_SIZE        # (300, 300)
```

**Przykład użycia:**
```python
if file.size > FileUpload.MAX_IMAGE_SIZE:
    raise ValidationError('File too large')
```

---

#### **TextValidation** - Walidacja tekstu

```python
from brashfox_app.api.utils import TextValidation

# Komentarze
TextValidation.MIN_COMMENT_LENGTH    # 10
TextValidation.MAX_COMMENT_LENGTH    # 1000

# Wiadomości (contact form)
TextValidation.MIN_MESSAGE_LENGTH    # 10
TextValidation.MAX_MESSAGE_LENGTH    # 5000

# Posty blogowe
TextValidation.MIN_TITLE_LENGTH      # 5
TextValidation.MAX_TITLE_LENGTH      # 200
TextValidation.MIN_POST_LENGTH       # 50
TextValidation.MAX_POST_LENGTH       # 50000

# Username
TextValidation.MIN_USERNAME_LENGTH   # 3
TextValidation.MAX_USERNAME_LENGTH   # 150
```

**Przykład użycia:**
```python
if len(comment) < TextValidation.MIN_COMMENT_LENGTH:
    raise ValidationError('Comment too short')
```

---

#### **API** - Ustawienia API

```python
from brashfox_app.api.utils import API

# Paginacja
API.DEFAULT_PAGE_SIZE    # 10
API.MAX_PAGE_SIZE        # 100

# Throttle rates
API.ANON_RATE           # '100/hour'
API.USER_RATE           # '1000/hour'
API.REGISTER_RATE       # '3/hour'
API.CONTACT_RATE        # '10/hour'

# Cache timeouts (sekundy)
API.CACHE_SHORT         # 300 (5 minut)
API.CACHE_MEDIUM        # 1800 (30 minut)
API.CACHE_LONG          # 86400 (24 godziny)
```

**Przykład użycia:**
```python
class AnonThrottle(AnonRateThrottle):
    rate = API.ANON_RATE
```

---

#### **Messages** - Komunikaty użytkownika

```python
from brashfox_app.api.utils import Messages

# Success
Messages.SUCCESS_CREATED    # 'Successfully created.'
Messages.SUCCESS_UPDATED    # 'Successfully updated.'
Messages.SUCCESS_DELETED    # 'Successfully deleted.'

# Errors
Messages.ERROR_NOT_FOUND       # 'Resource not found.'
Messages.ERROR_PERMISSION      # 'You do not have permission...'
Messages.ERROR_INVALID_DATA    # 'Invalid data provided.'
Messages.ERROR_FILE_TOO_LARGE  # 'File size exceeds maximum...'
Messages.ERROR_INVALID_FORMAT  # 'Invalid file format.'

# Validation
Messages.VALIDATION_REQUIRED    # 'This field is required.'
Messages.VALIDATION_UNIQUE      # 'This value must be unique.'
Messages.VALIDATION_MIN_LENGTH  # 'Ensure this field has at least {min}...'
Messages.VALIDATION_MAX_LENGTH  # 'Ensure this field has no more than {max}...'
```

**Przykład użycia:**
```python
return Response(
    {'detail': Messages.SUCCESS_CREATED},
    status=status.HTTP_201_CREATED
)
```

---

## ✅ Validators (`validators.py`)

### Kiedy używać?
- ✅ Walidacja w serializers (`validators=[...]`)
- ✅ Walidacja w services (przed save)
- ✅ Custom field validation

### Dostępne validatory

#### **validate_image_file(file)**

Waliduje format i rozmiar pliku obrazu.

```python
from brashfox_app.api.utils import validate_image_file

# W serializer
class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validate_image_file])

# W service
def upload_photo(file):
    validate_image_file(file)  # Rzuca ValidationError jeśli invalid
    # ... dalej
```

**Sprawdza:**
- ✅ Rozmiar ≤ 10MB
- ✅ Format: jpg, jpeg, png, gif, webp

---

#### **validate_avatar_file(file)**

Waliduje avatar (ostrzejsze limity niż obrazy).

```python
from brashfox_app.api.utils import validate_avatar_file

avatar = serializers.ImageField(validators=[validate_avatar_file])
```

**Sprawdza:**
- ✅ Rozmiar ≤ 2MB
- ✅ Format: jpg, jpeg, png, gif, webp

---

#### **validate_slug(value)**

Waliduje format slug (letters, numbers, hyphens, underscores).

```python
from brashfox_app.api.utils import validate_slug

# W modelu
class BlogPost(models.Model):
    slug = models.SlugField(validators=[validate_slug])
```

**Sprawdza:**
- ✅ Tylko: a-z, A-Z, 0-9, -, _

---

#### **validate_username(value)**

Waliduje nazwę użytkownika.

```python
from brashfox_app.api.utils import validate_username

validate_username('john_doe')  # OK
validate_username('ab')        # ValidationError (za krótkie)
```

**Sprawdza:**
- ✅ Długość ≥ 3 znaki
- ✅ Tylko: letters, numbers, @, ., +, -, _

---

#### **validate_comment_length(value)**

Waliduje długość komentarza.

```python
from brashfox_app.api.utils import validate_comment_length

# W service
def create_comment(text):
    validate_comment_length(text)  # 10-1000 znaków
    # ...
```

**Sprawdza:**
- ✅ Długość ≥ 10 znaków
- ✅ Długość ≤ 1000 znaków

---

#### **validate_message_length(value)**

Waliduje długość wiadomości (contact form).

```python
from brashfox_app.api.utils import validate_message_length

validate_message_length(message)  # 10-5000 znaków
```

---

#### **validate_post_title(value)**

Waliduje tytuł posta.

```python
from brashfox_app.api.utils import validate_post_title

validate_post_title(title)  # 5-200 znaków
```

---

## 🔧 Helpers (`helpers.py`)

### Kiedy używać?
- ✅ Funkcje używane w wielu miejscach
- ✅ Formatowanie danych
- ✅ Generowanie wartości

### Dostępne helpery

#### **generate_unique_filename(instance, filename)**

Generuje unikalną nazwę pliku z timestamp i UUID.

```python
from brashfox_app.api.utils import generate_unique_filename

# W modelu
class Photo(models.Model):
    image = models.ImageField(upload_to=generate_unique_filename)

# Wynik: uploads/2024/11/20241104_120530_a1b2c3d4_my-photo.jpg
```

**Zwraca:**
- `uploads/YYYY/MM/timestamp_uuid_safe-name.ext`

---

#### **generate_photo_path(instance, filename)**

Generuje ścieżkę dla zdjęć.

```python
from brashfox_app.api.utils import generate_photo_path

image = models.ImageField(upload_to=generate_photo_path)

# Wynik: photos/2024/11/a1b2c3d4_my-photo.jpg
```

---

#### **truncate_text(text, max_length=200, suffix='...')**

Przycina tekst do określonej długości.

```python
from brashfox_app.api.utils import truncate_text

excerpt = truncate_text(long_text, 100)
# "This is a very long text that will be truncated to 100 characters includi..."
```

**Użycie:**
- Wyciągi z postów
- Preview w listach
- Meta descriptions

---

#### **generate_excerpt(text, max_length=200)**

Generuje wyciąg (cięcie po słowach, nie w środku słowa).

```python
from brashfox_app.api.utils import generate_excerpt

excerpt = generate_excerpt(post.content, 150)
# "This is a very long text that will be truncated at word boundary..."
```

**Różnica vs truncate_text:**
- `truncate_text` - cięcie dokładnie po znaku
- `generate_excerpt` - cięcie po słowie (czytelniejsze)

---

#### **format_file_size(size_bytes)**

Formatuje rozmiar pliku (human-readable).

```python
from brashfox_app.api.utils import format_file_size

format_file_size(1024)           # "1.0 KB"
format_file_size(1024 * 1024)    # "1.0 MB"
format_file_size(1500000)        # "1.4 MB"
```

---

#### **sanitize_filename(filename)**

Czyści nazwę pliku z niebezpiecznych znaków.

```python
from brashfox_app.api.utils import sanitize_filename

sanitize_filename('My Photo!@#$.jpg')  # "my-photo.jpg"
sanitize_filename('Zdjęcie ąćę.PNG')   # "zdjecie-ace.png"
```

---

#### **get_client_ip(request)**

Pobiera IP klienta (uwzględnia proxy).

```python
from brashfox_app.api.utils import get_client_ip

# W view/service
ip = get_client_ip(request)
```

**Użycie:**
- Rate limiting per IP
- Logging
- Geolocation

---

#### **generate_unique_slug(model_class, base_slug, instance_id=None)**

Generuje unikalny slug (dodaje licznik jeśli duplikat).

```python
from brashfox_app.api.utils import generate_unique_slug

# W service
slug = generate_unique_slug(BlogPost, 'my-post')
# Jeśli 'my-post' istnieje → 'my-post-1'
# Jeśli 'my-post-1' istnieje → 'my-post-2'
# itd.
```

**Przykład użycia:**
```python
from django.utils.text import slugify

class BlogPostService:
    @staticmethod
    def create_post(title, ...):
        base_slug = slugify(title)
        slug = generate_unique_slug(BlogPost, base_slug)
        # ...
```

---

## 🚨 Exceptions (`exceptions.py`)

### Kiedy używać?
- ✅ Specyficzne błędy biznesowe
- ✅ Lepsze error messages dla API
- ✅ Właściwe HTTP status codes

### Dostępne wyjątki

#### **BusinessLogicError** (400)

Ogólny błąd logiki biznesowej.

```python
from brashfox_app.api.utils import BusinessLogicError

if user.balance < price:
    raise BusinessLogicError('Insufficient balance')
```

---

#### **ResourceNotFoundError** (404)

Zasób nie znaleziony.

```python
from brashfox_app.api.utils import ResourceNotFoundError

post = BlogPost.objects.filter(slug=slug).first()
if not post:
    raise ResourceNotFoundError(f'Post with slug "{slug}" not found')
```

---

#### **DuplicateResourceError** (409)

Próba utworzenia duplikatu.

```python
from brashfox_app.api.utils import DuplicateResourceError

if User.objects.filter(email=email).exists():
    raise DuplicateResourceError('User with this email already exists')
```

---

#### **InvalidFileError** (400)

Nieprawidłowy plik.

```python
from brashfox_app.api.utils import InvalidFileError

if not file.content_type.startswith('image/'):
    raise InvalidFileError('File must be an image')
```

---

#### **FileTooLargeError** (413)

Plik za duży.

```python
from brashfox_app.api.utils import FileTooLargeError

if file.size > MAX_SIZE:
    raise FileTooLargeError(f'File exceeds {MAX_SIZE} bytes')
```

---

## 📖 Best Practices

### ✅ DO

```python
# Używaj constans zamiast hardcode
from brashfox_app.api.utils import FileUpload

if file.size > FileUpload.MAX_IMAGE_SIZE:  # ✅ Dobrze
    ...
```

```python
# Używaj validatorów w serializers
from brashfox_app.api.utils import validate_image_file

class PhotoSerializer(serializers.ModelSerializer):
    image = ImageField(validators=[validate_image_file])  # ✅ Dobrze
```

```python
# Używaj helpers dla duplikującego się kodu
from brashfox_app.api.utils import generate_excerpt

excerpt = generate_excerpt(post.content)  # ✅ Dobrze
```

### ❌ DON'T

```python
# Nie hardcode wartości
if file.size > 10 * 1024 * 1024:  # ❌ Źle (duplikacja)
    ...
```

```python
# Nie twórz własnych validatorów jeśli istnieje w utils
def my_validate_image(file):  # ❌ Źle (duplikacja)
    if file.size > 10MB:
        ...
```

```python
# Nie używaj generic exceptions
raise Exception('Error')  # ❌ Źle
raise BusinessLogicError('Specific error')  # ✅ Dobrze
```

---

## 🔍 Quick Reference

### Cheat Sheet

```python
# Import wszystkiego
from brashfox_app.api.utils import (
    # Constants
    FileUpload, TextValidation, API, Messages,
    
    # Validators
    validate_image_file, validate_slug, validate_comment_length,
    
    # Helpers
    generate_unique_slug, truncate_text, get_client_ip,
    
    # Exceptions
    BusinessLogicError, ResourceNotFoundError, FileTooLargeError
)

# Lub import modułów
from brashfox_app.api.utils import constants, validators, helpers, exceptions
```

---

## 🧪 Testing Utils

```python
# Test validator
from brashfox_app.api.utils import validate_comment_length
from django.core.exceptions import ValidationError
import pytest

def test_validate_comment_length():
    # Too short
    with pytest.raises(ValidationError):
        validate_comment_length('short')
    
    # OK
    validate_comment_length('This is a valid comment text')
    
    # Too long
    with pytest.raises(ValidationError):
        validate_comment_length('x' * 1001)
```

---

## 📚 Related Documents

- **STRUCTURE.md** - Ogólna struktura projektu
- **API_ARCHITECTURE.md** - Architektura API
- **INTEGRATION.md** - Frontend-Backend integration

---

**Status:** Complete ✅  
**Wersja:** 1.0  
**Data:** 4 listopada 2025
