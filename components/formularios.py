import streamlit as st


def formulario_cliente():
    st.subheader("Nuevo cliente")

    nombre = st.text_input("Nombre / Empresa")

    identificacion = st.text_input(
        "Identificación / NIT"
    )

    telefono = st.text_input("Teléfono")

    email = st.text_input("Correo electrónico")

    direccion = st.text_input("Dirección")

    ciudad = st.text_input("Ciudad")

    return {
        "nombre": nombre,
        "identificacion": identificacion,
        "telefono": telefono,
        "email": email,
        "direccion": direccion,
        "ciudad": ciudad,
    }
