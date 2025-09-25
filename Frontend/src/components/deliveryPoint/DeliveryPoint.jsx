import React, { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import api from '../../lib/common/API';
import { DeliveryPointModal } from '../modals/DeliveryPointModal';
import { toast } from 'react-toastify';
import { LeafletMapModal } from '../modals/LeafletMapModal';
import { useNavigate } from 'react-router-dom';
import OptimizarPage from '../maps/OptimizarPage';

// Componente Loader
const CustomLoader = () => (
  <div className="flex justify-center items-center h-20">
    <svg
      className="animate-spin h-10 w-10 text-blue-500"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      ></circle>
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8v8h8a8 8 0 01-8 8V12H4z"
      ></path>
    </svg>
  </div>
);

const DeliveryPointsTable = () => {
  const [puntosDeEntrega, setPuntosDeEntrega] = useState([]);
  const [filteredPoints, setFilteredPoints] = useState([]);
  const [search, setSearch] = useState('');
  const [isModalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [mapModalOpen, setMapModalOpen] = useState(false);
  const [mapCoordinates, setMapCoordinates] = useState({ latitude: 0, longitude: 0 });
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [idRoutes, setIdRoutes] = useState({})
  const [optimizedRoutes, setOptimizedRoutes] = useState([])



  useEffect(() => {
    getDeliveryPoints();
  }, []);

  useEffect(() => {
    const results = puntosDeEntrega.filter((point) => {
      const cliente = point.cliente?.toLowerCase() || '';
      const estado = point.estado?.toLowerCase() || '';
      const telefono = point.numero_de_telefono?.toLowerCase() || '';

      return (
        cliente.includes(search.toLowerCase()) ||
        estado.includes(search.toLowerCase()) ||
        telefono.includes(search.toLowerCase())
      );
    });

    setFilteredPoints(results);
  }, [search, puntosDeEntrega]);

  const getDeliveryPoints = async () => {
    setIsLoading(true);
    try {
      const response = await api.get('resource/puntosdeentrega');
      const sortedDeliveryPoints = response.data.sort((a, b) => b.id - a.id);
      setPuntosDeEntrega(sortedDeliveryPoints);
      setFilteredPoints(sortedDeliveryPoints);
    } catch (error) {
      console.error(error);
      toast.error('Error al cargar los puntos de entrega');
    } finally {
      setIsLoading(false);
    }
  };



  const onSubmit = async (data) => {
    try {
      if (selectedPoint) {
        // Modo edición
        const payload = { ...data };
        const response = await api.patch(`resource/puntosdeentrega/${selectedPoint.id}/`, payload);

        setSelectedPoint(response.data);
        toast.success('Punto de entrega actualizado exitosamente');
      } else {
        // Modo creación
        const payload = { ...data };
        await api.post('resource/puntosdeentrega/', payload);
        toast.success('Punto de entrega creado exitosamente');
      }

      getDeliveryPoints();
      setModalOpen(false);

    } catch (error) {
      console.error('Error details:', error);
      toast.error(error.response?.data?.message || 'Error interno del servidor');
    }
  };

  const handleEditDeliveryPoint = (point) => {
    setSelectedPoint(point);
    setModalOpen(true);
  };

  const handleDeleteDeliveryPoint = async (row) => {
    // Verificar que 'row' y 'row.matricula' estén definidos
    if (!row || !row.id) {
      toast.error("No se ha seleccionado ningún Cliente o Cliente no válido");
      return;
    }

    const confirmDeleteToast = toast(
      <div>
        <p>¿Estás seguro de que deseas eliminar el Punto de Entrega Del Cliente {row.cliente}?</p>
        <div style={{ display: 'flex', justifyContent: 'space-around' }}>
          <button
            onClick={async () => {
              try {
                // Realizar la eliminación si el usuario confirma
                await api.delete(`resource/puntosdeentrega/${row.id}/`);
                toast.success("Punto de Entrega eliminado correctamente");
                setTimeout(() => {
                  toast.dismiss(); // Cierra el toast con el id especificado
                }, 2000);
                getDeliveryPoints(); // Actualizar la lista de vehículos
              } catch (error) {
                console.error("Error al eliminar el Punto de Entrega:", error);
                toast.error("Hubo un error al eliminar Punto De Entrega");
              }
            }}
            style={{ backgroundColor: 'red', color: 'white', padding: '5px 10px', border: 'none', cursor: 'pointer' }}
          >
            Sí, eliminar
          </button>
          <button
            onClick={() => {
              // Si el usuario cancela, cierra el toast
              toast.dismiss(confirmDeleteToast);
              toast.info("Eliminación cancelada");
            }}
            style={{ backgroundColor: 'gray', color: 'white', padding: '5px 10px', border: 'none', cursor: 'pointer' }}
          >
            Cancelar
          </button>
        </div>
      </div>,
      { autoClose: false, closeButton: false, style: { maxWidth: '400px', margin: 'auto' } }
    );
  };



  const columns = [
    {
      name: 'Cliente',
      selector: (row) => row.cliente,
      sortable: true,
    },
    {
      name: 'Latitud',
      selector: (row) => row.latitud,
      sortable: true,
    },
    {
      name: 'Longitud',
      selector: (row) => row.longitud,
      sortable: true,
    },
    {
      name: 'Demanda',
      selector: (row) => row.demanda,
      sortable: true,
    },
    {
      name: 'Estado',
      selector: (row) => row.estado,
      sortable: true,
    },
    {
      name: 'Teléfono',
      selector: (row) => row.numero_de_telefono,
      sortable: true,
    },
    {
      name: 'Acciones',
      cell: (row) => (
        <div className="flex space-x-2">
          <button
            onClick={() => handleEditDeliveryPoint(row)}
            className="text-blue-600 hover:text-blue-800"
          >
            <i className="fas fa-edit"></i>
          </button>
          <button
            onClick={() => handleDeleteDeliveryPoint(row)}
            className="text-red-600 hover:text-red-800"
          >
            <i className="fas fa-trash"></i>
          </button>
          <button
            onClick={() => handleViewOnMap(row.latitud, row.longitud)}
            className="text-green-600 hover:text-green-800"
          >
            <i className="fas fa-map-marker-alt"></i>
          </button>
        </div>
      ),
    },
  ];

  const handleViewOnMap = (latitude, longitude) => {
    setMapCoordinates({ latitude, longitude });
    setMapModalOpen(true);
  };

  const handleOptimizarClick = async () => {
    try {
      setIsLoading(true);
      // Paso 1: Llamar a la API de optimización
      const response = await api.get('/optimizer/optimizar');

      // Paso 2: Obtener los puntos de entrega más recientes del backend
      const latestPuntosResponse = await api.get('resource/puntosdeentrega');
      const latestPuntos = latestPuntosResponse.data.sort((a, b) => b.id - a.id);

      // Actualizar el estado local con los datos frescos
      setPuntosDeEntrega(latestPuntos);
      setFilteredPoints(latestPuntos);

      // Paso 3: Procesar las rutas optimizadas con los datos actualizados
      const depositCoords = { latitud: -27.326383, longitud: -55.872087 };

      const rutas = await Promise.all(
        response.data.result.map(async (vehiculo) => {
          const puntosDeEntregaOptimizado = vehiculo.ids_puntos_de_entrega;

          // Filtrar usando los datos recién obtenidos (latestPuntos)
          const optimizedPoints = latestPuntos.filter((point) =>
            puntosDeEntregaOptimizado.includes(point.id)
          );

          // Obtener descripción de la demanda
          const puntosConDescripcion = await Promise.all(
            optimizedPoints.map(async (point) => {
              const demandaResponse = await api.get(`/resource/demandas/${point.demanda}/`);
              return {
                ...point,
                descripcionDemanda: demandaResponse.data.descripción,
              };
            })
          );

          return {
            coords: puntosConDescripcion,
            deposit: depositCoords,
            vehiculo: vehiculo.vehiculo,
            cliente: puntosConDescripcion[0]?.cliente || 'Sin cliente',
            descripcionDemanda: puntosConDescripcion[0]?.descripcionDemanda || 'Sin descripción',
          };
        })
      );

      setOptimizedRoutes(rutas);
    } catch (error) {
      console.error(error);
      toast.error(error.response?.data?.message || 'Error al optimizar las rutas');
    } finally {
      setIsLoading(false);
    }
  };



  return (
    <div className="p-4 md:p-14 bg-gray-100 min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 space-y-2 md:space-y-0">
        <h1 className="text-lg md:text-xl font-semibold text-gray-700">Puntos de Entrega</h1>
        <div className="flex space-x-4">
          <button
            className=" bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600 transition w-full md:w-auto"
            onClick={() => {
              setModalOpen(true);
              setSelectedPoint(null);
            }}
          >
            Agregar Punto de Entrega
          </button>
          <button
            className="bg-green-500 text-white rounded-md px-4 py-2 hover:bg-green-600 transition w-full md:w-auto"
            onClick={handleOptimizarClick}
          >
            Optimizar
          </button>
        </div>
      </div>

      <div className="relative mb-4">
        <input
          type="text"
          placeholder="Buscar puntos de entrega..."
          className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring focus:ring-blue-300 focus:border-blue-500 shadow-sm"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="bg-white shadow-md rounded-md overflow-hidden">
        <DataTable
          columns={columns}
          data={filteredPoints} // Utiliza los puntos filtrados
          progressPending={isLoading}
          progressComponent={<CustomLoader />}
          pagination
          highlightOnHover
          responsive
          noDataComponent={
            <div className="py-6 text-center text-gray-500">
              No se encontraron puntos de entrega.
            </div>
          }
        />
      </div>



      {/* Componente OptimizerPage para rutas optimizadas */}
      <OptimizarPage routes={optimizedRoutes} />
      {/* Modal para agregar/editar puntos de entrega */}
      <DeliveryPointModal
        btn={selectedPoint ? "Editar" : "Agregar"}
        isOpenDeliveryPoint={isModalOpen}
        onCloseDeliveryPoint={() => setModalOpen(false)}
        onAddDeliveryPoint={onSubmit}
        initialData={selectedPoint}
      />

      {/* Modal para ver en el mapa el punto marcado */}
      <LeafletMapModal
        isOpen={mapModalOpen}
        onClose={() => setMapModalOpen(false)}
        selectedCoordinates={
          mapCoordinates.latitude && mapCoordinates.longitude
            ? { lat: mapCoordinates.latitude, lng: mapCoordinates.longitude }
            : null
        }
      />
    </div>
  );
};

export default DeliveryPointsTable;
