from django.contrib import admin
from Optimizer.models import RutasDeEntrega, DetalleRutaDeEntrega

class RutasDeEntregaAdmin(admin.ModelAdmin):
    list_display = ('ruta_id', 'fecha_creacion', 'distancia_total_recorrida')

# Clase de administrador personalizada para el modelo DetalleRutaDeEntrega
class DetalleRutaDeEntregaAdmin(admin.ModelAdmin):
    list_display = ('ruta', 'punto_de_entrega', 'orden_de_entrega', 'distancia_recorrida_al_punto', 'demanda_a_entregar')

admin.site.register(RutasDeEntrega, RutasDeEntregaAdmin)
admin.site.register(DetalleRutaDeEntrega, DetalleRutaDeEntregaAdmin)