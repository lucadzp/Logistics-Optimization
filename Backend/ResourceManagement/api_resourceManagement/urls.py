from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DepositoViewSet, VehiculoViewSet, DemandaViewSet, PuntoDeEntregaViewSet


router = DefaultRouter()
router.register(r'depositos', DepositoViewSet, basename='Deposito')
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'demandas', DemandaViewSet)
router.register(r'puntosdeentrega', PuntoDeEntregaViewSet)


urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas del router en la raíz de la aplicación
]

