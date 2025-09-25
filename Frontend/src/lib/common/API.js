import axios from "axios";

// Configuración base de axios
const api = axios.create({
  baseURL: import.meta.env.VITE_base_url || "http://localhost:8000/api/v1/", // Fallback a localhost si no hay env var
  withCredentials: false // No se necesitan credenciales si no hay autenticación
});

// Interceptor de respuesta para manejar errores globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Error en la respuesta de la API:', error);
    return Promise.reject(error);
  }
);

export default api;
