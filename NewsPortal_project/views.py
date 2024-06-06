from django.shortcuts import redirect
from django.views.generic import CreateView


def redirect_view(request):
    response = redirect('/about/')
    return response
