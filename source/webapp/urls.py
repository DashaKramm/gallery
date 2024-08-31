from django.urls import path
from django.views.generic import RedirectView

from webapp.views import PhotoListView, PhotoDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='webapp:index')),
    path('photos/', PhotoListView.as_view(), name='index'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='detail_photo'),
    path('photos/create/', PhotoCreateView.as_view(), name='create_photo'),
    path('photos/<int:pk>/update/', PhotoUpdateView.as_view(), name='update_photo'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete_photo')
]
