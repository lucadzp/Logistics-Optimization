from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from ResourceManagement.models import Deposito,PuntoDeEntrega, Demanda, Vehiculo
from Optimizer.models import RutasDeEntrega, DetalleRutaDeEntrega
from Optimizer.create_distance_matrix import calcular_distancia
from Optimizer.solvingCVRP import main



@api_view(['GET'])
def optimizador(request):
    id = request.query_params.get('depositoId',1)
    if(id is None):
        return Response({'error': 'No se ha especificado el deposito'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Paso 1: Obtener los datos necesarios del depósito y sus vehículos
        deposito, vehiculos = obtener_datos_deposito_y_vehiculos(id)
        # Paso 2: Obtener ubicaciones y demandas asignadas al depósito
        ubicaciones, ids_ubicaciones, demandas = obtener_ubicaciones_y_demandas(deposito)
        # Paso 3: Preparar los datos para la optimización
        data = preparar_datos_optimizacion(ubicaciones, ids_ubicaciones, demandas, vehiculos)
        # Paso 4: Ejecutar la optimización
        resultado_optimizacion = ejecutar_optimizacion(data)
        if resultado_optimizacion is not None:
            # preparar los datos para guardar en la base de datos
            dato_resumido = obtener_informacion_resumida(resultado_optimizacion)
            resultado = guardar_rutas_entrega(deposito, dato_resumido)
            # Paso 5: Devolver la respuesta
            return Response({'data': 'Optimizacion realizada con exito!', 'result': dato_resumido}, status=status.HTTP_200_OK)
        return Response({'data':"Solucion no encontrada!! ¡Asegúrate de verificar la capacidad de los vehículos y la demanda total de los elementos a transportar!"}, status=status.HTTP_400_BAD_REQUEST)

    except Deposito.DoesNotExist:
        return Response({'message': 'Deposito no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

def guardar_rutas_entrega(deposito, datos_rutas):
    for ruta_info in datos_rutas:
        if ruta_info['distancia_total'] > 0:
            ruta_entrega = RutasDeEntrega.objects.create(
                distancia_total_recorrida=ruta_info['distancia_total'],
                fecha_creacion=timezone.now()
            )
        
            for orden, data in enumerate(ruta_info['ids_puntos_de_entrega'][:-1]):
                instancia_punto_de_entrega = PuntoDeEntrega.objects.get(id=data)
                orden_de_entrega = orden
                distancia_recorrida_al_punto = ruta_info['distancia_entre_nodos'][orden]
                demanda_a_entrega = instancia_punto_de_entrega.demanda.peso_kg
                estado = 'procesada'
                crear_detalleRuta(ruta_entrega, instancia_punto_de_entrega,orden_de_entrega, distancia_recorrida_al_punto,demanda_a_entrega, estado)


def crear_detalleRuta(ruta, punto_de_entrega, 
                      orden_de_entrega, 
                      distancia_recorrida_al_punto,
                      demanda_a_entregar,
                      estado):
    detalle_ruta = DetalleRutaDeEntrega.objects.create(
        ruta=ruta,
        punto_de_entrega=punto_de_entrega,
        orden_de_entrega=orden_de_entrega,
        distancia_recorrida_al_punto=distancia_recorrida_al_punto,
        demanda_a_entregar=demanda_a_entregar,
        estado=estado
    )
    punto_de_entrega.estado = "optimizado"
    punto_de_entrega.save()
    return detalle_ruta
    
    
        
            

def obtener_informacion_resumida(datos):
    informacion_resumida = []
    for indice, ruta in datos.items():
        if isinstance(indice, int):
            if len(ruta['ruta']) < 3:
                continue
            informacion_resumida.append({
                'vehiculo': ruta['vehiculo'],
                'ruta': ruta['ruta'],
                'ids_puntos_de_entrega': ruta['ids_puntos_de_entrega'][1:],
                'distancia_entre_nodos': ruta['distancia_entre_nodos'],
                'distancia_total': ruta['distancia_total']
            })
    return informacion_resumida

def obtener_datos_deposito_y_vehiculos(deposito_id):
    deposito = Deposito.objects.get(id=deposito_id)
    vehiculos = Vehiculo.objects.filter(deposito=deposito, estado='disponible')
    return deposito, vehiculos


def obtener_ubicaciones_y_demandas(deposito):
    ubicaciones = [(float(deposito.latitud), float(deposito.longitud))]
    ids_ubicaciones = [deposito.id]
    demandas = [0]  # El depósito no tiene demanda

    demandas_asignadas = Demanda.objects.filter(deposito=deposito, estado='asignada')
    for demanda in demandas_asignadas:
        puntos_entrega = PuntoDeEntrega.objects.filter(demanda=demanda, estado='procesar')
        for punto in puntos_entrega:
            ubicaciones.append((float(punto.latitud), float(punto.longitud)))
            ids_ubicaciones.append(punto.id)
            demandas.append(int(demanda.peso_kg))

    return ubicaciones, ids_ubicaciones, demandas


def preparar_datos_optimizacion(ubicaciones, ids_ubicaciones, demandas, vehiculos):
    data = {}
    data['ubicaciones'] = ubicaciones
    data['ids_ubicaciones'] = ids_ubicaciones
    data["capacidades_vehiculos"] = [v.capacidad_de_carga for v in vehiculos]
    data['matriculas_vehiculos'] = [v.matricula for v in vehiculos]
    data["demandas"] = demandas
    data["num_vehicles"] = len(vehiculos)
    data["distance_matrix"] = calcular_distancia(ubicaciones)
    data["depot"] = 0  # El índice del depósito en la lista de ubicaciones

    verificarDatoss(data)

    return data



def verificarDatoss(data):
    capacidades_vehiculos = data['capacidades_vehiculos']
    demanda_kg = data['demandas']
    

    ubicaciones = len(data['ubicaciones'])
    if ubicaciones < 2:
        raise Exception("No existen ubicaciones suficientes para realizar la optimización.")
    if len(data['ids_ubicaciones']) != ubicaciones:
        raise Exception("La lista de ids de ubicaciones debe tener la misma longitud que la lista de ubicaciones.")
    

    vehiculos = len(data['capacidades_vehiculos'])
    if vehiculos < 1:
        raise Exception("No existen vehiculos disponibles para realizar la optimización.")
    if len(data['matriculas_vehiculos']) != vehiculos:
        raise Exception("La lista de matriculas de vehículos debe tener la misma longitud que la lista de capacidades de vehículos.")
    
    demandas = len(data['demandas'])
    if demandas < 1:
        raise Exception("No existen demandas disponibles para realizar la optimización.")
    
    return    


def ejecutar_optimizacion(data):
    return main(data)


