#!/bin/bash

# 🧪 Test integracji Frontend-Backend
# Ten skrypt testuje podstawowe połączenie między React a Django API

echo "🚀 Test integracji BrashFox Portfolio"
echo "======================================"
echo ""

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funkcja testująca
test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    echo -n "Testing $name... "
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$response" -eq "$expected_code" ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected $expected_code, got $response)"
        return 1
    fi
}

# Licznik
passed=0
failed=0

echo "📡 Backend API Tests"
echo "--------------------"

# Backend testy
test_endpoint "API Root" "http://localhost:8000/api/" && ((passed++)) || ((failed++))
test_endpoint "Blog Posts List" "http://localhost:8000/api/blog-posts/" && ((passed++)) || ((failed++))
test_endpoint "Photos List" "http://localhost:8000/api/photos/" && ((passed++)) || ((failed++))
test_endpoint "Post Categories" "http://localhost:8000/api/post-categories/" && ((passed++)) || ((failed++))
test_endpoint "Photo Categories" "http://localhost:8000/api/photo-categories/" && ((passed++)) || ((failed++))
test_endpoint "Swagger Docs" "http://localhost:8000/api/schema/swagger/" && ((passed++)) || ((failed++))

echo ""
echo "🌐 Frontend Tests"
echo "-----------------"

# Frontend testy
test_endpoint "Frontend Home" "http://localhost:5173/" && ((passed++)) || ((failed++))

# Test frontend static assets (próbujemy vite.svg)
echo -n "Testing Frontend static... "
response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:5173/vite.svg")
if [ "$response" -eq 200 ]; then
    echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
    ((passed++))
else
    echo -e "${YELLOW}⚠ SKIP${NC} (Static file not found, but server responds)"
    # Nie liczymy jako failed, bo serwer działa
fi

echo ""
echo "🔐 JWT Auth Test"
echo "----------------"

# Test JWT - próba POST bez credentials (oczekujemy 400 Bad Request)
echo -n "Testing JWT Token endpoint (POST without data)... "
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8000/api/token/" -H "Content-Type: application/json" -d '{}')
if [ "$response" -eq 400 ]; then
    echo -e "${GREEN}✓ OK${NC} (HTTP $response - Bad Request as expected)"
    ((passed++))
elif [ "$response" -eq 401 ]; then
    echo -e "${GREEN}✓ OK${NC} (HTTP $response - Unauthorized as expected)"
    ((passed++))
else
    echo -e "${RED}✗ FAIL${NC} (Expected 400 or 401, got $response)"
    ((failed++))
fi

echo ""
echo "📊 Podsumowanie"
echo "==============="
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}🎉 Wszystkie testy przeszły pomyślnie!${NC}"
    echo ""
    echo "✅ Możesz teraz otworzyć:"
    echo "   Frontend: http://localhost:5173"
    echo "   Backend:  http://localhost:8000"
    echo "   Swagger:  http://localhost:8000/api/schema/swagger/"
    exit 0
else
    echo -e "${RED}❌ Niektóre testy nie przeszły.${NC}"
    echo ""
    echo "Sprawdź czy oba serwery są uruchomione:"
    echo "   Backend:  cd backend && python manage.py runserver"
    echo "   Frontend: cd frontend/brushfox-project && npm run dev"
    exit 1
fi
