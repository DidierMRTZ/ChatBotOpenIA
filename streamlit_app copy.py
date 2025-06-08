import streamlit as st
import plotly.express as px
import pandas as pd
import pymysql
from sqlalchemy import create_engine, text


# Configure OpenAI API key - using older API style that works with Python 3.7
openai.api_key = api_key

# ##############################################################################
# ChatGPT con Streamlit - Implementación mejorada
# ##############################################################################

# Configuración de la página
st.set_page_config(page_title="ChatGPT con Streamlit", page_icon="💬")

# Título y descripción
st.title("ChatGPT con Streamlit")
st.subheader("Interactúa con el modelo GPT de OpenAI")

# Selector de modelo
model = st.sidebar.selectbox(
    "Selecciona el modelo:",
    ["gpt-3.5-turbo", "gpt-4-turbo"],
    index=0
)


# Inicializar historial de mensajes
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola, soy ChatGPT. ¿En qué puedo ayudarte hoy?"}]

# Botón para limpiar la conversación
if st.sidebar.button("Limpiar conversación"):
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola, soy ChatGPT. ¿En qué puedo ayudarte hoy?"}]
    # Use experimental_rerun() for older Streamlit versions
    st.experimental_rerun()

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    # Compatibility for older Streamlit versions without chat_message
    if msg["role"] == "assistant":
        st.markdown(f"**🤖 Assistant:** {msg['content']}")
    else:
        st.markdown(f"**👤 User:** {msg['content']}")

# Add empty space before the input field
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

# Campo de entrada para el usuario
# Use text_input for older Streamlit versions
user_input = st.text_input("Escribe tu mensaje aquí...")

# Procesar entrada del usuario
if user_input:
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Display user message in older Streamlit version style
    st.markdown(f"**👤 User:** {user_input}")
    
    # Mostrar indicador de carga mientras se genera la respuesta
    message_placeholder = st.empty()
    message_placeholder.markdown("**🤖 Assistant:** Pensando...")
    
    try:
        # Generar respuesta utilizando la API de OpenAI (old-style API for compatibility)
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.messages
            ]
        )
        # Extraer el contenido de la respuesta (compatible with old API)
        response_content = response.choices[0].message.content

        print(response_content)
        
        # Mostrar la respuesta completa
        message_placeholder.markdown(f"**🤖 Assistant:** {response_content}")
        
        # Agregar respuesta al historial
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        
    except Exception as e:
        message_placeholder.markdown(f"Error al generar respuesta: {str(e)}")
        st.error(f"Error: {str(e)}")
