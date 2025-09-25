import { Link } from 'react-router-dom';
import { useState } from 'react';

const NavBar = () => {
    const [isSidebarOpen, setSidebarOpen] = useState(false);

    return (
        <nav className=" bg-primary-100 dark:bg-primary-500 fixed top-0 left-0 w-full z-50 flex justify-center p-4 ">
          

            {/* Botón de menú (solo visible en mobile) */}
            <button
                className="  block md:hidden text-gray-900 dark:text-white focus:outline-none"
                onClick={() => setSidebarOpen(!isSidebarOpen)}
            >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            </button>

            {/* Menú en pantalla completa (solo visible en desktop) */}
            <div className="hidden md:flex space-x-6 ">
                <Link to="/" className="text-red-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold transition duration-300 ease-in-out transform hover:scale-105">
                    Inicio
                </Link>
                <Link to="deposit" className="text-red-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold transition duration-300 ease-in-out transform hover:scale-105">
                    Depositos
                </Link>
                <Link to="vehicules" className="text-red-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold transition duration-300 ease-in-out transform hover:scale-105">
                    Vehiculos
                </Link>
                <Link to="delivery-point" className="text-red-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold transition duration-300 ease-in-out transform hover:scale-105">
                    Punto de Entrega
                </Link>
                <Link to="Demand" className="text-red-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold transition duration-300 ease-in-out transform hover:scale-105">
                    Demanda
                </Link>
            </div>

            {/* Sidebar (solo visible en mobile) */}
            {isSidebarOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden" onClick={() => setSidebarOpen(false)}>
                    <div
                        className="fixed top-0 left-0 h-full w-64 bg-white dark:bg-gray-800 p-4 z-50"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <button
                            className="text-gray-900 dark:text-white mb-4 focus:outline-none"
                            onClick={() => setSidebarOpen(false)}
                        >
                            ✖ Cerrar
                        </button>
                        <nav className="flex flex-col space-y-4">
                            <Link to="/" className="text-primary-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold">
                                Inicio
                            </Link>
                            <Link to="deposit" className="text-primary-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold">
                                Depositos
                            </Link>
                            <Link to="vehicules" className="text-primary-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold">
                                Vehiculos
                            </Link>
                            <Link to="delivery-point" className="text-primary-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold">
                                Punto de Entrega
                            </Link>
                            <Link to="Demand" className="text-primary-100 hover:bg-blue-600 hover:text-white dark:text-white dark:hover:bg-blue-400 rounded-2xl p-2 font-semibold">
                                Demanda
                            </Link>
                        </nav>
                    </div>
                </div>
            )}
        </nav>
    );
};

export default NavBar;
