import streamlit as st
import pandas as pd
import os
import random

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Inglés UDAL - Estructuras Avanzadas", page_icon="🎓", layout="wide")

# ==========================================
# 2. INYECCIÓN DE DISEÑO VISUAL (CSS)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; }
    h1, h2, h3 { color: #002b5e !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #f2a900; color: #ffffff; font-weight: bold; border-radius: 8px; border: none; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #d19200; color: white; }
    .formula-box { font-size: 1.1rem; padding: 15px; background-color: #e8f4f8; border-radius: 8px; color: #002b5e; font-family: monospace; font-weight: bold; text-align: center; border: 1px dashed #002b5e; margin-bottom: 15px;}
    .header-box { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .reto-box { background-color: #002b5e; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-top: 10px;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SISTEMA DE SEGURIDAD
# ==========================================
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center;'><h2>Acceso al Simulador</h2></div>", unsafe_allow_html=True)
        password_ingresada = st.text_input("Clave de acceso:", type="password")
        if st.button("Ingresar"):
            if password_ingresada == "Comunicacion2026":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta.")
    st.stop()

# ==========================================
# 4. MOTOR GRAMATICAL AMPLIADO
# ==========================================
gramatica = {
    "Present Simple (Indicativo)": {
        "Uso": "Hechos, rutinas y verdades en comunicación.",
        "Formas": {
            "Afirmativa": {"Fórmula": "Sujeto + Verbo (s/es) + C", "Ej_EN": "The journalist writes the article.", "Ej_ES": "El periodista escribe el artículo."},
            "Negativa": {"Fórmula": "Sujeto + do/does not + Verbo base + C", "Ej_EN": "The journalist does not write the article.", "Ej_ES": "El periodista no escribe el artículo."},
            "Interrogativa": {"Fórmula": "Do/Does + Sujeto + Verbo base + C + ?", "Ej_EN": "Does the journalist write the article?", "Ej_ES": "¿Escribe el periodista el artículo?"}
        }
    },
    "Present Continuous (Progresivo)": {
        "Uso": "Acciones en curso o tendencias actuales.",
        "Formas": {
            "Afirmativa": {"Fórmula": "Sujeto + am/is/are + V-ing + C", "Ej_EN": "We are broadcasting live.", "Ej_ES": "Estamos transmitiendo en vivo."},
            "Negativa": {"Fórmula": "Sujeto + am/is/are not + V-ing + C", "Ej_EN": "We are not broadcasting live.", "Ej_ES": "No estamos transmitiendo en vivo."},
            "Interrogativa": {"Fórmula": "Am/Is/Are + Sujeto + V-ing + C + ?", "Ej_EN": "Are we broadcasting live?", "Ej_ES": "¿Estamos transmitiendo en vivo?"}
        }
    },
    "Past Continuous (Progresivo)": {
        "Uso": "Acciones interrumpidas o contexto en el pasado.",
        "Formas": {
            "Afirmativa": {"Fórmula": "Sujeto + was/were + V-ing + C", "Ej_EN": "The editor was checking the video.", "Ej_ES": "El editor estaba revisando el video."},
            "Negativa": {"Fórmula": "Sujeto + was/were not + V-ing + C", "Ej_EN": "The editor was not checking the video.", "Ej_ES": "El editor no estaba revisando el video."},
            "Interrogativa": {"Fórmula": "Was/Were + Sujeto + V-ing + C + ?", "Ej_EN": "Was the editor checking the video?", "Ej_ES": "¿Estaba el editor revisando el video?"}
        }
    },
    "Present Perfect (Perfecto)": {
        "Uso": "Experiencias o acciones pasadas con relevancia actual.",
        "Formas": {
            "Afirmativa": {"Fórmula": "Sujeto + have/has + V-Participio + C", "Ej_EN": "The brand has reached its target.", "Ej_ES": "La marca ha alcanzado su objetivo."},
            "Negativa": {"Fórmula": "Sujeto + have/has not + V-Participio + C", "Ej_EN": "The brand has not reached its target.", "Ej_ES": "La marca no ha alcanzado su objetivo."},
            "Interrogativa": {"Fórmula": "Have/Has + Sujeto + V-Participio + C + ?", "Ej_EN": "Has the brand reached its target?", "Ej_ES": "¿Ha alcanzado la marca su objetivo?"}
        }
    },
    "Past Perfect (Perfecto)": {
        "Uso": "Una acción que ocurrió antes que otra en el pasado.",
        "Formas": {
            "Afirmativa": {"Fórmula": "Sujeto + had + V-Participio + C", "Ej_EN": "The script had been approved before filming.", "Ej_ES": "El guion había sido aprobado antes de filmar."},
            "Negativa": {"Fórmula": "Sujeto + had not + V-Participio + C", "Ej_EN": "The script had not been approved.", "Ej_ES": "El guion no había sido aprobado."},
            "Interrogativa": {"Fórmula": "Had + Sujeto + V-Participio + C + ?", "Ej_EN": "Had the script been approved?", "Ej_ES": "¿Había sido aprobado el guion?"}
        }
    },
    "Imperative (Modo Imperativo)": {
        "Uso": "Órdenes, instrucciones técnicas o llamados a la acción (CTA).",
        "Formas": {
            "Afirmativa": {"Fórmula": "Verbo base + Complemento", "Ej_EN": "Check the microphone levels.", "Ej_ES": "Revisa los niveles del micrófono."},
            "Negativa": {"Fórmula": "Do not (Don't) + Verbo base + Complemento", "Ej_EN": "Don't release the news yet.", "Ej_ES": "No publiques la noticia aún."},
            "Interrogativa (Sugerencia)": {"Fórmula": "Shall we + Verbo base + C + ?", "Ej_EN": "Shall we start the interview?", "Ej_ES": "¿Comenzamos la entrevista?"}
        }
    }
}

# ==========================================
# 5. INTERFAZ PRINCIPAL
# ==========================================
st.markdown("""
<div class='header-box'>
    <h1 style='margin: 0;'>Sistema de Estructuras Gramaticales</h1>
    <p style='color: #555;'>UDAL - Ciencias de la Comunicación</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 Biblioteca de Tiempos", "🎯 Reto de Construcción"])

with tab1:
    tiempo = st.selectbox("Selecciona un tiempo o modo:", list(gramatica.keys()))
    
    col_info, col_form = st.columns([1, 2])
    
    with col_info:
        st.write(f"**Uso profesional:** {gramatica[tiempo]['Uso']}")
    
    with col_form:
        forma = st.radio("Variante:", list(gramatica[tiempo]["Formas"].keys()), horizontal=True)
        data = gramatica[tiempo]["Formas"][forma]
        
        st.markdown(f"<div class='formula-box'>{data['Fórmula']}</div>", unsafe_allow_html=True)
        st.info(f"🇬🇧 {data['Ej_EN']}")
        st.caption(f"🇪🇸 {data['Ej_ES']}")

with tab2:
    st.markdown("### Pon a prueba tu agilidad mental")
    if st.button("Generar Reto Aleatorio"):
        t_azar = random.choice(list(gramatica.keys()))
        f_azar = random.choice(list(gramatica[t_azar]["Formas"].keys()))
        d_azar = gramatica[t_azar]["Formas"][f_azar]
        
        st.markdown(f"""
        <div class='reto-box'>
            <h4>Traduce o construye:</h4>
            <p style='font-size: 1.2rem;'>Tiempo: <b>{t_azar}</b> | Forma: <b>{f_azar}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Ver solución"):
            st.markdown(f"**Fórmula:** `{d_azar['Fórmula']}`")
            st.success(f"Ejemplo: {d_azar['Ej_EN']}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #999;'>© 2026 Universidad de América Latina - Academic Support System</p>", unsafe_allow_html=True)
