from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal
from ResourceManagement.models import Deposito, Vehiculo, Demanda, PuntoDeEntrega
from datetime import datetime
import pytz

class DepositoTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()

    def test_create_deposito(self):
        data = {
            'nombre': 'Deposito1',
            'latitud': '-27.329040',
            'longitud': '-55.866783',
            'direccion': 'Calle Principal',
            'numero_de_telefono': '123456789',
        }

        url = "http://127.0.0.1:8000/api/v1/resource/depositos/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        deposito = Deposito.objects.get(pk=response.data['id'])
        self.assertEqual(deposito.nombre, data['nombre'])
        self.assertEqual(deposito.latitud, Decimal(data['latitud']))
        self.assertEqual(deposito.longitud, Decimal(data['longitud']))
        self.assertEqual(deposito.direccion, data['direccion'])
        self.assertEqual(deposito.numero_de_telefono, data['numero_de_telefono'])

    def test_update_deposito(self):
        deposito = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

        data = {
            'nombre': 'Deposito2',
            'latitud': '-27.329040',
            'longitud': '-55.866783',
            'direccion': 'Calle Principal',
            'numero_de_telefono': '123456789',
        }

        url = f"http://127.0.0.1:8000/api/v1/resource/depositos/{deposito.id}/"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        deposito.refresh_from_db()
        self.assertEqual(deposito.nombre, data['nombre'])

    
    def test_delete_deposito(self):
        deposito = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

        url = f"http://127.0.0.1:8000/api/v1/resource/depositos/{deposito.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class VehiculoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.deposito = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

    def test_create_vehiculo(self):
        data = {
            'matricula': 'ABC123',
            'capacidad_de_carga': 1000,
            'deposito': 1,
            'estado': 'disponible',
        }

        url = "http://127.0.0.1:8000/api/v1/resource/vehiculos/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        vehiculo = Vehiculo.objects.get(pk=response.data['matricula'])
        self.assertEqual(vehiculo.matricula, data['matricula'])
        self.assertEqual(vehiculo.capacidad_de_carga, data['capacidad_de_carga'])
        self.assertEqual(vehiculo.deposito.id, data['deposito'])
        self.assertEqual(vehiculo.estado, data['estado'])


    def test_update_vehiculo(self):
        vehiculo = Vehiculo.objects.create(
            matricula='ABC123',
            capacidad_de_carga=1000,
            deposito=self.deposito,
            estado='disponible',
        )

        data = {
            'matricula': 'ABC123',
            'capacidad_de_carga': 2000,
            'deposito': 1,
            'estado': 'no_disponible',
        }

        url = f"http://127.0.0.1:8000/api/v1/resource/vehiculos/{vehiculo.matricula}/"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vehiculo.refresh_from_db()
        self.assertEqual(vehiculo.capacidad_de_carga, data['capacidad_de_carga'])
        self.assertEqual(vehiculo.deposito.id, data['deposito'])
        self.assertEqual(vehiculo.estado, data['estado'])

    def test_delete_vehiculo(self):
        vehiculo = Vehiculo.objects.create(
            matricula='ABC123',
            capacidad_de_carga=1000,
            deposito=self.deposito,
            estado='disponible',
        )

        url = f"http://127.0.0.1:8000/api/v1/resource/vehiculos/{vehiculo.matricula}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class DemandaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.deposito = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

    def test_create_demanda(self):
        data = {
            'peso_kg': 1000,
            'fecha_creada': '2022-01-01T00:00:00Z',
            'descripción': 'Descripción',
            'estado': 'pendiente',
            'deposito': 1,
        }

        url = "http://127.0.0.1:8000/api/v1/resource/demandas/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        demanda = Demanda.objects.get(pk=response.data['id'])
        self.assertEqual(demanda.peso_kg, data['peso_kg'])
        fecha_creada = datetime.strptime(data['fecha_creada'], '%Y-%m-%dT%H:%M:%SZ')
        fecha_creada = fecha_creada.replace(tzinfo=pytz.UTC)      
        self.assertEqual(demanda.descripción, data['descripción'])
        self.assertEqual(demanda.estado, data['estado'])
        self.assertEqual(demanda.deposito.id, data['deposito'])


    def test_update_demanda(self):
        demanda = Demanda.objects.create(
            peso_kg=1000,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito,
        )

        data = {
            'peso_kg': 2000,
            'fecha_creada': '2022-01-01T00:00:00Z',
            'descripción': 'Descripción',
            'estado': 'asignada',
            'deposito': 1,
        }

        url = f"http://127.0.0.1:8000/api/v1/resource/demandas/{demanda.id}/"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        demanda.refresh_from_db()
        self.assertEqual(demanda.peso_kg, data['peso_kg'])
    
    def test_delete_demanda(self):
        demanda = Demanda.objects.create(
            peso_kg=1000,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito,
        )

        url = f"http://127.0.0.1:8000/api/v1/resource/demandas/{demanda.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    


class PuntoDeEntregaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.deposito = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

        self.demanda = Demanda.objects.create(
            peso_kg=1000,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito,
        )

    def test_create_punto_de_entrega(self):
        data = {
            'cliente': 'Cliente1',
            'latitud': '-27.329040',
            'longitud':'-55.866783',
            'demanda': 1,
            'numero_de_telefono': '123456789',
            'estado': 'pendiente',
        }

        url = "http://127.0.0.1:8000/api/v1/resource/puntosdeentrega/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        punto_de_entrega = PuntoDeEntrega.objects.get(pk=response.data['id'])
        self.assertEqual(punto_de_entrega.cliente, data['cliente'])
        self.assertEqual(punto_de_entrega.latitud, Decimal(data['latitud']))
        self.assertEqual(punto_de_entrega.longitud, Decimal(data['longitud']))
        self.assertEqual(punto_de_entrega.demanda.id, data['demanda'])
        self.assertEqual(punto_de_entrega.numero_de_telefono, data['numero_de_telefono'])
        self.assertEqual(punto_de_entrega.estado, data['estado'])

    def test_update_punto_de_entrega(self):
        punto_de_entrega = PuntoDeEntrega.objects.create(
            cliente='Cliente1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            demanda=self.demanda,
            numero_de_telefono='123456789',
            estado='pendiente',
        )

        data = {
            'cliente': 'Cliente2',
            'latitud': '-27.329040',
            'longitud': '-55.866783',
            'demanda': 1,
            'numero_de_telefono': '123456789',
            'estado': 'procesar',
        }

        url = f"http://127.0.0.1:8000/api/v1/resource/puntosdeentrega/{punto_de_entrega.id}/"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_delete_punto_de_entrega(self):
        punto_de_entrega = PuntoDeEntrega.objects.create(
            cliente='Cliente1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            demanda=self.demanda,
            numero_de_telefono='123456789',
            estado='pendiente',
        )

        url = f"http://127.0.0.1:8000/api/v1/resource/puntosdeentrega/{punto_de_entrega.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




class DepositoFailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.deposito1 = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )
        

    def test_create_deposito_fail(self):
        data = {
            'nombre': 'Deposito1',
            'latitud': '-27.329040',
            'longitud': '-55.866783',
            'direccion': 'Calle Principal',
            'numero_de_telefono': '123456789',
        }

        url = "http://127.0.0.1:8000/api/v1/resource/depositos/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_deposito_fail(self):
        data = {
            'nombre': 'Deposito2',
            'latitud': '-273290.40',
            'longitud': '-55.866783',
            'direccion': 'Calle Principal',
            'numero_de_telefono': '123456789',
        }

        url = f"http://127.0.0.1:8000/api/v1/resource/depositos/{self.deposito1.id}/"
        response = self.client.put(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_deposito_fail(self):
        url = f"http://127.0.0.1:8000/api/v1/resource/depositos/{self.deposito1.id}/"

        response = self.client.delete(url)

        url = f"http://127.0.0.1:8000/api/v1/resource/depositos/{self.deposito1.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VehiculoFailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.deposito1 = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

        self.vehiculo1 = Vehiculo.objects.create(
            matricula='ABC123',
            capacidad_de_carga=1000,
            deposito=self.deposito1
        )

    def test_create_vehiculo_fail(self):
        data = {
            'placa': 'ABC123',
            'capacidad_maxima': 1000,
            'deposito': self.deposito1.id,
        }

        url = "http://127.0.0.1:8000/api/v1/resource/vehiculos/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_vehiculo_fail(self):
        data = {
            'placa': 'DEF456',
            'capacidad_maxima': 2000,
            'deposito': self.deposito1.id,
        }

        url = f"http://127.0.0.1:8000/api/v1/resource/vehiculos/{self.vehiculo1.matricula}/"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class DemandaFailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.deposito1 = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

        self.vehiculo1 = Vehiculo.objects.create(
            matricula='ABC123',
            capacidad_de_carga=9999,
            deposito=self.deposito1
        )

        self.demanda1 = Demanda.objects.create(
            peso_kg=1234,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito1,
        )

    def test_create_demanda_fail(self):
        data = {
            'peso_kg': 150.588,
            'descripción': 'Paquete estándar',
            'deposito': 2,
            'estado': 'asignada'
        }

        url = "http://127.0.0.1:8000/api/v1/resource/demandas/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_demanda_fail(self):
        data = {
            'peso_kg': 150,
            'descripción': 'Paquete estándar',
            'deposito': 2,
            'estado': 'asignada'
        }

        url = f"http://127.0.0.1:8000/api/v1/resource/demandas/{self.demanda1.id}/"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class PuntoDeEntregaFailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.deposito1 = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

        self.vehiculo1 = Vehiculo.objects.create(
            matricula='ABC123',
            capacidad_de_carga=9999,
            deposito=self.deposito1
        )

        self.demanda1 = Demanda.objects.create(
            peso_kg=1234,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito1,
        )


    def test_create_punto_de_entrega_fail(self):
        data = {
            'cliente': 'Cliente1',
            'latitud': '-27.329040',
            'longitud': '-191.866783',
            'demanda': 1,
            'numero_de_telefono': '123456789'
        }

        url = "http://127.0.0.1:8000/api/v1/resource/puntosdeentrega/"
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)