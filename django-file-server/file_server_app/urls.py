from django.urls import path
from .views import serve_file, serve_file_secure

urlpatterns = [
    path('serve-file', serve_file, name='serve_file'),
    path('serve-file-secure', serve_file_secure, name='serve_file_secure'),
]