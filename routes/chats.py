from fastapi import APIRouter, HTTPException
from config.Database import engine
from sqlalchemy.orm import sessionmaker
from models.chat import Chat
from pydantic import BaseModel
from typing import Optional
from schema.chat import ChatCreate, ChatUpdate
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK


chat = APIRouter()

@chat.get('/chats', status_code=HTTP_200_OK)
def get_chats():
    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    # Consultar
    chats = session.query(Chat).all()
    return chats


@chat.get('/chats/{id}', status_code=HTTP_200_OK)
def get_chat_id(id: str):
    # Crear sesión
    Session = sessionmaker(bind=engine)
    db = Session()
    # Buscar el chat en la base de datos
    chat = db.query(Chat).filter(Chat.ChatId == id).first()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat no encontrado")
    
    return chat

@chat.post('/chats', status_code=HTTP_201_CREATED)
def create_chat(chat: ChatCreate):
    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    # Crear un nuevo chat
    new_chat = Chat(**chat.dict())
    session.add(new_chat)
    session.commit()
    session.refresh(new_chat)  # Actualiza la instancia con los datos del DB
    # Retornar el nuevo chat
    return new_chat 

@chat.delete('/chats/{id}', status_code=HTTP_204_NO_CONTENT)
def delete_chat_id(id: str):
    Session = sessionmaker(bind=engine)
    db = Session()
    # Buscar el chat en la base de datos
    chat = db.query(Chat).filter(Chat.ChatId == id).first()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat no encontrado")
    
    # Eliminar el chat
    db.delete(chat)
    db.commit()
    return chat

@chat.put('/chats/{id}')
def update_chat(id: str, chat_update: ChatUpdate):
    Session = sessionmaker(bind=engine)
    db = Session()
    # Buscar el chat en la base de datos
    chat = db.query(Chat).filter(Chat.ChatId == id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat no encontrado")
    
    # Actualizar los campos si se proporcionan
    for key, value in chat_update.dict(exclude_unset=True).items():
        setattr(chat, key, value)

    db.commit()
    db.refresh(chat)
    return chat
