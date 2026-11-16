from django.shortcuts import render
from .models import Comic, Editorial


def inicio(request):
    comics = Comic.objects.filter(disponible=True).select_related('editorial')
    editoriales = Editorial.objects.all()

    q = request.GET.get('q', '').strip()
    editorial_id = request.GET.get('editorial', '').strip()
    editorial_seleccionada = None

    if q:
        comics = comics.filter(titulo__icontains=q)

    if editorial_id.isdigit():
        editorial_seleccionada = int(editorial_id)
        comics = comics.filter(editorial_id=editorial_seleccionada)

    return render(request, 'catalogo/inicio.html', {
        'comics': comics,
        'editoriales': editoriales,
        'q': q,
        'editorial_seleccionada': editorial_seleccionada,
    })