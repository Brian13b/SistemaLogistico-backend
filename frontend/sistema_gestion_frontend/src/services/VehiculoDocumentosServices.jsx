import api from './api';

export const vehiculoDocumentosService = {
    getAll: () => api.get(`/documentos_vehiculos`),
    getById: (documentoId) => api.get(`/documentos_vehiculos/${documentoId}`),
    create: (data) => api.post(`/documentos_vehiculos`, data),
    update: (documentoId, data) => api.put(`/documentos_vehiculos/${documentoId}`, data),
    delete: (documentoId) => api.delete(`/documentos_vehiculos/${documentoId}`),
    getAllByVehiculo: (vehiculoId) => api.get(`/documentos_vehiculos/vehiculo/${vehiculoId}`),
};