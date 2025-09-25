from rest_framework import viewsets
from ResourceManagement.models import Deposito, Vehiculo, Demanda, PuntoDeEntrega
from .serializers import DepositoSerializer, VehiculoSerializer, DemandaSerializer, PuntoDeEntregaSerializer
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema



class DepositoViewSet(viewsets.ModelViewSet):
    queryset = Deposito.objects.all()
    serializer_class = DepositoSerializer

    @swagger_auto_schema(tags=["Depositos"], operation_summary="Listar todos los depositos")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Depositos"], operation_summary="Listar un deposito")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Depositos"], operation_summary="Crear un nuevo deposito")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Depositos"], operation_summary="Eliminar un deposito")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Depositos"], operation_summary="Eliminar un deposito")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    @swagger_auto_schema(tags=["Vehiculos"], operation_summary="Listar todos los vehiculos")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Vehiculos"], operation_summary="Listar un vehiculo")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Vehiculos"], operation_summary="Crear un nuevo vehiculo")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Vehiculos"], operation_summary="Actualizar un vehiculo")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Vehiculos"], operation_summary="Eliminar un vehiculo")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class DemandaViewSet(viewsets.ModelViewSet):
    queryset = Demanda.objects.all()
    serializer_class = DemandaSerializer

    @swagger_auto_schema(tags=["Demandas"], operation_summary="Listar todas las demandas")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Demandas"], operation_summary="Listar una demanda")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Demandas"], operation_summary="Crear una nueva demanda")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Demandas"], operation_summary="Actualizar una demanda")
    def  partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Demandas"], operation_summary="Eliminar una demanda")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
        
class PuntoDeEntregaViewSet(viewsets.ModelViewSet):
    queryset = PuntoDeEntrega.objects.all()
    serializer_class = PuntoDeEntregaSerializer

    @swagger_auto_schema(tags=["Puntos de Entrega"], operation_summary="Listar todos los puntos de entrega")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Puntos de Entrega"], operation_summary="Listar un punto de entrega")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Puntos de Entrega"], operation_summary="Crear un nuevo punto de entrega")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Puntos de Entrega"], operation_summary="Actualizar un punto de entrega")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["Puntos de Entrega"], operation_summary="Eliminar un punto de entrega")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        demanda = serializer.validated_data['demanda']
        
        # Verifica si la demanda está pendiente
        if demanda.estado != 'pendiente':
            raise ValidationError("La demanda ya está asignada o entregada y no está disponible para un nuevo punto de entrega.")

        serializer.save()
        demanda.estado = 'asignada'
        demanda.save()