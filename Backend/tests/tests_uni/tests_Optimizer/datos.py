from django.db.models import Sum
from ResourceManagement.models import Deposito, Vehiculo, Demanda, PuntoDeEntrega
from decimal import Decimal
from django.utils import timezone
from Optimizer.create_distance_matrix import calcular_distancia


def crear_datos():
    # Crear un depósito
    deposito = Deposito.objects.create(
        nombre="Depósito Central",
        latitud=Decimal("-27.31171"),
        longitud=Decimal("-55.87741"),
        direccion="Calle Falsa 123, Ciudad de México",
        numero_de_telefono="5551234567"
    )

    for i in range(1,6):
                # Creación del objeto Vehículo
        vehiculo = Vehiculo.objects.create(
            matricula=f"ABC12{i}",
            capacidad_de_carga=5000,
            deposito=deposito
        )

    # Crear demandas y puntos de entrega
    for i in range(1, 5):
        # Crear una demanda
        demanda = Demanda.objects.create(
            peso_kg=Decimal(f"{i*10}.500"),
            fecha_creada=timezone.now(),
            descripción=f"Descripción de la demanda {i}",
            estado='pendiente',
            deposito=deposito
        )
        
        # Crear un punto de entrega para cada demanda
        locations = [
            (-25.28646, -57.647),
            (-25.50972, -54.61111),
            (-25.33968, -57.50879),
            (-22.54722, -55.73333),
            (-25.3552, -57.44545),
        ]
        PuntoDeEntrega.objects.create(
            cliente=f"Cliente {i+1}",
            latitud=Decimal(f"{locations[i][0]}"),  # Usar el valor de latitud de la tupla en locations
            longitud=Decimal(f"{locations[i][1]}"),  # Usar el valor de longitud de la tupla en locations
            demanda=demanda,
            numero_de_telefono=f"555987654{i+1}"
        )

    print("Datos creados correctamente.")


def obtener_datos():
    data = {}
    
    # Obtener todos los depósitos, asumimos que solo hay uno para el ejemplo
    deposito = Deposito.objects.first()
    
    # Obtener vehículos asociados al depósito y sus capacidades
    vehiculos = Vehiculo.objects.filter(deposito=deposito)
    data["vehicle_capacities"] = [v.capacidad_de_carga for v in vehiculos]
    
    # Ubicaciones y demandas
    locations = [(float(deposito.latitud), float(deposito.longitud))]
    demands = [0]  # El depósito no tiene demanda
    
    # Obtener todas las demandas y sus correspondientes puntos de entrega
    demandas = Demanda.objects.all()
    for demanda in demandas:
        puntos_entrega = PuntoDeEntrega.objects.filter(demanda=demanda)
        for punto in puntos_entrega:
            locations.append((punto.latitud, punto.longitud))
            demands.append(demanda.peso_kg)
    
    data["locations"] = locations
    data["demands"] = demands
    data["num_vehicles"] = len(vehiculos)
    data["distance_matrix"] = calcular_distancia(data["locations"])
    data["depot"] = 0  # El índice del depósito en la lista de ubicacione
    return data