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
    .reto-box { background-color: #002b5e; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-top: 10px;}
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
            "Afirmativa": {"Fórmula": "Sujeto + Verbo (s/es) + Complemento", "Ej_EN": "The agency launches the campaign today.", "Ej_ES": "La agencia lanza la campaña hoy."},
            "Negativa": {"Fórmula": "Sujeto + do/does + not + Verbo base + Complemento", "Ej_EN": "The agency does not launch the campaign today.", "Ej_ES": "La agencia no lanza la campaña hoy."},
            "Interrogativa Afirmativa": {"Fórmula": "Do/Does + Sujeto + Verbo base + Complemento + ?", "Ej_EN": "Does the agency launch the campaign today?", "Ej_ES": "¿La agencia lanza la campaña hoy?"},
            "Interrogativa Negativa": {"Fórmula": "Don't/Doesn't + Sujeto + Verbo base + Complemento + ?", "Ej_EN": "Doesn't the agency launch the campaign today?", "Ej_ES": "¿No lanza la agencia la campaña hoy?"}
        }
    },
    "Present Continuous": {
        "Uso": "Acciones que ocurren en este preciso momento o tendencias actuales en redes sociales.",
        "Formas": {
            "Afirmativa": {"Fórmula": "Sujeto + am/is/are + Verbo(-ing) + Complemento", "Ej_EN": "The PR team is managing a crisis right now.", "Ej_ES": "El equipo de RP está gestionando una crisis en este momento."},
            "Negativa": {"Fórmula": "Sujeto + am/is/are + not + Verbo(-ing) + Complemento", "Ej_EN": "The PR team is not managing a crisis right now.", "Ej_ES": "El equipo de RP no está gestionando una crisis en este momento."},
            "Interrogativa Afirmativa": {"Fórmula": "Am/Is/Are + Sujeto + Verbo(-ing) + Complemento + ?", "Ej_EN": "Is the PR team managing a crisis right now?", "Ej_ES": "¿Está el equipo de RP gestionando una crisis en este momento?"},
            "Interrogativa Negativa": {"Fórmula": "Aren't/Isn't + Sujeto + Verbo(-ing) + Complemento + ?", "Ej_EN": "Isn't the PR team managing a crisis right now?", "Ej_ES": "¿No está el equipo de RP gestionando una crisis en este momento?"}
        }
    },
    "Present Perfect": {
        "Uso": "Acciones pasadas que tienen un impacto directo en el presente (muy usado en reportes de resultados).",
        "Formas": {
            "Afirmativa": {"Fórmula": "Sujeto + have/has + Verbo(Participio) + Complemento", "Ej_EN": "The influencer has published the viral video.", "Ej_ES": "El influencer ha publicado el video viral."},
            "Negativa": {"Fórmula": "Sujeto + have/has + not + Verbo(Participio) + Complemento", "Ej_EN": "The influencer has not published the viral video.", "Ej_ES": "El influencer no ha publicado el video viral."},
            "Interrogativa Afirmativa": {"Fórmula": "Have/Has + Sujeto + Verbo(Participio) + Complemento + ?", "Ej_EN": "Has the influencer published the viral video?", "Ej_ES": "¿Ha publicado el influencer el video viral?"},
            "Interrogativa Negativa": {"Fórmula": "Haven't/Hasn't + Sujeto + Verbo(Participio) + Complemento + ?", "Ej_EN": "Hasn't the influencer published the viral video?", "Ej_ES": "¿No ha publicado el influencer el video viral?"}
        }
    },
    "Past Simple": {
        "Uso": "Eventos de prensa, rodajes o campañas que ya terminaron.",
        "Formas": {
            "Afirmativa": {"Fórmula": "Sujeto + Verbo(Pasado) + Complemento", "Ej_EN": "The director filmed the documentary in Mexico.", "Ej_ES": "El director filmó el documental en México."},
            "Negativa": {"Fórmula": "Sujeto + did + not + Verbo base + Complemento", "Ej_EN": "The director did not film the documentary in Mexico.", "Ej_ES": "El director no filmó el documental en México."},
            "Interrogativa Afirmativa": {"Fórmula": "Did + Sujeto + Verbo base + Complemento + ?", "Ej_EN": "Did the director film the documentary in Mexico?", "Ej_ES": "¿Filmó el director el documental en México?"},
            "Interrogativa Negativa": {"Fórmula": "Didn't + Sujeto + Verbo base + Complemento + ?", "Ej_EN": "Didn't the director film the documentary in Mexico?", "Ej_ES": "¿No filmó el director el documental en México?"}
        }
    },
    "Future Simple (Will)": {
        "Uso": "Predicciones de mercado, proyecciones de audiencia y decisiones espontáneas.",
        "Formas": {
            "Afirmativa": {"Fórmula": "Sujeto + will + Verbo base + Complemento", "Ej_EN": "The algorithm will analyze the audience data.", "Ej_ES": "El algoritmo analizará los datos de la audiencia."},
            "Negativa": {"Fórmula": "Sujeto + will + not (won't) + Verbo base + Complemento", "Ej_EN": "The algorithm won't analyze the audience data.", "Ej_ES": "El algoritmo no analizará los datos de la audiencia."},
            "Interrogativa Afirmativa": {"Fórmula": "Will + Sujeto + Verbo base + Complemento + ?", "Ej_EN": "Will the algorithm analyze the audience data?", "Ej_ES": "¿Analizará el algoritmo los datos de la audiencia?"},
            "Interrogativa Negativa": {"Fórmula": "Won't + Sujeto + Verbo base + Complemento + ?", "Ej_EN": "Won't the algorithm analyze the audience data?", "Ej_ES": "¿No analizará el algoritmo los datos de la audiencia?"}
        }
    }
}

# ==========================================
# 6. APLICACIÓN PRINCIPAL (DISEÑO INSTITUCIONAL)
# ==========================================
st.markdown("""
<div class='header-box'>
    <div style='display: flex; align-items: center;'>
        <img src='https://cdn-icons-png.flaticon.com/512/1903/1903162.png' width='70' style='margin-right: 20px;'>
        <div>
            <h1 style='margin: 0; font-size: 2.2rem;'>Inglés Estructural y Técnico</h1>
            <p style='margin: 0; font-size: 1.1rem; color: #555;'>Universidad de América Latina | Área de Comunicación</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_vocab, tab_gram = st.tabs(["📖 Base de Datos Interactiva", "⚙️ Constructor y Retos"])

# --- PESTAÑA VOCABULARIO ---
with tab_vocab:
    st.markdown("### Vocabulario Especializado")
    if not df_vocabulario_completo.empty:
        categorias_disponibles = df_vocabulario_completo["Categoría Gramatical"].unique()
        categoria_seleccionada = st.selectbox("Selecciona la rama gramatical a estudiar:", categorias_disponibles)
        
        df_filtrado = df_vocabulario_completo[df_vocabulario_completo["Categoría Gramatical"] == categoria_seleccionada]
        
        columnas_a_mostrar = ["Palabra en Inglés"]
        if "Traducción" in df_filtrado.columns:
            columnas_a_mostrar.append("Traducción")
            
        df_mostrar = df_filtrado[columnas_a_mostrar].sort_values(by="Palabra en Inglés").reset_index(drop=True)
        st.dataframe(df_mostrar, use_container_width=True, height=500)
    else:
        st.error("Error cargando la base de datos.")

# --- PESTAÑA GRAMÁTICA (CON AZAR A PRUEBA DE FALLOS) ---
with tab_gram:
    st.image("https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    
    # SECCIÓN 1: ESTUDIO MANUAL
    st.markdown("### 1️⃣ Consulta Manual")
    st.info("💡 Construye la oración seleccionando el tiempo y la forma.")
    
    tiempo_seleccionado = st.selectbox("Tiempo Verbal:", list(gramatica.keys()))
    datos_tiempo = gramatica[tiempo_seleccionado]
    
    formas_disponibles = list(datos_tiempo["Formas"].keys())
    forma_seleccionada = st.radio("Forma / Modo:", formas_disponibles, horizontal=True)
    
    datos_forma = datos_tiempo["Formas"][forma_seleccionada]
    
    st.markdown(f"<div class='formula-box'>{datos_forma['Fórmula']}</div>", unsafe_allow_html=True)
    
    colA, colB = st.columns(2)
    with colA:
        st.success(f"🇬🇧 **Inglés:**\n\n{datos_forma['Ej_EN']}")
    with colB:
        st.info(f"🇪🇸 **Español:**\n\n{datos_forma['Ej_ES']}")

    st.markdown("---")

    # SECCIÓN 2: GAMIFICACIÓN (EL BOTÓN QUE NO CRASHEA)
    st.markdown("### 2️⃣ Modo Reto (Evaluación)")
    st.write("Presiona el botón. Intenta recordar la fórmula en tu cabeza antes de desplegar la respuesta.")

    if st.button("🎲 Generar Nuevo Reto al Azar", use_container_width=True):
        # Elegimos al azar internamente sin tocar los botones de arriba
        tiempo_azar = random.choice(list(gramatica.keys()))
        forma_azar = random.choice(list(gramatica[tiempo_azar]["Formas"].keys()))
        datos_azar = gramatica[tiempo_azar]["Formas"][forma_azar]
        
        st.markdown(f"""
        <div class='reto-box'>
            <h4 style='color: white; margin-bottom: 5px;'>🎯 Reto Estructural</h4>
            <p style='font-size: 1.1rem; margin-top: 0;'>Construye una oración en <b>{tiempo_azar}</b> usando la forma <b>{forma_azar}</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # El expansor oculta la respuesta hasta que el alumno haga clic
        with st.expander("👀 Desplegar Fórmula y Respuesta"):
            st.markdown(f"<div class='formula-box'>{datos_azar['Fórmula']}</div>", unsafe_allow_html=True)
            st.success(f"🇬🇧 **Ejemplo:** {datos_azar['Ej_EN']}")
            st.info(f"🇪🇸 **Traducción:** {datos_azar['Ej_ES']}")
