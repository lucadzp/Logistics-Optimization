from django.db import models


class Deposito(models.Model): 
    nombre = models.CharField(max_length=255, unique=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    numero_de_telefono = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.nombre}'


class Vehiculo(models.Model):
    matricula = models.CharField(max_length=255, primary_key=True) 
    capacidad_de_carga = models.IntegerField()
    deposito = models.ForeignKey(
        Deposito,
        on_delete=models.CASCADE,
    )
    estado = models.CharField(max_length=255, choices=[('disponible', 'Disponible'), ('no_disponible', 'No disponible')], default='disponible')

    def __str__(self):
        return f"{self.matricula} ({self.capacidad_de_carga})"


class Demanda(models.Model):
    peso_kg = models.DecimalField(max_digits=9, decimal_places=3)
    fecha_creada = models.DateTimeField(auto_now_add=True)
    descripción = models.TextField(blank=True)
    estado = models.CharField(max_length=255, choices=[('pendiente', 'Pendiente'), ('asignada', 'Asignada'), ('entregada', 'Entregada')], default='pendiente')
    deposito = models.ForeignKey(
        Deposito,
        on_delete=models.CASCADE,
    ) 

    def __str__(self):
        return f"{self.peso_kg}"


class PuntoDeEntrega(models.Model):
    cliente = models.CharField(max_length=255)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    demanda = models.ForeignKey(
        Demanda,
        on_delete=models.CASCADE,
    )
    numero_de_telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=255, choices=[('pendiente', 'Pendiente'), ('procesar', 'Procesar'), ('optimizado', 'Optimizado')], default='procesar')

    class Meta:
        verbose_name = 'Punto de Entrega'
        verbose_name_plural = 'Puntos de Entregas'

    def __str__(self):
        return f"{self.cliente} ({self.latitud}, {self.longitud})"
