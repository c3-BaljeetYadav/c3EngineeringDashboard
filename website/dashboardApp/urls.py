from django.urls import path
from .views import IndexView, SingleView, LoginView, NewsView

urlpatterns = [
    path('', SingleView.as_view(), name='index.html'),
    path('login', LoginView.as_view(), name='index-okta.html'),
    path('index.html', SingleView.as_view(), name='index.html'),
    path('news.html', NewsView.as_view(),  name='news.html')
]