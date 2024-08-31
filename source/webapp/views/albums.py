from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import AlbumForm
from webapp.models import Album, Photo


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'albums/detail.html'
    context_object_name = 'album'

    def dispatch(self, request, *args, **kwargs):
        album = self.get_object()
        if album.is_private and album.author != request.user:
            raise PermissionDenied("У вас нет прав для просмотра этого альбома")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = self.object.album_photos.filter(is_private=False).order_by('-created_at')
        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    template_name = 'albums/create.html'
    form_class = AlbumForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(PermissionRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/update.html'
    permission_required = 'webapp.change_album'

    def has_permission(self):
        album = self.get_object()
        return super().has_permission() or self.request.user == album.author


class AlbumDeleteView(PermissionRequiredMixin, DeleteView):
    model = Album
    template_name = 'albums/delete.html'
    permission_required = 'webapp.delete_album'

    def has_permission(self):
        album = self.get_object()
        return super().has_permission() or self.request.user == album.author

    def get_success_url(self):
        return reverse('webapp:index')

    def delete(self, request, *args, **kwargs):
        album = self.get_object()
        Photo.objects.filter(album=album).delete()
        return super().delete(request, *args, **kwargs)
