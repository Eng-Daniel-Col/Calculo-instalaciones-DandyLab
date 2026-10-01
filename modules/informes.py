# modules/informes.py
import io
import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generar_pdf_informe(datos_cliente, resumen, logo_path=None, fotos_nameplates=None, parametros_corte=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    story = []
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle('Titulo', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor("#1A365D"), leading=16)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=colors.HexColor("#475569"), leading=11)
    sec_style = ParagraphStyle('Sec', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#1A365D"), leading=12)

    # 1. Encabezado con Logo
    text_header = [
        Paragraph("<b>DANDYLAB SOLUCIONES</b>", titulo_style),
        Paragraph("Servicios de Ingeniería | Instalaciones Industriales & Láser", sub_style)
    ]
    
    if logo_path and os.path.exists(logo_path):
        tabla_header = Table([[Image(logo_path, width=70, height=45), text_header]], colWidths=[80, 472])
    else:
        tabla_header = Table([[text_header]], colWidths=[552])

    tabla_header.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(tabla_header)
    story.append(Spacer(1, 10))

    # 2. Datos Cliente
    datos_cli_tabla = [
        [f"<b>Cliente / Empresa:</b> {datos_cliente['cliente']}", f"<b>Teléfono:</b> {datos_cliente['telefono']}"],
        [f"<b>Dirección:</b> {datos_cliente['direccion']}", f"<b>Modelo Máquina:</b> {datos_cliente['modelo']}"],
        [f"<b>Norma Evaluada:</b> {datos_cliente['norma']}", f"<b>Fecha Instalación:</b> {datos_cliente['fecha']}"]
    ]
    t_cli = Table(datos_cli_tabla, colWidths=[300, 252])
    t_cli.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cli)
    story.append(Spacer(1, 10))

    # 3. Diagrama Unifilar
    story.append(Paragraph("<b>ARQUITECTURA Y ESQUEMA UNIFILAR DE CONEXIÓN</b>", sec_style))
    story.append(Spacer(1, 4))

    bloque_red = f"<b>RED CLIENTE</b><br/>{resumen['v_primario']}V (Trifásica)"
    bloque_trafo = f"<b>TRANSFORMADOR</b><br/>Capacidad: {resumen['transformador_kva']} kVA<br/>Entrada: {resumen['v_primario']}V | Salida: {resumen['v_secundario']}V"
    bloque_tablero = f"<b>TABLERO MÁQUINA</b><br/>Operación: {resumen['v_secundario']}V Trifásico<br/>Potencia Total: {resumen['potencia_total_kw']} kW"

    tabla_unifilar = Table([[
        Paragraph(bloque_red, sub_style),
        Paragraph("➔", titulo_style),
        Paragraph(bloque_trafo, sub_style),
        Paragraph("➔", titulo_style),
        Paragraph(bloque_tablero, sub_style)
    ]], colWidths=[140, 20, 220, 20, 152])

    tabla_unifilar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#FEF3C7")),
        ('BACKGROUND', (4,0), (4,0), colors.HexColor("#E2E8F0")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (0,0), 1, colors.HexColor("#94A3B8")),
        ('GRID', (2,0), (2,0), 1, colors.HexColor("#D97706")),
        ('GRID', (4,0), (4,0), 1, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tabla_unifilar)
    story.append(Spacer(1, 10))

    # 4. Circuitos Derivados
    story.append(Paragraph("<b>CIRCUITOS DERIVADOS (LADO MÁQUINA)</b>", sec_style))
    story.append(Spacer(1, 4))

    tabla_derivados_data = [["Equipo / Componente", "Pot (kW)", "I. Dis (A)", "Cable AWG", "Breaker"]]
    for c in resumen["circuitos_derivados"]:
        tabla_derivados_data.append([c["nombre"], f"{c['potencia_kw']} kW", f"{c['i_diseno_a']} A", c["cable"], c["breaker"]])

    t_der = Table(tabla_derivados_data, colWidths=[180, 80, 90, 90, 112])
    t_der.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_der)
    story.append(Spacer(1, 10))

    # 5. Tabla de Parámetros de Corte Calibrados
    if parametros_corte:
        story.append(Paragraph("<b>TABLA DE PARÁMETROS DE CORTE CALIBRADOS</b>", sec_style))
        story.append(Spacer(1, 4))
        
        tabla_params_data = [["Material", "Espesor", "Potencia", "Velocidad", "Gas Aux.", "Presión", "Foco"]]
        for p in parametros_corte:
            tabla_params_data.append([p["material"], p["espesor"], p["potencia"], p["velocidad"], p["gas"], p["presion"], p["foco"]])

        t_param = Table(tabla_params_data, colWidths=[132, 60, 70, 80, 70, 70, 70])
        t_param.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_param)
        story.append(Spacer(1, 10))

    # 6. Registro Fotográfico de Nameplates
    if fotos_nameplates:
        story.append(Paragraph("<b>REGISTRO FOTOGRÁFICO DE PLACAS TÉCNICAS (NAMEPLATES)</b>", sec_style))
        story.append(Spacer(1, 4))

        imgs_row = []
        for file in fotos_nameplates:
            img_bytes = io.BytesIO(file.getvalue())
            reportlab_img = Image(img_bytes, width=160, height=120)
            imgs_row.append(reportlab_img)

        # Agrupar de 3 en 3 por fila
        filas_imgs = [imgs_row[i:i + 3] for i in range(0, len(imgs_row), 3)]
        t_fotos = Table(filas_imgs, colWidths=[184, 184, 184])
        t_fotos.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_fotos)
        story.append(Spacer(1, 10))

    # Pie de página
    pie = Paragraph("<b>Ing. Daniel Araujo</b> | Especialista en Automatización, Robótica y Fibra Láser<br/>Dandylab Soluciones | Medellín, Colombia", sub_style)
    story.append(pie)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
