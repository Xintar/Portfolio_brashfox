"""
Contact views - Contact form and success page
LEGACY: Django template views (SSR)
"""
from django.shortcuts import render, redirect
from django.views import View

from brashfox_app.forms import ContactForm
from brashfox_app.models import Message


class ContactView(View):
    """Contact form view."""
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            new_message = Message.objects.create(**form.cleaned_data)
            return redirect('contact-succes')
        else:
            ctx = {
                'form': form,
                'coment': 'Proszę o poprawne dane'
            }
            return render(request, 'contact.html', ctx)


class ContactSucessView(View):
    """Contact form success page view."""
    def get(self, request):
        return render(request, 'contact_succes.html')
