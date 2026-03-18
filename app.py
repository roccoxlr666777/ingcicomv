import streamlit as st
import pandas as pd
import os
import random

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Inglés UDAL - Comunicación", page_icon="🎓", layout="wide")

# ==========================================
# 2. INYECCIÓN DE DISEÑO VISUAL Y COLORES (CSS)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; }
    h1, h2, h3 { color: #002b5e !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #f2a900; color: #ffffff; font-weight: bold; border-radius: 8px; border: none; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #d19200; color: white; }
    .stAlert { border-radius: 10px; border-left: 5px solid #002b5e; }
    .header-box { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .formula-box { font-size: 1.2rem; padding: 15px; background-color: #e8f4f8; border-radius: 8px; color: #002b5e; font-family: monospace; font-weight: bold; text-align: center; border: 1px dashed #002b5e; margin-bottom: 15px;}
    .btn-azar>div>button { background-color: #002b5e; color: white; border: 2px solid #f2a900;}
    .btn-azar>div>button:hover { background-color: #001a38; border: 2px solid white;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SISTEMA DE SEGURIDAD
# ==========================================
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;'>
            <img src='https://cdn-icons-png.flaticon.com/512/3308/3308395.png' width='80'>
            <h2 style='color: #002b5e; margin-top: 15px;'>Acceso al Simulador</h2>
            <p style='color: #666;'>Licenciatura en Ciencias de la Comunicación</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        password_ingresada = st.text_input("Ingresa la clave de acceso de la clase:", type="password")
        
        if st.button("Ingresar a la Plataforma"):
            if password_ingresada == "Comunicacion2026":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta. Acceso denegado.")
    st.stop()

# ==========================================
# 4. CARGA DE DATOS VOCABULARIO
# ==========================================
@st.cache_data
def cargar_vocabulario_csv():
    archivo_csv = 'vocabulario_comunicacion.csv'
    if not os.path.exists(archivo_csv):
        return pd.DataFrame()
    try:
        return pd.read_csv(archivo_csv, encoding='utf-8')
    except Exception as e:
        return pd.DataFrame()

df_vocabulario_completo = cargar_vocabulario_csv()

# ==========================================
# 5. MOTOR GRAMATICAL
# ==========================================
gramatica = {
    "Present Simple": {
        "Uso": "Rutinas periodísticas, verdades generales y hechos actuales de la industria.",
        "Formas": {
            "Afirmativa": {"Fórmula
