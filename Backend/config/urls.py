from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Congiguracion Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API para optimizacion de Distribucion",
      default_version='v1',
      description='''
        Esta API encuentra la ruta más eficiente para entregas de materiales de construccion de un punto a otro, a fin de optimizar la ruta de entrega, reducir el plazo y el coste de entrega.
    ''',
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="luca@gmail.com"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # apps
    path('admin/', admin.site.urls),
    path('api/v1/resource/', include(
        'ResourceManagement.api_resourceManagement.urls',)),
    path('api/v1/optimizer/', include(
        'Optimizer.api_optimizer.urls',)),
]