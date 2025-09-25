from geopy.distance import geodesic

def calcular_distancia(locations):
    distance_matrix = []
    for loc1 in locations:
        row = []
        for loc2 in locations:
            distance = geodesic(loc1, loc2).meters  # La distancia en kilómetros
            row.append(int(distance)) # 123.0934834938493 a esto 123
        distance_matrix.append(row)


    return distance_matrix
