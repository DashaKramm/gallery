import uuid

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.forms import PhotoForm
from webapp.models import Photo, Favorite, Album


class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos'
    paginate_by = 1

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


class PhotoLinkView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, pk, **kwargs):
        photo = get_object_or_404(Photo, pk=pk)
        if photo.access_token:
            return reverse('webapp:detail_photo_with_token', kwargs={'pk': photo.pk, 'token': photo.access_token})
        photo.access_token = uuid.uuid4().hex
        photo.save()
        return reverse('webapp:detail_photo_with_token', kwargs={'pk': photo.pk, 'token': photo.access_token})


class PhotoDetailWithTokenView(DetailView):
    model = Photo
    template_name = 'photos/detail.html'
    context_object_name = 'photo'

    def get_object(self, queryset=None):
        photo = super().get_object(queryset)
        token = self.kwargs.get('token')
        if token:
            if photo.access_token != token:
                return HttpResponseForbidden("Недопустимый токен доступа.")
        elif photo.is_private and photo.author != self.request.user:
            return HttpResponseForbidden("У вас нет прав для просмотра этой фотографии.")
        return photo


class AddToFavorites(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        photo_id = request.data.get('photo_id')
        album_id = request.data.get('album_id')
        if photo_id:
            try:
                photo = Photo.objects.get(id=photo_id)
                favorite, created = Favorite.objects.get_or_create(user=user, photo=photo)
                if not created:
                    return Response({'error': 'Photo already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'status': 'Photo added to favorites'}, status=status.HTTP_201_CREATED)
            except Photo.DoesNotExist:
                return Response({'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)
        if album_id:
            try:
                album = Album.objects.get(id=album_id)
                favorite, created = Favorite.objects.get_or_create(user=user, album=album)
                if not created:
                    return Response({'error': 'Album already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'status': 'Album added to favorites'}, status=status.HTTP_201_CREATED)
            except Album.DoesNotExist:
                return Response({'error': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromFavorites(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        photo_id = request.data.get('photo_id')
        album_id = request.data.get('album_id')
        if photo_id:
            try:
                photo = Photo.objects.get(id=photo_id)
                favorite = Favorite.objects.get(user=user, photo=photo)
                favorite.delete()
                return Response({'status': 'Photo removed from favorites'}, status=status.HTTP_204_NO_CONTENT)
            except Favorite.DoesNotExist:
                return Response({'error': 'Photo not in favorites'}, status=status.HTTP_400_BAD_REQUEST)
            except Photo.DoesNotExist:
                return Response({'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)
        if album_id:
            try:
                album = Album.objects.get(id=album_id)
                favorite = Favorite.objects.get(user=user, album=album)
                favorite.delete()
                return Response({'status': 'Album removed from favorites'}, status=status.HTTP_204_NO_CONTENT)
            except Favorite.DoesNotExist:
                return Response({'error': 'Album not in favorites'}, status=status.HTTP_400_BAD_REQUEST)
            except Album.DoesNotExist:
                return Response({'error': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
