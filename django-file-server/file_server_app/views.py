import socket
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.html import escape
import os
import validators
import urllib
import json
import re
import ipaddress

BASE_DIR = "/home/user/"

def serve_file(request): 
    filename = request.GET.get('file')
    file_path = os.path.join(BASE_DIR, filename)
    print("file_path:", file_path)  # Debugging line
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/plain')
    else:
        return HttpResponse("File not found", status=404)
    

def validate_filename(filename):
    if re.fullmatch(r"[A-Za-z0-9-.]+", filename):
        return True
    else:
        return False


def serve_file_secure(request): 
    filename = request.GET.get('file')
    if not validate_filename(filename):
       return HttpResponse("Wrong file name passed", status=500) 
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

def resolve_all_ips(host: str) -> set[str]:
    """Resolve A/AAAA using system resolver and return unique IP strings."""
    infos = socket.getaddrinfo(
        host,
        None,
        family=socket.AF_UNSPEC,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
        flags=socket.AI_ADDRCONFIG
    )
    print('resolve_all_ips -->',infos)
    return {sa[0] for *_unused, sa in infos}

def is_internal_address(ip: str) -> bool:
    print('ip address ',ip)
    """
    Return True if IP is NOT globally routable (i.e., private/loopback/link-local/multicast/etc.).
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True  # malformed -> treat as internal/disallowed
    # ipaddress defines .is_global accurately across v4/v6
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
        or addr.is_unspecified
        or getattr(addr, "is_site_local", False)  # legacy IPv6-only attribute
    )

def fetch(request):
    print('inside fetch')
    try:
        url = request.GET.get('url')
        print('url ',url)
        with urllib.request.urlopen(url, timeout=5) as response: 
            data = response.read()
        return HttpResponse(data, status=200)
    except Exception as e: 
        return HttpResponse(e, status=404)

def fetch_safe(request): 
    try:
        url = request.GET.get('url')
        if not url:
            return JsonResponse({"error": "Please provide the url"}, status=400)
        is_url_valid = validators.url(url)
        print("is_url_valid", is_url_valid)
        if not is_url_valid:
            return JsonResponse({"error": "Invalid URL supplied"}, status=403)
        hostname = urllib.parse.urlparse(url).hostname
        print("hostname", hostname)
        try:
            ips = resolve_all_ips(hostname)        
        except e:
            return HttpResponse(e, status=400)
        if not ips:
            return HttpResponse("cannopt resolve ip address for host", status=400)
        if any(is_internal_address(ip) for ip in ips):
            return HttpResponse("resolved address not allowed", status=400)
        if not hostname or hostname not in ["eczsdstfqcuazxpjznqig12uzsrz4wbeg.oast.fun"]:
            return HttpResponse({"error": "Domain is not allowed"}, status=403)
        with urllib.request.urlopen(url, timeout=5) as response: 
            data = response.read()
        return HttpResponse(data, status=200)
    except Exception as e: 
        return HttpResponse(e, status=404)