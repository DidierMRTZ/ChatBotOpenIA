import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

# Carga la clave de API desde .env
load_dotenv("env.env")
api_key = os.getenv("GOOGLE_API_KEY")

# Definición de la herramienta personalizada
@tool
def extraer_alimentos(texto: str) -> list[str]:
    """
    Extrae 'pan' y 'leche' del texto, si están presentes.
    """
    return [item for item in ("pan", "queso","leche") if item in texto.lower()]

# Construcción del prompt requerido por el agente
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un vendedor de productos. Utiliza las herramientas disponibles cuando el cliente pregunte por productos. "
               "Si no cuentas con una herramienta específica para resolver una pregunta, indícalo claramente y evita invocaciones innecesarias. "
               "Proporciona solo la respuesta directa en formato JSON, por ejemplo: AI: 'leche','queso'"),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Configuración del modelo LLM (Google Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
)

# Lista de herramientas disponibles
tools = [extraer_alimentos]

# Crear el agente con LangChain
agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

# Crear el ejecutor del agente
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Ejemplo de ejecución
result = agent_executor.invoke({"input": "Hola, me llamo Juan. ¿Tienes leche y PAN, zandia?"})
print(result["output"])
