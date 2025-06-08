from fastapi import APIRouter, HTTPException
from config.Database import engine, func
from sqlalchemy.orm import sessionmaker
from models.product import Product # Changed from User
from pydantic import BaseModel
from typing import Optional, List
from schema.product import ProductCreate, ProductUpdate, ProductRead # Changed from User schemas
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK

product = APIRouter() # Changed from user

@product.get('/products', status_code=HTTP_200_OK, response_model=List[ProductRead]) # Path and response_model changed
def get_products(): # Renamed
    Session = sessionmaker(bind=engine)
    session = Session()
    products = session.query(Product).all() # Changed from User
    session.close()
    return products

@product.get('/products/{productId}', status_code=HTTP_200_OK, response_model=ProductRead) # Path, param, response_model changed
def get_products_id(productId: int): # Renamed, param changed
    Session = sessionmaker(bind=engine)
    db = Session()
    product_record = db.query(Product).filter(Product.productId == productId).first() # Changed from User, userId. Variable 'product_record'
    db.close()
    if not product_record:
        raise HTTPException(status_code=404, detail="Producto no encontrado") # Message changed
    return product_record

@product.post('/products', status_code=HTTP_201_CREATED, response_model=ProductRead) # Path and response_model changed
def create_products(product_data: ProductCreate): # Renamed, param type changed. Variable 'product_data'
    Session = sessionmaker(bind=engine)
    session = Session()
    new_product = Product(**product_data.dict()) # Changed from User. Variable 'new_product'
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    session.close()
    return new_product

@product.delete('/products/{productId}', status_code=HTTP_204_NO_CONTENT) # Path and param changed
def delete_products_id(productId: int): # Renamed, param changed
    Session = sessionmaker(bind=engine)
    db = Session()
    product_to_delete = db.query(Product).filter(Product.productId == productId).first() # Changed from User, userId. Variable 'product_to_delete'
    if not product_to_delete:
        db.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado") # Message changed
    db.delete(product_to_delete)
    db.commit()
    db.close()
    return {"message": "Producto eliminado correctamente"} # Message changed

@product.put('/products/{productId}', status_code=HTTP_200_OK, response_model=ProductRead) # Path, param, response_model changed
def update_products(productId: int, product_update: ProductUpdate): # Renamed, params changed. Variable 'product_update'
    Session = sessionmaker(bind=engine)
    db = Session()
    product_record = db.query(Product).filter(Product.productId == productId).first() # Changed from User, userId. Variable 'product_record'
    if not product_record:
        db.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado") # Message changed
    
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(product_record, key, value)
    db.commit()
    db.refresh(product_record)
    db.close()
    return product_record

@product.get('/queryProductInfo', status_code=HTTP_200_OK) # Path changed from /queryTenant to match previous product route
def get_products_sales(): # Renamed from get_users_sales
    Session = sessionmaker(bind=engine)
    db = Session()
    data = db.query(
        Product.sku,
        Product.price,
        Product.stock,
        Product.description,
        Product.category,
        Product.brand,
        Product.isActive,   
        func.count(Product.productId) # Changed from User.userId
    ).group_by(Product.sku, Product.price, Product.stock, Product.description, Product.category, Product.brand, Product.isActive).all()
    db.close()
    return data
