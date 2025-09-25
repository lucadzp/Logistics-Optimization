import React, { useEffect, useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import api from '../../lib/common/API';

export const DemandModal = ({ isOpen, onClose, onAddDemand, initialData, btn }) => {
    const [depositos, setDepositos] = useState([]);

    useEffect(() => {
        if (initialData) {
            formik.setValues({
                peso_kg: initialData.peso_kg || '',
                descripción: initialData.descripción || '',
                estado: initialData.estado || '',
                deposito: initialData.deposito || '',
               
            });
        }
        else{
            formik.resetForm()
        }
    }, [initialData]);

    const formik = useFormik({
        initialValues: {
            peso_kg: '',
            descripción: '',
            estado: 'pendiente', // Valor inicial "pendiente"
            deposito: '',
        },
        validationSchema: Yup.object({
            peso_kg: Yup.string().required('Requerido'),
            descripción: Yup.string().required('Requerido').max(255, 'Máximo 255 caracteres'),
           
            deposito: Yup.number().integer('Debe ser un número entero').required('Requerido'),
        }),
        onSubmit: (values) => {
            onAddDemand(values)
            formik.resetForm();
        },
    });

    const getDeposit = async () => {
      try {
        const response = await api.get(`resource/depositos`)
        setDepositos(response.data)
  
      } catch (error) {
        console.log(error)
      }
    }

    useEffect(() => {
        getDeposit()
      }, [])
    
    

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg p-6 max-w-lg mx-auto h-auto max-h-[70vh] overflow-auto">
                <h2 className="text-lg font-bold mb-4">Agregar Demanda</h2>
                <div >
                    <div className="mb-4">
                        <label className="block mb-1">Peso (kg)</label>
                        <input
                            type="text"
                            name="peso_kg"
                            value={formik.values.peso_kg}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={`border rounded w-full p-2 ${formik.touched.peso_kg && formik.errors.peso_kg ? 'border-red-500' : ''}`}
                            required
                        />
                        {formik.touched.peso_kg && formik.errors.peso_kg ? (
                            <div className="text-red-500 text-sm">{formik.errors.peso_kg}</div>
                        ) : null}
                    </div>
                    <div className="mb-4">
                        <label className="block mb-1">Descripción</label>
                        <input
                            type="text"
                            name="descripción"
                            value={formik.values.descripción}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={`border rounded w-full p-2 ${formik.touched.descripción && formik.errors.descripción ? 'border-red-500' : ''}`}
                            required
                        />
                        {formik.touched.descripción && formik.errors.descripción ? (
                            <div className="text-red-500 text-sm">{formik.errors.descripción}</div>
                        ) : null}
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
                            <option value="">Selecciona una Deposito</option>
                            {depositos.map((deposit) => (
                                    <option key={deposit.id} value={deposit.id}>{`Deposito Nro: ${deposit.id} ${deposit.nombre}`}</option>
                                ))}
                        </select>
                        {formik.touched.deposito && formik.errors.deposito ? (
                            <div className="text-red-500 text-sm">{formik.errors.deposito}</div>
                        ) : null}
                    </div>
                    <div className="flex justify-between">
                        <button 
                        type="submit"
                        onClick={formik.handleSubmit} className="bg-blue-500 text-white rounded-md p-2">
                            {btn}
                        </button>
                        <button type="button" onClick={onClose} className="bg-gray-300 rounded-md p-2">
                            Cancelar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};
