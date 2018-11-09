from django.urls import path
from .views import IndexView, SingleView

urlpatterns = [
    path('', SingleView.as_view(), name='index.html'),
    path('index', IndexView.as_view(template_name='index.html')),
]