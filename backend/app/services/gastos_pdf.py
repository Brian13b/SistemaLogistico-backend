from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import tempfile

def generar_pdf_gastos(gastos):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Reporte de Gastos", styles['Title']))
    elements.append(Spacer(1, 12))

    data = [["ID", "Viaje", "Nombre", "Descripción", "Monto", "Fecha"]]
    for g in gastos:
        data.append([g.id, g.viaje_id, g.nombre, g.descripcion, g.monto, str(g.fecha)])
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    fechas = [str(g.fecha) for g in gastos]
    montos = [g.monto for g in gastos]
    if fechas and montos:
        plt.figure(figsize=(6,3))
        plt.bar(fechas, montos)
        plt.xticks(rotation=45)
        plt.title("Gastos por Fecha")
        plt.tight_layout()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            plt.savefig(tmpfile.name)
            plt.close()
            elements.append(Paragraph("Gráfico de Gastos por Fecha", styles['Heading2']))
            elements.append(Spacer(1, 12))
            elements.append(Image(tmpfile.name, width=400, height=200))

    doc.build(elements)
    buffer.seek(0)
    return buffer