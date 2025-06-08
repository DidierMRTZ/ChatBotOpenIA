from sqlalchemy import create_engine, MetaData, func
import os

# Configurar conexión a MySQL
# Usar el nombre del servicio de Docker para el host
db_host = os.environ.get('DB_HOST', 'db')  # Por defecto 'db' para Docker
DATABASE_URL = "mysql+pymysql://username:password@db:3306/nudges"
#DATABASE_URL = f"mysql+pymysql://username:password@db:3306/nudges" #para localhost 
engine = create_engine(DATABASE_URL)