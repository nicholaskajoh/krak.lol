from django.shortcuts import render

def page_not_found(request):
  return render(request, 'social/pages/error/404.html')

def internal_server_error(request):
  return render(request, 'social/pages/error/500.html')