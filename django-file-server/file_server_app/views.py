from django.http import HttpResponse
from django.views import View
from django.utils.html import escape
import os
BASE_DIR = "/home/user/"

def serve_file(request): 
    filename = request.GET.get('filename')
    file_path = os.path.join(BASE_DIR, filename)
    print("file_path:", file_path)  # Debugging line
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/plain')
    else:
        return HttpResponse("File not found", status=404)
    

def serve_file_secure(request): 
    filename = request.GET.get('filename')
    file_path = os.path.join(BASE_DIR, filename)
    print("file_path:", file_path)  # Debugging line
    resolved = os.path.realpath(file_path)
    print("resolved path:", resolved)  # Debugging line
    if resolved.startswith(BASE_DIR) and os.path.exists(resolved):
        with open(file_path, 'r') as file:
            content = file.read()
        print('content is returned')  # Debugging line
        return HttpResponse(content, content_type='text/plain')
    else:
        print('doesn\'t starts with base dir or file not found')  # Debugging line
        return HttpResponse("File not found", status=404)

def display_user_input(request): 
    username = request.GET.get('user_input', '')
    return HttpResponse(f'Weclome {username}')

def display_user_input_secure(request): 
    username = request.GET.get('user_input', '')
    sanitised_username = escape(username)
    return HttpResponse(f'Weclome {sanitised_username}')