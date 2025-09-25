import React, { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import api from '../../lib/common/API';
import { DemandModal } from '../modals/DemandModal';
import { toast } from 'react-toastify';

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

const Demand = () => {
  const [demands, setDemands] = useState([]);
  const [filteredDemands, setFilteredDemands] = useState([]);
  const [search, setSearch] = useState('');
  const [isModalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedDemand, setSelectedDemand] = useState(null);

  useEffect(() => {
    getDemands();
  }, []);

  useEffect(() => {
    const results = demands.filter((demand) => {
      const descripcion = demand.descripción?.toLowerCase() || '';
      const estado = demand.estado?.toLowerCase() || '';
      const deposito = typeof demand.deposito === 'string' ? demand.deposito.toLowerCase() : '';


      return (
        descripcion.includes(search.toLowerCase()) ||
        estado.includes(search.toLowerCase()) ||
        deposito.includes(search.toLowerCase())
      );
    });

    setFilteredDemands(results);
  }, [search, demands]);


  const getDemands = async () => {
    setIsLoading(true);
    try {
      const response = await api.get(`resource/demandas`);
      // Ordena las demandas por 'id' de forma descendente
      const sortedDemands = response.data.sort((a, b) => b.id - a.id);
      setDemands(sortedDemands);
      setFilteredDemands(sortedDemands);
    } catch (error) {
      console.error(error);
      toast.error('Error al cargar las demandas');
    } finally {
      setIsLoading(false);
    }
  };



  const onSubmit = async (data) => {
    try {
      if (selectedDemand) {

        const payload = { ...data };
        const response = await api.patch(`resource/demandas/${selectedDemand.id}/`, payload);
        setSelectedDemand(response.data);
        toast.success('Demanda actualizado exitosamente');
      }
      else {

        const payload = { ...data };
        await api.post(`resource/demandas/`, payload);
        toast.success('Demanda creada exitosamente');
      }
      getDemands();
      setModalOpen(false);
    } catch (error) {
      console.error(error);
      toast.error(error.response?.data?.message || 'Error interno del servidor');
    }
  };

  const handleDeleteDemand = async (row) => {

    if (!row || !row.id) {
      toast.error("No se ha seleccionado ningún vehículo o vehículo no válido");
      return;
    }

    // Muestra un toast con botones de confirmación
    const confirmDeleteToast = toast(
      <div>
        <p>¿Estás seguro de que deseas eliminar el vehículo con matrícula {row.matricula}?</p>
        <div style={{ display: 'flex', justifyContent: 'space-around' }}>
          <button
            onClick={async () => {
              try {
                // Realizar la eliminación si el usuario confirma
                await api.delete(`resource/demandas/${row.id}`);
                toast.success("Demanda eliminado correctamente");
                setTimeout(() => {
                  toast.dismiss(); // Cierra el toast con el id especificado
                }, 2000);
                getDemands(); // Actualizar la lista de vehículos
              } catch (error) {
                console.error("Error al eliminar la Demanda:", error);
                toast.error("Hubo un error al eliminar la demanda");
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


  const handleEditDemand = (demand) => {
    setSelectedDemand(demand);
    setModalOpen(true);
  };

  const columns = [
    {
      name: 'Peso (kg)',
      selector: (row) => row.peso_kg,
      sortable: true,
    },
    {
      name: 'Descripción',
      selector: (row) => row.descripción,
      sortable: true,
    },
    {
      name: 'Estado',
      selector: (row) => row.estado,
      sortable: true,
    },
    {
      name: 'Depósito',
      selector: (row) => row.deposito,
      sortable: true,
    },
    {
      name: 'Acciones',
      cell: (row, index) => (
        <div className="flex space-x-2">
          <button
            onClick={() => handleEditDemand(row)}
            className="text-blue-600 hover:text-blue-800"
          >
            <i className="fas fa-edit"></i>
          </button>
          <button
            onClick={() => handleDeleteDemand(row)}
            className="text-red-600 hover:text-red-800"
          >
            <i className="fas fa-trash"></i>
          </button>

        </div>
      ),
    },
  ];

  return (
    <div className="p-4 md:p-14 bg-gray-100 min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 space-y-2 md:space-y-0">
        <h1 className="text-lg md:text-xl font-semibold text-gray-700">Demandas</h1>
        <button
          className="bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600 transition w-full md:w-auto"
          onClick={() => {
            setModalOpen(true);
            setSelectedDemand(null)
          }}
        >
          Agregar Demanda
        </button>
      </div>

      <div className="relative mb-4">
        <input
          type="text"
          placeholder="Buscar demandas..."
          className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring focus:ring-blue-300 focus:border-blue-500 shadow-sm"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="bg-white shadow-md rounded-md overflow-hidden">
        <DataTable
          columns={columns}
          data={filteredDemands} // Utiliza las demandas filtradas
          progressPending={isLoading}
          progressComponent={<CustomLoader />}
          pagination
          highlightOnHover
          responsive
          sortServer={true} // Habilita la ordenación en el servidor
          sortColumn="peso_kg" // Columna a ordenar
          sortDirection="asc"
          noDataComponent={
            <div className="py-6 text-center text-gray-500">
              No se encontraron demandas.
            </div>
          }
        />
      </div>

      <DemandModal
        btn={selectedDemand ? "Editar" : "Agregar"}
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
        onAddDemand={onSubmit}
        initialData={selectedDemand}
      />
    </div>


  );
};

export default Demand;
