import api from './api';

export const viajesDocumentosService = {
    getAll: () => api.get(`/documentos_viajes`),
    getById: (documentoId) => api.get(`/documentos_viajes/${documentoId}`),
    create: (data) => {
        const formData = new FormData();
        formData.append('documento_data', JSON.stringify(data.documento_data));
        formData.append('archivo', data.archivo);
      
        return api.post(`/documentos_viajes/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
    },
    update: (documentoId, data) => {
        const formData = new FormData();
        formData.append('documento_data', JSON.stringify(data.documento_data));
        if (data.archivo) {
            formData.append('archivo', data.archivo);
        }
    
        return api.put(`/documentos_viajes/${documentoId}`, formData, {
            headers: {
            'Content-Type': 'multipart/form-data'
            }
        });
    },
    deleteDocumento: (documentoId) => api.delete(`/documentos_viajes/${documentoId}`),
    getAllByViaje: (viajeId) => api.get(`/documentos_viajes/viajes/${viajeId}`),
};