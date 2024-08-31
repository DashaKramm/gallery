from django.urls import path
from django.views.generic import RedirectView

from webapp.views import PhotoListView, PhotoDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView, \
    AlbumDetailView, AlbumCreateView, AlbumUpdateView, AlbumDeleteView, PhotoLinkView, PhotoDetailWithTokenView, \
    AddToFavorites, RemoveFromFavorites

app_name = 'webapp'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='webapp:index')),
    path('photos/', PhotoListView.as_view(), name='index'),
    path('photos/<int:pk>/link/', PhotoLinkView.as_view(), name='link_photo'),
    path('photo/<int:pk>/<str:token>/', PhotoDetailWithTokenView.as_view(), name='detail_photo_with_token'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='detail_photo'),
    path('photos/create/', PhotoCreateView.as_view(), name='create_photo'),
    path('photos/<int:pk>/update/', PhotoUpdateView.as_view(), name='update_photo'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete_photo'),
    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='detail_album'),
    path('albums/create/', AlbumCreateView.as_view(), name='create_album'),
    path('albums/<int:pk>/update/', AlbumUpdateView.as_view(), name='update_album'),
    path('albums/<int:pk>/delete/', AlbumDeleteView.as_view(), name='delete_album'),
    path('favorites/add/', AddToFavorites.as_view(), name='add_to_favorites'),
    path('favorites/remove/', RemoveFromFavorites.as_view(), name='remove_from_favorites'),
]
