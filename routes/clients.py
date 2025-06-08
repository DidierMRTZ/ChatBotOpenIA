from fastapi import APIRouter, HTTPException
from config.Database import engine, func # Assuming func might be used later, like in users.py
from sqlalchemy.orm import sessionmaker
from models.client import Client # Changed from models.user import User
from pydantic import BaseModel # Not strictly needed if only using schemas
from typing import Optional, List
from schema.client import ClientCreate, ClientUpdate, ClientRead # Changed from schema.user
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK


client = APIRouter() # Renamed from user to client_router, then to client

@client.get('/clients', status_code=HTTP_200_OK, response_model=List[ClientRead]) # Path changed, response_model changed
def get_clients(): # Renamed
    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    # Consultar
    clients = session.query(Client).all() # Changed from User
    session.close()
    return clients


@client.get('/clients/{clientId}', status_code=HTTP_200_OK, response_model=ClientRead) # Path and param changed
def get_clients_id(clientId: int): # Renamed, param changed
    # Crear sesión
    Session = sessionmaker(bind=engine)
    db = Session()
    # Buscar el cliente en la base de datos
    client = db.query(Client).filter(Client.clientId == clientId).first() # Changed from User, User.userId
    db.close()
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado") # Message changed
    
    return client

@client.post('/clients', status_code=HTTP_201_CREATED, response_model=ClientRead) # Path changed
def create_clients(client_data: ClientCreate): # Renamed, param type changed
   # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Crear un nuevo cliente
    new_client = Client(**client_data.dict()) # Changed from User, user.dict()
    session.add(new_client)
    session.commit()
    session.refresh(new_client)  # Actualiza la instancia con los datos del DB
    session.close()
    return new_client 

@client.delete('/clients/{clientId}', status_code=HTTP_204_NO_CONTENT) # Path and param changed
def delete_clients_id(clientId: int): # Renamed, param changed
    Session = sessionmaker(bind=engine)
    db = Session()
    # Buscar el cliente en la base de datos
    client_to_delete = db.query(Client).filter(Client.clientId == clientId).first() # Changed variable name and model
    
    if not client_to_delete:
        db.close()
        raise HTTPException(status_code=404, detail="Cliente no encontrado") # Message changed
    
    # Eliminar el cliente
    db.delete(client_to_delete)
    db.commit()
    db.close()
    return {"message": "Cliente eliminado correctamente"} # Message changed

@client.put('/clients/{clientId}', status_code=HTTP_200_OK, response_model=ClientRead) # Path and param changed
def update_clients(clientId: int, client_update: ClientUpdate): # Renamed, params changed
    Session = sessionmaker(bind=engine)
    db = Session()
    # Buscar el cliente en la base de datos
    client_record = db.query(Client).filter(Client.clientId == clientId).first() # Changed variable name and model
    if not client_record:
        db.close()
        raise HTTPException(status_code=404, detail="Cliente no encontrado") # Message changed
    
    # Actualizar los campos si se proporcionan
    for key, value in client_update.dict(exclude_unset=True).items():
        setattr(client_record, key, value)

    db.commit()
    db.refresh(client_record)
    db.close()
    return client_record

# If you had a get_users_sales or similar, you might replicate it here for clients
# For example:
# @client_router.get('/queryClientTenant', status_code=HTTP_200_OK) 
# def get_clients_extra_info():
#     Session = sessionmaker(bind=engine)
#     db = Session()
#     data = db.query(Client.firstName, Client.lastName, func.count(Client.clientId)).group_by(Client.firstName, Client.lastName).all()
#     db.close()
#     return data
