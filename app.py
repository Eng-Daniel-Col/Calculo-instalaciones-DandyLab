import streamlit as st
import math
from datetime import date
from PIL import Image
import io
import tempfile
import os
from fpdf import FPDF

# Configuración de página
st.set_page_config(page_title="Gestión e Instalación de Maquinaria", layout="wide")

st.title("⚡ Sistema de Cálculo Eléctrico y Registro de Instalaciones")

# Inicializar la lista de componentes en la sesión si no existe
if "componentes" not in st.session_state:
    st.session_state.componentes = [
        {"equipo": "Chiller", "watts": 3000.0},
        {"equipo": "Extractor", "watts": 800.0}
    ]

# Pestañas principales
tab1, tab2, tab3 = st.tabs(["🧮 Calculadora Eléctrica", "📋 Datos del Cliente", "📸 Fotos y Parámetros"])

# --- TAB 1: CALCULADORA ELÉCTRICA DINÁMICA ---
with tab1:
    st.header("1. Ingreso de Componentes del Sistema")
    
    # Formulario para agregar un nuevo componente
    with st.form("form_componente", clear_on_submit=True):
        col_tipo, col_custom, col_watts, col_btn = st.columns([2, 2, 2, 1])
        
        with col_tipo:
            tipo_seleccionado = st.selectbox(
                "Tipo de Equipo", 
                ["Chiller", "Fuente de Poder", "Extractor", "Compresor", "Otro (Especificar)"]
            )
        
        with col_custom:
            nombre_custom = st.text_input("Nombre personalizado", placeholder="Ej: Bomba de agua")
            
        with col_watts:
            watts_input = st.number_input("Potencia (Watts)", min_value=1.0, value=500.0, step=50.0)
            
        with col_btn:
            st.write("") # Espaciador para alinear el botón
            st.write("")
            btn_agregar = st.form_submit_button("➕ Agregar")

        if btn_agregar:
            nombre_final = nombre_custom if tipo_seleccionado == "Otro (Especificar)" and nombre_custom else tipo_seleccionado
            st.session_state.componentes.append({"equipo": nombre_final, "watts": watts_input})
            st.rerun()

    # Mostrar lista de componentes agregados
    st.subheader("Lista de Cargas Conectadas")
    if st.session_state.componentes:
        for idx, comp in enumerate(st.session_state.componentes):
            c1, c2, c3 = st.columns([3, 3, 1])
            c1.write(f"**{comp['equipo']}**")
            c2.write(f"{comp['watts']:,.2f} W")
            if c3.button("🗑️ Borrar", key=f"del_{idx}"):
                st.session_state.componentes.pop(idx)
                st.rerun()
    else:
        st.info("No hay componentes agregados. Agrega al menos uno para realizar el cálculo.")

    st.divider()

    # Sumatoria total de Watts
    potencia_total_watts = sum(c["watts"] for c in st.session_state.componentes)

    st.header("2. Parámetros Eléctricos y Resultados")
    col_params, col_res = st.columns(2)

    with col_params:
        voltaje = st.selectbox("Voltaje de alimentación (V)", [110, 220, 380, 440], index=1)
        fases = st.selectbox("Tipo de sistema", ["Monofásico / Bifásico", "Trifásico"])
        pf = st.slider("Factor de potencia (cos φ)", 0.7, 1.0, 0.85, 0.05)

    # Cálculos
    if fases == "Monofásico / Bifásico":
        corriente_nominal = potencia_total_watts / (voltaje * pf) if voltaje * pf > 0 else 0
    else:  # Trifásico
        corriente_nominal = potencia_total_watts / (math.sqrt(3) * voltaje * pf) if voltaje * pf > 0 else 0

    corriente_diseno = corriente_nominal * 1.25  # 125% según norma NEC

    # Selección de Breaker Comercial
    breakers_estandar = [10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 100, 125, 150, 200]
    breaker_sugerido = next((b for b in breakers_estandar if b >= corriente_diseno), "Revisar caso (+200A)")

    # Selección de Calibre de Cable
    def obtener_calibre(amp):
        if amp <= 15: return "14 AWG"
        elif amp <= 20: return "12 AWG"
        elif amp <= 30: return "10 AWG"
        elif amp <= 40: return "8 AWG"
        elif amp <= 55: return "6 AWG"
        elif amp <= 70: return "4 AWG"
        elif amp <= 85: return "3 AWG"
        elif amp <= 95: return "2 AWG"
        elif amp <= 115: return "1 AWG"
        elif amp <= 130: return "1/0 AWG"
        elif amp <= 150: return "2/0 AWG"
        else: return "Consultar calibres mayores"

    calibre_sugerido = obtener_calibre(corriente_diseno)

    with col_res:
        st.metric("Carga Total Instalada", f"{potencia_total_watts:,.2f} W")
        st.metric("Corriente Nominal Total", f"{corriente_nominal:.2f} A")
        st.metric("Corriente de Diseño (+25%)", f"{corriente_diseno:.2f} A")
        st.success(f"**Breaker Recomendado:** {breaker_sugerido} A")
        st.info(f"**Calibre de Cable Mínimo (Cobre):** {calibre_sugerido}")

# --- TAB 2: DATOS DEL CLIENTE ---
with tab2:
    st.header("Información del Cliente e Instalación")
    
    nombre_cliente = st.text_input("Nombre / Empresa del Cliente", value="Empresa Ejemplo S.A.S.")
    direccion = st.text_input("Dirección de la Instalación", value="Calle Principal # 45 - 67")
    telefono = st.text_input("Teléfono de Contacto", value="+57 300 000 0000")
    codigo_maquina = st.text_input("Modelo / ID de la Máquina", value="MAQ-2026-X")
    fecha_instalacion = st.date_input("Fecha de Instalación", value=date.today())

# --- TAB 3: REGISTRO FOTOGRÁFICO Y PARÁMETROS ---
with tab3:
    st.header("Registro Fotográfico")
    
    st.subheader("1. Placas de Características (Nameplates)")
    fotos_nameplates = st.file_uploader("Cargar fotos de Nameplates", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="np")
    
    if fotos_nameplates:
        cols = st.columns(3)
        for idx, file in enumerate(fotos_nameplates):
            img = Image.open(file)
            cols[idx % 3].image(img, caption=f"Nameplate {idx+1}", use_container_width=True)

    st.divider()

    st.subheader("2. Parámetros Creados / Configuración Final")
    fotos_parametros = st.file_uploader("Cargar fotos de parámetros de la máquina", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="pm")
    
    if fotos_parametros:
        cols_p = st.columns(3)
        for idx, file in enumerate(fotos_parametros):
            img = Image.open(file)
            cols_p[idx % 3].image(img, caption=f"Parámetro {idx+1}", use_container_width=True)

    notas_parametros = st.text_area("Notas adicionales de la configuración", value="Parámetros configurados y probados bajo carga.")

# --- CLASE PARA GENERACIÓN DE PDF CON FPDF ---
class PDFReporte(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 24, 'F')
        self.set_font('Arial', 'B', 13)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 5)
        self.cell(0, 8, 'INFORME TECNICO DE PUESTA EN MARCHA', 0, 1, 'L')
        self.set_font('Arial', '', 8)
        self.set_text_color(56, 189, 248)
        self.set_x(10)
        self.cell(0, 4, 'REGISTRO DE INSTALACION Y CALCULO ELECTRICO', 0, 1, 'L')
        self.ln(10)

    def section_title(self, title):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(2, 132, 199)
        self.cell(0, 6, title, 0, 1, 'L')
        self.set_draw_color(2, 132, 199)
        self.set_line_width(0.4)
        self.line(self.get_x(), self.get_y(), 200, self.get_y())
        self.ln(3)

def limpiar_texto(texto):
    return str(texto).encode('latin-1', 'replace').decode('latin-1')

def generar_pdf_fpdf():
    pdf = PDFReporte()
    pdf.add_page()
    
    # 1. CLIENTE
    pdf.section_title("1. INFORMACION DEL CLIENTE Y EQUIPO")
    
    def draw_row(l1, v1, l2, v2):
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(241, 245, 249)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(40, 6, limpiar_texto(l1), 1, 0, 'L', True)
        pdf.set_font('Arial', '', 8)
        pdf.cell(55, 6, limpiar_texto(v1), 1, 0, 'L')
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(40, 6, limpiar_texto(l2), 1, 0, 'L', True)
        pdf.set_font('Arial', '', 8)
        pdf.cell(55, 6, limpiar_texto(v2), 1, 1, 'L')

    draw_row("Cliente / Empresa", nombre_cliente, "Fecha Instalacion", fecha_instalacion)
    draw_row("Direccion", direccion, "Telefono", telefono)
    
    pdf.set_font('Arial', 'B', 8)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(40, 6, "ID / Modelo Maquina", 1, 0, 'L', True)
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(150, 6, limpiar_texto(codigo_maquina), 1, 1, 'L')
    pdf.ln(4)

    # 2. DESGLOSE DE COMPONENTES Y CÁLCULO ELÉCTRICO
    pdf.section_title("2. COMPONENTES Y DESGLOSE DE CARGA")
    
    # Tabla de componentes
    pdf.set_font('Arial', 'B', 8)
    pdf.set_fill_color(226, 232, 240)
    pdf.cell(130, 6, "Componente / Equipamiento", 1, 0, 'L', True)
    pdf.cell(60, 6, "Potencia (Watts)", 1, 1, 'R', True)
    
    pdf.set_font('Arial', '', 8)
    for c in st.session_state.componentes:
        pdf.cell(130, 5, limpiar_texto(c["equipo"]), 1, 0, 'L')
        pdf.cell(60, 5, f"{c['watts']:,.2f} W", 1, 1, 'R')
        
    pdf.set_font('Arial', 'B', 8)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(130, 6, "CARGA TOTAL SUMADA", 1, 0, 'L', True)
    pdf.cell(60, 6, f"{potencia_total_watts:,.2f} W", 1, 1, 'R', True)
    pdf.ln(4)

    # Especificaciones eléctricas
    pdf.section_title("3. CALCULOS Y ESPECIFICACIONES ELECTRICAS")
    draw_row("Potencia Total", f"{potencia_total_watts:,.2f} W", "Voltaje Entrada", f"{voltaje} V")
    draw_row("Tipo Sistema", fases, "Factor Potencia (cos phi)", str(pf))
    draw_row("Corriente Nominal", f"{corriente_nominal:.2f} A", "Corriente Diseno (+25%)", f"{corriente_diseno:.2f} A")
    
    pdf.set_font('Arial', 'B', 8)
    pdf.set_fill_color(224, 242, 254)
    pdf.cell(40, 6, "Breaker Sugerido", 1, 0, 'L', True)
    pdf.cell(55, 6, limpiar_texto(f"{breaker_sugerido} A"), 1, 0, 'L')
    pdf.cell(40, 6, "Calibre Cable Minimo", 1, 0, 'L', True)
    pdf.cell(55, 6, limpiar_texto(f"{calibre_sugerido} (Cu)"), 1, 1, 'L')
    pdf.ln(4)

    # Galería de imágenes
    def agregar_galeria(titulo, archivos_fotos):
        pdf.section_title(titulo)
        if not archivos_fotos:
            pdf.set_font('Arial', 'I', 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(0, 5, "No se adjuntaron fotografias en esta seccion.", 0, 1, 'L')
            pdf.ln(3)
            return

        x_start = 10
        y_pos = pdf.get_y()
        box_width = 58
        box_height = 45
        
        for idx, file in enumerate(archivos_fotos):
            col = idx % 3
            if idx > 0 and col == 0:
                y_pos += box_height + 5
                if y_pos > 240:
                    pdf.add_page()
                    y_pos = pdf.get_y()
            
            x_pos = x_start + col * (box_width + 5)
            
            file.seek(0)
            img = Image.open(file)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                img.convert('RGB').save(tmp_file.name, 'JPEG')
                tmp_path = tmp_file.name

            try:
                pdf.image(tmp_path, x=x_pos, y=y_pos, w=box_width, h=box_height - 5)
            except Exception:
                pass
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        pdf.set_y(y_pos + box_height + 5)

    # 4. FOTOS NAMEPLATES
    agregar_galeria("4. REGISTRO FOTOGRAFICO DE NAMEPLATES", fotos_nameplates)

    # 5. FOTOS PARÁMETROS
    agregar_galeria("5. PARAMETROS CONFIGURADOS Y EVIDENCIA", fotos_parametros)

    # 6. NOTAS
    pdf.section_title("6. NOTAS ADICIONALES")
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 5, limpiar_texto(notas_parametros if notas_parametros else "Sin observaciones adicionales."), 1, 'L')

    return bytes(pdf.output())

# --- BOTÓN DE DESCARGA DE PDF ---
st.divider()

try:
    pdf_bytes = generar_pdf_fpdf()
    st.download_button(
        label="📄 Descargar Informe Técnico Completo en PDF",
        data=pdf_bytes,
        file_name=f"Informe_{codigo_maquina.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
except Exception as e:
    st.error(f"Error generando el PDF: {e}")