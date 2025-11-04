# 📁 Struktura projektu BrashFox Portfolio

**Data aktualizacji:** 4 listopada 2025  
**Status:** Dual-mode architecture (Django Templates + REST API)

---

## 🏗️ Architektura

Projekt działa w **dwóch trybach równocześnie**:

1. **Django Templates (SSR)** - Tradycyjne widoki Django dla SEO i kompatybilności
2. **REST API (SPA)** - Nowoczesne API dla React frontend

---

## 📂 Backend (`/backend/`)

### `brashfox/` - Konfiguracja Django
- `settings.py` - Główna konfiguracja (Django + DRF + JWT + CORS)
- `urls.py` - Routing główny (templates + API)
- `local_settings.py` - Ustawienia lokalne (nie w repo)

### `brashfox_app/` - Główna aplikacja

#### 🔴 LEGACY (Django Templates - SSR)
- **`views.py`** (208 linii) - Widoki dla Django templates
- **`forms.py`** - Formularze Django
- **`templates/`** - Szablony HTML (Jinja2)
- **`admin.py`** - Panel admina Django

#### 🟢 AKTYWNE (REST API)
- **`api/`** - Nowoczesne REST API
  - `views.py` (219 linii) - ViewSets (BlogPost, Photo, Comment, User)
  - `serializers.py` (250 linii) - Serializacja danych (nested)
  - `permissions.py` (72 linii) - Uprawnienia (IsAuthorOrReadOnly, etc.)
  - `throttles.py` (25 linii) - Rate limiting
  - `auth_views.py` (22 linii) - JWT authentication
  - `urls.py` (36 linii) - Routing API

#### 🔵 WSPÓŁDZIELONE
- **`models.py`** (209 linii) - Modele bazy danych
  - `BlogPost` - Posty blogowe
  - `BlogCategory` - Kategorie postów
  - `FotoDescription` - Opisy zdjęć
  - `FotoCategory` - Kategorie zdjęć
  - `PostComments` - Komentarze
  - `Message` - Wiadomości kontaktowe

- **`migrations/`** - Migracje bazy danych
  - Ostatnia: `0010_improve_models.py`

- **`tests/`** - Testy pytest
  - `test_api_permissions.py` - Testy API (16/21 passing)
  - `test_blog.py` - Testy logiki biznesowej
  - `conftest.py` - Fixtures

---

## 📂 Frontend (`/frontend/brushfox-project/`)

### Struktura React (Vite)

```
src/
├── components/          # Komponenty React
│   ├── Layout/         # Layout (Header, Footer, Navigation)
│   ├── Common/         # Wspólne (LoadingSpinner, ErrorMessage)
│   ├── Blog/           # Blog (PostCard, PostList, CommentSection)
│   └── Portfolio/      # Portfolio (PhotoGrid, PhotoCard)
│
├── pages/              # Strony (routing)
│   ├── HomePage.jsx
│   ├── BlogPage.jsx
│   ├── PortfolioPage.jsx
│   ├── AboutPage.jsx
│   ├── ContactPage.jsx
│   ├── LoginPage.jsx
│   ├── RegisterPage.jsx
│   └── PostDetailPage.jsx
│
├── context/            # Context API
│   └── AuthContext.jsx # Zarządzanie autentykacją JWT
│
├── services/           # API services
│   └── api.js          # Axios config + interceptory JWT
│
├── hooks/              # Custom hooks
│   ├── useFetch.js     # Hook do pobierania danych
│   └── useForm.js      # Hook do formularzy
│
├── utils/              # Narzędzia
│   ├── constants.js    # Stałe (API_URL, etc.)
│   └── helpers.js      # Funkcje pomocnicze
│
├── App.jsx             # Główny komponent + routing
└── main.jsx            # Entry point
```

---

## 🔌 Endpointy

### Django Templates (Legacy)
- `http://localhost:8000/` - Strona główna
- `http://localhost:8000/blog/` - Lista postów
- `http://localhost:8000/portfolio/` - Galeria zdjęć
- `http://localhost:8000/contact/` - Formularz kontaktowy
- `http://localhost:8000/login/` - Logowanie
- `http://localhost:8000/register/` - Rejestracja
- `http://localhost:8000/admin/` - Panel admina

### REST API (Aktywne)
- `http://localhost:8000/api/` - API root
- `http://localhost:8000/api/blog-posts/` - Posty (GET, POST)
- `http://localhost:8000/api/blog-posts/{slug}/` - Szczegóły posta (GET, PUT, DELETE)
- `http://localhost:8000/api/blog-posts/{slug}/comments/` - Komentarze do posta
- `http://localhost:8000/api/photos/` - Zdjęcia (GET, POST)
- `http://localhost:8000/api/photos/{id}/` - Szczegóły zdjęcia (GET, PUT, DELETE)
- `http://localhost:8000/api/comments/` - Wszystkie komentarze (GET)
- `http://localhost:8000/api/users/` - Użytkownicy (GET, POST)
- `http://localhost:8000/api/users/me/` - Obecny użytkownik (GET)
- `http://localhost:8000/api/contact/` - Kontakt (POST)
- `http://localhost:8000/api/token/` - Logowanie JWT (POST)
- `http://localhost:8000/api/token/refresh/` - Odświeżenie tokenu (POST)

### Dokumentacja API
- `http://localhost:8000/api/schema/swagger/` - Swagger UI
- `http://localhost:8000/api/schema/redoc/` - ReDoc
- `http://localhost:8000/api/schema/` - OpenAPI schema (JSON)

---

## 🔐 Autentykacja

### Django Templates
- Session-based authentication
- Login/Logout przez formularze Django

### REST API
- **JWT (JSON Web Tokens)**
- Access token: 1 godzina
- Refresh token: 7 dni
- Header: `Authorization: Bearer <token>`

---

## 🗄️ Baza danych

- **PostgreSQL** (produkcja)
- Konfiguracja w `brashfox/local_settings.py` (nie w repo)

---

## 🚀 Uruchomienie

### Backend
```bash
cd backend
source ../.venv/bin/activate
python manage.py runserver
```

### Frontend
```bash
cd frontend/brushfox-project
npm run dev
```

---

## 📊 Metryki

- **Backend:**
  - Pliki Python: ~1040 linii (API) + ~415 linii (legacy)
  - Modele: 5 klas
  - API Endpoints: 12 głównych
  - Testy: 16/21 passing (76%)

- **Frontend:**
  - Komponenty: 50+ plików
  - Strony: 8
  - Custom hooks: 2
  - Context: 1 (Auth)

---

## 🎯 Roadmap

### ✅ Zrobione
- [x] Frontend: Kompletna struktura React
- [x] Backend: REST API z DRF
- [x] Backend: JWT authentication
- [x] Backend: Custom permissions
- [x] Backend: API documentation (Swagger)
- [x] Backend: Testy (76% coverage)
- [x] Weryfikacja: Dual-mode działa

### 🔄 W trakcie (teraz)
- [ ] Integracja frontend z API
- [ ] Podłączenie JWT w React
- [ ] Testy E2E

### 📋 Zaplanowane
- [ ] Optymalizacja: Podzielenie models.py na moduły
- [ ] Optymalizacja: Dodanie cache (Redis)
- [ ] Deployment: Konfiguracja produkcyjna
- [ ] CI/CD: GitHub Actions

---

## 📝 Uwagi dla developerów

1. **Nie usuwaj legacy views** - Są potrzebne dla SEO i backup
2. **API jest głównym interfejsem** - Nowe funkcje tylko przez API
3. **Dual-mode to feature** - Pozwala na stopniową migrację
4. **Testy przed commitem** - `pytest brashfox_app/tests/`
5. **Dokumentacja API** - Automatycznie generowana przez drf-spectacular

---

## 🐛 Znane problemy

- Throttling wymaga cache backend (Redis) - aktualnie uproszczone
- 5/21 testów failuje (blog creation, contact form)
- Frontend nie jest jeszcze podpięty do API

---

## 📞 Kontakt

**Projekt:** BrashFox Portfolio  
**Branch:** zadanie_0.1.1  
**Repo:** Portfolio_brashfox (Xintar)
