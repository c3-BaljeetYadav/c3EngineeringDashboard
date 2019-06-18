from django.urls import path
from .views import IndexView, LoginView

urlpatterns = [
    path('', IndexView.as_view(), name='index.html'),
    path('login', LoginView.as_view(), name='login.html'),
    path('index.html', IndexView.as_view(), name='index.html')
]
