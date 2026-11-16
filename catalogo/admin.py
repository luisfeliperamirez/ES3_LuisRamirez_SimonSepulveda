from django.contrib import admin
from .models import Editorial, Comic, Reserva

admin.site.site_header = "Página de Administración de Cómics"
admin.site.site_title = "Página Cómics"

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'editorial', 'numero_tomo', 'stock', 'disponible', 'precio_formateado')
    search_fields = ('titulo', 'autor', 'editorial__nombre')
    list_filter = ('editorial', 'disponible', 'tapa_dura')

    @admin.display(description='Precio', ordering='precio')
    def precio_formateado(self, obj):
        return f"${obj.precio:,}".replace(',', '.')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'comic', 'nombre_cliente', 'rut', 'cantidad_ejemplares', 'fecha_reserva')
    search_fields = ('codigo', 'nombre_cliente', 'rut', 'correo')
    list_filter = ('comic', 'fecha_reserva')