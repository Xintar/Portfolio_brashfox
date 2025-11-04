# API Endpoints Documentation

## Zmienione nazwy endpointów (RESTful)

### Przed vs Po

| Stara nazwa | Nowa nazwa | Powód zmiany |
|-------------|------------|--------------|
| `/api/foto_descriptions/` | `/api/photos/` | Prostsze, bardziej zrozumiałe |
| `/api/foto_categories/` | `/api/photo-categories/` | Kebab-case (standard REST) |
| `/api/foto_tags/` | `/api/photo-tags/` | Spójność z photo-categories |
| `/api/posts/` | `/api/blog-posts/` | Wyraźne odróżnienie od postów innych typów |
| `/api/post_comments/` | `/api/comments/` | Proste i zrozumiałe |

---

## Pełna lista endpointów

### 🔐 Authentication

| Method | Endpoint | Opis | Throttle |
|--------|----------|------|----------|
| POST | `/api/token/` | Uzyskaj access + refresh token | 10/hour |
| POST | `/api/token/refresh/` | Odśwież access token | 10/hour |
| POST | `/api/token/verify/` | Sprawdź ważność tokena | - |

**Przykład logowania:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 👤 Users

| Method | Endpoint | Permissions | Throttle | Opis |
|--------|----------|-------------|----------|------|
| GET | `/api/users/` | Authenticated | - | Lista użytkowników |
| POST | `/api/users/` | Anyone | 3/hour | Rejestracja |
| GET | `/api/users/{id}/` | Authenticated | - | Szczegóły użytkownika |
| GET | `/api/users/me/` | Authenticated | - | **Profil zalogowanego** |
| PATCH | `/api/users/{id}/` | Owner/Admin | - | Edycja profilu |
| DELETE | `/api/users/{id}/` | Owner/Admin | - | Usunięcie konta |

**Przykład rejestracji:**
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

**Przykład pobrania własnego profilu:**
```bash
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 📸 Photos (FotoDescription)

| Method | Endpoint | Permissions | Opis |
|--------|----------|-------------|------|
| GET | `/api/photos/` | Anyone | Lista zdjęć (pagination) |
| POST | `/api/photos/` | Authenticated | Dodaj zdjęcie (auto-set author) |
| GET | `/api/photos/{id}/` | Anyone | Szczegóły zdjęcia + tagi |
| PATCH | `/api/photos/{id}/` | Author/Admin | Edycja |
| DELETE | `/api/photos/{id}/` | Author/Admin | Usunięcie |

**Query parameters:**
- `?foto_category=1` - filtruj po kategorii
- `?author=username` - filtruj po autorze
- `?search=nature` - szukaj w nazwie/autorze/wydarzeniu
- `?ordering=-created` - sortuj (created, edited, name)

**Przykład:**
```bash
# Lista zdjęć z kategorii "Portraits"
curl "http://localhost:8000/api/photos/?foto_category=2&ordering=-created"

# Dodanie zdjęcia (autor ustawiany automatycznie)
curl -X POST http://localhost:8000/api/photos/ \
  -H "Authorization: Bearer TOKEN" \
  -F "name=Sunset" \
  -F "image=@sunset.jpg" \
  -F "foto_category=1" \
  -F "event=Summer Festival"
```

---

### 📂 Photo Categories

| Method | Endpoint | Permissions | Opis |
|--------|----------|-------------|------|
| GET | `/api/photo-categories/` | Anyone | Lista kategorii |
| POST | `/api/photo-categories/` | Admin | Dodaj kategorię |
| PATCH | `/api/photo-categories/{id}/` | Admin | Edycja |
| DELETE | `/api/photo-categories/{id}/` | Admin | Usunięcie |

---

### 🏷️ Photo Tags

| Method | Endpoint | Permissions | Opis |
|--------|----------|-------------|------|
| GET | `/api/photo-tags/` | Anyone | Lista tagów |
| POST | `/api/photo-tags/` | Authenticated | Dodaj tag |

**Query parameters:**
- `?search=landscape` - szukaj w tagach
- `?ordering=tags` - sortuj alfabetycznie

---

### 📝 Blog Posts

| Method | Endpoint | Permissions | Opis |
|--------|----------|-------------|------|
| GET | `/api/blog-posts/` | Anyone | Lista postów (pagination) |
| POST | `/api/blog-posts/` | Authenticated | Dodaj post (auto-set author) |
| GET | `/api/blog-posts/{slug}/` | Anyone | Szczegóły posta + autor |
| GET | `/api/blog-posts/{slug}/comments/` | Anyone | **Komentarze do posta** |
| PATCH | `/api/blog-posts/{slug}/` | Author/Admin | Edycja |
| DELETE | `/api/blog-posts/{slug}/` | Author/Admin | Usunięcie |

**⚠️ UWAGA: Używamy SLUG zamiast ID!**

**Query parameters:**
- `?author=1` - filtruj po autorze (ID)
- `?search=django` - szukaj w tytule/treści
- `?ordering=-created` - sortuj (created, edited, title)

**Przykład:**
```bash
# Pobranie posta po slug
curl http://localhost:8000/api/blog-posts/my-first-post/

# Dodanie posta (slug generowany automatycznie z title)
curl -X POST http://localhost:8000/api/blog-posts/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "post": "This is the content..."
  }'
# Slug będzie: "my-first-post"

# Komentarze do posta
curl http://localhost:8000/api/blog-posts/my-first-post/comments/
```

---

### 📂 Post Categories

| Method | Endpoint | Permissions | Opis |
|--------|----------|-------------|------|
| GET | `/api/post-categories/` | Anyone | Lista kategorii |
| POST | `/api/post-categories/` | Admin | Dodaj kategorię |

---

### 💬 Comments

| Method | Endpoint | Permissions | Opis |
|--------|----------|-------------|------|
| GET | `/api/comments/` | Anyone | Lista wszystkich komentarzy |
| POST | `/api/comments/` | Anyone | Dodaj komentarz |
| GET | `/api/comments/{id}/` | Anyone | Szczegóły komentarza |
| PATCH | `/api/comments/{id}/` | Authenticated | Edycja |
| DELETE | `/api/comments/{id}/` | Authenticated | Usunięcie |

**Query parameters:**
- `?blog_post=1` - filtruj po poście (ID)
- `?author=John` - filtruj po autorze (username)
- `?search=great` - szukaj w komentarzach
- `?ordering=-created` - sortuj

**Przykład:**
```bash
# Dodanie komentarza
curl -X POST http://localhost:8000/api/comments/ \
  -H "Content-Type: application/json" \
  -d '{
    "blog_post": 1,
    "author": "John Doe",
    "comment": "Great post!"
  }'
```

---

### ✉️ Contact Messages

| Method | Endpoint | Permissions | Throttle | Opis |
|--------|----------|-------------|----------|------|
| POST | `/api/messages/` | Anyone | 5/hour | Wyślij wiadomość |
| GET | `/api/messages/` | Admin | - | Lista wiadomości |
| GET | `/api/messages/{id}/` | Admin | - | Szczegóły |
| DELETE | `/api/messages/{id}/` | Admin | - | Usunięcie |

**Query parameters:**
- `?email=user@test.com` - filtruj po emailu
- `?topic=Bug` - filtruj po temacie
- `?search=problem` - szukaj w treści
- `?ordering=-created` - sortuj

**Przykład:**
```bash
curl -X POST http://localhost:8000/api/messages/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "topic": "Question",
    "message": "How can I...?"
  }'
```

---

### 👥 Groups

| Method | Endpoint | Permissions | Opis |
|--------|----------|-------------|------|
| GET | `/api/groups/` | Authenticated | Lista grup |
| POST | `/api/groups/` | Authenticated | Dodaj grupę |

---

## 📖 API Documentation

| URL | Opis |
|-----|------|
| `/api/schema/` | OpenAPI 3.0 schema (YAML/JSON) |
| `/api/schema/swagger/` | **Swagger UI** (interaktywna dokumentacja) |
| `/api/schema/redoc/` | ReDoc UI (alternatywna dokumentacja) |

**Zalecane: Swagger UI**
Otwórz w przeglądarce: `http://localhost:8000/api/schema/swagger/`

---

## 🔄 Migracja z frontendu

### Zmień w kodzie React:

**Przed:**
```javascript
// Stare endpointy
axios.get('/api/foto_descriptions/')
axios.get('/api/posts/')
axios.post('/api/post_comments/')
```

**Po:**
```javascript
// Nowe endpointy
axios.get('/api/photos/')
axios.get('/api/blog-posts/')
axios.post('/api/comments/')

// Używaj slug zamiast ID dla postów
axios.get('/api/blog-posts/my-first-post/')  // ✅
axios.get('/api/blog-posts/1/')              // ❌ nie zadziała
```

### Dodaj JWT authentication:

```javascript
// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Dodaj token do każdego requesta
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Automatyczne odświeżanie tokena przy 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) {
        const { data } = await axios.post('/api/token/refresh/', { refresh });
        localStorage.setItem('access_token', data.access);
        error.config.headers.Authorization = `Bearer ${data.access}`;
        return axios(error.config);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

## ⚡ Rate Limiting Summary

| Endpoint | Limit | Opis |
|----------|-------|------|
| Global (anonymous) | 100/hour | Wszystkie requesty niezalogowanych |
| Global (authenticated) | 1000/hour | Wszystkie requesty zalogowanych |
| `/api/token/` | 10/hour | Login attempts |
| `/api/token/refresh/` | 10/hour | Token refresh |
| `/api/users/` (POST) | 3/hour | Rejestracja |
| `/api/messages/` (POST) | 5/hour | Formularz kontaktowy |

---

## 🧪 Testowanie

```bash
# Sprawdź dostępne endpointy
curl http://localhost:8000/api/

# Test paginacji
curl "http://localhost:8000/api/blog-posts/?page=2"

# Test filtrowania
curl "http://localhost:8000/api/photos/?foto_category=1&search=sunset"

# Test autentykacji
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```
