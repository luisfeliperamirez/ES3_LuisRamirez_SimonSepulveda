from django.db import transaction
from django.shortcuts import render, get_object_or_404

from .forms import ReservaForm
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


def detalle_comic(request, comic_id):
    comic = get_object_or_404(
        Comic.objects.select_related('editorial'),
        pk=comic_id,
        disponible=True,
    )
    return render(request, 'catalogo/detalle.html', {
        'comic': comic,
    })


def comprar(request, comic_id):
    comic = get_object_or_404(
        Comic.objects.select_related('editorial'),
        pk=comic_id,
        disponible=True,
    )

    if request.method == 'POST':
        with transaction.atomic():
            comic = get_object_or_404(
                Comic.objects.select_for_update().select_related('editorial'),
                pk=comic_id,
                disponible=True,
            )
            if comic.stock > 0:
                form = ReservaForm(request.POST, stock=comic.stock)
                if form.is_valid():
                    reserva = form.save(commit=False)
                    reserva.comic = comic
                    reserva.save()

                    comic.stock -= reserva.cantidad_ejemplares
                    comic.save(update_fields=['stock'])
                    return render(request, 'comprar.html', {
                        'comic': comic,
                        'reserva': reserva,
                    })
            else:
                form = None
    else:
        form = ReservaForm(stock=comic.stock) if comic.stock > 0 else None

    return render(request, 'comprar.html', {
        'comic': comic,
        'form': form,
    })