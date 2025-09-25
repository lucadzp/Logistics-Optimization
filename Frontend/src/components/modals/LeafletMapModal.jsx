import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, useMap, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export const LeafletMapModal = ({ isOpen, onClose, onSaveCoordinates, selectedCoordinates }) => {
    const [position, setPosition] = useState(null);
    const [searchQuery, setSearchQuery] = useState(""); // Estado para la búsqueda
    const [searchResults, setSearchResults] = useState([]); // Resultados de búsqueda
    const [error, setError] = useState(null);
    const [debounceTimeout, setDebounceTimeout] = useState(null); // Timeout para debounce

    useEffect(() => {
        if (selectedCoordinates) {
            setPosition(selectedCoordinates);
        }
    }, [selectedCoordinates]);

    const fetchSuggestions = async (query) => {
        if (!query) {
            setSearchResults([]);
            return;
        }

        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
                    query
                )}&format=json&addressdetails=1&limit=5&countrycodes=PY`
            );
            const data = await response.json();
            setSearchResults(data);
        } catch (err) {
            setError("Error al obtener sugerencias. Por favor, intenta más tarde.");
        }
    };

    const handleSearchChange = (e) => {
        const query = e.target.value;
        setSearchQuery(query);

        // Limpiar el timeout anterior
        if (debounceTimeout) {
            clearTimeout(debounceTimeout);
        }

        // Configurar un nuevo timeout
        const newTimeout = setTimeout(() => {
            fetchSuggestions(query);
        }, 500); // 500ms de delay
        setDebounceTimeout(newTimeout);
    };

    const handleSearchSelect = (lat, lon) => {
        setPosition({ lat: parseFloat(lat), lng: parseFloat(lon) });
        setSearchResults([]);
        setSearchQuery("");
    };

    const LocationMarker = () => {
        useMapEvents({
            click(e) {
                setPosition(e.latlng);
            },
        });

        return position ? <Marker position={position} /> : null;
    };

    if (!isOpen) return null;

    const defaultPosition = [-27.3306, -55.8667]; // Posición inicial predeterminada (Encarnación, Paraguay)

    const MapRefresher = () => {
        const map = useMap();
        useEffect(() => {
            if (position) {
                map.setView(position, 14);
            }
        }, [position, map]);
        return null;
    };

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-4xl relative">
                <h2 className="text-lg font-bold mb-4">
                    {selectedCoordinates ? "Ver Punto Seleccionado" : "Seleccionar Punto en el Mapa"}
                </h2>

                {/* Input para búsqueda de direcciones */}
                <div className="mb-4 relative z-20">
                    <input
                        type="text"
                        placeholder="Buscar por Ciudad"
                        value={searchQuery}
                        onChange={handleSearchChange} // Cambiado para usar la función con setTimeout
                        className="border rounded w-full p-2"
                    />
                    {/* Menú desplegable de sugerencias */}
                    {searchResults.length > 0 && (
                        <ul className="absolute bg-white border rounded w-full max-h-40 overflow-y-auto top-12 shadow-lg">
                            {searchResults.map((result, index) => (
                                <li
                                    key={index}
                                    onClick={() => handleSearchSelect(result.lat, result.lon)}
                                    className="p-2 hover:bg-gray-200 cursor-pointer"
                                >
                                    {result.display_name}
                                </li>
                            ))}
                        </ul>
                    )}
                    {error && <div className="text-red-500 text-sm mt-2">{error}</div>}
                </div>

                {/* Contenedor del mapa */}
                <div className="h-96 relative z-10">
                    <MapContainer
                        center={position || defaultPosition}
                        zoom={14}
                        style={{ height: "100%", width: "100%" }}
                    >
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                        <LocationMarker />
                        <MapRefresher />
                    </MapContainer>
                </div>

                {/* Botones */}
                <div className="flex justify-between mt-4">
                    <button
                        className="bg-blue-500 text-white rounded-md p-2"
                        onClick={() => {
                            if (position) {
                                onSaveCoordinates(position);
                                onClose();
                            } else {
                                alert("Selecciona un punto en el mapa.");
                            }
                        }}
                    >
                        Guardar
                    </button>
                    <button onClick={onClose} className="bg-gray-300 rounded-md p-2">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    );
};
