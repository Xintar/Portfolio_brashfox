from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

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


class DetailFotoView(View):
    def get(self, request, id):
        foto = get_object_or_404(FotoDescription, id=id)
        ctx = {
            'foto': foto
        }
        return render(request, 'foto_detail.html', ctx)


class AddFotosView(LoginRequiredMixin, CreateView):
    model = FotoDescription
    fields = ['name', 'author', 'ivent', 'image', 'foto_category']
    template_name = 'fotodescription_form.html'
    success_url = reverse_lazy('add-fotos')

    def form_valid(self, form):
        form.instance.image = self.request.FILES['image']
        self.object = form.save()
        return super().form_valid(form)


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
    model = FotoDescription
    template_name = 'fotodescription_confirm_delete.html'
    success_url = reverse_lazy('portfolio')


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
            new_message = Message.objects.create(**form.cleaned_data)
            return redirect('contact-succes')
        else:
            ctx = {
                'form': form,
                'coment': 'Proszę o poprawne dane'
            }
            return render(request, 'contact.html', ctx)


class ContactSucessView(View):
    def get(self, request):
        return render(request, 'contact_succes.html')


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
            'pk': blog_post.pk

        }
        return render(request, 'post_detail.html', ctx)


class AddPostView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'post']
    template_name = 'blogpost_form.html'
    success_url = reverse_lazy('start')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        form.save()
        return redirect(self.success_url)


class EditPostView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'post']
    template_name = 'blogpost_update_form.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return BlogPost.objects.get(pk=pk)

    def form_valid(self, form):
        form.save()
        return redirect('blog')


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog')


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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
