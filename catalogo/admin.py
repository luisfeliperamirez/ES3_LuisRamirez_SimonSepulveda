from django.contrib import admin
from .models import Editorial, Comic, Reserva

admin.site.site_header = "Página de Administración de Cómics"
admin.site.site_title = "Página Cómics"

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'editorial__nombre', 'stock', 'disponible', 'precio_formateado',)
    search_fields = ('titulo', 'autor', 'editorial__nombre',)
    list_filter = ('editorial', 'disponible', 'tapa_dura',)

    @admin.display(description = 'Precio', ordering = 'precio')
    def precio_formateado(self, obj):
        return f"${obj.precio:,}".replace(',', '.')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'comic', 'fecha_reserva', 'nombre_cliente', 'correo', 'rut',)
    search_fields = ('codigo', 'nombre_cliente', 'correo',)
    list_filter = ('fecha_reserva',)