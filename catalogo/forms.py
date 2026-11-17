import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Reserva


class ReservaForm(forms.ModelForm):
    RUT_PATTERN = r'^(?:\d{7,8}|\d{1,2}\.\d{3}\.\d{3})-[\dKk]$'

    class Meta:
        model = Reserva
        fields = ('nombre_cliente', 'rut', 'correo', 'cantidad_ejemplares')
        labels = {
            'nombre_cliente': 'Nombre del cliente',
            'rut': 'RUT (Ejemplo: 12.345.678-5)',
            'correo': 'Correo electrónico',
            'cantidad_ejemplares': 'Cantidad de ejemplares (1 a 3)',
        }

    def __init__(self, *args, stock, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock = stock
        self.fields['cantidad_ejemplares'].widget.attrs.update({
            'min': 1,
            'max': min(3, stock),
        })
        self.fields['rut'].widget.attrs.update({
            'placeholder': '12.345.678-5',
        })

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_rut(self):
        rut = self.cleaned_data['rut'].strip().upper()
        if not re.fullmatch(self.RUT_PATTERN, rut):
            raise ValidationError(
                'Formato de RUT inválido. Usa puntos y guion (ejemplo: 12.345.678-5).'
            )

        cuerpo, dv_ingresado = rut.split('-')
        cuerpo_limpio = cuerpo.replace('.', '')

        suma = 0
        multiplicador = 2
        for digito in reversed(cuerpo_limpio):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = 11 - (suma % 11)
        if resto == 11:
            dv_esperado = '0'
        elif resto == 10:
            dv_esperado = 'K'
        else:
            dv_esperado = str(resto)

        if dv_ingresado != dv_esperado:
            raise ValidationError('El dígito verificador del RUT no es válido.')

        cuerpo_formateado = f"{int(cuerpo_limpio):,}".replace(',', '.')
        return f"{cuerpo_formateado}-{dv_esperado}"

    def clean_cantidad_ejemplares(self):
        cantidad = self.cleaned_data.get('cantidad_ejemplares')
        if cantidad is None:
            return cantidad

        if cantidad < 1 or cantidad > 3:
            raise ValidationError('La cantidad debe estar entre 1 y 3 ejemplares.')

        if cantidad > self.stock:
            raise ValidationError(
                f'Stock insuficiente. Solo quedan {self.stock} ejemplar(es) disponible(s).'
            )

        return cantidad