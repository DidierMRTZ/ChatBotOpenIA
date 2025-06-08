from fastapi import APIRouter, HTTPException
from config.Database import engine, func
from sqlalchemy.orm import sessionmaker
from models.user import User
from pydantic import BaseModel
from typing import Optional, List
from schema.user import UserCreate, UserUpdate, UserRead
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK


user = APIRouter()

@user.get('/users', status_code=HTTP_200_OK, response_model=List[UserRead])
def get_users():
    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    # Consultar
    users = session.query(User).all()
    session.close()
    return users


@user.get('/users/{userId}', status_code=HTTP_200_OK, response_model=UserRead)
def get_users_id(userId: int):
    # Crear sesión
    Session = sessionmaker(bind=engine)
    db = Session()
    # Buscar el usuario en la base de datos
    users = db.query(User).filter(User.userId == userId).first()
    db.close()
    
    if not users:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return users

@user.post('/users', status_code=HTTP_201_CREATED, response_model=UserRead)
def create_users(user: UserCreate):
   # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Crear un nuevo usuario
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # Actualiza la instancia con los datos del DB
    session.close()
    return new_user 

@user.delete('/users/{userId}', status_code=HTTP_204_NO_CONTENT)
def delete_users_id(userId: int):
    Session = sessionmaker(bind=engine)
    db = Session()
    # Buscar el usuario en la base de datos
    usuario = db.query(User).filter(User.userId == userId).first()
    
    if not usuario:
        db.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Eliminar el usuario
    db.delete(usuario)
    db.commit()
    db.close()
    return {"message": "Usuario eliminado correctamente"}

@user.put('/users/{userId}', status_code=HTTP_200_OK, response_model=UserRead)
def update_users(userId: int, user_update: UserUpdate):
    Session = sessionmaker(bind=engine)
    db = Session()
    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.userId == userId).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar los campos si se proporcionan
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    db.close()
    return user

@user.get('/queryTenant', status_code=HTTP_200_OK)
def get_users_sales():
    # Crear sesión
    Session = sessionmaker(bind=engine)
    db = Session()
    # Consultar nombres completos
    data = db.query(User.firstName, User.lastName, User.email, func.count(User.userId)).group_by(User.firstName, User.lastName, User.email).all()
    db.close()
    return data