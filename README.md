# � BrashFox Portfolio

**Modern full-stack portfolio application for makeup artists and beauty professionals**

[![Django](https://img.shields.io/badge/Django-5.1.5-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.2-red.svg)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-blue.svg)](https://www.postgresql.org/)

---

## 🎯 Overview

BrashFox Portfolio is a **dual-mode application** that combines:
- � **Portfolio Gallery** - Professional makeup work showcase
- 📝 **Blog Platform** - Beauty tips, tutorials, and content management
- 🔐 **User Authentication** - JWT-based secure access
- 📱 **Responsive Design** - Works on all devices
- 🚀 **Modern Stack** - React SPA + Django REST API

---

## ✨ Features

### Makeup Portfolio
- ✅ Gallery with categories (bridal, editorial, special effects, etc.)
- ✅ High-resolution image support (up to 10MB)
- ✅ Work metadata (artist, event, technique, products used)
- ✅ Before/After transformations
- ✅ Tags for styles and techniques
- ✅ Responsive image grid

### Blog Platform
- ✅ Beauty tips and tutorials
- ✅ Product reviews
- ✅ Create, edit, delete blog posts
- ✅ Auto-generated slugs for SEO
- ✅ Comment system
- ✅ Author profiles with statistics
- ✅ Categories and filtering

### Security & Performance
- ✅ JWT authentication (1h access, 7d refresh)
- ✅ Role-based permissions (Author, Admin)
- ✅ Rate limiting (throttling)
- ✅ Query optimization (select_related, prefetch_related)
- ✅ API documentation (Swagger, ReDoc)

---

## 🏗️ Architecture

**Dual-mode architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                     BrashFox Portfolio                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🌐 Frontend (React SPA)        🔧 Backend (Django API)    │
│  ├─ React 18.2                  ├─ Django 5.1.5            │
│  ├─ Vite build                  ├─ Django REST Framework   │
│  ├─ React Router                ├─ JWT Authentication      │
│  ├─ Axios (API client)          ├─ PostgreSQL Database     │
│  └─ Context API (state)         └─ Modular structure       │
│                                                             │
│  Port: 5173                     Port: 8000                 │
└─────────────────────────────────────────────────────────────┘
```

**Backend Structure (Modular):**
- 📦 `models/` - Database schema (5 files, 253 lines)
- 🔄 `serializers/` - Data transformation (6 files, 312 lines)
- 🌐 `views/` - HTTP routing (6 files, 309 lines)
- 💼 `services/` - Business logic (5 files, 481 lines)
- 🛠️ `utils/` - Reusable tools (5 files, 676 lines)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Xintar/Portfolio_brashfox.git
cd Portfolio_brashfox

# 2. Backend setup
cd backend
python -m venv ../.venv
source ../.venv/bin/activate  # Windows: ..\.venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure database
cp brashfox/local_settings.py.example brashfox/local_settings.py
# Edit local_settings.py with your PostgreSQL credentials

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Start backend
python manage.py runserver
# Backend running at http://localhost:8000

# 7. Frontend setup (new terminal)
cd ../frontend/brushfox-project
npm install
npm run dev
# Frontend running at http://localhost:5173
```

### Access Points

- **Frontend (React):** http://localhost:5173
- **Backend (Django):** http://localhost:8000
- **API Root:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/
- **Swagger Docs:** http://localhost:8000/api/schema/swagger/
- **ReDoc:** http://localhost:8000/api/schema/redoc/

---

## 📚 Documentation

Comprehensive documentation in [`docs/`](./docs/) folder:

| Document | Description |
|----------|-------------|
| [**QUICKSTART.md**](./docs/QUICKSTART.md) | 🚀 Quick start guide for developers |
| [**STRUCTURE.md**](./docs/STRUCTURE.md) | 📁 Complete project structure |
| [**API_ARCHITECTURE.md**](./docs/API_ARCHITECTURE.md) | 🏛️ API design patterns & layers |
| [**UTILS_GUIDE.md**](./docs/UTILS_GUIDE.md) | 🛠️ Utils reference guide |
| [**INTEGRATION.md**](./docs/INTEGRATION.md) | 🔗 Frontend-Backend integration |
| [**PROJECT_DIAGRAM.md**](./docs/PROJECT_DIAGRAM.md) | 📊 Architecture diagrams |
| [**PODSUMOWANIE_MODERNIZACJI.md**](./docs/PODSUMOWANIE_MODERNIZACJI.md) | 📝 Modernization summary (PL) |
| [**test_integration.sh**](./docs/test_integration.sh) | 🧪 API integration test script |

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 5.1.5
- **API:** Django REST Framework 3.15.2
- **Auth:** djangorestframework-simplejwt
- **Database:** PostgreSQL (psycopg2)
- **API Docs:** drf-spectacular (Swagger/OpenAPI)
- **CORS:** django-cors-headers
- **Images:** Pillow
- **Filtering:** django-filter

### Frontend
- **Framework:** React 18.2
- **Build Tool:** Vite
- **Routing:** React Router DOM 6
- **HTTP Client:** Axios
- **State:** Context API
- **Styling:** CSS Modules
- **Notifications:** React Toastify

### Testing
- **Backend:** pytest, pytest-django
- **Coverage:** 76% (16/21 tests passing)

---

## 📊 Project Stats

- **Backend Code:** 2,186 lines in 31 files
  - Models: 253 lines (5 files)
  - Serializers: 312 lines (6 files)
  - Views: 309 lines (6 files)
  - Services: 481 lines (5 files)
  - Utils: 676 lines (5 files)
  - Avg: 71 lines/file ✅

- **Frontend Code:** 50+ components, 8 pages
- **Documentation:** 76KB in 8 files
- **Test Coverage:** 76%

---

## 🔐 Security Features

- ✅ JWT token authentication
- ✅ Password hashing (Django PBKDF2)
- ✅ CORS protection
- ✅ Rate limiting (throttling)
- ✅ Permission classes (IsAuthorOrReadOnly, IsAdminOrReadOnly)
- ✅ Input validation (serializers + custom validators)
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection (React escaping)

---

## 📝 API Endpoints

### Authentication
- `POST /api/token/` - Login (get JWT tokens)
- `POST /api/token/refresh/` - Refresh access token
- `GET /api/users/me/` - Current user profile

### Blog
- `GET /api/blog-posts/` - List posts (paginated)
- `POST /api/blog-posts/` - Create post (auth required)
- `GET /api/blog-posts/{slug}/` - Post details
- `PUT /api/blog-posts/{slug}/` - Update post (author/admin)
- `DELETE /api/blog-posts/{slug}/` - Delete post (author/admin)
- `GET /api/blog-posts/{slug}/comments/` - Post comments

### Makeup Portfolio
- `GET /api/photos/` - List makeup work (paginated)
- `POST /api/photos/` - Upload makeup work (auth required)
- `GET /api/photos/{id}/` - Work details
- `PUT /api/photos/{id}/` - Update work (author/admin)
- `DELETE /api/photos/{id}/` - Delete work (author/admin)

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create comment (auth required)
- `DELETE /api/comments/{id}/` - Delete comment (author/admin)

### Contact
- `POST /api/messages/` - Send contact message (throttled)

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=brashfox_app

# Run specific test file
pytest brashfox_app/tests/test_api_permissions.py

# Integration tests (API endpoints)
cd docs
./test_integration.sh
```

---

## 🌍 Environment Variables

Create `backend/brashfox/local_settings.py`:

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'brashfox_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Security
SECRET_KEY = 'your-secret-key-here'
DEBUG = True  # False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Email (optional)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## 🚢 Deployment

*Coming soon: Docker, nginx, gunicorn configuration*

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is for educational purposes.

---

## 👤 Author

**Xintar**
- GitHub: [@Xintar](https://github.com/Xintar)
- Project: [Portfolio_brashfox](https://github.com/Xintar/Portfolio_brashfox)

---

## 🎯 Roadmap

### ✅ Completed
- [x] Modular backend architecture (6 refactoring stages)
- [x] JWT authentication
- [x] React frontend with routing
- [x] API documentation (Swagger)
- [x] Frontend-Backend integration
- [x] Comprehensive documentation

### 📋 Planned
- [ ] Redis cache implementation
- [ ] Celery for async tasks
- [ ] Docker deployment
- [ ] CI/CD (GitHub Actions)
- [ ] S3 for media files
- [ ] Test coverage 90%+
- [ ] i18n (internationalization)

---

## 🙏 Acknowledgments

- Django & Django REST Framework communities
- React community
- All contributors and testers

---

**Status:** ✅ Production-ready  
**Version:** 1.0  
**Branch:** zadanie_0.1.1  
**Last Updated:** November 4, 2025
