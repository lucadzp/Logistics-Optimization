from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from .create_distance_matrix import calcular_distancia


def obtener_rutas(solucion, ruteo, gestor, datos):
    # Obtener las rutas de los vehículos
    rutas = []
    distancias_rutas = []
    demandas_rutas = []
    vehiculos_rutas_ubicaciones = {}  
    distancias_entre_punto_entrega = []
    for numero_ruta in range(ruteo.vehicles()):
        indice = ruteo.Start(numero_ruta) #Obtiene el índice del nodo de inicio (depósito).
        ruta = [gestor.IndexToNode(indice)] #Convierte el índice interno de OR-Tools a un identificador real de la ubicación.
        distancia_total_ruta = 0
        demanda_total_ruta = 0
        demandas_nodos_ruta = [] 
        distancias_punto_de_entrega = []
        while not ruteo.IsEnd(indice): #Se obtiene el nodo actual y el siguiente de la ruta usando solucion.Value(ruteo.NextVar(indice)).
            nodo_actual = gestor.IndexToNode(indice)
            indice = solucion.Value(ruteo.NextVar(indice))
            nodo_siguiente = gestor.IndexToNode(indice)
            distancia_entre_nodos = datos["distance_matrix"][nodo_actual][nodo_siguiente] #Se obtiene la distancia entre los nodos desde la distance_matrix.
            distancias_punto_de_entrega.append(distancia_entre_nodos)
            distancia_total_ruta += distancia_entre_nodos
            ruta.append(nodo_siguiente)
            demanda_nodo = datos["demandas"][nodo_siguiente] if nodo_siguiente < len(datos["demandas"]) else 0 #Se obtiene la demanda del nodo y se almacena.
            demanda_total_ruta += demanda_nodo
            demandas_nodos_ruta.append(demanda_nodo)  
        rutas.append(ruta)
        distancias_rutas.append(distancia_total_ruta)
        demandas_rutas.append(demanda_total_ruta)
        distancias_entre_punto_entrega.append(distancias_punto_de_entrega)
        # Agregar la lista de demandas de nodos a vehiculos_rutas_ubicaciones
        vehiculos_rutas_ubicaciones[numero_ruta] = {'demandas_nodos': demandas_nodos_ruta}

    # Obtener los IDs de las ubicaciones
    ids_ubicaciones = datos.get('ids_ubicaciones', [])

    # Crear un diccionario donde la clave sea el índice del vehículo y el valor sea la matrícula del vehículo
    matricula_vehiculo = datos['matriculas_vehiculos']
    indice_vehiculo = {i: matricula for i, matricula in enumerate(matricula_vehiculo)}

    # Crear un diccionario donde la clave sea el índice del vehículo y el valor sea la ruta junto con las ubicaciones y sus IDs
    vehiculos_rutas_ubicaciones_final = {}
    for i, ruta in enumerate(rutas):
        vehiculo = indice_vehiculo[i]
        ubicaciones = [datos['ubicaciones'][nodo] for nodo in ruta]
        ids_ubicaciones_ruta = [ids_ubicaciones[nodo] for nodo in ruta]
        distancia_ruta = distancias_rutas[i]
        demanda_ruta = demandas_rutas[i]
        demandas_nodos_ruta = vehiculos_rutas_ubicaciones.get(i, {}).get('demandas_nodos', [])
        vehiculos_rutas_ubicaciones_final[i] = {'vehiculo': vehiculo, 'ruta': ruta, 'ubicaciones': ubicaciones, 'ids_puntos_de_entrega': ids_ubicaciones_ruta, 'distancia_total': distancia_ruta, 'demanda_total': demanda_ruta, 'demandas_nodos': demandas_nodos_ruta,'distancia_entre_nodos':distancia_entre_nodos, 'distancia_entre_nodos':distancias_entre_punto_entrega[i]}

    vehiculos_rutas_ubicaciones_final['distancia_total_recorrida'] = solucion.ObjectiveValue()
    return vehiculos_rutas_ubicaciones_final


def main(data):
    '''
    pywrapcp.RoutingIndexManager(): Esta es la creación de una instancia de la clase RoutingIndexManager proporcionada por OR-Tools. Esta clase se utiliza para gestionar los índices de los nodos en el problema de ruteo.
    '''
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )
    '''
    Las entradas a RoutingIndexManager son las siguientes:
       len(data["distance_matrix"]) => La cantidad de filas de la matriz de distancia, que es el número de ubicaciones (incluido el depósito).
        data["num_vehicles"] = > La cantidad de vehículos en el problema
       data["depot"] => El nodo que corresponde al depósito.

    '''

    # Create Routing Model.
    '''
    El objeto routing que se crea aquí es esencial para definir y resolver el problema de ruteo. Proporciona métodos y funciones para agregar restricciones, definir variables de decisión y configurar parámetros de búsqueda. Además, se utiliza para acceder a la solución del problema una vez que se ha resuelto.
    '''
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    '''
    ¿Qué es una devolución de llamada de distancia?

    En el contexto del problema de ruteo de vehículos (VRP), una devolución de llamada de distancia es una función que se utiliza para calcular la distancia entre dos ubicaciones. Esta información es crucial para el algoritmo de resolución de rutas, ya que le permite determinar el costo de cada posible camino entre ubicaciones.
    '''
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.

    '''
    Después de crear la función distance_callback, se registra con el agente de resolución de rutas utilizando el método RegisterTransitCallback. Esto le indica al agente de resolución que debe usar esta función para calcular las distancias entre las ubicaciones. El valor devuelto por RegisterTransitCallback (transit_callback_index) se utiliza posteriormente para definir el costo de cada arco (camino entre dos ubicaciones).'''
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    '''
    Además de la devolución de llamada de distancia, el solucionador también requiere una devolución de llamada de demanda, que muestra la demanda en cada ubicación y una dimensión para las restricciones de capacidad.
    A diferencia de la devolución de llamada de distancia, que toma un par de ubicaciones como entradas, la devolución de llamada de demanda solo depende de la ubicación (from_node) de la entrega.
    En el contexto del problema de ruteo de vehículos (VRP), una dimensión de capacidad es una restricción que limita la cantidad de carga que un vehículo puede transportar a lo largo de una ruta. Esta restricción es importante para garantizar que los vehículos no se sobrecarguen y que puedan entregar toda la carga de manera eficiente.
    '''
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demandas"][from_node]
    

    '''
    La dimensión de capacidad se implementa mediante el método AddDimensionWithVehicleCapacity del modelo de ruteo (routing). Este método toma los siguientes parámetros:
    demand_callback_index: El índice de la función de callback que se utiliza para obtener la demanda de cada ubicación.
    null_capacity_slack: Un valor que representa la holgura de capacidad nula. Esto indica que no se permite que un vehículo exceda su capacidad máxima en ningún momento de la ruta.
    vehicle_capacities: Una lista que contiene la capacidad máxima de cada vehículo de la flota.
    start_cumul_to_zero: Un valor booleano que indica si la acumulación de la dimensión de capacidad debe comenzar en cero.
    name: El nombre de la dimensión de capacidad.
    '''
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["capacidades_vehiculos"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Setting first solution heuristic.
    '''
    ¿Qué es una heurística de primera solución?
        En el contexto de la optimización, una heurística es un método para encontrar una solución "buena" a un problema, aunque no necesariamente sea la solución óptima. Una heurística de primera solución se utiliza específicamente para encontrar una solución inicial factible al problema. Esta solución inicial se puede utilizar posteriormente por otros algoritmos de optimización para mejorarla y potencialmente encontrar la solución óptima.
    '''

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    '''
    pywrapcp.DefaultRoutingSearchParameters()

    Crea una instancia de la clase pywrapcp.DefaultRoutingSearchParameters. Esta clase contiene los valores predeterminados para varios parámetros del algoritmo de resolución de rutas, como la heurística de primera solución, la metaheurística de búsqueda local y el límite de tiempo.
    '''
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC #Empieza por el nodo mas barato (Heuristico)
    )
    '''
    search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    Configura la heurística de primera solución que se utilizará para encontrar una solución inicial factible.
    En este caso, se establece la estrategia a PATH_CHEAPEST_ARC (arco más barato). Esta heurística construye rutas seleccionando iterativamente el arco (camino entre dos ubicaciones) más barato que no viole ninguna restricción del problema.
    '''
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH #Mejora la solucion Heuristico (MetaHeuristico)
    )
    '''
        search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )

        Configura la metaheurística de búsqueda local que se utilizará para mejorar la solución inicial.
        La metaheurística seleccionada es GUIDED_LOCAL_SEARCH (búsqueda local guiada). Esta técnica explora iterativamente el espacio de búsqueda, realizando pequeños cambios en la solución actual para encontrar mejores soluciones.
    '''
    search_parameters.time_limit.FromSeconds(1)
    '''
        search_parameters.time_limit.FromSeconds(1)

        Establece el límite de tiempo máximo para la búsqueda en un segundo utilizando el método FromSeconds.
        Esto indica al algoritmo que debe detener su búsqueda después de un segundo, independientemente de si ha encontrado la solución óptima o no.
    '''

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    '''
    SolveWithParameters(search_parameters): Este método del modelo de ruteo (routing) se encarga de resolver el problema utilizando los parámetros de búsqueda configurados previamente en search_parameters.
    
    search_parameters: Esta variable contiene la configuración de la heurística de primera solución, la metaheurística de búsqueda local y el límite de tiempo que se utilizarán para encontrar una solución óptima o factible.
    
    El método SolveWithParameters devuelve un objeto solution que representa la solución encontrada por el algoritmo de resolución de rutas. Esta solución contiene información sobre las rutas asignadas a cada vehículo, la distancia total recorrida y posiblemente otros detalles dependiendo de la implementación específica.
    
    '''
    if solution:
        routes = obtener_rutas(solution, routing, manager, data)
        return routes
    else:
        return None


if __name__ == "__main__":
    main()