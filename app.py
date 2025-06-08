from fastapi import FastAPI

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

# Ruta de prueba para la raíz
@app.get("/")
def read_root():
    return {"message": "¡Hola, Mundo!"}

