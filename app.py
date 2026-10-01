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

# app.py
import streamlit as st
from modules.cuadro_cargas import calcular_carga_red_cliente, calcular_calibre_y_breaker
from modules.informes import generar_pdf_informe

st.set_page_config(
    page_title="DandyLab Soluciones - Reportes de Instalación",
    page_icon="⚡",
    layout="wide"
)

# --- SISTEMA DE AUTENTICACIÓN / LOGIN ---
USUARIOS_AUTORIZADOS = {
    "daniel": "dandylab2026*",
    "tecnico1": "laser2026",
    "tecnico2": "retie2026"
}

def verificar_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("⚡ DandyLab Soluciones")
        st.subheader("🔒 Acceso Restringido - Instalaciones y Servicios")
        
        col_login, _ = st.columns([1, 1])
        with col_login:
            usuario = st.text_input("Usuario")
            clave = st.text_input("Contraseña", type="password")
            
            if st.button("Iniciar Sesión", type="primary", use_container_width=True):
                if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario] == clave:
                    st.session_state.autenticado = True
                    st.success("Acceso concedido")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")
        return False
    return True

if not verificar_login():
    st.stop()

# --- INTERFAZ PRINCIPAL DE LA APLICACIÓN ---
st.title("⚡ DandyLab Soluciones - Gestión de Instalación Laser")

# Formulario de datos generales del cliente
st.sidebar.header("📋 Datos de la Instalación")
nombre_cliente = st.sidebar.text_input("Cliente / Empresa", value="Empresa Cliente S.A.S.")
ciudad = st.sidebar.text_input("Ciudad / Ubicación", value="Medellín")
modelo_maquina = st.sidebar.text_input("Modelo de Cortadora Láser", value="Laser Cut 3015")
marca_fuente = st.sidebar.text_input("Marca / Serie de Fuente", value="Raycus 6kW")

# Pestañas principales
tab_cargas, tab_informe = st.tabs(["⚡ Carga Eléctrica (kW)", "📄 Generar Informe PDF"])

with tab_cargas:
    st.header("⚡ Requerimiento Energético y Carga en Red (kW)")
    st.caption("Ingrese la potencia en kilovatios (kW) de la fuente láser y los equipos auxiliares.")

    col1, col2 = st.columns(2)

    with col1:
        potencia_laser_kw = st.number_input(
            "Potencia de Fuente Láser / Módulo Principal (kW)", 
            min_value=0.5, 
            value=6.0, 
            step=0.5,
            help="Ingrese la potencia de la fuente láser en kW"
        )
        
        consumo_aux_kw = st.number_input(
            "Consumo Equipos Auxiliares (kW)", 
            min_value=0.0, 
            value=8.0, 
            step=0.5,
            help="Suma de potencias en kW del Chiller, Extractor de humo, Compresor y servomotores"
        )

    with col2:
        voltaje_red = st.selectbox(
            "Voltaje de Red del Cliente", 
            ["220V (3Ph)", "380V (3Ph)", "440V (3Ph)", "220V (1Ph/2Ph)"]
        )
        
        margen_seguridad = st.slider(
            "Margen de Seguridad de Red (%)", 
            min_value=10, 
            max_value=40, 
            value=25, 
            step=5
        )

    # Cálculo de carga en red
    resumen_carga = calcular_carga_red_cliente(potencia_laser_kw, consumo_aux_kw, voltaje_red)
    potencia_recomendada_kva = round(resumen_carga["potencia_aparente_kva"] * (1 + margen_seguridad/100), 1)
    
    # Cálculo de protecciones y conductores
    resumen_protecciones = calcular_calibre_y_breaker(resumen_carga["corriente_estimada_a"])

    # Guardar resultados en el estado de sesión
    st.session_state.resumen_carga = resumen_carga
    st.session_state.potencia_recomendada_kva = potencia_recomendada_kva
    st.session_state.margen_seguridad = margen_seguridad
    st.session_state.resumen_protecciones = resumen_protecciones

    # Despliegue visual de resultados
    st.subheader("📊 Resumen de Cargas y Acometida Calculadas")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Potencia Total (kW)", f"{resumen_carga['potencia_activa_kw']} kW")
    m2.metric("Potencia Aparente (kVA)", f"{resumen_carga['potencia_aparente_kva']} kVA")
    m3.metric(f"Capacidad Red Rec. (+{margen_seguridad}%)", f"{potencia_recomendada_kva} kVA")
    m4.metric("Corriente Nominal Est.", f"{resumen_carga['corriente_estimada_a']} A")

    st.subheader("🛡️ Protecciones y Conductores Sugeridos")
    p1, p2, p3 = st.columns(3)
    p1.metric("Corriente de Diseño (125%)", f"{resumen_protecciones['corriente_diseno_a']} A")
    p2.metric("Breaker Principal Recomendado", f"{resumen_protecciones['breaker_sugerido_a']} A")
    p3.metric("Calibre de Cable Cu (75°C)", f"{resumen_protecciones['calibre_sugerido']}")

    st.success(
        f"💡 **Recomendación para el cliente ({nombre_cliente}):**\n\n"
        f"- **Carga activa total instalada:** {resumen_carga['potencia_activa_kw']} kW\n"
        f"- **Transformador / Acometida requerida:** Mínimo **{potencia_recomendada_kva} kVA** a **{voltaje_red}**\n"
        f"- **Protección general:** Breaker de **{resumen_protecciones['breaker_sugerido_a']} A** con conductor **{resumen_protecciones['calibre_sugerido']}**"
    )

with tab_informe:
    st.header("📄 Generación del Informe Técnico en PDF")
    
    observaciones = st.text_area(
        "Observaciones Técnicas de la Instalación",
        value="La acometida eléctrica fue verificada. Se recomienda asegurar la capacidad en kVA especificada y la conexión a tierra independiente antes del encendido inicial."
    )

    if st.button("🚀 Generar PDF de la Instalación", type="primary"):
        datos_cliente = {
            "nombre": nombre_cliente,
            "ciudad": ciudad,
            "modelo": modelo_maquina,
            "fuente": marca_fuente,
            "observaciones": observaciones
        }
        
        pdf_bytes = generar_pdf_informe(
            datos_cliente=datos_cliente,
            resumen_carga=st.session_state.resumen_carga,
            potencia_recomendada_kva=st.session_state.potencia_recomendada_kva,
            margen_seguridad=st.session_state.margen_seguridad,
            resumen_protecciones=st.session_state.resumen_protecciones
        )
        
        st.download_button(
            label="📥 Descargar Informe PDF",
            data=pdf_bytes,
            file_name=f"Informe_Instalacion_{nombre_cliente.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
