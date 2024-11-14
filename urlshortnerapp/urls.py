from django.urls import path
from . import views

urlpatterns = [
    path('api/shorten', views.shorten_url, name='shorten_url'),
    path('api/<str:shortened_url>', views.get_original_url, name='get_original_url'),
    path('api/stats/<str:shortened_url>', views.url_stats, name='url_stats'),
]
