from os import listdir

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import ImageField

from brashfox_app.forms import ContactForm, LoginForm
from .models import Message, BlogPost, FotoDescription


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class PortfolioView(View):

    def get(self, request):
        fotos = FotoDescription.objects.all()

        ctx = {
            'fotos': fotos,
        }

        return render(request, 'portfolio.html', ctx)


class AddFotosView(LoginRequiredMixin, CreateView):
    model = FotoDescription
    fields = ['name', 'author', 'ivent', 'image', 'foto_category']
    template_name = 'fotodescription_form.html'
    success_url = reverse_lazy('add-fotos')

    def form_valid(self, form):
        form.instance.image = self.request.FILES['image']
        self.object = form.save()
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('addfot')


class EditFotosView(LoginRequiredMixin, UpdateView):
    model = FotoDescription
    fields = ['name', 'author', 'ivent', 'image']
    template_name = 'fotodescription_update_form.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return FotoDescription.objects.get(pk=pk)

    def form_valid(self, form):
        form.save()
        return redirect('portfolio')


class DeleteFotosView(LoginRequiredMixin, DeleteView):
    pass


class AboutMeView(View):
    def get(self, request):
        dane = 'dane'
        ctx = {
            'dane': dane
        }

        return render(request, 'about_me.html', ctx)


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # topic = form.cleaned_data['topic']
            # message = form.cleaned_data['message']
            new_message = Message.objects.create(**form.cleaned_data)
            ctx = {
                'coment': 'Dziękuję za wiadomość',
                'form': form
            }

            return render(request, 'contact.html', ctx)
        else:
            ctx = {
                'form': form,
                'coment': 'Proszę o poprawne dane'
            }
            return render(request, 'contact.html', ctx)


class BlogView(View):
    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created')
        ctx = {
            'posts': posts
        }
        return render(request, 'blog.html', ctx)


class PostDetailView(View):
    def get(self, request, slug):
        blog_post = get_object_or_404(BlogPost, slug=slug)
        ctx = {
            'title': blog_post.title,
            'post': blog_post.post,

        }
        return render(request, 'post_detail.html', ctx)


class AddPostView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['author', 'title', 'post', 'slug']
    template_name = 'blogpost_form.html'
    success_url = reverse_lazy('start')


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "logged.html", {"user": request.user})
        else:
            form = LoginForm()
            return render(request, 'login.html', {'form': form})

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
                return render(request, 'login.html', ctx)
        else:
            form = LoginForm()
            ctx = {
                'form': form,
                'comment': "Błędne dane logowania"
            }
            return render(request, 'login.html', ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('start')
