import React from 'react';

const GoogleMapsButton = ({ coordinates, deposito }) => {
    const handleClick = () => {
        const url = generateGoogleMapsUrl(coordinates, deposito);
        window.open(url, '_blank');
    };

    return (
        <button onClick={handleClick} className="btn btn-primary">
            Abrir en Google Maps
        </button>
    );
};

const generateGoogleMapsUrl = (coordinates, deposito) => {
    let googleMapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${deposito.latitud},${deposito.longitud}`;

    const waypoints = coordinates.map(coord => `${coord.latitud},${coord.longitud}`).join('|');
    if (waypoints) {
        googleMapsUrl += `&waypoints=${waypoints}`;
    }

    googleMapsUrl += `&destination=${deposito.latitud},${deposito.longitud}`;

    return googleMapsUrl;
};

export default GoogleMapsButton;
