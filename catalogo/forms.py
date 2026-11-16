from django import forms

from .models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('nombre_cliente', 'rut', 'correo', 'cantidad_ejemplares')
        labels = {
            'nombre_cliente': 'Nombre del cliente',
            'rut': 'RUT',
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

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
