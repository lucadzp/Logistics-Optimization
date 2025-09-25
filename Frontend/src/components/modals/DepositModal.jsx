import React, { useEffect } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';

export const DepositModal = ({ isOpen, onClose, onAddDeposit, initialData, btn }) => {

    useEffect(() => {
        if (initialData) {
            formik.setValues({
                nombre: initialData.nombre || '',
                latitud: initialData.latitud || '',
                longitud: initialData.longitud || '',
                direccion: initialData.direccion || '',
                numero_de_telefono: initialData.numero_de_telefono || '',
            });
        }
        else{
            formik.resetForm()
        }
    }, [initialData]);

    const formik = useFormik({
        initialValues: {
            nombre: '',
            latitud: '',
            longitud: '',
            direccion: '',
            numero_de_telefono: '',
        },
        validationSchema: Yup.object({
            nombre: Yup.string()
                .min(1, 'El nombre debe tener al menos 1 carácter')
                .max(255, 'El nombre no debe exceder 255 caracteres')
                .required('Requerido'),
            latitud: Yup.string().required('Requerido'),
            longitud: Yup.string().required('Requerido'),
            direccion: Yup.string().max(255, 'La dirección no debe exceder 255 caracteres'),
            numero_de_telefono: Yup.string().max(20, 'El número de teléfono no debe exceder 20 caracteres'),
        }),
        onSubmit: (values) => {
           onAddDeposit(values)
            formik.resetForm();
        },
    });

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 ">
            <div className="bg-white rounded-lg p-6 max-w-lg mx-auto h-auto max-h-[70vh] overflow-auto">
                <h2 className="text-lg font-bold mb-4">Agregar Depósito</h2>
                <form onSubmit={formik.handleSubmit}>
                    <div className="mb-4">
                        <label className="block mb-1">Nombre</label>
                        <input
                            type="text"
                            name="nombre"
                            value={formik.values.nombre}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={`border rounded w-full p-2 ${formik.touched.nombre && formik.errors.nombre ? 'border-red-500' : ''}`}
                            required
                        />
                        {formik.touched.nombre && formik.errors.nombre ? (
                            <div className="text-red-500 text-sm">{formik.errors.nombre}</div>
                        ) : null}
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
                        <label className="block mb-1">Dirección</label>
                        <input
                            type="text"
                            name="direccion"
                            value={formik.values.direccion}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={`border rounded w-full p-2 ${formik.touched.direccion && formik.errors.direccion ? 'border-red-500' : ''}`}
                        />
                        {formik.touched.direccion && formik.errors.direccion ? (
                            <div className="text-red-500 text-sm">{formik.errors.direccion}</div>
                        ) : null}
                    </div>
                    <div className="mb-4">
                        <label className="block mb-1">Número de Teléfono</label>
                        <input
                            type="text"
                            name="numero_de_telefono"
                            value={formik.values.numero_de_telefono}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={`border rounded w-full p-2 ${formik.touched.numero_de_telefono && formik.errors.numero_de_telefono ? 'border-red-500' : ''}`}
                        />
                        {formik.touched.numero_de_telefono && formik.errors.numero_de_telefono ? (
                            <div className="text-red-500 text-sm">{formik.errors.numero_de_telefono}</div>
                        ) : null}
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
