# BrashFox Portfolio Frontend

Nowoczesna aplikacja React do zarządzania portfolio fotograficznym i blogiem.

## 🚀 Funkcjonalności

- ✅ **Responsywny design** - działa na wszystkich urządzeniach
- ✅ **Routing** - React Router dla nawigacji SPA
- ✅ **Autentykacja** - Context API dla zarządzania użytkownikami
- ✅ **Blog** - Przeglądanie, tworzenie i zarządzanie postami
- ✅ **Portfolio** - Galeria zdjęć z możliwością dodawania nowych
- ✅ **Formularze** - Walidacja i obsługa błędów
- ✅ **Powiadomienia** - React Toastify dla informacji zwrotnych
- ✅ **Custom Hooks** - Wielokrotnego użytku logika (useFetch, useForm)
- ✅ **Modern UI** - Czyste, profesjonalne style CSS

## 📁 Struktura projektu

```
src/
├── components/          # Komponenty wielokrotnego użytku
│   ├── Layout/         # Header, Footer, Layout
│   ├── Common/         # Button, Loading, ErrorMessage
│   ├── Blog/           # Komponenty bloga
│   ├── Portfolio/      # Komponenty galerii
│   └── Contact/        # Formularz kontaktowy
├── pages/              # Główne strony aplikacji
│   ├── Home.jsx
│   ├── Blog.jsx
│   ├── BlogPostDetail.jsx
│   ├── Portfolio.jsx
│   ├── Contact.jsx
│   ├── About.jsx
│   └── Login.jsx
├── services/           # API i zewnętrzne serwisy
│   └── api.js
├── hooks/              # Custom React hooks
│   ├── useFetch.jsx
│   └── useForm.jsx
├── context/            # Context API
│   └── AuthContext.jsx
├── utils/              # Funkcje pomocnicze
│   ├── constants.js
│   └── helpers.js
├── App.jsx             # Główny komponent z routingiem
└── main.jsx            # Entry point
```

## 🛠️ Instalacja

```bash
# Zainstaluj zależności
npm install

# Skopiuj plik środowiskowy
cp .env.example .env

# Edytuj .env i ustaw URL API
VITE_API_URL=http://localhost:8000/api
```

## 🎯 Uruchomienie

```bash
# Development server
npm run dev

# Build dla produkcji
npm run build

# Preview produkcyjnego buildu
npm run preview
```

## 🔌 Integracja z Backend

Aplikacja wymaga działającego Django backend API. Upewnij się że:

1. Backend Django działa na porcie 8000
2. CORS jest poprawnie skonfigurowany
3. Wszystkie endpointy API są dostępne

W produkcji frontend i API powinny być dostępne przez HTTPS. Przed budowaniem
ustaw `VITE_API_URL` i `VITE_MEDIA_URL` na adresy `https://...`, jeśli backend
działa pod inną domeną. Gdy frontend i backend współdzielą domenę, domyślny
adres API to względne `/api`. Po stronie Django ustaw domenę frontendu w
`DJANGO_CORS_ALLOWED_ORIGINS` i `DJANGO_CSRF_TRUSTED_ORIGINS`.

## 📝 Endpointy API

- `/api/posts/` - Lista i tworzenie postów
- `/api/posts/:slug/` - Szczegóły posta
- `/api/fotos/` - Lista i upload zdjęć
- `/api/fotos/:id/` - Szczegóły zdjęcia
- `/api/messages/` - Wiadomości kontaktowe
- `/api/users/` - Użytkownicy
- `/api-auth/login/` - Logowanie
- `/api-auth/logout/` - Wylogowanie

## 🎨 Dostosowywanie

### Kolory
Główne kolory można zmienić w plikach CSS. Domyślny kolor accent: `#646cff`

### Layout
Maksymalna szerokość kontenera: `1200px` (można zmienić w `Layout.css`)

## 📦 Zależności

- React 18.2
- React Router DOM
- React Toastify
- Axios
- Vite

## 🐛 Znane problemy

- ESLint warnings dotyczące prop-types można zignorować lub dodać prop-types library
- Niektóre API endpointy mogą wymagać dostosowania do specyfiki backendu

## 📄 Licencja

Projekt edukacyjny - Portfolio BrashFox
