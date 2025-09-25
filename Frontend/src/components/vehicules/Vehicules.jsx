import React, { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import { VehiculesModals } from '../modals/VehiculesModals';
import api from '../../lib/common/API';
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

const VehicleTable = () => {
  const [vehicles, setVehicles] = useState([]);
  const [depositos, setDepositos] = useState([]);
  const [isModalOpen, setModalOpen] = useState(false);
  const [pending, setPending] = useState(true);
  const [search, setSearch] = useState('');
  const [filteredVehicles, setFilteredVehicles] = useState([]);
  const [selectedVehicules, setSelectedVehicules] = useState(null);

  useEffect(() => {
    getVehicles();
    getDeposits();
  }, []);

  useEffect(() => {
    const results = vehicles.filter((vehicle) => {
      const matricula = vehicle.matricula?.toLowerCase() || '';
      const estado = vehicle.estado?.toLowerCase() || '';

      const deposito = typeof vehicle.deposito === 'string' ? vehicle.deposito.toLowerCase() : '';

      return (
        matricula.includes(search.toLowerCase()) ||
        estado.includes(search.toLowerCase()) ||
        deposito.includes(search.toLowerCase())
      );
    });

    setFilteredVehicles(results);
  }, [search, vehicles]);

  const getVehicles = async () => {
    setPending(true);
    try {
      const response = await api.get('resource/vehiculos');
      setVehicles(response.data);
      setFilteredVehicles(response.data);
    } catch (error) {
      console.error(error);
      toast.error('Error al cargar los vehículos');
    } finally {
      setPending(false);
    }
  };

  const getDeposits = async () => {
    try {
      const response = await api.get('resource/depositos');
      setDepositos(response.data);
    } catch (error) {
      console.error(error);
      toast.error('Error al cargar los depósitos');
    }
  };


  
  const handleDeleteVehicle = async (row) => {
    // Verificar que 'row' y 'row.matricula' estén definidos
    if (!row || !row.matricula) {
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
                await api.delete(`resource/vehiculos/${row.matricula}`);
                toast.success("Vehículo eliminado correctamente");
                setTimeout(() => {
                  toast.dismiss(); // Cierra el toast con el id especificado
                }, 2000); 
                getVehicles(); // Actualizar la lista de vehículos
              } catch (error) {
                console.error("Error al eliminar el vehículo:", error);
                toast.error("Hubo un error al eliminar el vehículo");
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
  

  const onSubmit = async (data) => {
    try {
      if (selectedVehicules) {
        const payload = { ...data };
        const response = await api.patch(`resource/vehiculos/${selectedVehicules.matricula}/`, payload);
        setSelectedVehicules(response.data);
        toast.success('Vehiculo actualizado exitosamente');
      }
      else {

        const payload = { ...data };
        await api.post('resource/vehiculos/', payload);
        toast.success('Vehículo agregado exitosamente');
      }
      getVehicles();
      setModalOpen(false);
    } catch (error) {
      console.error('Error details:', error);
      if (error.response) {
        toast.error(`Error: ${error.response.data.message || 'Error interno del servidor'}`);
      } else {
        toast.error('Error de conexión o de configuración');
      }
    }
  };

  const handleEditVehicle = (id) => {
    setSelectedVehicules(id);
    setModalOpen(true);
  };
  const columns = [
    {
      name: 'Matrícula',
      selector: (row) => row.matricula,
      sortable: true,
    },
    {
      name: 'Capacidad de Carga',
      selector: (row) => row.capacidad_de_carga,
      sortable: true,
    },
    {
      name: 'Depósito',
      selector: (row) => {
        const deposito = depositos.find((dep) => dep.id === row.deposito);
        return deposito ? deposito.nombre : 'No asignado';
      },
      sortable: true,
    },
    {
      name: 'Estado',
      selector: (row) => (row.estado === 'disponible' ? 'Disponible' : 'No Disponible'),
      sortable: true,
    },
    {
      name: 'Acciones',
      cell: (row) => (
        <div className="flex space-x-2">
          <button onClick={() => handleEditVehicle(row)} className="text-blue-600 hover:text-blue-800">
            <i className="fas fa-edit"></i>
          </button>
          <button onClick={() => handleDeleteVehicle(row)} className="text-red-600 hover:text-red-800">
            <i className="fas fa-trash"></i>
          </button>
          <button onClick={() => console.log(row)} className="text-green-600 hover:text-green-800">
            <i className="fas fa-eye"></i>
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="p-4 md:p-14 bg-gray-100 min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start mb-4 space-y-2 md:space-y-0">
        <h1 className="text-lg md:text-xl font-semibold text-gray-700">Vehículos</h1>
        <button
          className="bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600 transition"
          onClick={() => {
            setModalOpen(true);
            setSelectedVehicules(null)
          }}
        >
          Agregar Vehículo
        </button>
      </div>

      <div className="relative mb-4">
        <input
          type="text"
          placeholder="Buscar vehículos..."
          className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring focus:ring-blue-300 focus:border-blue-500 shadow-sm"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="bg-white shadow-md rounded-md overflow-hidden">
        <DataTable
          columns={columns}
          data={filteredVehicles}
          progressPending={pending}
          progressComponent={<CustomLoader />}
          pagination
          highlightOnHover
          responsive
          noDataComponent={<div className="py-6 text-center text-gray-500">No se encontraron vehículos.</div>}
        />
      </div>

      {/* Modal para agregar vehículo */}
      <VehiculesModals
        btn={selectedVehicules ? "Editar" : "Agregar"}
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
        onAddVehicle={onSubmit}
        initialData={selectedVehicules}
      />
    </div>
  );
};

export default VehicleTable;
