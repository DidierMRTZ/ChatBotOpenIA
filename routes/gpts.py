from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_404_NOT_FOUND
from config.Database import engine
from models.gpt import Gpt
from schema.gpt import GptCreate, GptUpdate
from datetime import datetime
from sqlalchemy.orm import sessionmaker

# Definir el router
gpt = APIRouter()

# Obtener todos los GPTs
@gpt.get('/gpts', status_code=HTTP_200_OK)
def get_gpts():
    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    # Consultar
    gpts = session.query(Gpt).all()
    session.close()
    return gpts

# Obtener un GPT por ID
@gpt.get('/gpts/{id}', status_code=HTTP_200_OK)
def get_gpt_by_id(id: int):
    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    # Buscar el GPT en la base de datos
    gpt_item = session.query(Gpt).filter(Gpt.GptId == id).first()
    session.close()
    
    if not gpt_item:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="GPT no encontrado")
    return gpt_item

# Crear un nuevo GPT
@gpt.post('/gpts', status_code=HTTP_201_CREATED)
def create_gpt(gpt_data: GptCreate):
    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Crear objeto de GPT con los datos proporcionados
    new_gpt = Gpt(
        CreationTimestamp=gpt_data.CreationTimestamp or datetime.now(),
        CreatedBy=gpt_data.CreatedBy,
        ModificationTimestamp=gpt_data.ModificationTimestamp or datetime.now(),
        ModifiedBy=gpt_data.ModifiedBy,
        AsistentId=gpt_data.AsistentId
    )
    
    session.add(new_gpt)
    session.commit()
    session.refresh(new_gpt)
    session.close()
    return new_gpt

# Actualizar un GPT existente
@gpt.put('/gpts/{id}', status_code=HTTP_200_OK)
def update_gpt(id: int, gpt_data: GptUpdate):
    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Buscar el GPT por ID
    db_gpt = session.query(Gpt).filter(Gpt.GptId == id).first()
    if not db_gpt:
        session.close()
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="GPT no encontrado")
    
    # Actualizar los campos si están presentes en la solicitud
    update_data = gpt_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_gpt, key, value)
    
    # Actualizar el timestamp de modificación si no se especificó
    if "ModificationTimestamp" not in update_data:
        db_gpt.ModificationTimestamp = datetime.now()
    
    session.commit()
    session.refresh(db_gpt)
    session.close()
    return db_gpt

# Eliminar un GPT
@gpt.delete('/gpts/{id}', status_code=HTTP_204_NO_CONTENT)
def delete_gpt(id: int):
    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Buscar el GPT por ID
    db_gpt = session.query(Gpt).filter(Gpt.GptId == id).first()
    if not db_gpt:
        session.close()
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="GPT no encontrado")
    
    # Eliminar el GPT
    session.delete(db_gpt)
    session.commit()
    session.close()
    return {"message": "GPT eliminado correctamente"}
