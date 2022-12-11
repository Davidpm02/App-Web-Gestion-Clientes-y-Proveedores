from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# El engine le permite a SQLAlquemy comunicarse con la base de datos.
# https://docs.sqlalchemy.org/en/14/core/engines.html
engine = create_engine('sqlite:///database/mi_proyecto.db',  connect_args={'check_same_thread': False})
# ADVERTENCIA:Crear el engine no conecta directamente con la base de datos,eso lo hacemos mas adelante



# Ahora creamos la sesion, lo que nos permite realizar transacciones (operaciones) dentro de nuestra BD.
Session = sessionmaker(bind=engine)
session = Session()



# Ahora vamos al fichero models.py y en los modelos (clases) donde queramos que se transformen en tablas
# le anadiremos esta variable, y esto se encargara de mapear y vincular la clase a la tabla.
Base = declarative_base()