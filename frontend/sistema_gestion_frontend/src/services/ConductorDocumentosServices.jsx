import api from './api';

export const conductorDocumentosService = {
    getAll: () => api.get(`/documentos_conductores`),
    getById: (documentoId) => api.get(`/documentos_conductores/${documentoId}`),
    create: (data) => api.post(`/documentos_conductores`, data),
    update: (documentoId, data) => api.put(`/documentos_conductores/${documentoId}`, data),
    delete: (documentoId) => api.delete(`/documentos_conductores/${documentoId}`),
    getAllByConductor: (conductorId) => api.get(`/documentos_conductores/conductor/${conductorId}`),
};