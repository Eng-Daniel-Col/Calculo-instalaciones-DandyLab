# modules/informes.py
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generar_pdf_informe(datos_cliente, resumen_carga, potencia_recomendada_kva, margen_seguridad, resumen_protecciones):
    """
    Genera el archivo PDF del informe técnico con la tabla de carga en kW y kVA.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Estilos personalizados
    estilo_titulo = ParagraphStyle(
        'TituloDandyLab',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A365D"),
        alignment=0
    )
    
    estilo_subtitulo = ParagraphStyle(
        'SubtituloDandyLab',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#475569")
    )

    # 1. Encabezado
    story.append(Paragraph("DANDYLAB SOLUCIONES", estilo_titulo))
    story.append(Paragraph("Servicios de Ingeniería, Instalación y Mantenimiento Industrial", estilo_subtitulo))
    story.append(Spacer(1, 15))

    # 2. Datos Generales del Cliente
    datos_cliente_tabla = [
        ["Cliente / Empresa:", datos_cliente.get("nombre", "N/A"), "Fecha:", "2026"],
        ["Ubicación:", datos_cliente.get("ciudad", "N/A"), "Modelo Máquina:", datos_cliente.get("modelo", "N/A")],
        ["Fuente Láser:", datos_cliente.get("fuente", "N/A"), "Voltaje Red:", resumen_carga.get("voltaje_fases", "N/A")]
    ]
    
    tabla_cliente = Table(datos_cliente_tabla, colWidths=[110, 180, 90, 160])
    tabla_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(tabla_cliente)
    story.append(Spacer(1, 15))

    # 3. Tabla de Requerimientos Energéticos (kW y kVA)
    story.append(Paragraph("<b>1. Requerimiento Energético para Instalación (Entradas en kW)</b>", styles['Heading2']))
    story.append(Spacer(1, 6))

    datos_tabla_cargas = [
        ["Parámetro / Concepto", "Valor Requerido"],
        ["Potencia Fuente Láser (kW)", f"{resumen_carga['potencia_laser_kw']} kW"],
        ["Potencia Equipos Auxiliares (kW)", f"{resumen_carga['consumo_auxiliares_kw']} kW"],
        ["Potencia Activa Total Requerida (kW)", f"{resumen_carga['potencia_activa_kw']} kW"],
        ["Potencia Aparente Nominal (kVA)", f"{resumen_carga['potencia_aparente_kva']} kVA"],
        [f"Capacidad Recomendada en Red / Transf. (+{margen_seguridad}%)", f"{potencia_recomendada_kva} kVA"],
        ["Tensión de Alimentación", f"{resumen_carga['voltaje_fases']}"],
        ["Corriente Nominal Estimada por Fase", f"{resumen_carga['corriente_estimada_a']} A"]
    ]

    tabla_cargas = Table(datos_tabla_cargas, colWidths=[280, 260])
    tabla_cargas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,3), (1,3), colors.HexColor("#F1F5F9")), # Destacar Total kW
        ('BACKGROUND', (0,5), (1,5), colors.HexColor("#FEF3C7")), # Destacar kVA Recomendados
    ]))
    story.append(tabla_cargas)
    story.append(Spacer(1, 15))

    # 4. Tabla de Especificación de Acometida y Protecciones
    story.append(Paragraph("<b>2. Especificación de Protecciones y Conductores</b>", styles['Heading2']))
    story.append(Spacer(1, 6))

    datos_tabla_protecciones = [
        ["Elemento de Protección / Conductor", "Especificación Sugerida"],
        ["Corriente de Diseño (125% RETIE)", f"{resumen_protecciones['corriente_diseno_a']} A"],
        ["Interruptor Termomagnético Principal (Breaker)", f"{resumen_protecciones['breaker_sugerido_a']} A"],
        ["Calibre Recomendado de Conductor (Cu 75°C)", f"{resumen_protecciones['calibre_sugerido']}"]
    ]

    tabla_protecciones = Table(datos_tabla_protecciones, colWidths=[280, 260])
    tabla_protecciones.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(tabla_protecciones)
    story.append(Spacer(1, 15))

    # 5. Observaciones
    story.append(Paragraph("<b>3. Observaciones Técnicas</b>", styles['Heading2']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(datos_cliente.get("observaciones", "Sin observaciones."), styles['Normal']))

    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
