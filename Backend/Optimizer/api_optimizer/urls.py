from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RutasDeEntregaViewSet, DetalleRutaDeEntregaViewSet
from .viewsOptimizer import optimizador

app_name = 'Optimizer'

router = DefaultRouter()
router.register(r'rutas', RutasDeEntregaViewSet)
router.register(r'detalles', DetalleRutaDeEntregaViewSet)

urlpatterns = [
    path('optimizar/', optimizador, name='optimizador'),
    path('', include(router.urls)),
]
