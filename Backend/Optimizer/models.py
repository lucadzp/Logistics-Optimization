from django.db import models
from ResourceManagement.models import PuntoDeEntrega

class RutasDeEntrega(models.Model):
    ruta_id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True) 
    distancia_total_recorrida = models.DecimalField(max_digits=9, decimal_places=3)

    def __str__(self):
        return f"Ruta {self.ruta_id} ({self.distancia_total_recorrida} km)"

class DetalleRutaDeEntrega(models.Model):
    ruta = models.ForeignKey(
        RutasDeEntrega,
        on_delete=models.CASCADE,
    )
    punto_de_entrega = models.ForeignKey(
        PuntoDeEntrega,
        on_delete=models.CASCADE,
    )
    orden_de_entrega = models.IntegerField()
    distancia_recorrida_al_punto = models.DecimalField(max_digits=9, decimal_places=3)
    demanda_a_entregar = models.DecimalField(max_digits=9, decimal_places=3)
    estado = models.CharField(max_length=255, choices=[('procesada', 'Procesada'), ('finalizada', 'Finalizada')], default='procesada')

    def __str__(self):
        return f"Punto {self.punto_de_entrega} ({self.orden_de_entrega})"
