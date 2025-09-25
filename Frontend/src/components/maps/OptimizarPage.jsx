import React, { useEffect, useRef, useState } from 'react';
import 'leaflet-routing-machine';
import L from 'leaflet';
import 'leaflet-polylinedecorator'; // Asegúrate de tener esta librería instalada

const OptimizarPage = ({ routes }) => {
  const mapRefs = useRef([]);
  const routingControls = useRef([]);
  const [routeInfo, setRouteInfo] = useState([]);

  useEffect(() => {
    console.log(routes)
    routes.forEach((route, index) => {
      const mapId = `map-${index}`;

      // Solo inicializamos el mapa si no existe
      if (!mapRefs.current[index]) {
        // Inicializa el mapa y guarda la referencia
        mapRefs.current[index] = L.map(mapId).setView([route.deposit.latitud, route.deposit.longitud], 13);

        // Añadir capa de OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors',
        }).addTo(mapRefs.current[index]);

        // Configurar waypoints para Leaflet Routing Machine
        const waypoints = [
          L.latLng(route.deposit.latitud, route.deposit.longitud),
          ...route.coords.map((point) => L.latLng(point.latitud, point.longitud)),
          L.latLng(route.deposit.latitud, route.deposit.longitud),
        ];

        // Icono personalizado
        const customMarkerIcon = L.icon({
          iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png', // Cambia esta URL por la de tu icono
          iconSize: [30, 30], // Tamaño del icono
          iconAnchor: [15, 30], // Punto de anclaje
        });

        // Agregar control de rutas al mapa
        const routingControl = L.Routing.control({
          waypoints,
          lineOptions: {
            styles: [{ color: 'blue', weight: 5 }], // Estilo de la línea de ruta
          },
          show: false, // Ocultar instrucciones
          addWaypoints: false, // Deshabilitar edición
          draggableWaypoints: false, // No permitir arrastrar puntos
          routeWhileDragging: false, // No recalcular ruta al arrastrar
          createMarker: (i, waypoint) => {
            const point = route.coords[i - 1]; // El primer waypoint es el depósito, los demás son clientes
          
            // Si el punto es válido (evitamos el depósito)
            if (point) {
              const marker = L.marker(waypoint.latLng, {
                icon: customMarkerIcon,
              });
          
              // Agregar popup con información del cliente
              marker.bindPopup(`
                <strong>Cliente:</strong> ${point.cliente}<br>
                <strong>Descripción:</strong> ${point.descripcionDemanda}<br>
                <strong>Nro de telefono:</strong> ${point.numero_de_telefono}
              `);
          
              return marker;
            }
          
            // Si es el depósito, usa el marcador normal sin popup
            return L.marker(waypoint.latLng, { icon: customMarkerIcon });
          }
          
        }).addTo(mapRefs.current[index]);

        // Guardar la referencia de routingControl
        routingControls.current[index] = routingControl;

        // Añadir flechas a la ruta con PolylineDecorator
        routingControl.on('routesfound', (e) => {
          const route = e.routes[0];
          const latlngs = route.coordinates.map((coord) => L.latLng(coord.lat, coord.lng));
          const distanciaTotal = (route.summary.totalDistance / 1000).toFixed(2); // km
          const tiempoTotal = Math.round(route.summary.totalTime / 60)*2;

          setRouteInfo((prevInfo) => [
            ...prevInfo,
            { index, distancia: distanciaTotal, tiempo: tiempoTotal },
          ]);

          // Crear el polígono de la ruta
          const polyline = L.polyline(latlngs, {
            color: 'blue',
            weight: 5,
          }).addTo(mapRefs.current[index]);

          // Decorar con flechas
          L.polylineDecorator(polyline, {
            patterns: [
              {
                offset: '5%', // Inicio del patrón
                repeat: '5%', // Repetir cada 10% de la línea
                symbol: L.Symbol.arrowHead({
                  pixelSize: 10,
                  pathOptions: { fillOpacity: 1, color: 'green' }, // Estilo de las flechas
                }),
              },
            ],
          }).addTo(mapRefs.current[index]);

          // Elimina las instrucciones generadas por Leaflet Routing Machine
          const instructionsElements = document.querySelectorAll('.leaflet-routing-container');
          instructionsElements.forEach((el) => el.remove());
        });
      }
    });
    const prevMaps = [...mapRefs.current];
    const prevRoutingControls = [...routingControls.current];

    return () => {
      // Destruir mapas y controles anteriores
      prevMaps.forEach((map, index) => {
        if (map) {
          map.remove();
          prevRoutingControls[index]?.remove();
        }
      });
      mapRefs.current = [];
      routingControls.current = [];
      setRouteInfo([]); // Resetear información de rutas
    };
  }, [routes]); // Solo se ejecuta cuando 'routes' cambian

  if (!routes.length) {
    return <div>No hay rutas optimizadas disponibles.</div>;
  }

  return (
    <div className="space-y-6">
      {routes.map((route, index) => (
        <div
          key={index}
          className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-300"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-gray-800">
              🚛 Ruta {index + 1} - {route.vehiculo}
            </h3>
            <span className="text-sm bg-blue-100 text-blue-600 px-3 py-1 rounded-full">
              Recorrido Total  {routeInfo[index]?.distancia ? `${routeInfo[index]?.distancia} km` : 'Calculando...'}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-700">
            <div>
              <span className="font-medium text-gray-900">📌 Cliente:</span>
              <ul className="list-disc pl-5">
                {route.coords.map((point, i) => (
                  <li key={i}>{point.cliente}</li>
                ))}
              </ul>
            </div>
            <div>
              <span className="font-medium text-gray-900">📦 Descripción de la entrega:</span>
              <ul className="list-disc pl-5">
                {route.coords.map((point, i) => (
                  <li key={i}>{point.descripcionDemanda}</li>
                ))}
              </ul>
               <p>
              <span className="font-medium text-gray-900">⏳ Tiempo estimado del recorrido:</span>{' '}
              {routeInfo[index]?.tiempo ? `${routeInfo[index]?.tiempo} min` : 'Calculando...'}
            </p>
            </div>

          </div>

          <div
            id={`map-${index}`}
            className="h-64 w-full rounded-lg shadow-md mt-4 overflow-hidden border border-gray-300"
          ></div>
        </div>
      ))}
    </div>

  );
};

export default OptimizarPage;