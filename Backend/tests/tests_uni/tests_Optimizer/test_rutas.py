from django.test import TestCase
from .datos import crear_datos, obtener_datos
from Optimizer.models import RutasDeEntrega, DetalleRutaDeEntrega
from ResourceManagement.models import Deposito, Demanda, Vehiculo, PuntoDeEntrega
from Optimizer.solvingCVRP import main as run_optimization



class RutasTest(TestCase):
    def setUp(self):
        crear_datos()
        self.resultado = obtener_datos()
    
        return self.resultado 
        
    def test_get_data(self):
        print(self.resultado)
        
        
        
        
        
        
        
        
        
        
        
    #     # Asignar los resultados de la optimización a atributos de instancia





    #     self.data, self.manager, self.routing, self.solution = run_optimization()










    # def test_guardar_solucion(self):
    #     # Usar self para acceder a los atributos de la instancia
    #     print(f"Objective: {self.solution.ObjectiveValue()}")
    #     total_distance = 0
    #     total_load = 0
    #     for vehicle_id in range(self.data["num_vehicles"]):
    #         index = self.routing.Start(vehicle_id)
    #         route_distance = 0
    #         route_load = 0
    #         orden_de_entrega = 0  # Inicializa el orden de entrega para esta ruta

    #         # Lista para guardar temporalmente los detalles de la ruta
    #         detalles_de_ruta = []

    #         while not self.routing.IsEnd(index):
    #             node_index = self.manager.IndexToNode(index)
    #             route_load += self.data["demands"][node_index]
    #             previous_index = index
    #             index = self.solution.Value(self.routing.NextVar(index))
    #             distancia_recorrida = self.routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
    #             route_distance += distancia_recorrida

    #             # Agregar los detalles de este punto al listado temporal
    #             detalles_de_ruta.append({
    #                 'punto_de_entrega': node_index,  # Asumiendo que node_index se puede mapear directamente a un PuntoDeEntrega
    #                 'orden_de_entrega': orden_de_entrega,
    #                 'distancia_recorrida_al_punto': round(distancia_recorrida / 1000, 3),  # Convertido a kilómetros
    #                 'demanda_a_entregar': self.data["demands"][node_index],
    #             })
    #             orden_de_entrega += 1

    #         # Convertir distancia de metros a kilómetros y redondear
    #         distancia_en_km = round(route_distance / 1000, 3)
    #         # Crear y guardar la ruta en la base de datos
    #         ruta = RutasDeEntrega(distancia_total_recorrida=distancia_en_km)
    #         ruta.save()

    #         # Ahora, guardar los detalles de ruta
    #         for detalle in detalles_de_ruta:
    #             DetalleRutaDeEntrega.objects.create(
    #                 ruta=ruta,
    #                 punto_de_entrega=PuntoDeEntrega.objects.get(pk=detalle['punto_de_entrega']),  # Aquí necesitas asegurarte de obtener correctamente el PuntoDeEntrega
    #                 orden_de_entrega=detalle['orden_de_entrega'],
    #                 distancia_recorrida_al_punto=detalle['distancia_recorrida_al_punto'],
    #                 demanda_a_entregar=detalle['demanda_a_entregar'],
    #             )

    #         total_distance += route_distance
    #         total_load += route_load

    #     total_distance_km = round(total_distance / 1000, 3)
    #     print(f"Total distance of all routes: {total_distance_km}km")
    #     print(f"Total load of all routes: {total_load}")
