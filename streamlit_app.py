import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
api_key = "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"
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="ChatBot GPT 💬", page_icon="🤖", layout="centered")

# CSS con íconos y estilos
st.markdown("""
    <style>
        .message-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .chat-bubble {
            padding: 0.75em 1em;
            border-radius: 12px;
            max-width: 75%;
            line-height: 1.4;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 16px;
        }
        .user {
            background-color: #f8f8f8;
            color: #222;
            margin-left: auto;
            justify-content: flex-end;
            text-align: right;
        }
        .assistant {
            background-color: #34495e;
            color: white;
            margin-right: auto;
            justify-content: flex-start;
            text-align: left;
        }
        .icon {
            font-size: 1.5rem;
            user-select: none;
        }
        /* Icono a la derecha para usuario */
        .user .icon {
            order: 2;
        }
        /* Icono a la izquierda para asistente */
        .assistant .icon {
            order: 0;
        }
        /* Ajustar el texto dentro de la burbuja */
        .bubble-text {
            flex-grow: 1;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>🤖 ChatGPT con Streamlit</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Habla con un asistente GPT personalizado</p>", unsafe_allow_html=True)

model = st.sidebar.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4-turbo"], index=0)

if st.sidebar.button("🧹 Nueva conversación"):
    st.session_state["messages"] = [{"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy?"}]
    st.rerun()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy?"}]

st.markdown("<div class='message-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    icon = "👤" if role_class == "user" else "🤖"
    # Cada burbuja es flex, con icono y texto
    st.markdown(
        f"""
        <div class='chat-bubble {role_class}'>
            <div class='icon'>{icon}</div>
            <div class='bubble-text'>{msg['content']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

user_input = st.chat_input("Escribe tu mensaje aquí...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Pensando..."):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages
            )
            content = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": content})
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error al generar respuesta: {e}")
