from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import RegistrationView, LoginView, UserDetailView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail')
]