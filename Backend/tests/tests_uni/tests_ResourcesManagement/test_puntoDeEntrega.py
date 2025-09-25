from django.test import TestCase
from decimal import Decimal
from ResourceManagement.models import Deposito, Demanda, PuntoDeEntrega
import datetime

class PuntoDeEntregaTestCase(TestCase):
    def setUp(self):
        # Configuración inicial de un objeto Deposito
        self.deposito = Deposito.objects.create(
            nombre="Depósito Central",
            latitud=Decimal('40.712776'),
            longitud=Decimal('-74.005974'),
            direccion="123 Calle Principal",
            numero_de_telefono="1122334455"
        )

        # Creación de un objeto Demanda asociado al Deposito
        self.demanda = Demanda.objects.create(
            peso_kg=Decimal('120.300'),
            descripción="Envío urgente",
            estado='pendiente',
            deposito=self.deposito
        )

        # Creación de un objeto PuntoDeEntrega asociado a la Demanda
        self.punto_entrega = PuntoDeEntrega.objects.create(
            cliente="Juan Pérez",
            latitud=Decimal('40.714776'),
            longitud=Decimal('-73.998974'),
            demanda=self.demanda,
            numero_de_telefono="5566778899"
        )

    def test_punto_de_entrega_creation(self):
        # Verificar la correcta creación del objeto
        punto_entrega = PuntoDeEntrega.objects.get(id=self.punto_entrega.id)
        self.assertIsNotNone(punto_entrega)
        self.assertEqual(punto_entrega.cliente, "Juan Pérez")
        self.assertEqual(punto_entrega.latitud, Decimal('40.714776'))
        self.assertEqual(punto_entrega.longitud, Decimal('-73.998974'))
        self.assertEqual(punto_entrega.numero_de_telefono, "5566778899")
        self.assertEqual(punto_entrega.demanda, self.demanda)

    def test_punto_de_entrega_update(self):
        # Prueba la actualización del objeto
        self.punto_entrega.cliente = "Ana Gómez"
        self.punto_entrega.save()

        updated_punto_entrega = PuntoDeEntrega.objects.get(id=self.punto_entrega.id)
        self.assertEqual(updated_punto_entrega.cliente, "Ana Gómez")

    def test_punto_de_entrega_delete(self):
        # Comprobar existencia inicial y eliminar el objeto
        punto_entrega_id = self.punto_entrega.id
        self.assertIsNotNone(PuntoDeEntrega.objects.get(id=punto_entrega_id))
        self.punto_entrega.delete()

        # Verificar que el objeto ha sido eliminado
        with self.assertRaises(PuntoDeEntrega.DoesNotExist):
            PuntoDeEntrega.objects.get(id=punto_entrega_id)

    def test_punto_de_entrega_str(self):
        # Verifica que el método __str__ devuelve la representación correcta
        self.assertEqual(str(self.punto_entrega), "Juan Pérez (40.714776, -73.998974)")
