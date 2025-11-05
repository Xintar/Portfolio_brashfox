# Frontend Migration Guide - New API Endpoints

## ⚠️ Zmiany w endpointach API

### 1. Nazwy endpointów

| Stary | Nowy | Akcja |
|-------|------|-------|
| `/api/foto_descriptions/` | `/api/photos/` | Zmień wszystkie odwołania |
| `/api/foto_categories/` | `/api/photo-categories/` | Zmień wszystkie odwołania |
| `/api/foto_tags/` | `/api/photo-tags/` | Zmień wszystkie odwołania |
| `/api/posts/` | `/api/blog-posts/` | Zmień wszystkie odwołania |
| `/api/post_comments/` | `/api/comments/` | Zmień wszystkie odwołania |

### 2. Lookup po slug zamiast ID

**BlogPost używa teraz SLUG:**

```javascript
// ❌ STARE - nie zadziała
axios.get(`/api/blog-posts/${postId}/`)

// ✅ NOWE - używaj slug
axios.get(`/api/blog-posts/${postSlug}/`)

// Przykład:
axios.get(`/api/blog-posts/my-first-post/`)
```

**Slug generowany automatycznie:**
```javascript
// ❌ NIE musisz przesyłać slug
const data = {
  title: "My First Post",
  post: "Content...",
  slug: "my-first-post"  // ❌ Backend wygeneruje automatycznie
}

// ✅ Backend sam wygeneruje slug z title
const data = {
  title: "My First Post",
  post: "Content..."
}
```

### 3. Automatyczne ustawianie autora

**BlogPost i Photo:**

```javascript
// ❌ NIE musisz przesyłać author
const data = {
  title: "My Post",
  post: "Content...",
  author: userId  // ❌ Backend ustawi automatycznie
}

// ✅ Backend sam ustawi author na podstawie tokena JWT
const data = {
  title: "My Post",
  post: "Content..."
}
```

### 4. Nowy endpoint /users/me/

```javascript
// ✅ Pobierz profil zalogowanego użytkownika
const response = await axios.get('/api/users/me/', {
  headers: { Authorization: `Bearer ${accessToken}` }
});

// Zamiast:
const userId = getCurrentUserId();
const response = await axios.get(`/api/users/${userId}/`);
```

### 5. Komentarze do posta

```javascript
// ✅ Nowy endpoint - komentarze dla konkretnego posta
const comments = await axios.get(`/api/blog-posts/${slug}/comments/`);

// Lub nadal można:
const comments = await axios.get(`/api/comments/?blog_post=${postId}`);
```

---

## 🔐 JWT Authentication Flow

### Login
```javascript
const login = async (username, password) => {
  const response = await axios.post('/api/token/', {
    username,
    password
  });
  
  localStorage.setItem('access_token', response.data.access);
  localStorage.setItem('refresh_token', response.data.refresh);
  
  return response.data;
};
```

### Authenticated Requests
```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Token Refresh (gdy access wygaśnie)
```javascript
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('/api/token/refresh/', {
          refresh: refreshToken
        });
        
        localStorage.setItem('access_token', response.data.access);
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh token też wygasł - wyloguj użytkownika
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);
```

---

## 📝 Przykłady użycia

### Portfolio (Photos)

```javascript
// Lista zdjęć z filtrowaniem
const fetchPhotos = async (category = null) => {
  const params = category ? { foto_category: category } : {};
  const response = await api.get('/api/photos/', { params });
  return response.data.results;
};

// Szczegóły zdjęcia
const fetchPhotoDetail = async (id) => {
  const response = await api.get(`/api/photos/${id}/`);
  return response.data;
};

// Dodanie zdjęcia (wymaga auth)
const addPhoto = async (photoData) => {
  const formData = new FormData();
  formData.append('name', photoData.name);
  formData.append('image', photoData.file);
  formData.append('foto_category', photoData.category);
  formData.append('event', photoData.event);
  // NIE dodawaj 'author' - backend ustawi automatycznie
  
  const response = await api.post('/api/photos/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};
```

### Blog

```javascript
// Lista postów
const fetchBlogPosts = async (page = 1) => {
  const response = await api.get('/api/blog-posts/', {
    params: { page, ordering: '-created' }
  });
  return response.data;
};

// Szczegóły posta (używaj SLUG!)
const fetchPostDetail = async (slug) => {
  const response = await api.get(`/api/blog-posts/${slug}/`);
  return response.data;
};

// Dodanie posta (wymaga auth)
const createPost = async (postData) => {
  const response = await api.post('/api/blog-posts/', {
    title: postData.title,
    post: postData.content
    // NIE dodawaj 'slug' - wygeneruje się z title
    // NIE dodawaj 'author' - ustawi się automatycznie
  });
  return response.data;
};

// Edycja posta (używaj SLUG!)
const updatePost = async (slug, postData) => {
  const response = await api.patch(`/api/blog-posts/${slug}/`, postData);
  return response.data;
};

// Usunięcie posta (używaj SLUG!)
const deletePost = async (slug) => {
  await api.delete(`/api/blog-posts/${slug}/`);
};

// Komentarze do posta
const fetchPostComments = async (slug) => {
  const response = await api.get(`/api/blog-posts/${slug}/comments/`);
  return response.data;
};
```

### Comments

```javascript
// Dodanie komentarza (nie wymaga auth)
const addComment = async (postId, author, comment) => {
  const response = await api.post('/api/comments/', {
    blog_post: postId,
    author: author,
    comment: comment
  });
  return response.data;
};

// Lista komentarzy dla posta
const fetchComments = async (postId) => {
  const response = await api.get('/api/comments/', {
    params: { blog_post: postId, ordering: '-created' }
  });
  return response.data.results;
};
```

### Contact Form

```javascript
// Wysłanie wiadomości (nie wymaga auth, ale rate limit 5/h)
const sendMessage = async (messageData) => {
  try {
    const response = await api.post('/api/messages/', {
      name: messageData.name,
      email: messageData.email,
      topic: messageData.topic,
      message: messageData.message
    });
    return response.data;
  } catch (error) {
    if (error.response?.status === 429) {
      throw new Error('Too many messages. Please try again later.');
    }
    throw error;
  }
};
```

### User Profile

```javascript
// Pobranie własnego profilu
const getMyProfile = async () => {
  const response = await api.get('/api/users/me/');
  return response.data;
};

// Rejestracja (rate limit 3/h)
const register = async (userData) => {
  try {
    const response = await axios.post('/api/users/', {
      username: userData.username,
      email: userData.email,
      password: userData.password
    });
    return response.data;
  } catch (error) {
    if (error.response?.status === 429) {
      throw new Error('Too many registration attempts. Please try again later.');
    }
    throw error;
  }
};
```

---

## ⚡ Rate Limiting - Obsługa błędów

```javascript
// Globalna obsługa 429 Too Many Requests
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 429) {
      alert('Too many requests. Please slow down and try again later.');
    }
    return Promise.reject(error);
  }
);
```

---

## 🔍 Search & Filtering

### Wyszukiwanie
```javascript
// Szukaj w postach
const searchPosts = async (query) => {
  const response = await api.get('/api/blog-posts/', {
    params: { search: query }
  });
  return response.data.results;
};

// Szukaj w zdjęciach
const searchPhotos = async (query) => {
  const response = await api.get('/api/photos/', {
    params: { search: query }
  });
  return response.data.results;
};
```

### Filtrowanie
```javascript
// Posty konkretnego autora
const fetchUserPosts = async (authorId) => {
  const response = await api.get('/api/blog-posts/', {
    params: { author: authorId }
  });
  return response.data.results;
};

// Zdjęcia z kategorii
const fetchPhotosByCategory = async (categoryId) => {
  const response = await api.get('/api/photos/', {
    params: { foto_category: categoryId }
  });
  return response.data.results;
};
```

### Sortowanie
```javascript
// Najnowsze posty
const fetchLatestPosts = await api.get('/api/blog-posts/', {
  params: { ordering: '-created' }
});

// Najstarsze posty
const fetchOldestPosts = await api.get('/api/blog-posts/', {
  params: { ordering: 'created' }
});

// Alfabetycznie po tytule
const fetchPostsByTitle = await api.get('/api/blog-posts/', {
  params: { ordering: 'title' }
});
```

---

## ✅ Checklist migracji

- [ ] Zmień wszystkie `/api/foto_descriptions/` → `/api/photos/`
- [ ] Zmień wszystkie `/api/foto_categories/` → `/api/photo-categories/`
- [ ] Zmień wszystkie `/api/posts/` → `/api/blog-posts/`
- [ ] Zmień wszystkie `/api/post_comments/` → `/api/comments/`
- [ ] Używaj **slug** zamiast ID dla BlogPost
- [ ] Usuń przesyłanie `author` przy tworzeniu postów/zdjęć
- [ ] Usuń przesyłanie `slug` przy tworzeniu postów
- [ ] Dodaj interceptor JWT do axios
- [ ] Zaimplementuj auto-refresh tokena
- [ ] Obsłuż błędy 429 (rate limiting)
- [ ] Użyj `/api/users/me/` dla profilu użytkownika
- [ ] Testuj z `http://localhost:8000/api/schema/swagger/`
