import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="MLOps",
    page_icon="🚀",
    layout="centered" 
)

logo_comillas = "https://upload.wikimedia.org/wikipedia/commons/e/e4/Comillas_Universidad_Pontificia_logo_%282018%29.jpg?utm_source=es.wikipedia.org&utm_campaign=index&utm_content=original"
python_logo = "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg?utm_source=ext.wikipedia.org&utm_campaign=index&utm_content=original"
#st.image(URL_LOGO, width=350)


# Creamos las columnas (4 partes para el logo horizontal, 1 para Python)
col1, col2 = st.columns([4, 1])

with col1:
    st.image(
        logo_comillas, 
        use_container_width=True
    )

with col2:
    st.image(
        python_logo, 
        use_container_width=True
    )



st.markdown(
    '<h1 style="font-size: 3rem; margin-top: 15px; margin-bottom: 0px;"> ¿Cómo hacer una web demo con Streamlit? 💻</h1>', 
    unsafe_allow_html=True
)

st.subheader("Y de paso conseguir una camiseta de ElevenLabs 👕🧪")

st.write("Santiago Lillo, MLOps - MUIAAp")

st.divider()



st.header("🚀 Pasos para iniciar el proyecto con UV")
st.write("Sigue estos pasos en tu termial:")

# Paso 1
st.markdown("### 1️⃣ Crea la estructura base con `uv`:")
st.code("uv init", language="bash")


# Paso 2
st.markdown("### 2️⃣ Añade Streamlit")
st.code("uv add streamlit", language="bash")


# Paso 3
st.markdown("### 3️⃣ Crea el scrpit")
st.code("touch demo.py", language="bash")

st.write("(o manualmente). Luego, copia y pega este código dentro de `demo.py`:")
codigo_base = """import streamlit as st

st.title("¡Hola Mundo!")
st.write("¡Andrés y Sergio son los mejores!")"""
st.code(codigo_base, language="python")


# Paso 4
st.markdown("### 4️⃣ Visualización")
st.code("uv run streamlit run demo.py", language="bash")

st.success("🎉 ¡Listo! Tu navegador debería abrir automáticamente una pestaña en `http://localhost:8501`.")




st.divider()

st.header("🤔 ¿Qué más podemos hacer?")

# Desplegable
modelo_seleccionado = st.selectbox(
    "Selecciona un modelo de IA:",
    ["GPT-4o (OpenAI)", "Claude 3.5 Sonnet (Anthropic)", "Llama 3 (Meta)", "Random Forest Regressor"]
)

# Hiperparámetro
temperatura = st.slider(
    "🌡️ Ajusta la creatividad del modelo (cuanto menos creatividad, más determinismo):",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.001
)

# Botón  
if st.button("🚀 Ejecutar Inferencia"):
    st.info(f"Generando respuesta con **{modelo_seleccionado}**...")
    # Simulación de carga
    import time
    time.sleep(1)
    st.success("✨ ¡Inferencia completada con éxito!")


st.divider()


st.markdown("### 📥 Descarga y Visualización de datos")

# Creamos un DataFrame falso, pero se actualiza cuando le demos al botón de predicciones
df_ejemplo = pd.DataFrame({
    'id_prediccion': range(1, 6),
    'modelo': [modelo_seleccionado] * 5,
    'score': np.random.uniform(0.85, 0.99, 5),
    'timestamp': pd.date_range(start='2026-10-01', periods=5, freq='D')
})

# Convertimos el dataframe a CSV para la descarga
csv_data = df_ejemplo.to_csv(index=False).encode('utf-8')


st.download_button(
    label="💾 Descarga este CSV de Predicciones",
    data=csv_data,
    file_name="predicciones_mlops.csv",
    mime="text/csv",
)


st.dataframe(df_ejemplo, use_container_width=True)

st.line_chart(
    data=df_ejemplo,
    x='timestamp',
    y='score',
    use_container_width=True
)