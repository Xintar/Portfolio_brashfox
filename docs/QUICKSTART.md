# 🚀 Quick Start - BrashFox Portfolio

Quick guide for launching the makeup artist portfolio project with integrated Frontend-Backend.

---

## ⚡ Szybkie uruchomienie (TL;DR)

```bash
# Terminal 1 - Backend
cd backend
source ../.venv/bin/activate
python manage.py runserver

# Terminal 2 - Frontend  
cd frontend/brushfox-project
npm run dev
```

**Gotowe!** Otwórz: http://localhost:5173

---

## 📋 Szczegółowe kroki

### 1️⃣ Wymagania
- Python 3.10+
- Node.js 18+
- PostgreSQL (z konfiguracją w `backend/brashfox/local_settings.py`)
- virtualenv

### 2️⃣ Backend Setup (jednorazowo)

```bash
# Przejdź do folderu projektu
cd "Blok 3/Projekt_koncowy"

# Aktywuj wirtualne środowisko
source .venv/bin/activate

# Przejdź do backend
cd backend

# Zainstaluj zależności (jeśli jeszcze nie)
pip install -r requirements.txt

# Wykonaj migracje
python manage.py migrate

# Utwórz superusera (opcjonalne)
python manage.py createsuperuser

# Uruchom serwer
python manage.py runserver
```

**Backend dostępny na:** http://localhost:8000

### 3️⃣ Frontend Setup (jednorazowo)

```bash
# W nowym terminalu
cd "Blok 3/Projekt_koncowy/frontend/brushfox-project"

# Zainstaluj zależności (jeśli jeszcze nie)
npm install

# Uruchom dev server
npm run dev
```

**Frontend dostępny na:** http://localhost:5173

---

## 🧪 Weryfikacja

### Automatyczny test
```bash
cd "Blok 3/Projekt_koncowy"
bash test_integration.sh
```

### Manualny test
1. **Backend API:**
   ```bash
   curl http://localhost:8000/api/blog-posts/
   ```
   Powinno zwrócić JSON z listą postów

2. **Frontend:**
   - Otwórz http://localhost:5173
   - Przejdź do `/blog`
   - Sprawdź czy posty się ładują

3. **Swagger Docs:**
   - Otwórz http://localhost:8000/api/schema/swagger/
   - Eksploruj API

---

## 🔐 Logowanie

### Przez frontend (http://localhost:5173/login)
- Username: `marta` (lub twój superuser)
- Password: (twoje hasło)

### Przez API
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "marta", "password": "hasło"}'
```

Otrzymasz:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 📁 Ważne pliki

### Konfiguracja
- `backend/brashfox/settings.py` - Główna konfiguracja Django
- `backend/brashfox/local_settings.py` - **Lokalna konfiguracja DB (nie w repo!)**
- `frontend/brushfox-project/.env` - Zmienne środowiskowe (API_URL)

### Dokumentacja
- `STRUCTURE.md` - Architektura projektu
- `INTEGRATION.md` - Przewodnik integracji + testy
- `README.md` - Ogólne info o projekcie

### API
- Backend: `/backend/brashfox_app/api/`
- Routing: `/backend/brashfox_app/api/urls.py`
- Dokumentacja: http://localhost:8000/api/schema/swagger/

---

## 🌐 Główne URL-e

### Frontend (React SPA)
- Home: http://localhost:5173/
- Blog: http://localhost:5173/blog
- Portfolio: http://localhost:5173/portfolio
- Contact: http://localhost:5173/contact
- Login: http://localhost:5173/login

### Backend (Django + API)
- Django Admin: http://localhost:8000/admin/
- API Root: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/api/schema/swagger/
- ReDoc: http://localhost:8000/api/schema/redoc/

### Legacy (Django Templates)
- Home: http://localhost:8000/
- Blog: http://localhost:8000/blog/
- Portfolio: http://localhost:8000/portfolio/

---

## 🆘 Troubleshooting

### Backend nie startuje
```bash
# Sprawdź czy port 8000 jest wolny
lsof -ti:8000 | xargs kill -9

# Sprawdź migracje
cd backend
python manage.py showmigrations

# Sprawdź konfigurację
python manage.py check
```

### Frontend nie startuje
```bash
# Sprawdź czy port 5173 jest wolny
lsof -ti:5173 | xargs kill -9

# Reinstaluj zależności
cd frontend/brushfox-project
rm -rf node_modules package-lock.json
npm install
```

### CORS errors
Sprawdź `backend/brashfox/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
```

### JWT token issues
Wyczyść localStorage w przeglądarce:
```javascript
// DevTools Console
localStorage.clear();
```

---

## 📊 Status projektu

✅ **Zakończone:**
- Frontend: Kompletna struktura React + Vite
- Backend: REST API z DRF + JWT auth
- Integracja: API endpoints podłączone
- Dokumentacja: 3 pliki MD + Swagger
- Testy: 16/21 passing (76%)

🔄 **Do zrobienia:**
- Sekcja komentarzy w BlogPostDetail
- Edycja postów/zdjęć
- Profile użytkownika
- Paginacja UI (Next/Previous buttons)
- Upload zdjęć z preview

---

## 🎯 Pierwsze kroki po uruchomieniu

1. **Zaloguj się** - http://localhost:5173/login
2. **Sprawdź blog** - http://localhost:5173/blog
3. **Zobacz portfolio** - http://localhost:5173/portfolio  
4. **Przetestuj API** - http://localhost:8000/api/schema/swagger/
5. **Sprawdź strukturę** - Przeczytaj `STRUCTURE.md`

---

## 🎉 Gotowe!

Projekt działa w trybie dual-mode:
- **React SPA** (nowoczesny) - port 5173
- **Django Templates** (legacy) - port 8000

Możesz używać obu równocześnie lub skupić się na React.

**Miłego kodowania! 🦊**
