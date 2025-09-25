import React, { useEffect, useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import api from '../../lib/common/API';
import { DemandModal } from './DemandModal';
import { toast } from 'react-toastify';
import { LeafletMapModal } from './LeafletMapModal';
import { AiTwotonePlusCircle } from "react-icons/ai";



export const DeliveryPointModal = ({ isOpenDeliveryPoint, onCloseDeliveryPoint, onAddDeliveryPoint, initialData, btn }) => {
    const [demands, setDemands] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isDemandModalOpen, setDemandModalOpen] = useState(false);
    const [isMapModalOpen, setMapModalOpen] = useState(false);
    const [formData, setFormData] = useState({
        cliente: '',
        latitud: '',
        longitud: '',
        demanda: '',
        estado: '',
        numero_de_telefono: '',
    });

    const handleSaveCoordinates = (coordinates) => {
        formik.setFieldValue("latitud", coordinates.lat.toFixed(6));
        formik.setFieldValue("longitud", coordinates.lng.toFixed(6));
    };

    const getDemands = async () => {
        try {
            const response = await api.get(`resource/demandas`);
            setDemands(response.data);
        } catch (error) {
            console.log(error);
        }
    };



    const formik = useFormik({
        initialValues: {
            cliente: '',
            latitud: '',
            longitud: '',
            demanda: '',
            numero_de_telefono: '',
        },

        validationSchema: Yup.object({
            cliente: Yup.string().required('Requerido').max(255, 'Máximo 255 caracteres').min(1, 'Debe tener al menos 1 carácter'),
            latitud: Yup.string()
                .length(10, 'Debe contener exactamente 10 caracteres')
                .required('Requerido'),
            longitud: Yup.string()
                .length(10, 'Debe contener exactamente 10 caracteres')
                .required('Requerido'),

            demanda: Yup.number().integer('Debe ser un número entero').required('Requerido'),

            numero_de_telefono: Yup.string().required('Requerido').max(20, 'Máximo 20 caracteres').min(1, 'Debe tener al menos 1 carácter'),
        }),
        onSubmit: (values) => {

            onAddDeliveryPoint(values);
            formik.resetForm();
        },
    });


    useEffect(() => {
        if (initialData) {
            formik.setValues({
                cliente: initialData.cliente || '',
                latitud: initialData.latitud || '',
                longitud: initialData.longitud || '',
                demanda: initialData.demanda || '',
                estado: initialData.estado || 'pendiente',
                numero_de_telefono: initialData.numero_de_telefono || '',
            });
        } else {
            formik.resetForm();
        }
    }, [initialData]);

    useEffect(() => {
        if (isOpenDeliveryPoint) getDemands();
    }, [isOpenDeliveryPoint]);
    
    
    const onSubmitDemands = async (data) => {
        try {
            setIsLoading(true)
            await api.post(`resource/demandas/`, data);
            toast.success('Demanda creada exitosamente');
            getDemands();  // Refresca las demandas
            setDemandModalOpen(false); // Cierra el modal solo después de éxito
        } catch (error) {
            // Muestra el mensaje de error pero no cierra el modal.
            console.error('Error details:', error);
            if (error.response) {
                toast.error(`Error: ${error.response.data.message || 'Error interno del servidor'}`);
            } else {
                toast.error('Error de conexión o de configuración');
            }
        } finally {

            setIsLoading(false);

        }
    };


    const handleOpenModal = () => {
        setDemandModalOpen(true);
    };

    const handleCloseModal = () => {
        setDemandModalOpen(false);
    };

    if (!isOpenDeliveryPoint) return null;

    return (
        <div className="z-[1000] fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="z-50000 bg-white rounded-lg p-6 max-w-lg mx-auto h-auto max-h-[70vh] overflow-auto">
                <h2 className="text-lg font-bold mb-4">Agregar Punto de Entrega</h2>
                {isLoading ? (
                    <div className="z-500 flex justify-center items-center">
                        <div className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full" role="status"></div>
                        <span className="ml-2 text-blue-500">Procesando...</span>
                    </div>
                ) : (
                    <form onSubmit={formik.handleSubmit}>
                        <div className="mb-4">
                            <label className="block mb-1">Cliente</label>
                            <input
                                type="text"
                                name="cliente"
                                value={formik.values.cliente}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                className={`border rounded w-full p-2 ${formik.touched.cliente && formik.errors.cliente ? 'border-red-500' : ''}`}
                                required
                            />
                            {formik.touched.cliente && formik.errors.cliente ? (
                                <div className="text-red-500 text-sm">{formik.errors.cliente}</div>
                            ) : null}
                        </div>
                        <div className="mb-4 flex justify-center">
                            <button
                                type="button"
                                onClick={() => setMapModalOpen(true)}
                                className="bg-green-500 text-white rounded-md p-2"
                            >
                                Seleccionar en Mapa
                            </button>
                        </div>
                        <div className="mb-4">
                            <label className="block mb-1">Latitud</label>
                            <input
                                type="text"
                                name="latitud"
                                value={formik.values.latitud}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                className={`border rounded w-full p-2 ${formik.touched.latitud && formik.errors.latitud ? 'border-red-500' : ''}`}
                                required
                            />
                            {formik.touched.latitud && formik.errors.latitud ? (
                                <div className="text-red-500 text-sm">{formik.errors.latitud}</div>
                            ) : null}
                        </div>
                        <div className="mb-4">
                            <label className="block mb-1">Longitud</label>
                            <input
                                type="text"
                                name="longitud"
                                value={formik.values.longitud}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                className={`border rounded w-full p-2 ${formik.touched.longitud && formik.errors.longitud ? 'border-red-500' : ''}`}
                                required
                            />
                            {formik.touched.longitud && formik.errors.longitud ? (
                                <div className="text-red-500 text-sm">{formik.errors.longitud}</div>
                            ) : null}
                        </div>
                        <div className="mb-4">
                            <label className="block mb-1">Demandas</label>
                            <div className="flex items-center relative">
                                <select
                                    name="demanda"
                                    value={formik.values.demanda}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    className={`border rounded w-full p-2 ${formik.touched.demanda && formik.errors.demanda ? 'border-red-500' : ''}`}
                                    required
                                >
                                    <option value="">Selecciona una Demanda</option>
                                    {demands
                                        .filter(demand => demand.estado == 'pendiente') // Filtramos para no mostrar las demandas "pendientes"
                                        .sort((a, b) => {
                                            // Primero las pendientes, luego las demás (aunque ya no las mostramos)
                                            if (a.estado === 'pendiente' && b.estado !== 'pendiente') return -1;
                                            if (a.estado !== 'pendiente' && b.estado === 'pendiente') return 1;
                                            return 0;
                                        })
                                        .map((demand) => (
                                            <option
                                                className={`${demand.estado === 'pendiente' ? 'text-gray-900 hover:bg-gray-200' : 'text-gray-400 cursor-not-allowed'
                                                    } px-4 py-2`}
                                                key={demand.id}
                                                value={demand.id}
                                                disabled={demand.estado !== 'pendiente'} // Deshabilitar si no está pendiente
                                            >
                                                {demand.descripción}
                                            </option>
                                        ))}
                                </select>



                                <button
                                    type="button"
                                    onClick={() => setDemandModalOpen(true)}
                                    className="ml-2 text-white rounded-md"
                                >
                                    <AiTwotonePlusCircle size={32} />
                                </button>
                            </div>
                            {formik.touched.demanda && formik.errors.demanda ? (
                                <div className="text-red-500 text-sm">{formik.errors.demanda}</div>
                            ) : null}
                        </div>

                        {/* Modal para agregar demanda */}
                        {isDemandModalOpen && (
                            <DemandModal
                                isOpen={isDemandModalOpen}
                                onClose={handleCloseModal}
                                onAddDemand={onSubmitDemands}
                                btn={"Agregar"}
                            />
                        )}

                        <div className="mb-4">
                            <label className="block mb-1">Número de Teléfono</label>
                            <input
                                type="text"
                                name="numero_de_telefono"
                                value={formik.values.numero_de_telefono}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                className={`border rounded w-full p-2 ${formik.touched.numero_de_telefono && formik.errors.numero_de_telefono ? 'border-red-500' : ''}`}
                                required
                            />
                            {formik.touched.numero_de_telefono && formik.errors.numero_de_telefono ? (
                                <div className="text-red-500 text-sm">{formik.errors.numero_de_telefono}</div>
                            ) : null}
                        </div>
                        <div className="flex justify-between">
                            <button type="submit" className="bg-blue-500 text-white rounded-md p-2">
                                {btn}
                            </button>
                            <button type="button" onClick={onCloseDeliveryPoint} className="bg-gray-300 rounded-md p-2">
                                Cancelar
                            </button>
                        </div>
                    </form>
                )}
            </div>
            {/* Modal del mapa */}
            <LeafletMapModal
                isOpen={isMapModalOpen}
                onClose={() => setMapModalOpen(false)}
                onSaveCoordinates={handleSaveCoordinates}
            />
        </div>
    );
};
