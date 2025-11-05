"""
About Me view - About page
LEGACY: Django template view (SSR)
"""
from django.shortcuts import render
from django.views import View
from brashfox_app.models import AboutMe


adres_prefix = "about/"

class AboutMeView(View):
    """About Me page view - displays artist bio and profile."""
    def get(self, request):
        # Fetch AboutMe singleton instance
        about_me = AboutMe.get_instance()
        
        ctx = {
            'about_me': about_me
        }
        return render(request, f'{adres_prefix}about_me.html', ctx)
