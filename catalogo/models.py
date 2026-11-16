import uuid
from django.db import models

class Editorial(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")

    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Comic(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.CASCADE,
        related_name='comics',
        verbose_name="Editorial"
    )
    numero_tomo = models.PositiveIntegerField(default=1, verbose_name="Número de tomo")
    autor = models.CharField(max_length=150, verbose_name="Autor / Guionista")
    sinopsis = models.TextField(blank=True, verbose_name="Sinopsis")
    precio = models.PositiveIntegerField(verbose_name="Precio (CLP)")
    tapa_dura = models.BooleanField(default=False, verbose_name="¿Es tapa dura?")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    disponible = models.BooleanField(default=True, verbose_name="Disponible para venta")
    portada = models.ImageField(upload_to='portadas/', verbose_name="Imagen de portada")

    class Meta:
        verbose_name = "Cómic"
        verbose_name_plural = "Cómics"
        ordering = ['titulo', 'numero_tomo']

    def __str__(self):
        return f"{self.titulo} - Tomo #{self.numero_tomo}"

class Reserva(models.Model):
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    nombre_cliente = models.CharField(max_length=100)
    correo = models.EmailField()
    rut = models.CharField(max_length=12)
    cantidad_ejemplares = models.IntegerField()

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['fecha_reserva']

    def __str__(self):
        return f"{self.nombre_cliente} - {self.comic.titulo} ({str(self.codigo)[:8]})"