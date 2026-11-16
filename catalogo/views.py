from django.shortcuts import render
from .models import Comic

def inicio(request):
    comics = Comic.objects.filter(disponible=True).select_related('editorial')
    return render(request, 'catalogo/inicio.html', {
        'comics': comics,
    })