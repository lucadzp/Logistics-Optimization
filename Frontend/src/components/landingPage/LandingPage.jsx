// src/components/LandingPage.jsx
import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const LandingPage = () => {
    // Configuración del carrusel
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
    };

    return (
        <div className="bg-gray-50 text-gray-900">
            {/* Header */}
            <header className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-6 py-4">
                    <h1 className="text-3xl font-bold">Optimización de Rutas</h1>
                    <p className="mt-2 text-lg">Maximiza la eficiencia de tus entregas y reduce costos con nuestra solución innovadora.</p>
                    
                </div>
            </header>

            {/* Features - Carrusel */}
            <section className="py-16 bg-gray-100">
                <div className="max-w-7xl mx-auto px-6">
                    <h2 className="text-2xl font-bold text-center">Características Clave</h2>
                    <Slider {...settings} className="mt-8">
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h3 className="font-semibold text-lg">Carga de Vehículos en el Sistema</h3>
                            <p className="mt-2">Gestiona la carga de cada vehículo en el sistema para una distribución eficiente.</p>
                        </div>
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h3 className="font-semibold text-lg">Depósito</h3>
                            <p className="mt-2">Controla el inventario en tu depósito para asegurar que cada carga esté disponible.</p>
                        </div>
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h3 className="font-semibold text-lg">Punto de Entrega</h3>
                            <p className="mt-2">Marca múltiples puntos de entrega en el mapa para optimizar tus rutas.</p>
                        </div>
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h3 className="font-semibold text-lg">Optimización de Rutas</h3>
                            <p className="mt-2">Nuestro sistema calcula la ruta más corta y eficiente de acuerdo a la carga y demanda.</p>
                        </div>
                    </Slider>
                </div>
            </section>

       

            {/* Footer */}
            <footer className="bg-primary-600 text-white py-4">
                <div className="max-w-7xl mx-auto text-center">
                    <p>&copy; {new Date().getFullYear()} Optimización de Rutas. Todos los derechos reservados.</p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
