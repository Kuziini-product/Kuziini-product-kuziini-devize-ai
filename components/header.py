import streamlit as st

def afiseaza_header():
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("Logo_Kuziini.png", width=120)
    with col2:
        st.title("Kuziini – AI Generator de Devize")
        st.caption("Configurează, estimează și exportă automat oferte profesionale.")
