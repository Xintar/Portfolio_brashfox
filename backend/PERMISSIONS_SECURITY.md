# API Permissions & Security

## Custom Permission Classes

Plik: `brashfox_app/api/permissions.py`

### IsAuthorOrReadOnly
- **Zastosowanie**: BlogPost, FotoDescription
- **Zachowanie**:
  - Czytanie (GET, HEAD, OPTIONS): wszyscy
  - Edycja/Usuwanie (PUT, PATCH, DELETE): tylko autor obiektu
- **Sprawdza**: `obj.author == request.user`

### IsOwnerOrReadOnly
- **Zastosowanie**: Modele z polem `user` zamiast `author`
- **Zachowanie**:
  - Czytanie: wszyscy
  - Edycja/Usuwanie: tylko właściciel
- **Sprawdza**: `obj.user == request.user`

### IsOwnerOrAdmin
- **Zastosowanie**: User (profile edits)
- **Zachowanie**:
  - Czytanie: wszyscy
  - Edycja/Usuwanie: właściciel lub admin
- **Sprawdza**: `obj.author == request.user OR request.user.is_staff`

### IsAdminOrReadOnly
- **Zastosowanie**: FotoCategory, PostCategory
- **Zachowanie**:
  - Czytanie: wszyscy
  - Edycja/Usuwanie: tylko admini
- **Sprawdza**: `request.user.is_staff`

---

## Rate Limiting (Throttling)

Plik: `brashfox_app/api/throttles.py`

### Globalne limity (settings.py)
```python
'anon': '100/hour'      # Użytkownicy niezalogowani
'user': '1000/hour'     # Użytkownicy zalogowani
```

### Specyficzne limity dla akcji
```python
'contact': '5/hour'     # Formularz kontaktowy
'register': '3/hour'    # Rejestracja nowych kont
'login': '10/hour'      # Próby logowania
```

### ContactFormThrottle
- **Zastosowanie**: `MessageViewSet.create`
- **Limit**: 5 wiadomości na godzinę
- **Cel**: Zapobieganie spamowi

### RegisterThrottle
- **Zastosowanie**: `UserViewSet.create`
- **Limit**: 3 rejestracje na godzinę
- **Cel**: Zapobieganie automatycznej kreacji kont

### LoginThrottle
- **Zastosowanie**: Token endpoints (simplejwt)
- **Limit**: 10 prób logowania na godzinę
- **Cel**: Zapobieganie atakom brute force

---

## Automatyczne ustawianie autora

### BlogPost
```python
def perform_create(self, serializer):
    serializer.save(author=self.request.user)
```
- Przy tworzeniu posta, autor ustawiany automatycznie na zalogowanego użytkownika
- Frontend nie musi przesyłać pola `author`

### FotoDescription
```python
def perform_create(self, serializer):
    serializer.save(author=self.request.user.username)
```
- Autor zapisywany jako username (CharField)
- Frontend nie musi przesyłać pola `author`

---

## Macierz uprawnień

| Endpoint | List | Retrieve | Create | Update | Delete |
|----------|------|----------|--------|--------|--------|
| **users** | Auth | Auth | Anyone* | Owner/Admin | Owner/Admin |
| **groups** | Auth | Auth | Auth | Auth | Auth |
| **foto-categories** | Anyone | Anyone | Admin | Admin | Admin |
| **fotos** | Anyone | Anyone | Auth** | Author/Admin | Author/Admin |
| **foto-tags** | Anyone | Anyone | Auth | Auth | Auth |
| **blog-posts** | Anyone | Anyone | Auth** | Author/Admin | Author/Admin |
| **post-categories** | Anyone | Anyone | Admin | Admin | Admin |
| **comments** | Anyone | Anyone | Anyone | Auth | Auth |
| **messages** | Admin | Admin | Anyone* | Admin | Admin |

*Rate limited  
**Auto-set author

---

## Testowanie permissions

### Test 1: Niezalogowany użytkownik próbuje stworzyć post
```bash
curl -X POST http://localhost:8000/api/blog-posts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "post": "Content"}'
```
**Oczekiwany wynik**: `403 Forbidden`

### Test 2: Zalogowany użytkownik tworzy post
```bash
curl -X POST http://localhost:8000/api/blog-posts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "post": "Content"}'
```
**Oczekiwany wynik**: `201 Created` + autor ustawiony automatycznie

### Test 3: Użytkownik próbuje edytować cudzy post
```bash
curl -X PATCH http://localhost:8000/api/blog-posts/test-slug/ \
  -H "Authorization: Bearer USER_B_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hacked!"}'
```
**Oczekiwany wynik**: `403 Forbidden` (jeśli post należy do USER_A)

### Test 4: Rate limiting - spam w formularz kontaktowy
```bash
# 6 próba w ciągu godziny
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/messages/ \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Spam $i\", \"email\": \"spam@test.com\", \"message\": \"Test\"}"
done
```
**Oczekiwany wynik**: Pierwszych 5 OK, szósta `429 Too Many Requests`

---

## Security Best Practices

✅ **Zaimplementowane:**
- JWT authentication (token-based)
- Per-action permissions
- Rate limiting (globalne + per-action)
- Automatic author assignment
- Admin-only access dla kategorii
- CORS configuration
- File upload validation (10MB limit)

🔜 **Do rozważenia (produkcja):**
- HTTPS only (SECURE_SSL_REDIRECT)
- Django security middleware settings
- CSRF protection dla cookie-based auth
- Input sanitization dla rich text
- Image upload virus scanning
- Backup authentication method
- Two-factor authentication (2FA)
- Email verification dla nowych kont
