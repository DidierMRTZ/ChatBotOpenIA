import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import BaseTool, StructuredTool, tool
# Cargar variables de entorno
load_dotenv('env.env')

# Obtener la clave de API de Google
api_key = os.getenv("GOOGLE_API_KEY")

# Verificar que la clave se haya cargado correctamente
if not api_key:
    raise ValueError("Se requiere una clave de API de Google")

# Inicializar el modelo
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=api_key
)

# Definir la plantilla del prompt
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(""" Eres un vendedor de productos en un supermercado. Al iniciar la conversacion suguierele al cliente el numero de documento sin espacios ni puntos
    y el nombre del cliente. Luego, pregunta al cliente qué producto desea comprar y proporciona una respuesta clara y concisa. Si el cliente no menciona un producto, infórmale que no puedes ayudar sin esa información.
    Responde únicamente con el nombre del producto y evita cualquier información adicional o innecesaria.
    Adcionalmente no le permitas comprar sin antes haberle preguntado el nombre y el numero de documento.
                                              
    Utiliza únicamente las herramientas disponibles para responder preguntas relacionadas con productos de supermercado de manera precisa y concisa.
    
        """),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

# Configurar la memoria
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Crear la cadena de conversación
chat = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)

@tool
def add(*args):
  """Verificar si los productos están disponibles en la tienda."""
  lista_productos = ["pan", "leche", "huevo", "queso", "carne"]
  lista_productos_disponibles = []
  for arg in args:
    if arg in lista_productos:
      lista_productos_disponibles.append(arg)

  return lista_productos_disponibles if lista_productos_disponibles else "No hay productos disponibles."


# Función para interactuar con el chatbot
def interactuar_con_chatbot(input_usuario):
    respuesta = chat.predict(input=input_usuario)
    return respuesta


# Ejemplo de uso

print(interactuar_con_chatbot("Hola, qué productos tienen?"))

print(interactuar_con_chatbot("Hola, quiero comprar pan y leche."))







