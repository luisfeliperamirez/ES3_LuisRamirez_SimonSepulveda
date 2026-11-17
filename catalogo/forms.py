import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Reserva


class ReservaForm(forms.ModelForm):
    RUT_PATTERN = r'(?:[0-9]{1,8}|[0-9]{1,2}(?:\.[0-9]{3}){1,2})-?[0-9Kk]'

    class Meta:
        model = Reserva
        fields = ('nombre_cliente', 'rut', 'correo', 'cantidad_ejemplares')
        labels = {
            'nombre_cliente': 'Nombre del cliente',
            'rut': 'RUT (Ejemplo: 12345678-K)',
            'correo': 'Correo electrónico',
            'cantidad_ejemplares': 'Cantidad de ejemplares',
        }

    def __init__(self, *args, stock, **kwargs):
        super().__init__(*args, **kwargs)
        cantidad = self.fields['cantidad_ejemplares']
        self.fields['cantidad_ejemplares'] = forms.IntegerField(
            min_value=1,
            max_value=stock,
            label=cantidad.label,
            widget=cantidad.widget,
        )
        cantidad = self.fields['cantidad_ejemplares']
        cantidad.widget.attrs.update({'min': 1, 'max': stock})
        self.fields['rut'].widget.attrs.update({
            'pattern': self.RUT_PATTERN,
            'title': 'Ingresa un RUT con números y K como dígito verificador.',
        })

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_rut(self):
        rut = self.cleaned_data['rut'].strip()
        if not re.fullmatch(self.RUT_PATTERN, rut):
            raise ValidationError(
                'Ingresa un RUT con números y K como dígito verificador '
                '(por ejemplo, 12.345.678-K).'
            )
        return rut.upper()
