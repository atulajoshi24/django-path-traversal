from django.urls import path
from .views import serve_file, serve_file_secure, display_user_input, display_user_input_secure

urlpatterns = [
    path('serve-file', serve_file, name='serve_file'),
    path('serve-file-secure', serve_file_secure, name='serve_file_secure'),
    path('display', display_user_input, name='display'),
    path('display-secure', display_user_input_secure, name='display-secure'),
]