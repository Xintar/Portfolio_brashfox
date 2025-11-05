"""
Authentication views - Login, Logout, Register
LEGACY: Django template views (SSR)
"""
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from brashfox_app.forms import LoginForm


adres_prefix = "auth/"

class LoginView(View):
    """User login view."""
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, f"{adres_prefix}logged.html", {"user": request.user})
        else:
            form = LoginForm()
            return render(request, f"{adres_prefix}login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('start')
            else:
                form = LoginForm()
                ctx = {
                    'form': form,
                    'comment': "Błędne dane logowania"
                }
                return render(request, f'{adres_prefix}login.html', ctx)
        else:
            form = LoginForm()
            ctx = {
                'form': form,
                'comment': "Błędne dane logowania"
            }
            return render(request, f'{adres_prefix}login.html', ctx)


class LogoutView(View):
    """User logout view."""
    def get(self, request):
        logout(request)
        return redirect('start')


def register(request):
    """User registration view (function-based)."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, f'{adres_prefix}register.html', {'form': form})
