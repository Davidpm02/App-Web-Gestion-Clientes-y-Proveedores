# Este archivo lo utilizaremos para crear las clases que necesitamos para nuestro proyecto.

from sqlalchemy.orm import relationship
from aem import con
import db as db
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, VARCHAR

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

"""Creamos la clase 'Producto'. Esta clase va a ser mapeada por SQLAlchemy y nos creara una tabla
   del mismo nombre en una base de datos. Cada objeto que creemos, se insertara en una de las
   filas de la tabla.
   
   args:
   -id_producto
   -nombre
   -precio
"""
        
        
class Cliente(db.Base, UserMixin):
    __tablename__ = 'cliente'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)  # Este valor no lo vamos a inicializar nosotros.Se creara de
    # manera automatica al crear cada objeto.
    nombre = Column(String(200), nullable=False)  # El parametro 'nullable' hace que la columna 'nombre'
    # de la tabla nunca pueda estar vacia o recibir como dato un None.
    edad = Column(Integer, nullable=False)
    email = Column (String, nullable=False)
    password_hash = Column(String(100), nullable=False)
    admin = Column(Boolean, default = False)
    proveedor = Column(Boolean, default = False)
    carrito = relationship('Carrito',backref='Cliente',lazy='dynamic')
    compras = relationship('ComprasRealizadas',backref='Cliente',lazy='dynamic')
    
    def __init__(self,nombre,edad,email,password_hash):
        self.nombre = nombre
        self.edad = edad
        self.email = email
        self.password_hash = password_hash
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password) 
    
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
        
            
    def __str__(self):
        return " {} --> {} --> {} --> Proveedor:{}".format(self.id,
                                                           self.nombre,
                                                           self.email,
                                                           self.proveedor)
        

class Proveedor(db.Base, UserMixin):
    __tablename__ = 'proveedor'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)  # Este valor no lo vamos a inicializar nosotros.Se creara de
    # manera automatica al crear cada objeto.
    nombre_empresa = Column(String(200), nullable=False)  # El parametro 'nullable' hace que la columna 'nombre'
    # de la tabla nunca pueda estar vacia o recibir como dato un None.
    telefono = Column(Integer, nullable=False)
    direccion = Column(String(200))
    cif = Column(String)
    email = Column (String, nullable=False)
    password_hash = Column(String(100), nullable=False)
    proveedor = Column(Boolean, default = True)
    admin = Column(Boolean, default = False)
    solicitudes = relationship('Solicitud',backref='Proveedor',lazy='dynamic')
    
    def __init__(self, nombre_empresa, telefono, direccion, cif, email, password_hash):
        self.nombre_empresa = nombre_empresa
        self.telefono = telefono
        self.direccion = direccion
        self.cif= cif
        self.email = email
        self.password_hash = password_hash
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)     
        
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
        
        
        
    def __str__(self):
        return "{} {} --> {} --> {} --> {}".format(self.id,
                                                   self.nombre_empresa,
                                                   self.telefono,
                                                   self.direccion,
                                                   self.cif)




class Admin(db.Base, UserMixin):
    __tablename__ = 'admin'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)  # Este valor no lo vamos a inicializar nosotros.Se creara de
    # manera automatica al crear cada objeto.
    nombre = Column(String(200), nullable=False)  # El parametro 'nullable' hace que la columna 'nombre'
    # de la tabla nunca pueda estar vacia o recibir como dato un None.
    edad = Column(Integer, nullable=False)
    email = Column (String, nullable=False)
    password_hash = Column(String(100), nullable=False)
    admin = Column(Boolean, default = True)
    
    def __init__(self,nombre,edad,email, password_hash):
        self.nombre = nombre
        self.edad = edad
        self.email = email
        self.password_hash = password_hash
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password) 
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
            
    def __str__(self):
        return " {} --> {} --> {} --> Admin:{}".format(self.id,
                                                       self.nombre,
                                                       self.email,
                                                       self.admin)








class Categorias(db.Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    articulos = relationship('Articulos',backref='Categorias',lazy='dynamic')

    
    def __init__(self,nombre):
        self.nombre = nombre
        
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))



    

""" La clase 'Articulos' representa cada un modelo para cada uno de los articulos que hay disponibles en nuestra web.

    args:
    - nombre
    - precio
    - iva
    - descripcion
    - image
    - stock
    - CategoriaId
    
    mtds:
    - precio_final
"""
class Articulos(db.Base):
    __tablename__ = 'articulos'
    id = Column(Integer, primary_key=True) # Este valor no lo vamos a inicializar nosotros.Se creara de
# manera automatica al crear cada objeto.
    nombre = Column(String(100),nullable=False) # El parametro 'nullable' hace que la columna 'nombre'
# de la tabla nunca pueda estar vacia o recibir como dato un None.
    precio = Column(Float,default=0)
    iva = Column(Integer,default=21)
    descripcion = Column(String)
    image = Column(VARCHAR(5000))
    stock = Column(Integer,default=0)
    CategoriaId = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    categoria = relationship('Categorias',backref='Articulos')
    precio_sin_iva = Column(Float,default=0)
    precio_produccion = Column(Float,default=0)
    
    def __init__(self,nombre,precio,descripcion,stock,CategoriaId):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.CategoriaId = CategoriaId
    

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
    

class Carrito(db.Base):
    __tablename__ = 'carrito'
    id = Column(Integer, primary_key=True) # Este valor no lo vamos a inicializar nosotros.Se creara de
# manera automatica al crear cada objeto.
    nombre = Column(String(100),nullable=False) # El parametro 'nullable' hace que la columna 'nombre'
# de la tabla nunca pueda estar vacia o recibir como dato un None.
    precio = Column(Float,default=0)
    descripcion = Column(String)
    image = Column(VARCHAR(5000))
    Unidades = Column(Integer, default=1)
    PrecioTotal = Column(Float,default=0)
    CarritoId = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    cliente = relationship('Cliente',backref='Carrito')
    
    def __init__(self,nombre,precio,descripcion,CarritoId):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.CarritoId = CarritoId
        
        
        
class Solicitud(db.Base):
    __tablename__ = 'solicitudes'
    id = Column(Integer, primary_key=True) # Este valor no lo vamos a inicializar nosotros.Se creara de
# manera automatica al crear cada objeto.
    nombre = Column(String(100),nullable=False) # El parametro 'nullable' hace que la columna 'nombre'
# de la tabla nunca pueda estar vacia o recibir como dato un None.
    precio = Column(Float,default=0)
    coste_produccion = Column(Float,default=0)
    descripcion = Column(String)
    image = Column(VARCHAR(5000))
    Unidades = Column(Integer, default=1)
    SolicitudId = Column(Integer, ForeignKey('proveedor.id'), nullable=False)
    proveedor = relationship('Proveedor',backref='Solicitud')
    
    def __init__(self,nombre,precio,descripcion,SolicitudId):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.SolicitudId = SolicitudId


class ComprasRealizadas(db.Base):
    __tablename__ = 'compras'
    id = Column(Integer, primary_key=True)
    PrecioTotal = Column(Float,default=0)
    ComprasId = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship('Cliente',backref='ComprasRealizadas')
    
    def __init__(self,PrecioTotal):
        self.PrecioTotal = PrecioTotal
        
        
class GananciasAdmin(db.Base):
    __tablename__ = 'ganancias_admin'
    id = Column(Integer, primary_key=True)
    PrecioTotal = Column(Float,default=0)
    
    
    def __init__(self,PrecioTotal):
        self.PrecioTotal = PrecioTotal
        

class PerdidasAdmin(db.Base):
    __tablename__ = 'perdidas_admin'
    id = Column(Integer, primary_key=True)
    PrecioTotal = Column(Float,default=0)
    
    
    def __init__(self,PrecioTotal):
        self.PrecioTotal = PrecioTotal
        
        
class GananciasProveedor(db.Base):
    __tablename__ = 'ganancias_proveedor'
    id = Column(Integer, primary_key=True)
    PrecioTotal = Column(Float,default=0)
    
    
    def __init__(self,PrecioTotal):
        self.PrecioTotal = PrecioTotal
        
        
class PerdidasProveedor(db.Base):
    __tablename__ = 'perdidas_proveedor'
    id = Column(Integer, primary_key=True)
    PrecioTotal = Column(Float,default=0)
    
    
    def __init__(self,PrecioTotal):
        self.PrecioTotal = PrecioTotal