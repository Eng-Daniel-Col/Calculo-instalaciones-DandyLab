# modules/informes.py
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_pdf_informe(
    nombre_archivo: str,
    datos_cliente: dict,
    resultado_calculo: dict
) -> str:
    doc = SimpleDocTemplate(
        nombre_archivo,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    titulo_style = ParagraphStyle(
        'TituloDandy',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0f172a"),
        bold=True
    )
    
    story = []

    # RUTA RÍGIDA DEL LOGO
    ruta_logo = os.path.abspath(os.path.join("assets", "logo", "logo.png"))
    
    if os.path.exists(ruta_logo):
        img_logo = Image(ruta_logo, width=110, height=45)
        encabezado_data = [
            [img_logo, Paragraph("<b>DANDYLAB SOLUCIONES</b><br/><font size=8 color='#475569'>Servicios de Ingeniería | Instalaciones Industriales & Láser</font>", titulo_style)]
        ]
        t_header = Table(encabezado_data, colWidths=[120, 420])
        t_header.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_header)
    else:
        story.append(Paragraph("<b>DANDYLAB SOLUCIONES</b>", titulo_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563eb"), spaceAfter=15))

  
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_pdf_informe(
    nombre_archivo: str,
    datos_cliente: dict,
    resultado_calculo: dict
) -> str:
    doc = SimpleDocTemplate(
        nombre_archivo,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    titulo_style = ParagraphStyle(
        'TituloDandy',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0f172a"),
        bold=True
    )
    
    story = []

    # RUTA RÍGIDA DEL LOGO
    ruta_logo = os.path.abspath(os.path.join("assets", "logo", "logo.png"))
    
    if os.path.exists(ruta_logo):
        img_logo = Image(ruta_logo, width=110, height=45)
        encabezado_data = [
            [img_logo, Paragraph("<b>DANDYLAB SOLUCIONES</b><br/><font size=8 color='#475569'>Servicios de Ingeniería | Instalaciones Industriales & Láser</font>", titulo_style)]
        ]
        t_header = Table(encabezado_data, colWidths=[120, 420])
        t_header.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_header)
    else:
        story.append(Paragraph("<b>DANDYLAB SOLUCIONES</b>", titulo_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563eb"), spaceAfter=15))


import os
from reportlab.platypus import Image

# ... resto de importaciones ...

def generar_pdf_informe(nombre_archivo: str, datos_cliente: dict, resultado_calculo: dict) -> str:
    # ... configuración de doc y styles ...
    story = []

    # Ruta del logo
    ruta_logo = os.path.join("assets", "logo", "logo.png")
    
    # Encabezado con Logo y Texto
    if os.path.exists(ruta_logo):
        img_logo = Image(ruta_logo, width=120, height=50) # Ajusta ancho y alto según tu imagen
        encabezado_data = [
            [img_logo, Paragraph("<b>DANDYLAB SOLUCIONES</b><br/><font size=8 color='#475569'>Servicios de Ingeniería | Instalaciones Industriales & Láser</font>", titulo_style)]
        ]
        t_header = Table(encabezado_data, colWidths=[130, 410])
        t_header.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(t_header)
    else:
        story.append(Paragraph("<b>DANDYLAB SOLUCIONES</b>", titulo_style))
        story.append(Paragraph("Servicios de Ingeniería | Instalaciones Industriales & Láser", subtitulo_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563eb"), spaceAfter=15))
    
    # ... resto del código del PDF ...

# modules/informes.py
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generar_pdf_informe(
    nombre_archivo: str,
    datos_cliente: dict,
    resultado_calculo: dict
) -> str:
    """
    Genera un informe técnico profesional en PDF para la instalación eléctrica.
    """
    doc = SimpleDocTemplate(
        nombre_archivo,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_style = ParagraphStyle(
        'TituloDandy',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        bold=True
    )
    
    subtitulo_style = ParagraphStyle(
        'SubTituloDandy',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#475569")
    )
    
    header_seccion = ParagraphStyle(
        'HeaderSeccion',
        parent=styles['Heading2'],
        fontSize=12,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=5,
        bold=True
    )
    
    texto_normal = ParagraphStyle(
        'TextoNormal',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#334155")
    )

    story = []

    # 1. ENCABEZADO Y MEMBRETE
    story.append(Paragraph("<b>DANDYLAB SOLUCIONES</b>", titulo_style))
    story.append(Paragraph("Servicios de Ingeniería | Instalaciones Industriales & Láser", subtitulo_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563eb"), spaceAfter=15))

    # 2. DATOS DEL CLIENTE Y PROYECTO
    story.append(Paragraph("DATOS DEL PROYECTO", header_seccion))
    info_cliente = [
        [
            Paragraph(f"<b>Cliente:</b> {datos_cliente.get('nombre', 'N/A')}", texto_normal),
            Paragraph(f"<b>Ubicación:</b> {datos_cliente.get('ubicacion', 'N/A')}", texto_normal)
        ],
        [
            Paragraph(f"<b>Norma Evaluada:</b> {resultado_calculo['norma_aplicada']}", texto_normal),
            Paragraph(f"<b>Fecha:</b> {datos_cliente.get('fecha', '15/09/2026')}", texto_normal)
        ]
    ]
    t_cliente = Table(info_cliente, colWidths=[270, 270])
    t_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0"))
    ]))
    story.append(t_cliente)
    story.append(Spacer(1, 15))

    # 3. CUADRO DE CARGAS - CIRCUITOS DERIVADOS
    story.append(Paragraph("CUADRO DE CARGAS - CIRCUITOS DERIVADOS", header_seccion))
    
    tabla_datos = [["Equipo", "Pot (kW)", "I. Dis (A)", "Cable AWG", "ΔV (%)", "Protección Breaker"]]
    for c in resultado_calculo["cuadro_cargas_circuitos"]:
        tabla_datos.append([
            c["equipo"],
            f"{c['potencia_kw']} kW",
            f"{c['corriente_diseno_a']} A",
            c["cable_awg"],
            f"{c['caida_pct']}%",
            c["breaker"]
        ])

    t_cuadro = Table(tabla_datos, colWidths=[110, 55, 65, 75, 55, 180])
    t_cuadro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f1f5f9")]),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_cuadro)
    story.append(Spacer(1, 15))

    # 4. TABLERO PRINCIPAL / ALIMENTADOR
    story.append(Paragraph("ESPECIFICACIONES DEL TABLERO PRINCIPAL", header_seccion))
    tab = resultado_calculo["tablero_principal"]
    bp = tab["breaker_principal"]

    info_principal = [
        ["Potencia Total Requerida:", f"{tab['potencia_total_kw']} kW"],
        ["Corriente de Diseño Alimentador:", f"{tab['corriente_diseno_a']} A"],
        ["Conductor Alimentador Recomendado:", f"{tab['alimentador_awg']} (Caída ΔV: {tab['caida_acometida_pct']}%)"],
        ["Interruptor Principal (Breaker):", f"{bp['amperios']}A | {bp['polos']} Polos | {bp['capacidad_interrupcion_ka']} kA | Curva {bp['curva']}"]
    ]
    t_principal = Table(info_principal, colWidths=[200, 340])
    t_principal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f1f5f9")),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_principal)
    story.append(Spacer(1, 25))

    # 5. FIRMA Y RESPONSABLE TÉCNICO
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#94a3b8"), spaceAfter=15))
    story.append(Paragraph("<b>Ing. Daniel Araujo</b> — Ingeniero Mecatrónico | Especialista en Automatización , Robotica y Fibra Láser", texto_normal))
    story.append(Paragraph("Dandylab Soluciones | Medellín, Colombia", subtitulo_style))

    doc.build(story)
    return nombre_archivo
