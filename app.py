# AgroAdvisor GPT - App con Streamlit (versión final para Streamlit Cloud)

import streamlit as st
from openai import OpenAI

# CONFIGURACION
st.set_page_config(page_title="AgroAdvisor GPT", layout="centered")

# Obtener la API Key desde los secrets de Streamlit Cloud
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.title("🌱 AgroAdvisor GPT")
st.markdown("Asistente inteligente para recomendaciones agronómicas de Corteva")

# Inputs del usuario
ubicacion = st.text_input("Ubicación del productor (provincia/localidad):")
cultivo = st.selectbox("Cultivo:", ["Maíz", "Soja"])
fecha_siembra = st.text_input("Fecha estimada de siembra:")
consulta = st.text_area("Consulta puntual:")

# Botón para generar
if st.button("Generar Recomendación"):
    if not all([ubicacion, cultivo, fecha_siembra, consulta]):
        st.warning("Por favor completá todos los campos.")
    else:
        with st.spinner("Generando respuesta..."):
            prompt = f"""
            Sos un asesor técnico de Corteva en Argentina. Tu tarea es responder consultas agronómicas de forma profesional, clara y adaptada al contexto local.

            Datos del productor:
            - Ubicación: {ubicacion}
            - Cultivo: {cultivo}
            - Fecha estimada de siembra: {fecha_siembra}
            - Consulta: {consulta}

            Proporcioná una recomendación técnica basada en buenas prácticas agronómicas y productos sugeridos por Corteva.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": "Sos un asesor agronómico de Corteva en Argentina."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                respuesta = response.choices[0].message.content
                st.success("Respuesta generada:")
                st.markdown(respuesta)
            except Exception as e:
                st.error(f"Error al generar respuesta: {e}")
