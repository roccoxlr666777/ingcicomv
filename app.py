import streamlit as st
import pandas as pd
import os

# Configuración de la página para que se vea bien en celulares
st.set_page_config(page_title="Simulador de Inglés para Comunicación", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# FUNCIÓN PARA CARGAR EL VOCABULARIO (Nuevo método)
# ==========================================
@st.cache_data # Cacheamos la carga para que sea rápida
def cargar_vocabulario_csv():
    """Carga la base de datos de vocabulario desde el archivo CSV."""
    archivo_csv = 'vocabulario_comunicacion.csv'
    
    # Verificamos si el archivo existe en el servidor
    if not os.path.exists(archivo_csv):
        st.error(f"⚠️ Error Crítico: No se encontró el archivo '{archivo_csv}'. Asegúrate de haberlo subido a GitHub junto con este código.")
        return pd.DataFrame(columns=["Palabra en Inglés", "Categoría Gramatical"]) # Retornamos tabla vacía para no romper la app

    try:
        df = pd.read_csv(archivo_csv, encoding='utf-8') # Leemos el CSV
        return df
    except Exception as e:
        st.error(f"⚠️ Error al leer el archivo CSV: {e}")
        return pd.DataFrame(columns=["Palabra en Inglés", "Categoría Gramatical"])

# Intentamos cargar los datos
df_vocabulario_completo = cargar_vocabulario_csv()

# ==========================================
# BASE DE DATOS DE GRAMÁTICA (Se mantiene igual)
# ==========================================
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

# ==========================================
# INTERFAZ DE USUARIO (UI)
# ==========================================
# Diseño simplificado para pantallas táctiles
st.title("📚 Inglés para Comunicólogos")
st.markdown("Domina el vocabulario clave y las fórmulas gramaticales de tu profesión.")

# Pestañas táctiles en lugar de menú lateral para mejor UX en celular
tab_vocab, tab_gram = st.tabs(["📖 Vocabulario de Comunicación", "⚙️ Fórmulas y Tiempos"])

# --- Pestaña de Vocabulario ---
with tab_vocab:
    st.header("Base de Datos Estructural")
    
    # Verificamos que haya datos
    if not df_vocabulario_completo.empty:
        # Obtener categorías únicas dinámicamente desde el CSV
        categorias_disponibles = df_vocabulario_completo["Categoría Gramatical"].unique()
        
        # Filtro interactivo (selectbox grande para dedo)
        categoria_seleccionada = st.selectbox("Categoría Gramatical:", categorias_disponibles)
        
        # Filtrar el DataFrame
        df_filtrado = df_vocabulario_completo[df_vocabulario_completo["Categoría Gramatical"] == categoria_seleccionada]
        
        # Mostrar datos en una tabla limpia, ordenada alfabéticamente
        df_mostrar = df_filtrado[["Palabra en Inglés"]].sort_values(by="Palabra en Inglés").reset_index(drop=True)
        st.dataframe(df_mostrar, use_container_width=True, height=450)
        
        # Contador profesional
        num_palabras = len(df_mostrar)
        st.info(f"Mostrando **{num_palabras}** términos de la categoría: {categoria_seleccionada}.")
        
        st.markdown("---")
        st.caption("Tip: Para agregar más palabras, edita el archivo 'vocabulario_comunicacion.csv' en GitHub.")
    else:
        st.warning("No hay vocabulario cargado. Verifica tu archivo CSV.")

# --- Pestaña de Gramática ---
with tab_gram:
    st.header("Estructuras Clave con Ejemplos del Área")
    
    # Botones grandes para seleccionar el tiempo
    tiempo_seleccionado = st.radio("Tiempo/Modo Gramatical:", list(gramatica.keys()))
    
    # Obtener los datos del tiempo seleccionado
    datos_tiempo = gramatica[tiempo_seleccionado]
    
    # Diseño en tarjetas limpias
    with st.container():
        st.subheader(f"📌 {tiempo_seleccionado}")
        st.write(f"**Uso:** {datos_tiempo['Uso']}")
        
        st.markdown("#### 🧮 Fórmulas")
        
        # Fórmulas separadas en contenedores de color
        with st.container():
            st.success(f"➕ Afirmativa: {datos_tiempo['Fórmula (+)']}")
        with st.container():
            st.error(f"➖ Negativa: {datos_tiempo['Fórmula (-)']}")
            
        st.markdown("#### 💡 Ejemplo Práctico de Comunicación")
        st.info(f"🇬🇧 **Inglés:** {datos_tiempo['Ejemplo']}\n\n🇪🇸 **Español:** {datos_tiempo['Traducción']}")

# Pie de página ligero
st.markdown("---")
st.caption("Desarrollado para el análisis estructural del idioma inglés en el sector Comunicación.")