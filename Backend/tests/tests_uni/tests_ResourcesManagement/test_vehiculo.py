from django.test import TestCase
from decimal import Decimal
from ResourceManagement.models import Deposito, Vehiculo

class VehiculoTestCase(TestCase):
    def setUp(self):
        # Configura el objeto Deposito que se utilizará en las pruebas de Vehiculo
        self.deposito = Deposito.objects.create(
            nombre="Depósito Central",
            latitud=Decimal('40.712776'),
            longitud=Decimal('-74.005974'),
            direccion="123 Calle Falsa",
            numero_de_telefono="1234567890"
        )

        # Creación del objeto Vehiculo
        self.vehiculo = Vehiculo.objects.create(
            matricula="ABC123",
            capacidad_de_carga=5000,
            deposito=self.deposito
        )

    def test_vehiculo_creation(self):
        # Verifica la creación correcta del objeto Vehiculo
        vehiculo = Vehiculo.objects.get(matricula="ABC123")
        self.assertIsNotNone(vehiculo)
        self.assertEqual(vehiculo.matricula, "ABC123")
        self.assertEqual(vehiculo.capacidad_de_carga, 5000)
        self.assertEqual(vehiculo.deposito, self.deposito)

    def test_vehiculo_update(self):
        # Prueba la actualización del objeto Vehiculo
        self.vehiculo.capacidad_de_carga = 4500
        self.vehiculo.save()

        # Recuperar de nuevo el objeto para asegurar que los cambios se guardaron
        updated_vehiculo = Vehiculo.objects.get(matricula="ABC123")
        self.assertEqual(updated_vehiculo.capacidad_de_carga, 4500)

    def test_vehiculo_delete(self):
        # Comprobar existencia inicial del objeto
        matricula = self.vehiculo.matricula
        self.assertIsNotNone(Vehiculo.objects.get(matricula=matricula))

        # Eliminar el objeto
        self.vehiculo.delete()

        # Verificar que el objeto ha sido eliminado
        with self.assertRaises(Vehiculo.DoesNotExist):
            Vehiculo.objects.get(matricula=matricula)

    def test_deposito_str(self):
        # Verifica que el método __str__ devuelve la representación correcta
        self.assertEqual(str(self.vehiculo), f"{self.vehiculo.matricula} ({self.vehiculo.capacidad_de_carga})")
