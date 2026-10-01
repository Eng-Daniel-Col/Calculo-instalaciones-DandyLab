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
import os
from PIL import Image
from modules.cuadro_cargas import calcular_cuadro_completo
from modules.informes import generar_pdf_informe

st.set_page_config(
    page_title="DandyLab Soluciones - Reportes Técnicos",
    page_icon="⚡",
    layout="wide"
)

# --- LOGIN ---
USUARIOS = {"daniel": "dandylab2026*", "tecnico1": "laser2026"}

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("⚡ DandyLab Soluciones")
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("Iniciar Sesión", type="primary"):
        if u in USUARIOS and USUARIOS[u] == p:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
    st.stop()

# --- DATOS GENERALES Y LOGO EN SIDEBAR ---
st.sidebar.header("🖼️ Logo de la Empresa")
logo_file = st.sidebar.file_uploader("Subir Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
logo_path = "assets/logo/logo_temp.png"
os.makedirs("assets/logo", exist_ok=True)

if logo_file:
    with open(logo_path, "wb") as f:
        f.write(logo_file.getbuffer())
    st.sidebar.image(logo_path, width=140)
elif not os.path.exists(logo_path):
    logo_path = None

st.sidebar.header("📋 Datos de la Instalación")
cliente = st.sidebar.text_input("Cliente / Empresa", "Empresa Ejemplo S.A.S.")
direccion = st.sidebar.text_input("Dirección", "Calle Principal # 45-67")
telefono = st.sidebar.text_input("Teléfono", "+57 300 000 0000")
modelo = st.sidebar.text_input("Modelo Máquina", "MAQ-2026-X")
fecha = st.sidebar.text_input("Fecha", "22/09/2026")
norma = st.sidebar.text_input("Norma Evaluada", "RETIE/NTC 2050 (COLOMBIA)")

# Pestañas
tab_cargas, tab_fotos, tab_parametros, tab_pdf = st.tabs([
    "⚡ Carga y Componentes", 
    "📷 Nameplates / Fotos", 
    "🎯 Parámetros de Corte", 
    "📄 Generar PDF"
])

# 1. TAB CARGAS Y COMPONENTES
with tab_cargas:
    st.header("🔌 Voltajes y Componentes (kW)")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        v_primario = st.number_input("Voltaje Red Cliente (V)", value=220, step=10)
    with col_v2:
        v_secundario = st.number_input("Voltaje Lado Máquina (V)", value=380, step=10)

    if "lista_equipos" not in st.session_state:
        st.session_state.lista_equipos = [
            {"nombre": "Fuente Láser", "potencia_kw": 6.0},
            {"nombre": "Chiller de Enfriamiento", "potencia_kw": 3.0}
        ]

    for i, eq in enumerate(st.session_state.lista_equipos):
        c1, c2, c3 = st.columns([3, 2, 1])
        with c1:
            eq["nombre"] = st.text_input(f"Componente #{i+1}", value=eq["nombre"], key=f"nom_{i}")
        with c2:
            eq["potencia_kw"] = st.number_input(f"Potencia (kW)", min_value=0.1, value=float(eq["potencia_kw"]), step=0.5, key=f"kw_{i}")
        with c3:
            st.write(" ")
            st.write(" ")
            if st.button("❌", key=f"del_{i}"):
                st.session_state.lista_equipos.pop(i)
                st.rerun()

    if st.button("➕ Agregar Componente"):
        st.session_state.lista_equipos.append({"nombre": "Nuevo Equipo", "potencia_kw": 1.0})
        st.rerun()

    resumen = calcular_cuadro_completo(st.session_state.lista_equipos, v_primario, v_secundario)
    st.session_state.resumen = resumen

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Potencia Total", f"{resumen['potencia_total_kw']} kW")
    m2.metric("Transformador Rec.", f"{resumen['transformador_kva']} kVA")
    m3.metric("Corriente Primaria", f"{resumen['i_diseno_primario']} A")
    m4.metric("Breaker Sugerido", resumen['breaker_primario'])

# 2. TAB FOTOS DE NAMEPLATES
with tab_fotos:
    st.header("📷 Registro Fotográfico de Nameplates / Placas Técnicas")
    st.caption("Tome fotos con la cámara de su celular o adjunte imágenes de las placas de los equipos.")

    if "fotos_nameplates" not in st.session_state:
        st.session_state.fotos_nameplates = []

    uploaded_files = st.file_uploader("Agregar fotos de Nameplates", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    if uploaded_files:
        st.session_state.fotos_nameplates = uploaded_files

    if st.session_state.fotos_nameplates:
        cols = st.columns(3)
        for idx, file in enumerate(st.session_state.fotos_nameplates):
            with cols[idx % 3]:
                img = Image.open(file)
                st.image(img, caption=f"Foto Placa #{idx+1}", use_container_width=True)

# 3. TAB PARÁMETROS DE CORTE
with tab_parametros:
    st.header("🎯 Parámetros de Corte Probados y Calibrados")
    st.caption("Registre las recetas de corte para dejar como constancia técnica al cliente.")

    if "parametros_corte" not in st.session_state:
        st.session_state.parametros_corte = [
            {"material": "Acero al Carbono (HR/CR)", "espesor": "3.0 mm", "potencia": "80%", "velocidad": "3.5 m/min", "gas": "O2", "presion": "0.8 Bar", "foco": "-1.5 mm"},
            {"material": "Acero Inoxidable (304)", "espesor": "1.5 mm", "potencia": "100%", "velocidad": "12.0 m/min", "gas": "N2", "presion": "14.0 Bar", "foco": "+0.5 mm"}
        ]

    for i, p in enumerate(st.session_state.parametros_corte):
        st.markdown(f"**Receta #{i+1}**")
        col_p1, col_p2, col_p3, col_p4, col_p5, col_p6, col_p7, col_p8 = st.columns([2, 1.2, 1.2, 1.2, 1, 1, 1, 0.6])
        
        with col_p1: p["material"] = st.text_input("Material", value=p["material"], key=f"mat_{i}")
        with col_p2: p["espesor"] = st.text_input("Espesor", value=p["espesor"], key=f"esp_{i}")
        with col_p3: p["potencia"] = st.text_input("Potencia", value=p["potencia"], key=f"pot_{i}")
        with col_p4: p["velocidad"] = st.text_input("Velocidad", value=p["velocidad"], key=f"vel_{i}")
        with col_p5: p["gas"] = st.text_input("Gas", value=p["gas"], key=f"gas_{i}")
        with col_p6: p["presion"] = st.text_input("Presión", value=p["presion"], key=f"pres_{i}")
        with col_p7: p["foco"] = st.text_input("Foco", value=p["foco"], key=f"foc_{i}")
        with col_p8:
            st.write(" ")
            st.write(" ")
            if st.button("❌", key=f"del_param_{i}"):
                st.session_state.parametros_corte.pop(i)
                st.rerun()

    if st.button("➕ Agregar Ficha de Corte"):
        st.session_state.parametros_corte.append({
            "material": "Aluminio", "espesor": "2.0 mm", "potencia": "90%", 
            "velocidad": "6.0 m/min", "gas": "N2", "presion": "12.0 Bar", "foco": "0.0 mm"
        })
        st.rerun()

# 4. TAB GENERAR PDF
with tab_pdf:
    st.header("📄 Generación de Reporte Completo")
    
    if st.button("🚀 Generar Informe PDF", type="primary"):
        datos_cliente = {
            "cliente": cliente, "direccion": direccion, "telefono": telefono,
            "modelo": modelo, "fecha": fecha, "norma": norma
        }
        
        pdf_bytes = generar_pdf_informe(
            datos_cliente=datos_cliente,
            resumen=st.session_state.resumen,
            logo_path=logo_path,
            fotos_nameplates=st.session_state.get("fotos_nameplates", []),
            parametros_corte=st.session_state.get("parametros_corte", [])
        )
        
        st.download_button(
            label="📥 Descargar PDF Completo",
            data=pdf_bytes,
            file_name=f"Informe_Instalacion_{cliente.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
