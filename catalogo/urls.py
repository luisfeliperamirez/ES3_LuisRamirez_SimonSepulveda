from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('comic/<int:comic_id>/', views.detalle_comic, name='detalle_comic'),
    path('comic/<int:comic_id>/comprar/', views.comprar, name='comprar'),
]