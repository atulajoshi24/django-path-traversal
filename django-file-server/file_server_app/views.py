from django.http import HttpResponse
from django.views import View
import os
BASE_DIR = "E:\\CyberSecurity\wordlists"

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