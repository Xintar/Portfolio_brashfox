# 📁 Project Structure - BrashFox Portfolio (Makeup Artist)

**Updated:** November 4, 2025  
**Status:** Production-ready dual-mode architecture (Django Templates + REST API)  
**Refactoring:** Modular structure (Stages 1-6 completed)

---

## 🏗️ Architecture

Project operates in **two modes simultaneously**:

1. **Django Templates (SSR)** - Traditional Django views for SEO and compatibility
2. **REST API (SPA)** - Modern API for React frontend (makeup portfolio showcase)

### Architecture Principles:
- **Separation of Concerns** - Each layer has its own responsibility
- **DRY** - No code duplication (utils, constants)
- **Modular** - Code split into small, maintainable modules (~40-100 lines/file)
- **Testable** - Business logic in Services, easy to test
- **Scalable** - Ready for growth (cache, throttling, pagination)

---

## 📂 Backend (`/backend/`)

### `brashfox/` - Django Configuration
- `settings.py` - Main configuration (Django + DRF + JWT + CORS)
- `urls.py` - Main routing (templates + API)
- `local_settings.py` - Local settings (not in repo)

### `brashfox_app/` - Main Application

#### 🔴 LEGACY (Django Templates - SSR)
- **`views.py`** (208 lines) - Views for Django templates
- **`forms.py`** - Django forms
- **`templates/`** - HTML templates (Jinja2)
- **`admin.py`** - Django admin panel

#### 🟢 ACTIVE (REST API) - **Modular Structure**

##### **`api/`** - Modern REST API (Production-ready)

```
api/
├── models/              # 🎯 Models (253 lines in 5 files)
│   ├── __init__.py      # Export all models
│   ├── photo.py         # FotoDescription (makeup work), FotoCategory, FotoTags
│   ├── blog.py          # BlogPost, PostCategory (beauty tips & tutorials)
│   ├── comment.py       # PostComments
│   └── message.py       # Message (contact form)
│
├── serializers/         # 🔄 Serializery (312 linii w 6 plikach)
│   ├── __init__.py      # Eksport wszystkich serializerów
│   ├── user.py          # User, UserCreate, Group
│   ├── photo.py         # Photo serializers (list/detail)
│   ├── blog.py          # BlogPost serializers (auto-slug, auto-author)
│   ├── comment.py       # PostComments (nested blog_post)
│   └── message.py       # Message (email validation)
│
├── views/               # 🌐 ViewSety (309 linii w 6 plikach)
│   ├── __init__.py      # Eksport wszystkich ViewSetów
│   ├── user.py          # UserViewSet (/users/me/), GroupViewSet
│   ├── photo.py         # PhotoViewSet (select_related, filtry)
│   ├── blog.py          # BlogPostViewSet (lookup by slug, /comments/)
│   ├── comment.py       # CommentViewSet
│   └── message.py       # MessageViewSet (throttled contact form)
│
├── services/            # 💼 Logika biznesowa (481 linii w 5 plikach)
│   ├── __init__.py      # Eksport wszystkich serwisów
│   ├── user_service.py  # Rejestracja, update, statystyki
│   ├── blog_service.py  # BlogPost + Comment logic
│   ├── photo_service.py # Walidacja uploadów, queries
│   └── message_service.py # Contact form + email notifications
│
├── utils/               # 🛠️ Narzędzia (676 linii w 5 plikach)
│   ├── __init__.py      # Eksport wszystkich utils
│   ├── constants.py     # Stałe (FileUpload, API, TextValidation)
│   ├── validators.py    # Custom validatory (image, slug, comment)
│   ├── helpers.py       # Funkcje pomocnicze (slug, filename, excerpt)
│   └── exceptions.py    # Custom wyjątki (BusinessLogicError, etc.)
│
├── permissions.py       # 🔐 Uprawnienia (72 linie)
├── throttles.py         # ⏱️ Rate limiting (25 linii)
├── auth_views.py        # 🔑 JWT authentication (22 linie)
└── urls.py              # 🗺️ Routing API (36 linii)
```

**Metryki API:**
- **Łącznie:** ~2007 linii w 31 plikach
- **Średnio:** ~65 linii/plik (łatwe w utrzymaniu)
- **Backup pliki:** models_old.py.bak, serializers_old.py.bak, views_old.py.bak

#### 🔵 WSPÓŁDZIELONE
- **`models/`** (5 plików, 253 linie) - **MODUŁOWE** - Modele bazy danych
  - `photo.py` - FotoDescription, FotoCategory, FotoTags
  - `blog.py` - BlogPost, PostCategory
  - `comment.py` - PostComments
  - `message.py` - Message (contact form)
  - `__init__.py` - Eksport wszystkich modeli

- **`migrations/`** - Migracje bazy danych
  - Ostatnia: `0009_postcomments_comment.py`

- **`tests/`** - Testy pytest
  - `test_api_permissions.py` - Testy API (16/21 passing)
  - `test_blog.py` - Testy logiki biznesowej
  - `conftest.py` - Fixtures

---

## 📂 Frontend (`/frontend/brushfox-project/`)

### Struktura React (Vite)

```
src/
├── components/          # React Components
│   ├── Layout/         # Layout (Header, Footer, Navigation)
│   ├── Common/         # Common (LoadingSpinner, ErrorMessage)
│   ├── Blog/           # Blog (PostCard, PostList, CommentSection)
│   └── Portfolio/      # Portfolio (MakeupGrid, MakeupCard, BeforeAfter)
│
├── pages/              # Pages (routing)
│   ├── HomePage.jsx
│   ├── BlogPage.jsx    # Beauty tips & tutorials
│   ├── PortfolioPage.jsx  # Makeup work showcase
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
- `http://localhost:8000/` - Home page
- `http://localhost:8000/blog/` - Blog posts (beauty tips)
- `http://localhost:8000/portfolio/` - Makeup work gallery
- `http://localhost:8000/contact/` - Contact form
- `http://localhost:8000/login/` - Logowanie
- `http://localhost:8000/register/` - Rejestracja
- `http://localhost:8000/admin/` - Panel admina

### REST API (Active)
- `http://localhost:8000/api/` - API root
- `http://localhost:8000/api/blog-posts/` - Posts (GET, POST) - beauty tips & tutorials
- `http://localhost:8000/api/blog-posts/{slug}/` - Post details (GET, PUT, DELETE)
- `http://localhost:8000/api/blog-posts/{slug}/comments/` - Post comments
- `http://localhost:8000/api/photos/` - Makeup work (GET, POST)
- `http://localhost:8000/api/photos/{id}/` - Makeup work details (GET, PUT, DELETE)
- `http://localhost:8000/api/comments/` - All comments (GET)
- `http://localhost:8000/api/users/` - Users (GET, POST)
- `http://localhost:8000/api/users/me/` - Current user (GET)
- `http://localhost:8000/api/contact/` - Contact (POST)
- `http://localhost:8000/api/token/` - JWT Login (POST)
- `http://localhost:8000/api/token/refresh/` - Refresh token (POST)

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
  - **API (modułowe):** 2007 linii w 31 plikach (~65 linii/plik)
    - Models: 253 linie (5 plików)
    - Serializers: 312 linii (6 plików)
    - Views: 309 linii (6 plików)
    - Services: 481 linii (5 plików)
    - Utils: 676 linii (5 plików)
    - Other: 72+25+22+36 = 155 linii (permissions, throttles, auth, urls)
  - **Legacy:** ~415 linii (views, forms, templates)
  - Modele: 5 klas (photo, blog, comment, message, user-related)
  - API Endpoints: 12 głównych + custom actions
  - Testy: 16/21 passing (76%)
  - **Refactoring:** Etap 1-6 zakończone ✅

- **Frontend:**
  - Komponenty: 50+ plików
  - Strony: 8
  - Custom hooks: 2
  - Context: 1 (Auth)
  - **Status:** Zintegrowany z API ✅

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
- [x] **REFACTORING: Etap 1 - Modułowe modele** (5 plików)
- [x] **REFACTORING: Etap 2 - Modułowe serializery** (6 plików)
- [x] **REFACTORING: Etap 3 - Modułowe views** (6 plików)
- [x] **REFACTORING: Etap 4 - Services (logika biznesowa)** (5 plików)
- [x] **REFACTORING: Etap 5 - Utils & Constants** (5 plików)
- [x] **REFACTORING: Etap 6 - Dokumentacja struktury**
- [x] Integracja frontend z API
- [x] Podłączenie JWT w React

### 📋 Zaplanowane
- [ ] Optymalizacja: Dodanie cache (Redis)
- [ ] Deployment: Konfiguracja produkcyjna
- [ ] CI/CD: GitHub Actions
- [ ] Testy E2E (Cypress/Playwright)
- [ ] Pokrycie testów: 76% → 90%+

---

## 📝 Uwagi dla developerów

### Organizacja kodu
1. **Models** (`api/models/`) - Po domenie (photo, blog, comment, message)
2. **Serializers** (`api/serializers/`) - Odpowiadają modelom, auto-slug, nested
3. **Views** (`api/views/`) - Cienkie (routing + walidacja), logika w Services
4. **Services** (`api/services/`) - **TU jest logika biznesowa** (tworzenie, update, queries)
5. **Utils** (`api/utils/`) - Reusable functions (validators, helpers, constants, exceptions)

### Zasady
- **Nie usuwaj legacy views** - Są potrzebne dla SEO i backup
- **API jest głównym interfejsem** - Nowe funkcje tylko przez API
- **Dual-mode to feature** - Pozwala na stopniową migrację
- **Services first** - Nowa logika biznesowa → serwis, potem ViewSet
- **Utils dla duplikacji** - Jeśli kod się powtarza → utils
- **Constants dla wartości** - Nie hardcode, użyj `constants.py`
- **Testy przed commitem** - `pytest brashfox_app/tests/`
- **Dokumentacja API** - Automatycznie generowana przez drf-spectacular

### Gdzie co dodawać?
- **Nowy model** → `api/models/{domena}.py` + update `__init__.py`
- **Nowy endpoint** → `api/views/{domena}.py` + update `api/urls.py`
- **Nowa walidacja** → `api/utils/validators.py`
- **Nowa stała** → `api/utils/constants.py`
- **Logika biznesowa** → `api/services/{domena}_service.py`
- **Helper function** → `api/utils/helpers.py`

### Przykład workflow (dodawanie nowej funkcji):
1. Model → `api/models/`
2. Serializer → `api/serializers/`
3. Service (logika) → `api/services/`
4. ViewSet (routing) → `api/views/`
5. URL → `api/urls.py`
6. Test → `tests/test_{domena}.py`

---

## 🐛 Znane problemy

- ~~Throttling wymaga cache backend (Redis) - aktualnie uproszczone~~ ✅ Działa (in-memory)
- 5/21 testów failuje (blog creation, contact form) - do naprawy
- ~~Frontend nie jest jeszcze podpięty do API~~ ✅ Zintegrowane

---

## 🔗 Dodatkowe dokumenty

- **INTEGRATION.md** - Przewodnik integracji frontend-backend
- **QUICKSTART.md** - Szybki start dla nowych developerów
- **test_integration.sh** - Skrypt testowania wszystkich endpointów
- **API_ARCHITECTURE.md** - (w przygotowaniu) Szczegółowa architektura API
- **UTILS_GUIDE.md** - (w przygotowaniu) Przewodnik po utils

---

## 📞 Kontakt

**Projekt:** BrashFox Portfolio  
**Branch:** zadanie_0.1.1  
**Repo:** Portfolio_brashfox (Xintar)
