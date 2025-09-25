from rest_framework import serializers
from Optimizer.models import RutasDeEntrega, DetalleRutaDeEntrega
from ResourceManagement.models import PuntoDeEntrega, Demanda, Deposito

class RutasDeEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutasDeEntrega
        fields = ['ruta_id', 'fecha_creacion', 'distancia_total_recorrida']


class DepositoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposito
        fields = ['id', 'nombre', 'latitud', 'longitud', 'direccion', 'numero_de_telefono']
        ref_name = 'depositoOptimizado'

class DemandaSerializer(serializers.ModelSerializer):
    deposito = DepositoSerializer(read_only=True)
    class Meta:
        model = Demanda
        fields = ['id', 'peso_kg', 'fecha_creada', 'descripción', 'estado', 'deposito']
        ref_name = 'demandaOptimizada'

class PuntoDeEntregaSerializer(serializers.ModelSerializer):
    demanda = DemandaSerializer(read_only=True)
    class Meta:
        model = PuntoDeEntrega  # Ajusta esto al nombre de tu modelo de punto de entrega
        fields = [
            'id',
            'cliente',
            'latitud',
            'longitud',
            'demanda',
            'estado',
            'numero_de_telefono'
        ]
        depth = 1
        ref_name = 'puntoDeEntregaOptimizado'


class DetalleRutaDeEntregaSerializer(serializers.ModelSerializer):
    ruta = serializers.PrimaryKeyRelatedField(read_only=True)
    punto_de_entrega = PuntoDeEntregaSerializer(read_only=True)

    class Meta:
        model = DetalleRutaDeEntrega
        fields = [
            'ruta',
            'punto_de_entrega',
            'orden_de_entrega',
            'distancia_recorrida_al_punto',
            'demanda_a_entregar',
            'estado',
        ]
        dephth = 1


