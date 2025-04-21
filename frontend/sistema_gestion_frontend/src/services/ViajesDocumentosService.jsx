import api from './api';

export const viajesDocumentosService = {
    getAll: () => api.get(`/documentos_viajes`),
    getById: (documentoId) => api.get(`/documentos_viajes/${documentoId}`),
    create: (data) => api.post(`/documentos_viajes`, data),
    update: (documentoId, data) => api.put(`/documentos_viajes/${documentoId}`, data),
    deleteDocumento: (documentoId) => api.delete(`/documentos_viajes/${documentoId}`),
    getAllByViaje: (viajeId) => api.get(`/documentos_viajes/viaje/${viajeId}`),
};