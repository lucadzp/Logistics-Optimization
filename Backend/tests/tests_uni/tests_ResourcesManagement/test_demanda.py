from django.test import TestCase
from decimal import Decimal
from ResourceManagement.models import Deposito, Demanda
import datetime

class DemandaTestCase(TestCase):
    def setUp(self):
        # Configurar un objeto Deposito para usar en las pruebas de Demanda
        self.deposito = Deposito.objects.create(
            nombre="Depósito Norte",
            latitud=Decimal('41.40338'),
            longitud=Decimal('2.17403'),
            direccion="Calle Ejemplo 456",
            numero_de_telefono="9876543210"
        )
        
        # Creación del objeto Demanda
        self.demanda = Demanda.objects.create(
            peso_kg=Decimal('150.500'),
            descripción="Paquete estándar",
            estado='pendiente',
            deposito=self.deposito
        )

    def test_demanda_creation(self):
        # Verifica la creación correcta del objeto Demanda
        demanda = Demanda.objects.get(id=self.demanda.id)
        self.assertIsNotNone(demanda)
        self.assertEqual(demanda.peso_kg, Decimal('150.500'))
        self.assertEqual(demanda.descripción, "Paquete estándar")
        self.assertEqual(demanda.estado, "pendiente")
        self.assertEqual(demanda.deposito, self.deposito)

    def test_demanda_update(self):
        # Prueba la actualización del objeto Demanda
        self.demanda.estado = 'asignada'
        self.demanda.save()

        # Recuperar de nuevo el objeto para asegurar que los cambios se guardaron
        updated_demanda = Demanda.objects.get(id=self.demanda.id)
        self.assertEqual(updated_demanda.estado, 'asignada')

    def test_demanda_delete(self):
        # Comprobar existencia inicial del objeto
        demanda_id = self.demanda.id
        self.assertIsNotNone(Demanda.objects.get(id=demanda_id))

        # Eliminar el objeto
        self.demanda.delete()

        # Verificar que el objeto ha sido eliminado
        with self.assertRaises(Demanda.DoesNotExist):
            Demanda.objects.get(id=demanda_id)

    def test_demanda_str(self):
        # Verifica que el método __str__ devuelve la representación correcta
        self.assertEqual(str(self.demanda), "150.500")
