import React, { useEffect, useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import api from '../../lib/common/API';

export const VehiculesModals = ({ isOpen, onClose, onAddVehicle,initialData, btn  }) => {
    const [depositos, setDepositos] = useState([]);

    useEffect(() => {
        if (initialData) {
            formik.setValues({
                matricula: initialData.matricula || '',
                capacidad_de_carga: initialData.capacidad_de_carga || '',
                deposito: initialData.deposito || '',
                estado: initialData.estado || '',
               
            });
        }
        else{
            formik.resetForm()
        }
    }, [initialData]);

    const getDeposit = async () => {
        try {
            const response = await api.get(`resource/depositos`);
            setDepositos(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    useEffect(() => {
        getDeposit();
    }, []);

    const formik = useFormik({
        initialValues: {
            matricula: '',
            capacidad_de_carga: '',
            deposito: '',
            estado: '',
        },
        validationSchema: Yup.object({
            matricula: Yup.string().required('Requerido'),
            capacidad_de_carga: Yup.string().required('Requerido'),
            deposito: Yup.string().required('Requerido'),
            estado: Yup.string().required('Requerido'),
        }),
        onSubmit: (values) => {
            onAddVehicle(values); // Genera un ID único
            formik.resetForm();
        },
    });

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg p-6 max-w-lg mx-auto h-auto max-h-[70vh] overflow-auto">
                <h2 className="text-lg font-bold mb-4">Agregar Vehículo</h2>
                <form onSubmit={formik.handleSubmit}>
                    <div className="mb-4">
                        <label className="block mb-1">Matrícula</label>
                        <input
                            type="text"
                            name="matricula"
                            value={formik.values.matricula}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={`border rounded w-full p-2 ${formik.touched.matricula && formik.errors.matricula ? 'border-red-500' : ''}`}
                            required
                        />
                        {formik.touched.matricula && formik.errors.matricula && (
                            <div className="text-red-500 text-sm">{formik.errors.matricula}</div>
                        )}
                    </div>
                    <div className="mb-4">
                        <label className="block mb-1">Capacidad de Carga</label>
                        <input
                            type="number"
                            name="capacidad_de_carga"
                            value={formik.values.capacidad_de_carga}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={`border rounded w-full p-2 ${formik.touched.capacidad_de_carga && formik.errors.capacidad_de_carga ? 'border-red-500' : ''}`}
                            required
                        />
                        {formik.touched.capacidad_de_carga && formik.errors.capacidad_de_carga && (
                            <div className="text-red-500 text-sm">{formik.errors.capacidad_de_carga}</div>
                        )}
                    </div>
                    <div className="mb-4">
                        <label className="block mb-1">Depósito</label>
                        <select
                            name="deposito"
                            value={formik.values.deposito}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={`border rounded w-full p-2 ${formik.touched.deposito && formik.errors.deposito ? 'border-red-500' : ''}`}
                            required
                        >
                            <option value="">Selecciona un depósito</option>
                            {depositos.map((deposito) => (
                                <option key={deposito.id} value={deposito.id}>{deposito.nombre}</option>
                            ))}
                        </select>
                        {formik.touched.deposito && formik.errors.deposito && (
                            <div className="text-red-500 text-sm">{formik.errors.deposito}</div>
                        )}
                    </div>
                    <div className="mb-4">
                        <label className="block mb-1">Estado</label>
                        <select
                            name="estado"
                            value={formik.values.estado}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={`border rounded w-full p-2 ${formik.touched.estado && formik.errors.estado ? 'border-red-500' : ''}`}
                            required
                        >
                            <option value="" label="Seleccionar estado" />
                            <option value="disponible" label="Disponible" />
                            <option value="no_disponible" label="No Disponible" />
                        </select>
                        {formik.touched.estado && formik.errors.estado && (
                            <div className="text-red-500 text-sm">{formik.errors.estado}</div>
                        )}
                    </div>

                    <div className="flex justify-between">
                        <button type="submit" className="bg-blue-500 text-white rounded-md p-2">
                           {btn}
                        </button>
                        <button type="button" onClick={onClose} className="bg-gray-300 rounded-md p-2">
                            Cancelar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};
