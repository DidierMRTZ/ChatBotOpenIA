from fastapi import FastAPI
from routes.users import user
from routes.chats import chat
from routes.conversations import conversation
from routes.gpts import gpt
from routes.products import product
from routes.companies import company
from routes.clients import client
from routes.inventories import inventory
from routes.invoices import invoice
import models
from config.Database import engine, Base

# Crear todas las tablas
Base.metadata.create_all(bind=engine)


# Crear la instancia de la aplicación FastAPI
app = FastAPI()

app.include_router(user)
app.include_router(chat)
app.include_router(conversation)
app.include_router(gpt)
app.include_router(product)
app.include_router(company)
app.include_router(client)
app.include_router(inventory)
app.include_router(invoice)