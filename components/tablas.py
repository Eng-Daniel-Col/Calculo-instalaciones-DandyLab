import streamlit as st


def mostrar_clientes(clientes):
    st.dataframe(
        clientes,
        use_container_width=True,
    )
