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


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/detail.html'
    context_object_name = 'photo'


class PhotoCreateView(CreateView):
    model = Photo
    template_name = 'photos/create.html'
    form_class = PhotoForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PhotoUpdateView(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/update.html'


class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'photos/delete.html'

    def get_success_url(self):
        return reverse('webapp:index')
