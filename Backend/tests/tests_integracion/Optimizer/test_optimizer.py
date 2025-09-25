from django.test import TestCase
from Optimizer.models import RutasDeEntrega, DetalleRutaDeEntrega
from ResourceManagement.models import Deposito, Vehiculo, Demanda, PuntoDeEntrega
from Optimizer.solvingCVRP import main as run_optimization
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.response import Response


class OptimizerTestCase(TestCase):

    def setUp(self):
        self.deposito = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

        self.vehiculo1 = Vehiculo.objects.create(
            matricula='AAA331',
            capacidad_de_carga=1500,
            deposito=self.deposito
        )

        self.vehiculo2 = Vehiculo.objects.create(
            matricula='AAA332',
            capacidad_de_carga=2500,
            deposito=self.deposito
        )

        self.vehiculo3 = Vehiculo.objects.create(
            matricula='AAA333',
            capacidad_de_carga=2500,
            deposito=self.deposito
        )

        self.vehiculo4 = Vehiculo.objects.create(
            matricula='AAA334',
            capacidad_de_carga=15,
            deposito=self.deposito
        )

        self.demanda1 = Demanda.objects.create(
            peso_kg=1000,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito,
        )

        self.demanda2 = Demanda.objects.create(
            peso_kg=1000,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito,
        )

        self.demanda3 = Demanda.objects.create(
            peso_kg=1000,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito,
        )

        self.demanda4 = Demanda.objects.create(
            peso_kg=1000,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito,
        )

        self.demanda5 = Demanda.objects.create(
            peso_kg=1000,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito,
        )

        

        self.client = APIClient()
        
        punto_de_entrega1 = {
            "cliente": "Cliente 1",
            "latitud": "-27.325438", 
            "longitud": "-55.873748",
            "demanda": 1,
            "numero_de_telefono": "0995380999"
        }

        punto_de_entrega2 = {
            "cliente": "Cliente 2",
            "latitud": "-27.325068", 
            "longitud": "-55.870423",
            "demanda": 2,
            "numero_de_telefono": "0995380999"
        }

        punto_de_entrega3 = {
            "cliente": "Cliente 3",
            "latitud": "-27.325114", 
            "longitud": "-55.867219",
            "demanda": 3,
            "numero_de_telefono": "0995380999"
        }

        punto_de_entrega4 = {
            "cliente": "Cliente 4",
            "latitud": "-27.325114", 
            "longitud": "-55.867219",
            "demanda": 4,
            "numero_de_telefono": "0995380999"
        }

        punto_de_entrega5 = {
            "cliente": "Cliente 5",
            "latitud": "-27.325114", 
            "longitud": "-55.867219",
            "demanda": 5,
            "numero_de_telefono": "0995380999"
        }

        urlPuntoDeEntrega = "http://127.0.0.1:8000/api/v1/resource/puntosdeentrega/"
        self.client.post(urlPuntoDeEntrega, punto_de_entrega1, format='json')
        self.client.post(urlPuntoDeEntrega, punto_de_entrega2, format='json')
        self.client.post(urlPuntoDeEntrega, punto_de_entrega3, format='json')
        self.client.post(urlPuntoDeEntrega, punto_de_entrega4, format='json')
        self.client.post(urlPuntoDeEntrega, punto_de_entrega5, format='json')
        

        self.url = 'http://127.0.0.1:8000/api/v1/optimizer/optimizar/'


    def test_optimizar(self):
        params = {
            "depositoId": self.deposito.id
        }
        response = self.client.get(self.url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OptimizerTestCaseFail(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = 'http://127.0.0.1:8000/api/v1/optimizer/optimizar/'

        self.deposito = Deposito.objects.create(
            nombre='Deposito1',
            latitud=Decimal('-27.329040'),
            longitud=Decimal('-55.866783'),
            direccion='Calle Principal',
            numero_de_telefono='123456789',
        )

        self.vehiculo1 = Vehiculo.objects.create(
            matricula='AAA331',
            capacidad_de_carga=15,
            deposito=self.deposito
        )


        self.demanda1 = Demanda.objects.create(
            peso_kg=1000,
            fecha_creada='2022-01-01T00:00:00Z',
            descripción='Descripción',
            estado='pendiente',
            deposito=self.deposito,
        )


        self.punto_de_entrega1 = PuntoDeEntrega.objects.create(
            cliente='Cliente 1',
            latitud=Decimal('-27.309864'),
            longitud=Decimal('-55.886429'),
            demanda=self.demanda1,
            numero_de_telefono='0995380999'
        )



    def test_optimizar_fail_parmas(self):
        params = {
            "depositoId": 0
        }
        response = self.client.get(self.url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_optimizar_fail_no_params(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

{
    "cliente": "Cliente 1",
    "latitud": "-27.325438", 
    "longitud": "-55.873748",
    "demanda": 1,
    "numero_de_telefono": "0995380999"
}

{
    "cliente": "Cliente 2",
    "latitud": "-27.325068", 
    "longitud": "-55.870423",
    "demanda": 2,
    "numero_de_telefono": "0995380999"
}

{
    "cliente": "Cliente 3",
    "latitud": "-27.325114", 
    "longitud": "-55.867219",
    "demanda": 3,
    "numero_de_telefono": "0995380999"
}

{
    "cliente": "Cliente 4",
    "latitud": "-27.322719", 
    "longitud": "-55.864315",
    "demanda": 4,
    "numero_de_telefono": "0995380999"
}

{
    "cliente": "Cliente 5",
    "latitud": "-27.324239", 
    "longitud": "-55.857556",
    "demanda": 5,
    "numero_de_telefono": "0995380999"
}

{
    "cliente": "Cliente 6",
    "latitud": "-27.326043", 
    "longitud": "-55.858514",
    "demanda": 6,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 7",
    "latitud": "-27.328156", 
    "longitud": "-55.856831",
    "demanda": 7,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 8",
    "latitud": "-27.329677,", 
    "longitud": "-55.860341",
    "demanda": 8,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 9",
    "latitud": "-27.332511", 
    "longitud": "-55.863039",
    "demanda": 9,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 10",
    "latitud": "27.334995,", 
    "longitud": "-55.862620",
    "demanda": 10,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 11",
    "latitud": "-27.339064", 
    "longitud": "-55.861050",
    "demanda": 11,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 12",
    "latitud": "-27.340482", 
    "longitud": "-55.863650",
    "demanda": 12,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 13",
    "latitud": "-27.343679", 
    "longitud": "-55.865645",
    "demanda": 13,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 14",
    "latitud": "-27.345336", 
    "longitud": "-55.861569",
    "demanda": 14,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 15",
    "latitud": "-27.343063", 
    "longitud": "-55.866809",
    "demanda": 15,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 16",
    "latitud": "-27.335769,", 
    "longitud": "-55.870831",
    "demanda": 16,
    "numero_de_telefono": "0995380999"
}
{
    "cliente": "Cliente 17",
    "latitud": "-27.331055", 
    "longitud": "-55.872395",
    "demanda": 17,
    "numero_de_telefono": "0995380999"
}


        # self.punto_de_entrega = PuntoDeEntrega.objects.create(
        #     cliente='Cliente 1',
        #     latitud=Decimal('-27.325438'),
        #     longitud=Decimal('-55.873748'),
        #     demanda=self.demanda1,
        #     numero_de_telefono='0995380999',
        # )

        # self.punto_de_entrega2 = PuntoDeEntrega.objects.create(
        #     cliente='Cliente 2',
        #     latitud=Decimal('27.325068'),
        #     longitud=Decimal('-55.870423'),
        #     demanda=self.demanda2,
        #     numero_de_telefono='0995380999',
        # )

        # self.punto_de_entrega3 = PuntoDeEntrega.objects.create(
        #     cliente='Cliente 3',
        #     latitud=Decimal('-27.325114'),
        #     longitud=Decimal('-55.867219'),
        #     demanda=self.demanda3,
        #     numero_de_telefono='0995380999',
        # )

        # self.punto_de_entrega4 = PuntoDeEntrega.objects.create(
        #     cliente='Cliente 4',
        #     latitud=Decimal('-27.322719'),
        #     longitud=Decimal('-55.864315'),
        #     demanda=self.demanda4,
        #     numero_de_telefono='0995380999',
        # )

        # self.punto_de_entrega5 = PuntoDeEntrega.objects.create(
        #     cliente='Cliente 5',
        #     latitud=Decimal('-27.324239'),
        #     longitud=Decimal('-55.857556'),
        #     demanda=self.demanda5,
        #     numero_de_telefono='0995380999',
        # )