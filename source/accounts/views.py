from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView as BaseLoginView

from accounts.forms import CustomUserCreationForm
from webapp.models import Photo, Album, Favorite


class LoginView(BaseLoginView):
    template_name = "login.html"

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.context_data['has_error'] = True
        return response


class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration.html"
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        user_photos = Photo.objects.filter(author=user).exclude(is_private=True)
        user_albums = Album.objects.filter(author=user).exclude(is_private=True)
        user_favorites = Favorite.objects.filter(user=user)
        if user == self.request.user:
            private_albums = Album.objects.filter(author=user, is_private=True)
            private_pictures = Photo.objects.filter(author=user, is_private=True)
            context['private_albums'] = private_albums
            context['private_pictures'] = private_pictures
            context['user_favorites'] = user_favorites
        context['user_photos'] = user_photos
        context['user_albums'] = user_albums
        return context
