import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser lo primero)
st.set_page_config(page_title="Inglés UDAL - Comunicación", page_icon="🎓", layout="wide")

# ==========================================
# 2. INYECCIÓN DE DISEÑO VISUAL Y COLORES (CSS)
# ==========================================
# Aquí forzamos los colores institucionales para darle el toque universitario
st.markdown("""
    <style>
    /* Fondo principal ligeramente gris para que resalten las tarjetas */
    .stApp {
        background-color: #f4f6f9;
    }
    /* Títulos en Azul Institucional Profundo */
    h1, h2, h3 {
        color: #002b5e !important; 
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Estilo del botón principal (Dorado/Naranja) */
    .stButton>button {
        background-color: #f2a900;
        color: #ffffff;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #d19200;
        color: white;
    }
    /* Cajas de información con bordes elegantes */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #002b5e;
    }
    /* Encabezado superior */
    .header-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SISTEMA DE SEGURIDAD (PANTALLA DE LOGIN)
# ==========================================
# Creamos una variable en la memoria para saber si el usuario ya puso la clave
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# Si no está autenticado, mostramos SOLO la pantalla de login
if not st.session_state.autenticado:
    st.markdown("<br><br>", unsafe_allow_html=True) # Espacio en blanco
    col1, col2, col3 = st.columns([1, 2, 1]) # Centramos el cuadro de login
    
    with col2:
        st.markdown("""
        <div style='background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;'>
            <img src='https://cdn-icons-png.flaticon.com/512/3308/3308395.png' width='80'>
            <h2 style='color: #002b5e; margin-top: 15px;'>Acceso al Simulador</h2>
            <p style='color: #666;'>Licenciatura en Ciencias de la Comunicación</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Espacio
        password_ingresada = st.text_input("Ingresa la clave de acceso de la clase:", type="password")
        
        if st.button("Ingresar a la Plataforma"):
            if password_ingresada == "Comunicacion2026": # <--- AQUÍ CAMBIAS TU CONTRASEÑA
                st.session_state.autenticado = True
                st.rerun() # Recarga la página ya con acceso
            else:
                st.error("❌ Contraseña incorrecta. Acceso denegado.")
    st.stop() # Detiene todo el código aquí abajo si no hay contraseña

# ==========================================
# 4. CARGA DE DATOS (CON TRADUCCIÓN)
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
# 5. APLICACIÓN PRINCIPAL (DISEÑO INSTITUCIONAL)
# ==========================================
# Encabezado visual de la Universidad
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
        
        # Ahora mostramos la columna de Traducción si existe
        columnas_a_mostrar = ["Palabra en Inglés"]
        if "Traducción" in df_filtrado.columns:
            columnas_a_mostrar.append("Traducción")
            
        df_mostrar = df_filtrado[columnas_a_mostrar].sort_values(by="Palabra en Inglés").reset_index(drop=True)
        
        # Mostramos la tabla ocupando todo el ancho
        st.dataframe(df_mostrar, use_container_width=True, height=500)
        st.success(f"📊 Mostrando {len(df_mostrar)} términos de la categoría: {categoria_seleccionada}.")
    else:
        st.error("Error cargando la base de datos.")

with tab_gram:
    st.markdown("### Estructuras Clave en la Comunicación")
    # Agregué una imagen de contexto para la sección gramatical
    st.image("https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    
    st.info("💡 Recuerda: Dominar estas fórmulas te permite redactar campañas, guiones y comunicados de prensa con impacto global.")
    
    # Aquí puedes mantener el diccionario de gramática que teníamos antes.
    # Por brevedad en la explicación, he omitido el diccionario, pero 
    # puedes pegar las fórmulas que ya teníamos en tu código anterior aquí mismo.
    st.write("*(Aquí van tus tarjetas de Present Simple, Continuous, etc. que ya teníamos)*")
