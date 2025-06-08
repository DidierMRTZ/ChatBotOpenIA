from fastapi import APIRouter, HTTPException
from config.Database import engine, func
from sqlalchemy.orm import sessionmaker
from models.inventory import Inventory # Changed from User
from pydantic import BaseModel
from typing import Optional, List
from schema.inventory import InventoryCreate, InventoryUpdate, InventoryRead # Changed from User schemas
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK

inventory = APIRouter() # Changed from user

@inventory.get('/inventories', status_code=HTTP_200_OK, response_model=List[InventoryRead]) # Path and response_model changed
def get_inventories(): # Renamed
    Session = sessionmaker(bind=engine)
    session = Session()
    inventories_list = session.query(Inventory).all() # Changed from User, variable 'inventories_list'
    session.close()
    return inventories_list

@inventory.get('/inventories/{inventoryId}', status_code=HTTP_200_OK, response_model=InventoryRead) # Path, param, response_model changed
def get_inventories_id(inventoryId: int): # Renamed, param changed
    Session = sessionmaker(bind=engine)
    db = Session()
    inventory_record = db.query(Inventory).filter(Inventory.inventoryId == inventoryId).first() # Changed from User, userId. Variable 'inventory_record'
    db.close()
    if not inventory_record:
        raise HTTPException(status_code=404, detail="Inventario no encontrado") # Message changed
    return inventory_record

@inventory.post('/inventories', status_code=HTTP_201_CREATED, response_model=InventoryRead) # Path and response_model changed
def create_inventories(inventory_data: InventoryCreate): # Renamed, param type changed. Variable 'inventory_data'
    Session = sessionmaker(bind=engine)
    session = Session()
    new_inventory = Inventory(**inventory_data.dict()) # Changed from User. Variable 'new_inventory'
    session.add(new_inventory)
    session.commit()
    session.refresh(new_inventory)
    session.close()
    return new_inventory

@inventory.delete('/inventories/{inventoryId}', status_code=HTTP_204_NO_CONTENT) # Path and param changed
def delete_inventories_id(inventoryId: int): # Renamed, param changed
    Session = sessionmaker(bind=engine)
    db = Session()
    inventory_to_delete = db.query(Inventory).filter(Inventory.inventoryId == inventoryId).first() # Changed from User, userId. Variable 'inventory_to_delete'
    if not inventory_to_delete:
        db.close()
        raise HTTPException(status_code=404, detail="Inventario no encontrado") # Message changed
    db.delete(inventory_to_delete)
    db.commit()
    db.close()
    return {"message": "Inventario eliminado correctamente"} # Message changed

@inventory.put('/inventories/{inventoryId}', status_code=HTTP_200_OK, response_model=InventoryRead) # Path, param, response_model changed
def update_inventories(inventoryId: int, inventory_update: InventoryUpdate): # Renamed, params changed. Variable 'inventory_update'
    Session = sessionmaker(bind=engine)
    db = Session()
    inventory_record = db.query(Inventory).filter(Inventory.inventoryId == inventoryId).first() # Changed from User, userId. Variable 'inventory_record'
    if not inventory_record:
        db.close()
        raise HTTPException(status_code=404, detail="Inventario no encontrado") # Message changed
    
    for key, value in inventory_update.dict(exclude_unset=True).items():
        setattr(inventory_record, key, value)
    db.commit()
    db.refresh(inventory_record)
    db.close()
    return inventory_record

@inventory.get('/queryInventoryInfo', status_code=HTTP_200_OK) # Path changed from /queryTenant
def get_inventories_summary(): # Renamed from get_users_sales, and 'summary' instead of 'sales'
    Session = sessionmaker(bind=engine)
    db = Session()
    # Query adjusted for Inventory model
    data = db.query(
        Inventory.inventoryId,
        Inventory.productId,
        Inventory.companyId,
        Inventory.quantity,
        Inventory.costPrice,
        Inventory.salePrice,
        Inventory.createdAt,
        Inventory.updatedAt,
        func.count(Inventory.inventoryId) # Changed from User.userId
    ).group_by(Inventory.inventoryId).all()
    db.close()
    return data
