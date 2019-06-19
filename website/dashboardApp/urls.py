from django.urls import path
from django.contrib.auth.views import LoginView
from .views import IndexView, signup_view, logout_view

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login', LoginView.as_view(template_name='ui-template/pages/login.html'), name='login'),
    path('signup', signup_view, name='signup'),
    path('logout', logout_view, name='logout')
]
