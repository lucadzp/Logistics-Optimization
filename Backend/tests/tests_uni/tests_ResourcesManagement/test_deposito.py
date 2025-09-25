from django.test import TestCase
from ResourceManagement.models import Deposito
from decimal import Decimal

class DepositoTestCase(TestCase):
    def setUp(self):
        # Configura el objeto Deposito que se utilizará en las pruebas
        self.deposito = Deposito.objects.create(
            nombre="Depósito Central",
            latitud='40.712776',
            longitud='-74.005974',
            direccion="123 Calle Falsa",
            numero_de_telefono="1234567890"
        )


    def test_deposito_creation(self):
        # Verifica la creación correcta del objeto
        deposito = Deposito.objects.get(nombre="Depósito Central")
        self.assertIsNotNone(deposito)
        self.assertEqual(deposito.nombre, "Depósito Central")
        self.assertEqual(deposito.latitud, Decimal('40.712776'))
        self.assertEqual(deposito.longitud, Decimal('-74.005974'))
        self.assertEqual(deposito.direccion, "123 Calle Falsa")
        self.assertEqual(deposito.numero_de_telefono, "1234567890")

    def test_deposito_str(self):
        # Verifica que el método __str__ devuelve el nombre correcto
        deposito = Deposito.objects.get(nombre="Depósito Central")
        self.assertEqual(str(deposito), "Depósito Central")

    def test_deposito_update(self):
        # Prueba la actualización del objeto Deposito
        deposito = Deposito.objects.get(nombre="Depósito Central")
        deposito.nombre = "Depósito Modificado"
        deposito.numero_de_telefono = "0987654321"
        deposito.save()

        # Recuperar de nuevo el objeto para asegurar que los cambios se guardaron
        updated_deposito = Deposito.objects.get(id=deposito.id)
        self.assertEqual(updated_deposito.nombre, "Depósito Modificado")
        self.assertEqual(updated_deposito.numero_de_telefono, "0987654321")

    def test_delete_deposito(self):
        # Comprobar existencia inicial del objeto
        deposito_id = self.deposito.id
        self.assertIsNotNone(Deposito.objects.get(id=deposito_id))

        # Eliminar el objeto
        self.deposito.delete()

        # Verificar que el objeto ha sido eliminado
        with self.assertRaises(Deposito.DoesNotExist):
            Deposito.objects.get(id=deposito_id)
