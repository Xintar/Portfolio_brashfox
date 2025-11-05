"""
Blog views - Blog posts and articles
LEGACY: Django template views (SSR)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from brashfox_app.models import BlogPost


class BlogView(View):
    """Blog posts list view."""
    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created')
        ctx = {
            'posts': posts
        }
        return render(request, 'blog/blog.html', ctx)


class PostDetailView(View):
    """Single blog post detail view."""
    def get(self, request, slug):
        blog_post = get_object_or_404(BlogPost, slug=slug)
        ctx = {
            'title': blog_post.title,
            'post': blog_post.post,
            'pk': blog_post.pk
        }
        return render(request, 'blog/post_detail.html', ctx)


class AddPostView(LoginRequiredMixin, CreateView):
    """Add new blog post view."""
    model = BlogPost
    fields = ['title', 'post']
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('start')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        form.save()
        return redirect(self.success_url)


class EditPostView(LoginRequiredMixin, UpdateView):
    """Edit blog post view."""
    model = BlogPost
    fields = ['title', 'post']
    template_name = 'blog/blogpost_update_form.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return BlogPost.objects.get(pk=pk)

    def form_valid(self, form):
        form.save()
        return redirect('blog')


class DeletePostView(LoginRequiredMixin, DeleteView):
    """Delete blog post view."""
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog')
