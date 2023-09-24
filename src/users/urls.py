from django.urls import path

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='Регистрация пользователя'),
    path('login/', LoginView.as_view(), name='Авторизация'),
]