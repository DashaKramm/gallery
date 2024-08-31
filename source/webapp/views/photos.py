from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PhotoForm
from webapp.models import Photo


class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos'
    paginate_by = 5

    def get_queryset(self):
        return Photo.objects.filter(is_private=False).order_by('-created_at')


class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photos/detail.html'
    context_object_name = 'photo'

    def dispatch(self, request, *args, **kwargs):
        photo = self.get_object()
        if photo.is_private and photo.author != request.user:
            raise PermissionDenied("У вас нет прав для просмотра этой фотографии")
        return super().dispatch(request, *args, **kwargs)


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'photos/create.html'
    form_class = PhotoForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PhotoUpdateView(PermissionRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/update.html'
    permission_required = 'webapp.change_photo'

    def has_permission(self):
        photo = self.get_object()
        return super().has_permission() or self.request.user == photo.author

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PhotoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photos/delete.html'
    permission_required = 'webapp.delete_photo'

    def has_permission(self):
        photo = self.get_object()
        return super().has_permission() or self.request.user == photo.author

    def get_success_url(self):
        return reverse('webapp:index')
