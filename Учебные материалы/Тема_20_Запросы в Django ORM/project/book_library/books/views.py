from django.shortcuts import render
from . import models


def start_page(request):
    data = models.Book.objects.all()
    return render(request, 'index.html', context={'data': data})