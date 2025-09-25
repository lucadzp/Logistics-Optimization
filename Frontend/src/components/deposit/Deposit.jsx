import React, { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import api from '../../lib/common/API';
import { DepositModal } from '../modals/DepositModal';
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

const Deposit = () => {
  const [depositos, setDepositos] = useState([]);
  const [filteredDepositos, setFilteredDepositos] = useState([]);
  const [search, setSearch] = useState('');
  const [isModalOpen, setModalOpen] = useState(false);
  const [pending, setPending] = useState(true);
  const [selectedDeposit, setSelectedDeposit] = useState(null);

  useEffect(() => {
    getDepositos();
  }, []);

  useEffect(() => {
    const results = depositos.filter((deposito) => {
      const nombre = deposito.nombre?.toLowerCase() || '';
      const direccion = deposito.direccion?.toLowerCase() || '';
      const telefono = deposito.numero_de_telefono?.toLowerCase() || '';

      return (
        nombre.includes(search.toLowerCase()) ||
        direccion.includes(search.toLowerCase()) ||
        telefono.includes(search.toLowerCase())
      );
    });

    setFilteredDepositos(results);
  }, [search, depositos]);

  const getDepositos = async () => {
    setPending(true);
    try {
      const response = await api.get(`resource/depositos`);
      setDepositos(response.data);
      setFilteredDepositos(response.data);
    } catch (error) {
      console.error(error);
      toast.error('Error al cargar los depósitos');
    } finally {
      setPending(false);
    }
  };

  const onSubmit = async (data) => {
    try {
      if (selectedDeposit) {
        // Modo edición

        const payload = { ...data };
        const response = await api.patch(`resource/depositos/${selectedDeposit.id}/`, payload);
        setSelectedDeposit(response.data);
        toast.success('Deposito actualizado exitosamente');
      }
      else {
        // Modo creación
        const payload = { ...data };
        await api.post('resource/depositos/', payload);
        toast.success('Deposito creado exitosamente');
      }
      getDepositos()
      setModalOpen(false)
    } catch (error) {
      console.error(error);
      toast.error(error.response?.data?.message || 'Error interno del servidor');
    }
  };

  const handleEditDeposit = (deposit) => {
    setSelectedDeposit(deposit);
    setModalOpen(true);
  };

  const columns = [
    {
      name: 'Nombre',
      selector: (row) => row.nombre,
      sortable: true,
    },
    {
      name: 'Dirección',
      selector: (row) => row.direccion || 'N/A',
      sortable: true,
    },
    {
      name: 'Latitud',
      selector: (row) => row.latitud,
    },
    {
      name: 'Longitud',
      selector: (row) => row.longitud,
    },
    {
      name: 'Teléfono',
      selector: (row) => row.numero_de_telefono || 'N/A',
      sortable: true,
    },
    {
      name: 'Acciones',
      cell: (row) => (
        <div className="flex space-x-2">
          <button
            onClick={() => handleEditDeposit(row)}
            className="text-blue-600 hover:text-blue-800"
          >
            <i className="fas fa-edit"></i>
          </button>
          
          <button
            onClick={() => console.log(row)}
            className="text-green-600 hover:text-green-800"
          >
            <i className="fas fa-eye"></i>
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="p-4 md:p-14 bg-gray-100 min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 space-y-2 md:space-y-0">
        <h1 className="text-lg md:text-xl font-semibold text-gray-700">Depósitos</h1>
        <button
          className="bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600 transition w-full md:w-auto"
          onClick={() => {
            setModalOpen(true);
            setSelectedDeposit(null)
          }}
        >
          Agregar Depósito
        </button>
      </div>

      <div className="relative mb-4">
        <input
          type="text"
          placeholder="Buscar depósitos..."
          className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring focus:ring-blue-300 focus:border-blue-500 shadow-sm"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="bg-white shadow-md rounded-md overflow-hidden">
        <DataTable
          columns={columns}
          data={filteredDepositos}
          progressPending={pending}
          progressComponent={<CustomLoader />}
          pagination
          highlightOnHover
          responsive
          noDataComponent={
            <div className="py-6 text-center text-gray-500">
              No se encontraron depósitos.
            </div>
          }
        />
      </div>

      <DepositModal
        btn={selectedDeposit ? "Editar" : "Agregar"}
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
        onAddDeposit={onSubmit}
        initialData={selectedDeposit}
      />
    </div>
  );
};

export default Deposit;
