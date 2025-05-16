import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

export const generateFichaPDF = async (type, data, documentos = [], formatDate) => {
  const pdf = new jsPDF('p', 'mm', 'a4');
  const margin = 10;
  let y = margin;

  const width = pdf.internal.pageSize.getWidth();
  const height = pdf.internal.pageSize.getHeight();

  // Título principal
  pdf.setFontSize(16);
  pdf.setFont(undefined, 'bold');

  if (type === 'vehiculo') {
    pdf.text(`Ficha del Vehículo: ${data.marca} ${data.modelo}`, margin, y);
    y += 10;

    y = renderVehiculo(pdf, data, y, margin);
  }

  if (type === 'conductor') {
    pdf.text(`Ficha de Conductor: ${data.nombre} ${data.apellido}`, margin, y);
    y += 10;

    y = await renderConductor(pdf, data, y, margin, formatDate);
  }

  if (type === 'viaje') {
    pdf.text(`Detalles del Viaje: ${data.origen} - ${data.destino}`, margin, y);
    y += 10;

    y = renderViaje(pdf, data, y, margin, formatDate);
  }

  if (documentos.length > 0) {
    pdf.setFont(undefined, 'bold');
    pdf.text('Documentos', margin, y + 10);
    y += 17;

    autoTable(pdf, {
      startY: y,
      head: [['Tipo de Documento', 'Fecha Emisión', 'Fecha Vencimiento']],
      body: documentos.map(doc => [
        doc.tipo_documento || 'No especificado',
        formatDate(doc.fecha_emision) || 'N/A',
        formatDate(doc.fecha_vencimiento) || 'N/A',
      ]),
      margin: { left: margin },
      styles: { fontSize: 10 },
    });
  }

  pdf.setProperties({
    title: `Ficha ${type}`,
    subject: 'Información',
    creator: 'Sistema de Gestión'
  });

  const filename = `Ficha_${type}_${(data.nombre || data.marca || data.origen || 'registro').replace(/\s/g, '_')}.pdf`;
  pdf.save(filename);
};

const renderVehiculo = (pdf, vehiculo, y, margin) => {
  pdf.setFontSize(12);
  pdf.setFont(undefined, 'bold');
  pdf.text('Información del Vehículo:', margin, y);
  y += 7;

  pdf.setFont(undefined, 'normal');
  const fields = [
    ['Patente', vehiculo.patente],
    ['Código', vehiculo.codigo],
    ['Estado', vehiculo.estado],
    ['Año', vehiculo.anio],
    ['Tipo', vehiculo.tipo],
    ['Tara', vehiculo.tara],
    ['Carga Máxima', vehiculo.carga_maxima],
    ['Kilometraje', vehiculo.kilometraje],
  ];

  fields.forEach(([label, value]) => {
    pdf.text(`${label}: ${value || 'No especificado'}`, margin, y);
    y += 6;
  });

  return y;
};

const renderConductor = async (pdf, conductor, y, margin, formatDate) => {
  if (conductor.foto) {
    try {
      const img = new Image();
      img.crossOrigin = 'Anonymous';
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = conductor.foto;
      });
      pdf.addImage(img, 'JPEG', margin, y, 30, 30);
      y += 35;
    } catch (e) {
      console.warn('Imagen conductor no cargada', e);
    }
  }

  pdf.setFontSize(12);
  pdf.setFont(undefined, 'bold');
  pdf.text('Información Personal', margin, y);
  y += 7;

  pdf.setFont(undefined, 'normal');
  const info = [
    ['DNI', conductor.dni || 'No especificado'],
    ['Código', conductor.codigo || `C-${String(conductor.id).padStart(3, '0')}`],
    ['Estado', conductor.estado || 'N/A'],
    ['Teléfono', conductor.numero_contacto || 'No especificado'],
    ['Email', conductor.email_contacto || 'No especificado'],
    ['Dirección', conductor.direccion || 'No especificada'],
    ['Fecha Vencimiento', formatDate(conductor.fecha_vencimiento) || 'No especificada'],
  ];

  info.forEach(([label, value]) => {
    pdf.text(`${label}: ${value || 'No especificado'}`, margin, y);
    y += 6;
  });

  return y;
};

const renderViaje = (pdf, viaje, y, margin, formatDate) => {
  pdf.setFont(undefined, 'bold');
  pdf.text('Información del Viaje', margin, y);
  y += 7;

  pdf.setFont(undefined, 'normal');
  const data = [
    ['Código', viaje.codigo || 'No especificado'],
    ['Estado', viaje.estado || 'N/A'],
    ['Origen', viaje.origen || 'N/A'],
    ['Destino', viaje.destino || 'N/A'],
    ['Fecha Salida', formatDate(viaje.fecha_salida) || 'N/A'],
    ['Fecha Llegada', formatDate(viaje.fecha_llegada) || 'N/A'],
  ];

  data.forEach(([label, value]) => {
    pdf.text(`${label}: ${value || 'N/A'}`, margin, y);
    y += 6;
  });

  if (viaje.conductor) {
    pdf.setFont(undefined, 'bold');
    pdf.text('Conductor', margin, y);
    y += 7;

    pdf.setFont(undefined, 'normal');
    pdf.text(`Nombre: ${viaje.conductor.nombre} ${viaje.conductor.apellido}`, margin, y);
    y += 6;
  }

  if (viaje.vehiculo) {
    pdf.setFont(undefined, 'bold');
    pdf.text('Vehículo', margin, y);
    y += 7;

    pdf.setFont(undefined, 'normal');
    pdf.text(`Patente: ${viaje.vehiculo.patente}`, margin, y);
    y += 6;
  }

  if (viaje.observaciones) {
    pdf.setFont(undefined, 'bold');
    pdf.text('Observaciones', margin, y);
    y += 7;

    pdf.setFont(undefined, 'normal');
    const split = pdf.splitTextToSize(viaje.observaciones, 180);
    pdf.text(split, margin, y);
    y += split.length * 6;
  }

  return y;
};
