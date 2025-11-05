"""
Common/General views - Index page
LEGACY: Django template views (SSR)
"""
from django.shortcuts import render
from django.views import View


class IndexView(View):
    """Home page view."""
    def get(self, request):
        return render(request, 'index.html')
