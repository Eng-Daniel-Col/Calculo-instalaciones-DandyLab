import streamlit as st


def mostrar_sidebar():
    st.sidebar.title("DandyLab Ingeniería")

    menu = st.sidebar.radio(
        "Menú principal",
        [
            "Dashboard",
            "Clientes",
            "Máquinas",
            "Instalaciones",
            "Cálculo eléctrico",
            "Informes",
        ],
    )

    return menu
