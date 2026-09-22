# app.py
import os
import glob
import uuid
from datetime import datetime
import streamlit as st
from modules.cuadro_cargas import generar_cuadro_de_cargas
from modules.informes import generar_pdf_informe

st.set_page_config(
    page_title="DandyLab Soluciones - Dimensionamiento Eléctrico",
    page_icon="⚡",
    layout="wide"
)

# app.py (Inicio del archivo)
import streamlit as st

# Configuración de contraseñas autorizadas para tu equipo
USUARIOS_AUTORIZADOS = {
    "Eng.daniel": "dandylab2026*",
    "Eng.sebastian": "laser2026",
    "Eng.dannier": "test2026"
}

def verificar_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.subheader("🔒 Acceso Restringido - DandyLab Soluciones")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar Sesión", type="primary"):
            if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario] == clave:
                st.session_state.autenticado = True
                st.success("Acceso concedido")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
        return False
    return True

# Si no está autenticado, detiene la ejecución del resto de la app
if not verificar_login():
    st.stop()

# --- AQUÍ CONTINÚA TODO EL CÓDIGO ACTUAL DE TU APP ---

# Previene errores de reconciliación DOM con traductores del navegador
st.markdown('<html lang="es"></html>', unsafe_allow_html=True)

# Encabezado y Logo
carpeta_logo = os.path.abspath(os.path.join("assets", "logo"))
archivos_encontrados = glob.glob(os.path.join(carpeta_logo, "*.*"))

col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if archivos_encontrados:
        st.image(archivos_encontrados[0], width=140)
    else:
        st.warning("⚠️ Sin logo en assets/logo/")

with col_titulo:
    st.title("⚡ DandyLab Soluciones")
    st.caption("Dimensionamiento Eléctrico Industrial & Especializado bajo RETIE / NTC 2050")

# Inicialización de estado con identificadores únicos
if "equipos" not in st.session_state:
    st.session_state.equipos = [
        {"id": str(uuid.uuid4()), "nombre": "Fuente Láser", "potencia_w": 6000.0, "voltaje": 380.0, "fases": 3, "fp": 0.90, "distancia_m": 10.0},
        {"id": str(uuid.uuid4()), "nombre": "Chiller de Enfriamiento", "potencia_w": 3000.0, "voltaje": 380.0, "fases": 3, "fp": 0.85, "distancia_m": 15.0}
    ]

tab_calc, tab_cliente, tab_fotos = st.tabs([
    "📊 Calculadora Eléctrica", 
    "📋 Datos del Cliente", 
    "📷 Fotos y Parámetros"
])

# ---------------------------------------------------------
# PESTAÑA 1: CALCULADORA ELÉCTRICA
# ---------------------------------------------------------
with tab_calc:
    st.header("1. Configuración de Acometida y Transformador")
    
    usar_trafo = st.checkbox("🔌 La instalación incluye Transformador (Ej. 220V → 380V)", value=True)
    
    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)
    with col_t1:
        v_primario = st.selectbox("Voltaje Red Cliente", [220, 440, 380, 110], index=0 if usar_trafo else 2)
    with col_t2:
        fases_primario = st.selectbox("Fases Red Cliente", [3, 2, 1], index=0, format_func=lambda x: f"{x}P / {'Trifásica' if x==3 else 'Bifásica' if x==2 else 'Monofásica'}")
    with col_t3:
        v_secundario = st.selectbox("Voltaje Máquina", [380, 220, 440], index=0)
    with col_t4:
        dist_acometida = st.number_input("Distancia Red -> Trafo (m)", min_value=1.0, value=15.0, step=1.0)
    with col_t5:
        norma_seleccionada = st.selectbox("Norma Aplicable", ["COLOMBIA", "MEXICO", "EEUU"], index=0)

    # Diagrama textual de flujo
    st.subheader("💡 Arquitectura de Conexión Seleccionada")
    str_fases = "Trifásica" if fases_primario == 3 else ("Bifásica" if fases_primario == 2 else "Monofásica")
    if usar_trafo:
        st.info(f"**RED CLIENTE ({v_primario}V {str_fases})** ──[Breaker {fases_primario}P]──> **TRANSFORMADOR** ──({v_secundario}V 3P)──> **TABLERO MÁQUINA** ──> **DERIVADOS**")
    else:
        st.info(f"**RED CLIENTE ({v_primario}V {str_fases})** ──[Breaker {fases_primario}P]──> **TABLERO MÁQUINA** ──> **DERIVADOS ({v_primario}V)**")

    st.header("2. Circuitos Derivados (Equipos de la Máquina)")
    col_eq1, col_eq2, col_eq3, col_eq4, col_eq5 = st.columns([2, 1.5, 1.2, 1.2, 1])

    with col_eq1:
        nuevo_nombre = st.text_input("Nombre del Equipo", value="Extractor de Humos")
    with col_eq2:
        nueva_potencia = st.number_input("Potencia (Watts)", min_value=100.0, value=1500.0, step=100.0)
    with col_eq3:
        nuevas_fases = st.selectbox("Fases", [3, 1], index=0, key="nuevo_f")
    with col_eq4:
        nueva_distancia = st.number_input("Distancia (m)", min_value=1.0, value=15.0, step=1.0, key="nuevo_d")
    with col_eq5:
        st.write("##")
        if st.button("➕ Agregar"):
            st.session_state.equipos.append({
                "id": str(uuid.uuid4()),
                "nombre": nuevo_nombre,
                "potencia_w": nueva_potencia,
                "voltaje": v_secundario,
                "fases": nuevas_fases,
                "fp": 0.85,
                "distancia_m": nueva_distancia
            })
            st.success(f"Equipo '{nuevo_nombre}' añadido.")

    if st.session_state.equipos:
        st.subheader("Lista de Equipos Registrados")
        for eq in list(st.session_state.equipos):
            c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 1])
            c1.write(f"**{eq['nombre']}**")
            c2.write(f"⚡ {eq['potencia_w']} W")
            c3.write(f"🌀 {'Trifásico' if eq['fases'] == 3 else 'Monofásico'}")
            c4.write(f"📏 {eq['distancia_m']} m")
            if c5.button("🗑️", key=f"del_{eq['id']}"):
                st.session_state.equipos = [e for e in st.session_state.equipos if e["id"] != eq["id"]]
                st.rerun()

# ---------------------------------------------------------
# PESTAÑA 2: DATOS DEL CLIENTE
# ---------------------------------------------------------
with tab_cliente:
    st.header("Información del cliente e instalación")
    cliente_nombre = st.text_input("Nombre / Empresa del Cliente", value="Empresa Ejemplo S.A.S.")
    cliente_direccion = st.text_input("Dirección de la Instalación", value="Calle Principal # 45 - 67")
    cliente_telefono = st.text_input("Teléfono de Contacto", value="+57 300 000 0000")
    cliente_modelo = st.text_input("Modelo / ID de la Máquina", value="MAQ-2026-X")
    cliente_fecha = st.date_input("Fecha de Instalación", value=datetime.now())

# ---------------------------------------------------------
# PESTAÑA 3: FOTOS
# ---------------------------------------------------------
with tab_fotos:
    st.header("Fotos y Registro de Nameplates (Placas de Características)")
    archivos_subidos = st.file_uploader("Subir imágenes de Nameplates (JPG, PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    rutas_fotos_guardadas = []
    if archivos_subidos:
        cols_foto = st.columns(3)
        os.makedirs("temp_uploads", exist_ok=True)
        for idx, file in enumerate(archivos_subidos):
            temp_path = os.path.join("temp_uploads", f"nameplate_{idx}_{file.name}")
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())
            rutas_fotos_guardadas.append(temp_path)
            with cols_foto[idx % 3]:
                st.image(file, caption=file.name, use_column_width=True)

# ---------------------------------------------------------
# CÁLCULO GENERAL Y GENERACIÓN
# ---------------------------------------------------------
st.divider()

if st.button("🚀 Calcular Dimensionamiento y Generar Informe PDF", type="primary", use_container_width=True):
    if not st.session_state.equipos:
        st.error("Debes agregar al menos un equipo en la pestaña 'Calculadora Eléctrica'.")
    else:
        datos_tablero = {
            "usar_transformador": usar_trafo,
            "voltaje_primario": v_primario,
            "fases_primario": fases_primario,
            "voltaje_secundario": v_secundario,
            "fases_secundario": 3,
            "distancia_acometida_m": dist_acometida,
            "eficiencia_trafo": 0.95
        }

        resultado = generar_cuadro_de_cargas(
            datos_tablero=datos_tablero,
            lista_equipos=st.session_state.equipos,
            pais_norma=norma_seleccionada
        )

        st.subheader("📊 Resultados del Dimensionamiento")

        if usar_trafo:
            st.success(f"⚡ **Transformador Sugerido:** {resultado['transformador']['capacidad_sugerida_kva']} kVA ({v_primario}V {fases_primario}P ➔ {v_secundario}V 3P)")

        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        tab_info = resultado["tablero_principal"]
        col_r1.metric("Potencia Entrada", f"{tab_info['potencia_primario_kw']} kW")
        col_r2.metric("Corriente Entrada (Primario)", f"{tab_info['corriente_diseno_a']} A")
        col_r3.metric("Alimentador Principal", f"{tab_info['alimentador_awg']}")
        col_r4.metric("Breaker Acometida", f"{tab_info['breaker_principal']['amperios']} A ({fases_primario}P)")

        st.markdown("### Circuitos Derivados (Lado Máquina)")
        st.dataframe(resultado["cuadro_cargas_circuitos"], use_container_width=True)

        # Generación del PDF
        pdf_path = "informe_dimensionamiento.pdf"
        datos_cliente_dict = {
            "nombre": cliente_nombre,
            "direccion": cliente_direccion,
            "telefono": cliente_telefono,
            "modelo_maquina": cliente_modelo,
            "fecha": cliente_fecha.strftime("%d/%m/%Y")
        }

        generar_pdf_informe(
            nombre_archivo=pdf_path,
            datos_cliente=datos_cliente_dict,
            resultado_calculo=resultado,
            fotos_nameplates=rutas_fotos_guardadas
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Descargar Informe Técnico Oficial en PDF",
                data=f,
                file_name=f"Informe_Tecnico_{cliente_nombre.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
