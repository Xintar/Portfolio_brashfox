"""
About Me view - About page
LEGACY: Django template view (SSR)
"""
from django.shortcuts import render
from django.views import View


class AboutMeView(View):
    """About Me page view."""
    def get(self, request):
        dane = 'dane'
        ctx = {
            'dane': dane
        }
        return render(request, 'about_me.html', ctx)
