import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Inglés UDAL - Comunicación", page_icon="🎓", layout="wide")

# 2. INYECCIÓN DE DISEÑO VISUAL Y COLORES (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; }
    h1, h2, h3 { color: #002b5e !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #f2a900; color: #ffffff; font-weight: bold; border-radius: 8px; border: none; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #d19200; color: white; }
    .stAlert { border-radius: 10px; border-left: 5px solid #002b5e; }
    .header-box { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 3. SISTEMA DE SEGURIDAD (PANTALLA DE LOGIN)
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

# 4. CARGA DE DATOS VOCABULARIO
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

# 5. BASE DE DATOS DE GRAMÁTICA (¡AQUÍ ESTÁ LO QUE FALTABA!)
gramatica = {
    "Present Simple": {
        "Uso": "Hábitos, verdades generales, rutinas y hechos en Comunicación.",
        "Fórmula (+)": "Sujeto + Verbo (s/es para he/she/it) + Complemento",
        "Fórmula (-)": "Sujeto + do/does + not + Verbo base + Complemento",
        "Ejemplo": "The journalist interviews the source.",
        "Traducción": "El periodista entrevista a la fuente."
    },
    "Present Continuous": {
        "Uso": "Acciones que ocurren en este momento o planes futuros cercanos (campañas).",
        "Fórmula (+)": "Sujeto + am/is/are + Verbo(-ing) + Complemento",
        "Fórmula (-)": "Sujeto + am/is/are + not + Verbo(-ing) + Complemento",
        "Ejemplo": "They are analyzing the engagement data right now.",
        "Traducción": "Ellos están analizando los datos de participación en este momento."
    },
    "Past Simple": {
        "Uso": "Acciones completadas en un momento específico del pasado (eventos de prensa).",
        "Fórmula (+)": "Sujeto + Verbo en pasado + Complemento",
        "Fórmula (-)": "Sujeto + did + not + Verbo base + Complemento",
        "Ejemplo": "The PR agency launched the viral campaign yesterday.",
        "Traducción": "La agencia de RP lanzó la campaña viral ayer."
    },
    "Future (Will)": {
        "Uso": "Predicciones de mercado, promesas o decisiones espontáneas.",
        "Fórmula (+)": "Sujeto + will + Verbo base + Complemento",
        "Fórmula (-)": "Sujeto + will + not (won't) + Verbo base + Complemento",
        "Ejemplo": "Consumers will trust a credible brand.",
        "Traducción": "Los consumidores confiarán en una marca creíble."
    },
    "Present Perfect": {
        "Uso": "Acciones que iniciaron en el pasado y continúan en el presente, o experiencias relevantes.",
        "Fórmula (+)": "Sujeto + have/has + Verbo en participio + Complemento",
        "Fórmula (-)": "Sujeto + have/has + not + Verbo en participio + Complemento",
        "Ejemplo": "We have developed a new social media strategy.",
        "Traducción": "Hemos desarrollado una nueva estrategia de redes sociales."
    }
}

# 6. APLICACIÓN PRINCIPAL (DISEÑO INSTITUCIONAL)
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

tab_vocab, tab_gram = st.tabs(["📖 Base de Datos Interactiva", "⚙️ Fórmulas y Tiempos"])

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
        st.success(f"📊 Mostrando {len(df_mostrar)} términos de la categoría: {categoria_seleccionada}.")
    else:
        st.error("Error cargando la base de datos.")

with tab_gram:
    st.markdown("### Estructuras Clave en la Comunicación")
    st.image("https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    st.info("💡 Recuerda: Dominar estas fórmulas te permite redactar campañas, guiones y comunicados de prensa con impacto global.")
    
    # RENDERIZADO DE LAS TARJETAS GRAMATICALES
    tiempo_seleccionado = st.radio("Selecciona un Tiempo Gramatical:", list(gramatica.keys()))
    datos_tiempo = gramatica[tiempo_seleccionado]
    
    with st.container():
        st.subheader(f"📌 {tiempo_seleccionado}")
        st.write(f"**Uso:** {datos_tiempo['Uso']}")
        
        st.markdown("#### 🧮 Fórmulas")
        with st.container():
            st.success(f"➕ Afirmativa: {datos_tiempo['Fórmula (+)']}")
        with st.container():
            st.error(f"➖ Negativa: {datos_tiempo['Fórmula (-)']}")
            
        st.markdown("#### 💡 Ejemplo Práctico")
        st.info(f"🇬🇧 **Inglés:** {datos_tiempo['Ejemplo']}\n\n🇪🇸 **Español:** {datos_tiempo['Traducción']}")
