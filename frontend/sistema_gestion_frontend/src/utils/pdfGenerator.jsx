import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

// Colores para el diseño del PDF
const COLORS = {
  primary: '#3498db',
  secondary: '#2ecc71',
  accent: '#e74c3c',
  dark: '#2c3e50',
  light: '#ecf0f1',
  text: '#333333'
};

export const generarReportePDF = (reportesSeleccionados, tiposReportes, datosEjemplo, fechaInicio, fechaFin) => {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm'
  });
  
  // Configuración inicial
  doc.setFont('helvetica');
  doc.setTextColor(COLORS.text);
  
  // Logo (puedes reemplazar con tu propio logo en base64)
  // doc.addImage(logoData, 'PNG', 15, 10, 30, 15);
  
  // Encabezado
  doc.setFontSize(20);
  doc.setTextColor(COLORS.primary);
  doc.setFont('helvetica', 'bold');
  doc.text('Reporte del Sistema', 105, 20, { align: 'center' });
  
  doc.setFontSize(12);
  doc.setTextColor(COLORS.dark);
  doc.setFont('helvetica', 'normal');
  doc.text(`Período: ${formatearFechaAR(fechaInicio)} - ${formatearFechaAR(fechaFin)}`, 105, 28, { align: 'center' });
  
  // Línea decorativa
  doc.setDrawColor(COLORS.primary);
  doc.setLineWidth(0.5);
  doc.line(15, 32, 195, 32);
  
  // Fecha de generación
  const fechaGen = new Date();
  doc.setFontSize(10);
  doc.setTextColor(COLORS.text);
  doc.text(`Generado el: ${fechaGen.toLocaleDateString('es-AR')} a las ${fechaGen.toLocaleTimeString('es-AR')}`, 15, 40);
  
  let posY = 45;
  
  // Agregar cada reporte seleccionado
  Object.entries(reportesSeleccionados).forEach(([id, seleccionado]) => {
    if (seleccionado) {
      const reporte = tiposReportes.find(r => r.id === id);
      const datos = datosEjemplo[id];
      
      if (!datos || datos.length === 0) return;
      
      // Configuración de la tabla
      let headers = [];
      let rows = [];
      let columnStyles = {};
      
      // Configurar según el tipo de reporte
      switch(id) {
        case 'viajes':
          headers = ['ID', 'Origen', 'Destino', 'Fecha', 'Kilómetros'];
          rows = datos.map(item => [
            item.id,
            item.origen,
            item.destino,
            item.fecha,
            item.kilometros
          ]);
          columnStyles = {
            0: { cellWidth: 15 },
            3: { cellWidth: 20 },
            4: { cellWidth: 20 }
          };
          break;
          
        case 'vehiculos':
          headers = ['ID', 'Patente', 'Marca', 'Modelo', 'Año', 'Kilometraje'];
          rows = datos.map(item => [
            item.id,
            item.patente,
            item.marca,
            item.modelo,
            item.año,
            item.km
          ]);
          columnStyles = {
            0: { cellWidth: 15 },
            1: { cellWidth: 20 },
            4: { cellWidth: 15 },
            5: { cellWidth: 20 }
          };
          break;
          
        case 'conductores':
          headers = ['ID', 'Nombre', 'Licencia', 'Vencimiento', 'Viajes'];
          rows = datos.map(item => [
            item.id,
            item.nombre,
            item.licencia,
            item.vencimiento,
            item.viajes
          ]);
          columnStyles = {
            0: { cellWidth: 15 },
            2: { cellWidth: 20 },
            4: { cellWidth: 15 }
          };
          break;
          
        case 'facturacion':
          headers = ['N° Factura', 'Cliente', 'Monto', 'Fecha', 'Estado'];
          rows = datos.map(item => [
            item.num,
            item.cliente,
            `$${item.monto.toLocaleString('es-AR')}`,
            item.fecha,
            item.estado
          ]);
          columnStyles = {
            0: { cellWidth: 25 },
            2: { cellWidth: 20 },
            3: { cellWidth: 20 },
            4: { cellWidth: 20 }
          };
          break;
      }
      
      // Título de la sección
      doc.setFontSize(14);
      doc.setTextColor(COLORS.secondary);
      doc.setFont('helvetica', 'bold');
      doc.text(reporte.nombre, 15, posY);
      posY += 8;
      
      // Generar tabla con autoTable
      doc.autoTable({
        startY: posY,
        head: [headers],
        body: rows,
        theme: 'grid',
        headStyles: {
          fillColor: COLORS.primary,
          textColor: COLORS.light,
          fontStyle: 'bold'
        },
        alternateRowStyles: {
          fillColor: COLORS.light
        },
        columnStyles,
        margin: { left: 15, right: 15 },
        styles: {
          fontSize: 10,
          cellPadding: 3,
          overflow: 'linebreak'
        },
        didDrawPage: (data) => {
          posY = data.cursor.y + 10;
        }
      });
      
      // Espacio después de la tabla
      posY += 10;
      
      // Verificar si necesitamos una nueva página
      if (posY > 270) {
        doc.addPage();
        posY = 20;
      }
    }
  });
  
  // Pie de página
  doc.setFontSize(10);
  doc.setTextColor(COLORS.dark);
  doc.setFont('helvetica', 'italic');
  doc.text('© 2023 Transportes App - Todos los derechos reservados', 105, 287, { align: 'center' });
  
  return doc;
};

const formatearFechaAR = (fechaISO) => {
  if (!fechaISO) return '';
  const fecha = new Date(fechaISO);
  return fecha.toLocaleDateString('es-AR');
};