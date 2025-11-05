"""
Portfolio/Photo views - Gallery and photo management
LEGACY: Django template views (SSR)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from brashfox_app.models import FotoDescription


class PortfolioView(View):
    """Portfolio gallery list view."""
    def get(self, request):
        fotos = FotoDescription.objects.all()
        ctx = {
            'fotos': fotos,
        }
        return render(request, 'portfolio/portfolio.html', ctx)


class DetailFotoView(View):
    """Single photo detail view."""
    def get(self, request, id):
        foto = get_object_or_404(FotoDescription, id=id)
        ctx = {
            'foto': foto
        }
        return render(request, 'portfolio/foto_detail.html', ctx)


class AddFotosView(LoginRequiredMixin, CreateView):
    """Add new photo view."""
    model = FotoDescription
    fields = ['name', 'author', 'event', 'image', 'foto_category']
    template_name = 'portfolio/fotodescription_form.html'
    success_url = reverse_lazy('add-fotos')

    def form_valid(self, form):
        form.instance.image = self.request.FILES['image']
        self.object = form.save()
        return super().form_valid(form)


class EditFotosView(LoginRequiredMixin, UpdateView):
    """Edit photo view."""
    model = FotoDescription
    fields = ['name', 'author', 'event', 'image']
    template_name = 'portfolio/fotodescription_update_form.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return FotoDescription.objects.get(pk=pk)

    def form_valid(self, form):
        form.save()
        return redirect('portfolio')


class DeleteFotosView(LoginRequiredMixin, DeleteView):
    """Delete photo view."""
    model = FotoDescription
    template_name = 'portfolio/fotodescription_confirm_delete.html'
    success_url = reverse_lazy('portfolio')
