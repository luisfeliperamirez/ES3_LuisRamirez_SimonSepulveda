from django.urls import reverse
from django.test import TestCase

from .forms import ReservaForm
from .models import Comic, Editorial, Reserva


class ComprarViewTests(TestCase):
    def setUp(self):
        editorial = Editorial.objects.create(nombre='Editorial de prueba')
        self.comic = Comic.objects.create(
            titulo='Cómic de prueba',
            editorial=editorial,
            autor='Autor de prueba',
            precio=5000,
            stock=5,
            portada='portadas/prueba.png',
        )

    def test_detalle_enlaza_al_formulario_de_compra_del_comic(self):
        response = self.client.get(
            reverse('catalogo:detalle_comic', args=[self.comic.pk])
        )
        self.assertContains(
            response,
            reverse('catalogo:comprar', args=[self.comic.pk]),
        )

    def test_compra_registra_reserva_redirige_y_actualiza_stock(self):
        response = self.client.post(
            reverse('catalogo:comprar', args=[self.comic.pk]),
            {
                'nombre_cliente': 'Cliente de prueba',
                'rut': '12.345.678-5',
                'correo': 'cliente@example.com',
                'cantidad_ejemplares': 2,
            },
        )

        self.assertEqual(Reserva.objects.count(), 1)
        reserva = Reserva.objects.get()
        self.assertRedirects(
            response,
            reverse('catalogo:comprobante', args=[reserva.codigo]),
        )
        self.comic.refresh_from_db()
        self.assertEqual(self.comic.stock, 3)

    def test_no_permite_reservar_mas_de_tres_ni_mas_que_el_stock(self):
        response = self.client.post(
            reverse('catalogo:comprar', args=[self.comic.pk]),
            {
                'nombre_cliente': 'Cliente de prueba',
                'rut': '12.345.678-5',
                'correo': 'cliente@example.com',
                'cantidad_ejemplares': 4,
            },
        )
        self.assertIn('cantidad_ejemplares', response.context['form'].errors)
        self.assertEqual(Reserva.objects.count(), 0)

    def test_rut_rechaza_digito_verificador_incorrecto(self):
        form = ReservaForm({
            'nombre_cliente': 'Cliente de prueba',
            'rut': '12.345.678-9',
            'correo': 'cliente@example.com',
            'cantidad_ejemplares': 1,
        }, stock=5)
        self.assertFalse(form.is_valid())
        self.assertIn('rut', form.errors)

    def test_rut_acepta_k_como_digito_verificador_valido(self):
        form = ReservaForm({
            'nombre_cliente': 'Cliente de prueba',
            'rut': '18.613.267-k',
            'correo': 'cliente@example.com',
            'cantidad_ejemplares': 1,
        }, stock=5)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['rut'], '18.613.267-K')