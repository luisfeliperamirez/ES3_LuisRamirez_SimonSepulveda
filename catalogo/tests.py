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

    def test_comprar_muestra_campos_del_formulario(self):
        response = self.client.get(
            reverse('catalogo:comprar', args=[self.comic.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comprar.html')
        self.assertContains(response, 'Nombre del cliente')
        self.assertContains(response, 'RUT')
        self.assertContains(response, 'Correo electrónico')
        self.assertContains(response, 'Cantidad de ejemplares')

    def test_compra_registra_reserva_y_actualiza_stock(self):
        response = self.client.post(
            reverse('catalogo:comprar', args=[self.comic.pk]),
            {
                'nombre_cliente': 'Cliente de prueba',
                'rut': '12345678-9',
                'correo': 'cliente@example.com',
                'cantidad_ejemplares': 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reserva.objects.count(), 1)
        self.assertEqual(Reserva.objects.get().comic, self.comic)
        self.comic.refresh_from_db()
        self.assertEqual(self.comic.stock, 3)
        self.assertContains(response, 'Reserva registrada')

    def test_no_permite_reservar_mas_unidades_que_el_stock(self):
        response = self.client.post(
            reverse('catalogo:comprar', args=[self.comic.pk]),
            {
                'nombre_cliente': 'Cliente de prueba',
                'rut': '12345678-9',
                'correo': 'cliente@example.com',
                'cantidad_ejemplares': 6,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('cantidad_ejemplares', response.context['form'].errors)
        self.assertEqual(Reserva.objects.count(), 0)
        self.comic.refresh_from_db()
        self.assertEqual(self.comic.stock, 5)

    def test_rut_rechaza_letras_distintas_de_k(self):
        response = self.client.post(
            reverse('catalogo:comprar', args=[self.comic.pk]),
            {
                'nombre_cliente': 'Cliente de prueba',
                'rut': '123A5678-9',
                'correo': 'cliente@example.com',
                'cantidad_ejemplares': 1,
            },
        )

        self.assertIn('rut', response.context['form'].errors)
        self.assertEqual(Reserva.objects.count(), 0)

    def test_rut_acepta_k_como_digito_verificador(self):
        form = ReservaForm({
            'nombre_cliente': 'Cliente de prueba',
            'rut': '12.345.678-k',
            'correo': 'cliente@example.com',
            'cantidad_ejemplares': 1,
        }, stock=5)

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['rut'], '12.345.678-K')
