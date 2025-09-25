import { useState } from 'react';
import { FaBars, FaHome, FaTruck, FaUser } from 'react-icons/fa';

const Sidebar = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="flex">
            {/* Botón para abrir/cerrar el sidebar */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="p-3 bg-gray-800 text-white focus:outline-none"
            >
                <FaBars />
            </button>

            {/* Sidebar */}
            <div
                className={`fixed top-0 left-0 h-full bg-gray-900 text-white transform ${isOpen ? 'translate-x-0' : '-translate-x-full'
                    } transition-transform duration-300 ease-in-out`}
            >
                <div className="p-4 text-lg font-bold">
                    Logística
                </div>
                <ul className="space-y-6 p-4">
                    <li className="flex items-center space-x-2">
                        <FaHome />
                        <span>Inicio</span>
                    </li>
                    <li className="flex items-center space-x-2">
                        <FaTruck />
                        <span>Envíos</span>
                    </li>
                    <li className="flex items-center space-x-2">
                        <FaUser />
                        <span>Clientes</span>
                    </li>
                    {/* Agrega más enlaces según sea necesario */}
                </ul>
            </div>
        </div>
    );
};

export default Sidebar;
