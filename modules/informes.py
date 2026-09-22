# modules/informes.py
import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line

def crear_diagrama_unifilar(resultado_calculo: dict) -> Drawing:
    """Genera un esquema unifilar gráfico vectorial para el PDF."""
    d = Drawing(500, 140)
    usar_trafo = resultado_calculo.get("usar_transformador", False)
    tab = resultado_calculo["tablero_principal"]
    trafo = resultado_calculo["transformador"]
    
    c_box = colors.HexColor("#1e293b")
    c_trafo = colors.HexColor("#2563eb")
    c_txt = colors.white

    texto_fases_primario = "Trifásica" if trafo['fases_primario'] == 3 else ("Bifásica" if trafo['fases_primario'] == 2 else "Monofásica")

    # Nodo 1: Red Cliente
    d.add(Rect(10, 40, 120, 65, rx=4, ry=4, fillColor=c_box, strokeColor=None))
    d.add(String(18, 88, "RED CLIENTE", fillColor=c_txt, fontSize=9, fontName="Helvetica-Bold"))
    d.add(String(18, 73, f"{trafo['v_primario']}V ({texto_fases_primario})", fillColor=c_txt, fontSize=8))
    d.add(String(18, 58, f"Breaker: {tab['breaker_principal']['amperios']}A / {trafo['fases_primario']}P", fillColor=colors.HexColor("#93c5fd"), fontSize=8))

    # Línea 1
    d.add(Line(130, 72, 175, 72, strokeColor=colors.HexColor("#64748b"), strokeWidth=2))

    if usar_trafo:
        # Nodo 2: Transformador
        d.add(Rect(175, 35, 140, 75, rx=4, ry=4, fillColor=c_trafo, strokeColor=None))
        d.add(String(185, 93, "TRANSFORMADOR", fillColor=c_txt, fontSize=9, fontName="Helvetica-Bold"))
        d.add(String(185, 78, f"Capacidad: {trafo['capacidad_sugerida_kva']} kVA", fillColor=c_txt, fontSize=8))
        d.add(String(185, 63, f"Entrada: {trafo['v_primario']}V ({trafo['fases_primario']}P)", fillColor=c_txt, fontSize=8))
        d.add(String(185, 48, f"Salida: {trafo['v_secundario']}V (3P)", fillColor=colors.HexColor("#bfdbfe"), fontSize=8))

        # Línea 2
        d.add(Line(315, 72, 360, 72, strokeColor=colors.HexColor("#64748b"), strokeWidth=2))
        x_final = 360
    else:
        x_final = 175

    # Nodo 3: Tablero Máquina
    d.add(Rect(x_final, 40, 130, 65, rx=4, ry=4, fillColor=c_box, strokeColor=None))
    d.add(String(x_final + 10, 88, "TABLERO MÁQUINA", fillColor=c_txt, fontSize=9, fontName="Helvetica-Bold"))
    d.add(String(x_final + 10, 73, f"Operación: {trafo['v_secundario']}V Trifásico", fillColor=c_txt, fontSize=8))
    d.add(String(x_final + 10, 58, f"Potencia Total: {tab['potencia_total_kw']} kW", fillColor=colors.HexColor("#86efac"), fontSize=8))

    return d

def generar_pdf_informe(
    nombre_archivo: str,
    datos_cliente: dict,
    resultado_calculo: dict,
    fotos_nameplates: list = None
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
    
    titulo_style = ParagraphStyle('TituloDandy', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor("#0f172a"), bold=True)
    subtitulo_style = ParagraphStyle('SubTituloDandy', parent=styles['Normal'], fontSize=10, leading=12, textColor=colors.HexColor("#475569"))
    header_seccion = ParagraphStyle('HeaderSeccion', parent=styles['Heading2'], fontSize=12, leading=14, textColor=colors.HexColor("#1e293b"), spaceBefore=10, spaceAfter=5, bold=True)
    texto_normal = ParagraphStyle('TextoNormal', parent=styles['Normal'], fontSize=9, leading=11, textColor=colors.HexColor("#334155"))

    story = []

    # 1. ENCABEZADO Y LOGO
    carpeta_logo = os.path.abspath(os.path.join("assets", "logo"))
    archivos_logo = glob.glob(os.path.join(carpeta_logo, "*.*"))
    
    if archivos_logo:
        img_logo = Image(archivos_logo[0], width=110, height=45)
        encabezado_data = [[img_logo, Paragraph("<b>DANDYLAB SOLUCIONES</b><br/><font size=8 color='#475569'>Servicios de Ingeniería | Instalaciones Industriales & Láser</font>", titulo_style)]]
        t_header = Table(encabezado_data, colWidths=[120, 420])
        t_header.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story.append(t_header)
    else:
        story.append(Paragraph("<b>DANDYLAB SOLUCIONES</b>", titulo_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563eb"), spaceAfter=10))

    # 2. DATOS PROYECTO
    story.append(Paragraph("INFORMACIÓN DEL CLIENTE E INSTALACIÓN", header_seccion))
    info_cliente = [
        [Paragraph(f"<b>Cliente / Empresa:</b> {datos_cliente.get('nombre', 'N/A')}", texto_normal), Paragraph(f"<b>Teléfono:</b> {datos_cliente.get('telefono', 'N/A')}", texto_normal)],
        [Paragraph(f"<b>Dirección:</b> {datos_cliente.get('direccion', 'N/A')}", texto_normal), Paragraph(f"<b>Modelo Máquina:</b> {datos_cliente.get('modelo_maquina', 'N/A')}", texto_normal)],
        [Paragraph(f"<b>Norma Evaluada:</b> {resultado_calculo.get('norma_aplicada', 'N/A')}", texto_normal), Paragraph(f"<b>Fecha Instalación:</b> {datos_cliente.get('fecha', 'N/A')}", texto_normal)]
    ]
    t_cliente = Table(info_cliente, colWidths=[270, 270])
    t_cliente.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
    story.append(t_cliente)
    story.append(Spacer(1, 10))

    # 3. ESQUEMA DE CONEXIÓN
    story.append(Paragraph("ARQUITECTURA Y ESQUEMA UNIFILAR DE CONEXIÓN", header_seccion))
    story.append(crear_diagrama_unifilar(resultado_calculo))
    story.append(Spacer(1, 10))

    # 4. TABLERO PRINCIPAL Y TRANSFORMACIÓN
    story.append(Paragraph("ACOMETIDA PRINCIPAL Y TRANSFORMACIÓN", header_seccion))
    tab = resultado_calculo["tablero_principal"]
    trafo = resultado_calculo["transformador"]
    bp = tab["breaker_principal"]

    texto_fases = "Trifásica (3P)" if trafo['fases_primario'] == 3 else ("Bifásica (2P)" if trafo['fases_primario'] == 2 else "Monofásica (1P)")

    info_principal = [
        ["Red del Cliente (Primario):", f"{trafo['v_primario']} V AC | Tipo: {texto_fases}"],
        ["Salida Máquina (Secundario):", f"{trafo['v_secundario']} V AC | Tipo: Trifásica (3P)"],
        ["Transformador Recomendado:", f"{trafo['capacidad_sugerida_kva']} kVA (Eficiencia {trafo['eficiencia']})" if resultado_calculo['usar_transformador'] else "No requiere transformador"],
        ["Corriente Diseñada (Primario):", f"{tab['corriente_diseno_a']} A"],
        ["Cable Alimentador Primario:", f"{tab['alimentador_awg']} (Caída ΔV: {tab['caida_acometida_pct']}%)"],
        ["Breaker Principal Acometida:", f"{bp['amperios']} A | {bp['polos']} Polos | {bp['capacidad_interrupcion_ka']} kA (Curva {bp['curva']})"]
    ]
    t_principal = Table(info_principal, colWidths=[200, 340])
    t_principal.setStyle(TableStyle([('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f1f5f9")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")), ('PADDING', (0,0), (-1,-1), 5)]))
    story.append(t_principal)
    story.append(Spacer(1, 10))

    # 5. CUADRO DE CARGAS - DERIVADOS
    story.append(Paragraph("CIRCUITOS DERIVADOS (LADO MÁQUINA / SECUNDARIO)", header_seccion))
    tabla_datos = [["Equipo", "Pot (kW)", "I. Dis (A)", "Cable AWG", "ΔV (%)", "Protección Breaker"]]
    for c in resultado_calculo["cuadro_cargas_circuitos"]:
        tabla_datos.append([c["equipo"], f"{c['potencia_kw']} kW", f"{c['corriente_diseno_a']} A", c["cable_awg"], f"{c['caida_pct']}%", c["breaker"]])

    t_cuadro = Table(tabla_datos, colWidths=[110, 55, 65, 75, 55, 180])
    t_cuadro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f1f5f9")]),
        ('PADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_cuadro)
    story.append(Spacer(1, 10))

    # 6. REGISTRO FOTOGRÁFICO
    if fotos_nameplates:
        story.append(Paragraph("REGISTRO FOTOGRÁFICO (NAMEPLATES / PLACAS)", header_seccion))
        tabla_fotos, fila_temp = [], []
        for foto_path in fotos_nameplates:
            if os.path.exists(foto_path):
                img = Image(foto_path, width=240, height=130)
                fila_temp.append(img)
                if len(fila_temp) == 2:
                    tabla_fotos.append(fila_temp)
                    fila_temp = []
        if fila_temp:
            if len(fila_temp) == 1:
                fila_temp.append(Paragraph("", texto_normal))
            tabla_fotos.append(fila_temp)
        
        if tabla_fotos:
            t_fotos = Table(tabla_fotos, colWidths=[270, 270])
            t_fotos.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1"))]))
            story.append(t_fotos)
            story.append(Spacer(1, 10))

    # 7. FIRMA
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#94a3b8"), spaceAfter=10))
    story.append(Paragraph("<b>Ing. Daniel Araujo</b> — Especialista en Automatización e Instalaciones Industriales", texto_normal))
    story.append(Paragraph("Dandylab Soluciones | Medellín, Colombia", subtitulo_style))

    doc.build(story)
    return nombre_archivo
