from django.contrib import admin
from .models import Deposito, Vehiculo, Demanda, PuntoDeEntrega

# Clase de administrador personalizada para el modelo Deposito
class DepositoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud', 'direccion', 'numero_de_telefono')

# Clase de administrador personalizada para el modelo Vehículo
class VehículoAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'capacidad_de_carga', 'deposito')

# Clase de administrador personalizada para el modelo Demanda
class DemandaAdmin(admin.ModelAdmin):
    list_display = ('peso_kg', 'fecha_creada', 'estado', 'deposito')

# Clase de administrador personalizada para el modelo PuntoDeEntrega
class PuntoDeEntregaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'latitud', 'longitud', 'demanda', 'numero_de_telefono')

# Registrando los modelos con las clases de administrador personalizadas
admin.site.register(Deposito, DepositoAdmin)
admin.site.register(Vehiculo, VehículoAdmin)
admin.site.register(Demanda, DemandaAdmin)





class PuntoDeEntregaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'latitud', 'longitud', 'demanda', 'estado', 'numero_de_telefono')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('demanda')
    

admin.site.register(PuntoDeEntrega, PuntoDeEntregaAdmin)



