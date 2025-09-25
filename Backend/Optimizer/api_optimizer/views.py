from rest_framework import viewsets, mixins
from Optimizer.models import RutasDeEntrega, DetalleRutaDeEntrega
from .serializers import RutasDeEntregaSerializer, DetalleRutaDeEntregaSerializer
from rest_framework.response import Response

class RutasDeEntregaViewSet(mixins.ListModelMixin, 
                            mixins.RetrieveModelMixin, 
                            viewsets.GenericViewSet):
    queryset = RutasDeEntrega.objects.all()
    serializer_class = RutasDeEntregaSerializer

class DetalleRutaDeEntregaViewSet(mixins.ListModelMixin, 
                                  mixins.RetrieveModelMixin, 
                                  viewsets.GenericViewSet):
    queryset = DetalleRutaDeEntrega.objects.all()
    serializer_class = DetalleRutaDeEntregaSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Puedes realizar cualquier manipulación adicional de datos aquí
        # antes de serializarlos.

        serializer = self.get_serializer(queryset, many=True)
        rutas = []
        trayectorias = {}
        for ruta in serializer.data:
            print(ruta)
            deposito = ruta['punto_de_entrega']['demanda']['deposito']
            punto_de_entrega = ruta['punto_de_entrega']
            data = {
                    "Ruta": ruta['ruta'],
                    "Deposito": {
                        "latitud": deposito['latitud'],
                        "longitud": deposito['longitud']
                    },
                    "Punto_de_entrega": {
                        "latitud": punto_de_entrega['latitud'],
                        "longitud": punto_de_entrega['longitud']
                    },
                    "Cliente": punto_de_entrega['cliente'],
                    "Demanda": punto_de_entrega['demanda']['peso_kg'],
                    "Orden_de_entrega": ruta['orden_de_entrega'],
                    "Distancia": ruta['distancia_recorrida_al_punto']
                }
            if ruta['ruta'] in trayectorias:
                trayectorias[ruta['ruta']].append(data)
            else:
                trayectorias[ruta['ruta']] = [data]
        for tryectoria in trayectorias:
            rutas.append(trayectorias[tryectoria])
        return Response(rutas)




    