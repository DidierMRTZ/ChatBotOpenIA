from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_404_NOT_FOUND
from config.Database import engine
from models.conversation import Conversation
from schema.conversation import ConversationCreate, ConversationUpdate
from datetime import datetime
from sqlalchemy.orm import sessionmaker

# Definir el router
conversation = APIRouter()


# Obtener todas las conversaciones
@conversation.get('/conversations', status_code=HTTP_200_OK)
def get_conversations():
    Session = sessionmaker(bind=engine)
    session = Session()
    conversations = session.query(Conversation).all()
    session.close()
    return conversations

# Obtener una conversación por ID
@conversation.get('/conversations/{id}', status_code=HTTP_200_OK)
def get_conversation_by_id(id: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    conversation = session.query(Conversation).filter(Conversation.ConversationId == id).first()
    session.close()
    
    if not conversation:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Conversación no encontrada")
    return conversation

# Crear una nueva conversación
@conversation.post('/conversations', status_code=HTTP_201_CREATED)
def create_conversation(conversation_data: ConversationCreate):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Crear objeto de conversación con los datos proporcionados
    new_conversation = Conversation(
        CreationTimestamp=conversation_data.CreationTimestamp or datetime.now(),
        CreatedBy=conversation_data.CreatedBy,
        ModificationTimestamp=conversation_data.ModificationTimestamp,
        ModifiedBy=conversation_data.ModifiedBy,
        CommetCpt=conversation_data.CommetCpt,
        CommetUser=conversation_data.CommetUser,
        TextCommet=conversation_data.TextCommet,
        ChatId=conversation_data.ChatId
    )
    
    session.add(new_conversation)
    session.commit()
    session.refresh(new_conversation)
    session.close()
    return new_conversation

# Actualizar una conversación existente
@conversation.put('/conversations/{id}', status_code=HTTP_200_OK)
def update_conversation(id: int, conversation_data: ConversationUpdate):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Buscar la conversación por ID
    db_conversation = session.query(Conversation).filter(Conversation.ConversationId == id).first()
    if not db_conversation:
        session.close()
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Conversación no encontrada")
    
    # Actualizar los campos si están presentes en la solicitud
    for key, value in conversation_data.dict(exclude_unset=True).items():
        setattr(db_conversation, key, value)
    
    # Actualizar el timestamp de modificación
    db_conversation.ModificationTimestamp = datetime.now()
    
    session.commit()
    session.refresh(db_conversation)
    session.close()
    return db_conversation

# Eliminar una conversación
@conversation.delete('/conversations/{id}', status_code=HTTP_204_NO_CONTENT)
def delete_conversation(id: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Buscar la conversación por ID
    db_conversation = session.query(Conversation).filter(Conversation.ConversationId == id).first()
    if not db_conversation:
        session.close()
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Conversación no encontrada")
    
    # Eliminar la conversación
    session.delete(db_conversation)
    session.commit()
    session.close()
    return {"message": "Conversación eliminada correctamente"}
