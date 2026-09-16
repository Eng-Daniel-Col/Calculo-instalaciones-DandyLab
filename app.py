# app.py
import os
import streamlit as st
from modules.cuadro_cargas import generar_cuadro_de_cargas
from modules.informes import generar_pdf_informe

st.set_page_config(
    page_title="DandyLab Soluciones - Dimensionamiento Eléctrico",
    page_icon="⚡",
    layout="wide"
)

# CARGAR LOGO EN LA INTERFAZ WEB
ruta_logo = os.path.join("assets", "logo", "logo.png")

col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, width=150)
    else:
        st.warning("⚠️ Logo no encontrado")

with col_titulo:
    st.title("⚡ DandyLab Soluciones")
    st.caption("Dimensionamiento Eléctrico Industrial & Especializado bajo RETIE / NTC 2050")

st.divider()

# app.py
import streamlit as st
from modules.cuadro_cargas import generar_cuadro_de_cargas
from modules.informes import generar_pdf_informe

st.set_page_config(
    page_title="DandyLab Soluciones - Dimensionamiento Eléctrico",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ DandyLab Soluciones - Dimensionamiento Eléctrico Industrial")
st.caption("Cálculo de conductores, protecciones y cuadro de cargas bajo normativa RETIE / NTC 2050.")

# Inicializar lista de equipos en estado de sesión
if "equipos" not in st.session_state:
    st.session_state.equipos = [
        {"nombre": "Fuente Láser", "potencia_w": 6000.0, "voltaje": 220.0, "fases": 3, "fp": 0.90, "distancia_m": 10.0},
        {"nombre": "Chiller de Enfriamiento", "potencia_w": 3000.0, "voltaje": 220.0, "fases": 1, "fp": 0.85, "distancia_m": 25.0}
    ]

# ---------------------------------------------------------
# DATOS DEL CLIENTE Y TABLERO PRINCIPAL
# ---------------------------------------------------------
st.header("1. Datos del Cliente y Tablero Principal")

col_c1, col_c2 = st.columns(2)
with col_c1:
    nombre_cliente = st.text_input("Nombre del Cliente / Empresa", value="Cliente Industrial S.A.S.")
with col_c2:
    ubicacion_cliente = st.text_input("Ubicación de la Instalación", value="Medellín, Antioquia")

col_tab1, col_tab2, col_tab3, col_tab4 = st.columns(4)

with col_tab1:
    v_tablero = st.selectbox("Voltaje Red (V)", [220, 380, 440, 110], index=0)
with col_tab2:
    f_tablero = st.selectbox("Sistema Fases", [3, 1], index=0, format_func=lambda x: "Trifásico (3P)" if x == 3 else "Monofásico / Bifásico (1P/2P)")
with col_tab3:
    dist_acometida = st.number_input("Distancia a Acometida (m)", min_value=1.0, value=15.0, step=1.0)
with col_tab4:
    norma_seleccionada = st.selectbox("Norma Aplicable", ["COLOMBIA", "MEXICO", "EEUU"], index=0)

# ---------------------------------------------------------
# GESTIÓN DE CIRCUITOS DERIVADOS (EQUIPOS)
# ---------------------------------------------------------
st.header("2. Circuitos Derivados (Equipos a Conectar)")

st.subheader("Añadir Nuevo Equipo")
col_eq1, col_eq2, col_eq3, col_eq4, col_eq5, col_eq6 = st.columns([2, 1.5, 1.2, 1.2, 1.2, 1])

with col_eq1:
    nuevo_nombre = st.text_input("Nombre del Equipo", value="Extractor de Humos")
with col_eq2:
    nueva_potencia = st.number_input("Potencia (Watts)", min_value=100.0, value=1500.0, step=100.0)
with col_eq3:
    nuevo_voltaje = st.selectbox("Voltaje (V)", [220, 380, 440, 110], index=0, key="nuevo_v")
with col_eq4:
    nuevas_fases = st.selectbox("Fases", [3, 1], index=0, key="nuevo_f")
with col_eq5:
    nueva_distancia = st.number_input("Distancia (m)", min_value=1.0, value=15.0, step=1.0, key="nuevo_d")
with col_eq6:
    st.write("##")
    if st.button("➕ Agregar"):
        st.session_state.equipos.append({
            "nombre": nuevo_nombre,
            "potencia_w": nueva_potencia,
            "voltaje": nuevo_voltaje,
            "fases": nuevas_fases,
            "fp": 0.85,
            "distancia_m": nueva_distancia
        })
        st.success(f"Equipo '{nuevo_nombre}' añadido.")

# Tabla de equipos cargados
if st.session_state.equipos:
    st.subheader("Lista de Equipos Registrados")
    for idx, eq in enumerate(st.session_state.equipos):
        c1, c2, c3, c4, c5, c6 = st.columns([3, 2, 2, 2, 2, 1])
        c1.write(f"**{eq['nombre']}**")
        c2.write(f"⚡ {eq['potencia_w']} W")
        c3.write(f"🔌 {eq['voltaje']} V")
        c4.write(f"🌀 {'Trifásico' if eq['fases'] == 3 else 'Monofásico'}")
        c5.write(f"📏 {eq['distancia_m']} m")
        if c6.button("🗑️", key=f"del_{idx}"):
            st.session_state.equipos.pop(idx)
            st.rerun()

st.divider()

# ---------------------------------------------------------
# PROCESAMIENTO Y CUADRO DE CARGAS
# ---------------------------------------------------------
if st.button("🚀 Calcular Dimensionamiento y Cuadro de Cargas", type="primary", use_container_width=True):
    if not st.session_state.equipos:
        st.error("Debes agregar al menos un equipo antes de realizar el cálculo.")
    else:
        datos_tablero = {
            "voltaje": v_tablero,
            "fases": f_tablero,
            "distancia_acometida_m": dist_acometida
        }

        resultado = generar_cuadro_de_cargas(
            datos_tablero=datos_tablero,
            lista_equipos=st.session_state.equipos,
            pais_norma=norma_seleccionada
        )

        st.subheader(f"📊 Resultados del Cuadro de Cargas ({resultado['norma_aplicada']})")

        # Visualización de Circuitos Derivados
        st.markdown("### Circuitos Derivados")
        st.dataframe(resultado["cuadro_cargas_circuitos"], use_container_width=True)

        # Visualización Alimentador y Tablero Principal
        st.markdown("### Tablero Principal / Alimentador")
        tab_info = resultado["tablero_principal"]
        bp_info = tab_info["breaker_principal"]

        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        col_r1.metric("Potencia Total", f"{tab_info['potencia_total_kw']} kW")
        col_r2.metric("Corriente de Diseño Total", f"{tab_info['corriente_diseno_a']} A")
        col_r3.metric("Alimentador Sugerido", f"{tab_info['alimentador_awg']}")
        col_r4.metric("Caída de Tensión", f"{tab_info['caida_acometida_pct']} %")

        st.info(
            f"**Interruptor Principal Recomendado:** {bp_info['amperios']} A | "
            f"**Polos:** {bp_info['polos']} P | "
            f"**Capacidad de Interrupción:** {bp_info['capacidad_interrupcion_ka']} kA | "
            f"**Curva:** {bp_info['curva']}"
        )

        # GENERACIÓN Y DESCARGA DEL PDF
        st.divider()
        pdf_path = "informe_dimensionamiento.pdf"
        generar_pdf_informe(
            nombre_archivo=pdf_path,
            datos_cliente={"nombre": nombre_cliente, "ubicacion": ubicacion_cliente},
            resultado_calculo=resultado
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Descargar Informe Técnico Oficial en PDF",
                data=f,
                file_name=f"Informe_Tecnico_{nombre_cliente.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
