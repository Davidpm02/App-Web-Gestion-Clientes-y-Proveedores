from flask import Flask, render_template, redirect, url_for, request, flash
from flask import send_from_directory
from flask_login import LoginManager, logout_user, login_required,login_user
from werkzeug.security import generate_password_hash

import time
import pygal
import json

import db as db

from models import Cliente, Proveedor, Admin
from forms import RegisterForm, LoginForm, ProveedorRegisterForm

import sqlite3

from datetime import datetime

import os



app = Flask(__name__) #En esta variable, almacenaremos nuestro servidor.

login_manager = LoginManager(app) 
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_ALGORITHM'] = 'HS256'

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)



                        # # # # # # #  # # # #  # # # # # REGISTRO DE USUARIOS # # # # # #  # # #  # # # #  # # # 
               
 # Registro Proveedor ----------------------              
               
@app.route('/registro-Proveedor')
def registro_proveedor():
    form = ProveedorRegisterForm()
    return render_template('registroProveedor.html',form=form)
@app.route('/registrar_proveedor', methods = ['GET','POST'])
def registrar_proveedor():
    form = ProveedorRegisterForm(meta = { 'csrf':False})

    if form.validate_on_submit():
        if db.session.query(Proveedor).filter_by(email=form.email.data).first():
            print('El correo introducido ya esta registrado.')
        else:
            proveedor = Proveedor(nombre_empresa = form.nombre_empresa.data,
                                  telefono = form.telefono.data,
                                  direccion = form.direccion.data,
                                  cif = form.cif.data,
                                  email = form.email.data,
                                  password_hash = generate_password_hash(form.contrasenia.data))
            db.session.add(proveedor)
            db.session.commit()
            print('Proveedor registrado!')
            
    return render_template('index_proveedor.html',form=form)               
                            
                        
# Pagina Login Proveedor --------------
@app.route('/index_proveedor', methods=['GET','POST'])
def index_proveedor():
    form = LoginForm()
    
    if form.validate_on_submit():
        proveedor = db.session.query(Proveedor).filter_by(email=form.email.data).first()
        if proveedor is not None and proveedor.check_password(form.contrasenia.data):
            login_user(proveedor,remember=True)
            next = request.args.get('next')
            return redirect(next or url_for('retorno-proveedor'))
        form.username.errors.append("Usuario o contraseña incorrectas.")
        
        
    return render_template('index_proveedor.html', form=form)


# Logeo Proveedor ---------------------
@app.route('/login_proveedor', methods=['GET','POST'])
def login_proveedor():
    
    form = LoginForm()
    print(form.errors)
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")
    print(form.errors)
        
    if form.validate_on_submit():
        proveedor = db.session.query(Proveedor).filter_by(email=form.email.data).first()
        print(proveedor)
        if proveedor is not None and proveedor.check_password(form.contrasenia.data):
            login_user(proveedor)
            return redirect(url_for('pagina_proveedor'))
            
        else:
            print("Usuario o contrasenia incorrectos.")
    return render_template('index_proveedor.html', form=form)
            
   
                          #----------------------------------------------------------------------------------#
   
# Registro Admin --------------------------------------

                         
@app.route('/registro-administrador')
def registro_administrador():
    form = RegisterForm()
    return render_template('registroAdministrador.html',form=form)

@app.route('/registrar_admin', methods=['GET','POST'])
def registrar_admin():
    
    form = RegisterForm(meta = { 'csrf':False})

    if form.validate_on_submit():
        if db.session.query(Admin).filter_by(email=form.email.data).first():
            print('El correo introducido ya esta registrado.')
        else:
            admin = Admin(nombre = form.nombre.data,
                          edad = form.edad.data,
                          email = form.email.data,
                          password_hash = generate_password_hash(form.contrasenia.data))
            db.session.add(admin)
            db.session.commit()
            print('Administrador registrado!')
            
                  
    return render_template('index_admin.html',form=form)
  
# Pagina login Admin --------------
@app.route('/index_admin', methods=['GET','POST'])
def index_admin():
    form = LoginForm()
    
    if form.validate_on_submit():
        admin = db.session.query(Admin).filter_by(email=form.email.data).first()
        if admin is not None and admin.check_password(form.contrasenia.data):
            login_user(admin)
            next = request.args.get('next')
            return redirect(next or url_for('pagina_admin'))
        form.username.errors.append("Usuario o contraseña incorrectas.")
        
    return render_template('index_admin.html', form=form)

# Logeo Admin ---------------------
@app.route('/login_admin', methods=['GET','POST'])
def login_admin():
    
    form = LoginForm()
    print(form.errors)
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")
    print(form.errors)
        
    if form.validate_on_submit():
        admin = db.session.query(Admin).filter_by(email=form.email.data).first()
        print(admin)
        if admin is not None and admin.check_password(form.contrasenia.data):
            login_user(admin)
            return redirect(url_for('pagina_admin'))
            
        else:
            print("Usuario o contrasenia incorrectos.")
    return render_template('index_admin.html', form=form)
      

                           #--------------------------------------------------------------------------------#

@app.route('/registro-Cliente')  # Esto me lleva a la pagina de registro
def registro_cliente():
    form = RegisterForm(meta = { 'csrf':False})
    
    return render_template('registroCliente.html',form=form)


@login_manager.user_loader
def load_user(cliente_id):
    return db.session.query(Cliente).get(cliente_id)


@app.route('/registrar_cliente', methods=['GET','POST'])   # Esto registra al cliente
def registrar_cliente():
    
    form = RegisterForm(meta = { 'csrf':False})

    if form.validate_on_submit():
        if db.session.query(Cliente).filter_by(email=form.email.data).first():
            print('El correo introducido ya esta registrado.')
        else:
            cliente = Cliente(nombre = form.nombre.data,
                              edad = form.edad.data,
                              email = form.email.data,
                              password_hash = generate_password_hash(form.contrasenia.data))
            db.session.add(cliente)
            db.session.commit()
            print("Cliente registrado!")
            
                  
    return render_template('index.html',form=form)




                                  ################################################################# 

@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    print(form.errors)
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")
    print(form.errors)
        
    if form.validate_on_submit():
        cliente = db.session.query(Cliente).filter_by(email=form.email.data).first()
        print(cliente)
        if cliente is not None and cliente.check_password(form.contrasenia.data):
            login_user(cliente)  
            return redirect(url_for('retornarCliente'))
            
        else:
            print("Usuario o contrasenia incorrectos.")
    return render_template('index.html', form=form)
          
      

          # # # # #  # # # # # # #  # ## # # #  # # # # # # #  # # # #  # # # # # #  # # # #  # # # #  # # # # # # # # # # # # # # 

# PAGINAS DE PRODUCTOS
@login_required
@app.route('/cliente-impresoras')
def pagina_impresoras():
    return render_template('impresoras.html')
@login_required
@app.route('/cliente-consolas')
def pagina_consolas():
    return render_template('consolas.html')
@login_required
@app.route('/cliente-arduinos')
def pagina_arduinos():
    return render_template('arduinos.html')
@login_required
@app.route('/cliente-raspberrys')
def pagina_raspberrys():
    return render_template('raspberrys.html')
@login_required

@app.route('/retorno-cliente')
def retornarCliente():
    
    crearJsonCliente()
    
    with open ('fichero_json/comprasCliente1.json','r') as bar_file:
        data = json.load(bar_file)
    chart = pygal.Bar()
    lista_compras = [x['TotalPrecio'] for x in data]
    [x['id'] for x in data]
    chart.add('Historial de compras',lista_compras)
    chart.x_labels = [x['id'] for x in data]
    chart.render_to_file('static/imagenes/graficoClientes.svg')
    img_url = 'static/imagenes/graficoClientes.svg?cache=' + str(time.time())
    
    
    return render_template('cliente.html', image_url=img_url)



# IMPRESORAS
@login_required
@app.route('/impresora1')
def go_to_impresora1():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=1 AND id=1'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    imp1 = cursor.execute(sql)
    
    return render_template('impresora_1.html', imp1 = imp1)
@login_required
@app.route('/impresora2')
def go_to_impresora2():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=1 AND id=2'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    imp2 = cursor.execute(sql)
    
    return render_template('impresora_2.html',imp2 = imp2)
@login_required
@app.route('/impresora3')
def go_to_impresora3():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=1 AND id=3'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    imp3 = cursor.execute(sql)
    
    return render_template('impresora_3.html', imp3 = imp3)
@login_required
@app.route('/impresora4')
def go_to_impresora4():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=1 AND id=4'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    imp4 = cursor.execute(sql)
    
    return render_template('impresora_4.html',imp4 = imp4)


# ARDUINOS
@login_required
@app.route('/arduinor3')
def go_to_arduinor3():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=2 AND id=5'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    ard1 = cursor.execute(sql)
    
    return render_template('arduino-r3.html', ard1 = ard1)
@login_required
@app.route('/arduino-leonardo')
def go_to_arduino_leonardo():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=2 AND id=6'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    ard2 = cursor.execute(sql)
    
    return render_template('arduino-leonardo.html', ard2 = ard2)
@login_required
@app.route('/arduino-due')
def go_to_arduino_due():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=2 AND id=7'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    ard3 = cursor.execute(sql)
    
    return render_template('arduino-due.html', ard3 = ard3)
@login_required
@app.route('/arduino-nano')
def go_to_arduino_nano():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=2 AND id=8'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    ard4 = cursor.execute(sql)
    return render_template('arduino-nano.html', ard4 = ard4)


# RASPBERRY PI's
@login_required
@app.route('/raspberry-pi1')
def go_to_raspberry_pi1():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=3 AND id=9'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    rasp1 = cursor.execute(sql)
    
    return render_template('raspberry-pi1.html', rasp1 = rasp1)
@login_required
@app.route('/raspberry-pi2')
def go_to_raspberry_pi2():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=3 AND id=10'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    rasp2 = cursor.execute(sql)
    
    return render_template('raspberry-pi2.html', rasp2 = rasp2)
@login_required
@app.route('/raspberry-pi3')
def go_to_raspberry_pi3():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=3 AND id=11'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    rasp3 = cursor.execute(sql)
    
    return render_template('raspberry-pi3.html', rasp3 = rasp3)
@login_required
@app.route('/raspberry-pi4')
def go_to_raspberry_pi4():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=3 AND id=12'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    rasp4 = cursor.execute(sql)
    
    return render_template('raspberry-pi4.html', rasp4 = rasp4)


# CONSOLAS 
@login_required
@app.route('/ps5')
def go_to_ps5():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=4 AND id=13'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    con1 = cursor.execute(sql)
    
    return render_template('ps5.html', con1 = con1)
@login_required
@app.route('/switch')
def go_to_switch():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=4 AND id=14'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    con2 = cursor.execute(sql)
    
    return render_template('switch.html', con2 = con2)
@login_required
@app.route('/xbox')
def go_to_xbox():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=4 AND id=15'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    con3 = cursor.execute(sql)
    
    return render_template('xbox.html', con3 = con3)
@login_required
@app.route('/steamdeck')
def go_to_steamdeck():
    
    sql = 'SELECT * FROM articulos WHERE CategoriaId=4 AND id=16'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    con4 = cursor.execute(sql)
    
    return render_template('steamdeck.html', con4 = con4)




# VUELTA A LAS PAGINAS DE ARTICULOS
@login_required
@app.route('/impresoras')
def go_to_impresoras():
    return render_template('impresoras.html')
@login_required
@app.route('/arduinos')
def go_to_arduinos():
    return render_template('arduinos.html')
@login_required
@app.route('/raspberrys')
def go_to_raspberrys():
    return render_template('raspberrys.html')
@login_required
@app.route('/consolas')
def go_to_consolas():
    return render_template('consolas.html')



# PEDIDOS PROVEEDORES
@login_required
@app.route('/pedidos_impresoras')
def pedidos_impresoras():
    return render_template('pedidos_impresoras.html')
@login_required
@app.route('/pedidos_arduinos')
def pedidos_arduinos():
    return render_template('pedidos_arduinos.html')
@login_required
@app.route('/pedidos_raspberrys')
def pedidos_raspberrys():
    return render_template('pedidos_raspberrys.html')
@login_required
@app.route('/pedidos_consolas')
def pedidos_consolas():
    return render_template('pedidos_consolas.html')


@login_required
@app.route('/retorno-proveedor')
def pagina_proveedor():
    
    crearJsonProveedorGanancias()
    crearJsonProveedorPerdidas()
    
    with open ('fichero_json/gananciasProveedor.json','r') as bar_file:
        data = json.load(bar_file)
    chart_ingresos = pygal.Bar()
    lista_ganancias = [x['TotalPrecio'] for x in data]
    [x['id'] for x in data]
    chart_ingresos.add('Registro de ingresos',lista_ganancias)
    chart_ingresos.x_labels = [x['id'] for x in data]
    chart_ingresos.render_to_file('static/imagenes/graficoGananciasProveedor.svg')
    img_url1 = 'static/imagenes/graficoGananciasProveedor.svg?cache=' + str(time.time())
    
    
    with open ('fichero_json/perdidasProveedor.json','r') as bar_file:
        data = json.load(bar_file)
    chart_perdidas = pygal.Bar()
    lista_ganancias = [x['TotalPrecio'] for x in data]
    [x['id'] for x in data]
    chart_perdidas.add('Registro de costes de Produccion',lista_ganancias)
    chart_perdidas.x_labels = [x['id'] for x in data]
    chart_perdidas.render_to_file('static/imagenes/graficoPerdidasProveedor.svg')
    img_url2 = 'static/imagenes/graficoPerdidasProveedor.svg?cache=' + str(time.time())
    
    return render_template('proveedor.html', ganancias_url = img_url1, perdidas_url = img_url2)
@login_required
@app.route('/retorno-admin')
def pagina_admin():
    
    return redirect(url_for('admin'))

#SOLICITUDES PEDIDOS ADMIN A PROVEEDOR   ------------------------------
@app.route('/solicitudes_proveedor', methods=['GET','POST'])
def solicitudes_proveedor():   
    sql = 'SELECT * FROM "solicitudes";'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    articulos = cursor.fetchall()
    conn.commit()
    
    sql = 'SELECT SUM(precio*Unidades) FROM solicitudes;'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    precio_total = cursor.fetchall()
    
    sql = 'SELECT SUM(coste_produccion*Unidades) FROM solicitudes;'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    coste_produccion = cursor.fetchall()
    
        
    return render_template('solicitudes_proveedor.html', articulos = articulos, precio_total = precio_total, coste_produccion = coste_produccion)

@app.route('/eliminar_solicitud_articulo/<int:id>')
def eliminar_solicitud_articulo(id): 
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM solicitudes WHERE id=?;', (id,))
    conn.commit()
    
    print("Solicitud de articulo borrada!")
    return redirect(url_for('solicitudes_proveedor'))


@app.route('/enviar_solicitud_articulo/<int:id>')
def enviar_solicitud_pedido(id):
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM solicitudes WHERE id=?', (id,))
    solicitud = cursor.fetchall()
    unidades = solicitud[0][6]
    cursor.execute('UPDATE articulos SET stock=stock+? WHERE id=?;',(unidades,id,))
    conn.commit()
    
    cursor.execute('SELECT * FROM solicitudes;')
    total_perdidas_admin = cursor.fetchall()
    cursor.execute('INSERT INTO perdidas_admin (id, PrecioTotal) VALUES (NULL, ?);',((total_perdidas_admin[0][2])*total_perdidas_admin[0][6],))
    conn.commit()
    
    cursor.execute('SELECT * FROM solicitudes;')
    total_ganancias_proveedor = cursor.fetchall()
    cursor.execute('INSERT INTO ganancias_proveedor (id, PrecioTotal) VALUES (NULL, ?);',((total_ganancias_proveedor[0][2])*total_ganancias_proveedor[0][6],))
    conn.commit()
    
    cursor.execute('SELECT * FROM solicitudes;')
    total_perdidas_proveedor = cursor.fetchall()
    cursor.execute('INSERT INTO perdidas_proveedor (id, PrecioTotal) VALUES (NULL, ?);',((total_perdidas_proveedor[0][3])*total_perdidas_proveedor[0][6],))
    conn.commit()
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM solicitudes WHERE id=?;', (id,))
    conn.commit()
    
    print('Solicitud de articulo aceptada y enviada!')
    return redirect(url_for('solicitudes_proveedor'))
    
    
    
    
    
    
    
    
    
















                          #-------------------------------------------------------------------------------#











@login_required
@app.route('/logout')
def logout():
    logout_user()
    
    sql = 'SELECT * FROM carrito;'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    
    articulos = cursor.fetchall()
    for item in articulos:
        conn = sqlite3.connect('database/mi_proyecto.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE articulos SET stock=stock+? WHERE nombre=?;',(item[5],item[1]))
        conn.commit()
        
    cursor.execute('DELETE FROM carrito;')
    conn.commit()
    
        
        
    return redirect('/')


@app.route('/home')
def retornarInicio():
    
    
    return redirect(url_for('home'))

@app.route('/')
def home():
    
    form = LoginForm()
      
    return render_template('index.html', form=form)







                                                    # FUNCIONES ADMINISTRADOR 

@app.route('/admin')
def admin():
    
    crearJsonAdminGanancias()
    crearJsonAdminPerdidas()
    
    with open ('fichero_json/gananciasAdmin.json','r') as bar_file:
        data = json.load(bar_file)
    chart_ingresos = pygal.Bar()
    lista_ganancias = [x['TotalPrecio'] for x in data]
    [x['id'] for x in data]
    chart_ingresos.add('Registro de ingresos',lista_ganancias)
    chart_ingresos.x_labels = [x['id'] for x in data]
    chart_ingresos.render_to_file('static/imagenes/graficoGananciasAdmin.svg')
    img_url1 = 'static/imagenes/graficoGananciasAdmin.svg?cache=' + str(time.time())
    
    
    with open ('fichero_json/perdidasAdmin.json','r') as bar_file:
        data = json.load(bar_file)
    chart_costes = pygal.Bar()
    lista_costes = [x['TotalPrecio'] for x in data]
    [x['id'] for x in data]
    chart_costes.add('Costes de Solicitudes',lista_costes)
    chart_costes.x_labels = [x['id'] for x in data]
    chart_costes.render_to_file('static/imagenes/graficoPerdidasAdmin.svg')
    img_url2 = 'static/imagenes/graficoPerdidasAdmin.svg?cache=' + str(time.time())
    
    return render_template('admin.html', ganancias_url = img_url1, perdidas_url = img_url2)

#Ir a Categorias.html
@login_required
@app.route('/categorias')
def categorias_inicio():
        
    sql = 'SELECT * FROM "categorias";'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    
    categorias = cursor.fetchall()
    conn.commit()
        
    return render_template('categorias/categorias.html', categorias=categorias)

# Crear Categorias -------------------------
@login_required
@app.route('/crearCategoria')
def crear_categoria():
    
    return render_template('categorias/categorias_crear.html')

@app.route('/store_categoria', methods=['POST'])
def storageCategoria():
    _nombre = request.form['txtNombre']
    
    
    if _nombre == '':
        flash('Recuerda llenar los datos de todos los campos.')
        return redirect(url_for('crear_categoria'))
    
    sql = 'INSERT INTO "categorias" ("id","nombre") VALUES (NULL,?);'
    datos_categoria = (_nombre,)
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql,datos_categoria)
    conn.commit()
    print('Categoria creada!')
    return redirect(url_for('categorias_inicio'))

# Eliminar Categorias ----------------------
@login_required
@app.route('/borrar_categoria/<int:id>')
def borrar_categoria(id):
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categorias WHERE id=?', (id,))
    conn.commit()
    print("Categoria borrada!")
    return redirect(url_for('categorias_inicio'))
    
# EDITAR CATEGORIA ----------------
@login_required
@app.route('/editar_categoria/<int:id>')
def editar_categoria(id):
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categorias WHERE id=?', (id,))
    categorias = cursor.fetchall()
    conn.commit()
    
    return render_template('categorias/categorias_editar.html',categorias=categorias)

@app.route('/actualizar_categoria', methods=['POST'])
def actualizar_categoria():
    
     _nombre = request.form['txtNombre']
     id = request.form['txtID']
     
     sql = 'UPDATE "categorias" SET "nombre"=? WHERE id=?;'
     datos_categoria = (_nombre,id,)
     conn = sqlite3.connect('database/mi_proyecto.db')
     cursor = conn.cursor()
     cursor.execute(sql,datos_categoria)
     conn.commit()
     print('Categoria editada!')
    
     return redirect(url_for('categorias_inicio'))
    
    

#Ir a Articulos.html
@login_required
@app.route('/articulos')
def articulos_inicio():
    
    sql = 'SELECT * FROM "articulos";'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    articulos = cursor.fetchall()
    conn.commit()
    
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    c = conn.cursor()
    c.execute('SELECT * FROM "articulos" WHERE stock<=9;')
    stockBajo = c.fetchall()
    print(stockBajo)
    if len(stockBajo) != 0:
        flash(r"""Hay articulos con stock al 90% o inferior.
                  Se recomienda pedir al proveedor.""","warning")
    else:
        pass
        
    return render_template('articulos/articulos.html',articulos=articulos)

#Crear Articulos --------------------------
@login_required
@app.route('/crearArticulo')
def crearArticulo():
    
    return render_template('articulos/articulos_crear.html')

@app.route('/store_articulo', methods=['POST'])
def storageArticulo():
    _nombre = request.form['txtNombre']
    _precio = request.form['txtPrecio']
    _iva = request.form['txtIva']
    _descripcion = request.form['txtDescripcion']
    _imagen = request.files['txtImage']
    _stock = request.form['txtStock']
    _categoriaId = request.form['txtCategoriaId']
    
    if _nombre == '' or _precio == '' or _iva == '' or _descripcion == '' or _imagen == '' or _stock == '' or _categoriaId == '':
        flash('Recuerda llenar los datos de todos los campos.')
        return redirect(url_for('crearArticulo'))
    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    
    if _imagen.filename !='':
        nuevoNombreFoto = tiempo+_imagen.filename # Creamos un nuevo nombre para la foto, que contiene la fecha actual al inicio,
        _imagen.save('uploads/'+nuevoNombreFoto)  # esto para evitar problemas si existen dos imagenes con el mismo nombre en 'uploads'.
    
    sql = 'INSERT INTO "articulos" ("id","nombre","precio","iva","descripcion","image","stock","CategoriaId") VALUES (NULL,?,?,?,?,?,?,?);'
    datos_articulo = (_nombre,_precio,_iva,_descripcion,nuevoNombreFoto,_stock,_categoriaId,)
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql,datos_articulo)
    conn.commit()
    print('Articulo creado!')
    return redirect(url_for('articulos_inicio'))

# ELIMINAR ARTICULO ------------------------
@login_required
@app.route('/borrar_articulo/<int:id>')
def borrar_articulo(id):
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT image FROM articulos WHERE id=?', (id,))
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    
    cursor.execute('DELETE FROM articulos WHERE id=?', (id,))
    conn.commit()
    print("Articulo borrado!")
    return redirect(url_for('articulos_inicio'))

# EDITAR ARTICULO ----------------
@login_required
@app.route('/editar_articulo/<int:id>')
def editar_articulo(id):
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articulos WHERE id=?', (id,))
    articulos = cursor.fetchall()
    conn.commit()
    
    return render_template('articulos/articulos_editar.html',articulos=articulos)

@app.route('/actualizar_articulo', methods=['POST'])
def actualizar_articulo():
    
    _nombre = request.form['txtNombre']
    _precio = request.form['txtPrecio']
    _iva = request.form['txtIva']
    _descripcion = request.form['txtDescripcion']
    _imagen = request.files['txtImage']
    _categoriaId = request.form['txtCategoriaId']
    id = request.form['txtID']
    
    sql = 'UPDATE "articulos" SET "nombre"=?, "precio"=? ,"iva"=? ,"descripcion"=? ,"CategoriaId"=? WHERE id=? ;'
    datos_articulo = (_nombre,_precio,_iva,_descripcion,_categoriaId,id)
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    
    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    
    if _imagen.filename !='':
        nuevoNombreFoto = tiempo+_imagen.filename # Creamos un nuevo nombre para la foto, que contiene la fecha actual al inicio,
        _imagen.save('uploads/'+nuevoNombreFoto)  # esto para evitar problemas si existen dos imagenes con el mismo nombre en 'uploads'.
    
        cursor.execute('SELECT image FROM articulos WHERE id=?', id)
        fila=cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute('UPDATE articulos SET image=? WHERE id=?',(nuevoNombreFoto,id,))
        conn.commit()
        
    cursor.execute(sql,datos_articulo)
    conn.commit()
    print("Articulo editado!")
    
    return redirect(url_for('articulos_inicio'))  
    
    
                           #-------------------------------------------------------------------------------#    
    
    
# CARRITO DE COMPRA

@app.route('/carrito')
def carrito_inicio():
    
    sql = 'SELECT * FROM "carrito";'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    articulos = cursor.fetchall()
    conn.commit()
    
    sql = 'SELECT SUM(precio*Unidades) FROM carrito;'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    precio_total = cursor.fetchall()
    
        
    return render_template('carrito.html', articulos=articulos, precio_total = precio_total)

@app.route('/agregar/<int:id>', methods=['GET','POST'])
def agregar_carrito(id):
    
    unidades = int(input('Cuantas unidades desea incluir en el carrito?'))
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articulos WHERE id=?;',(id,))
    articulos = cursor.fetchall()
    stock = articulos[0][6]
    if stock == 0:
        flash('No queda stock disponible del producto seleccionado({}).'.format(articulos[0][1]))
        cursor.execute('DELETE FROM carrito WHERE id=?;',(id,))
        conn.commit()
        redirect(url_for('carrito_inicio'))
    for item in articulos:
        cursor.execute('''INSERT INTO carrito (id, nombre, precio, descripcion, image, Unidades, PrecioTotal, CarritoId )
                          VALUES (? ,?, ?, ?, ?, ?, ?, ?) ;''',(item[0], item[1], item[2], item[4], item[5], unidades, item[2]*unidades, id,))
        conn.commit()
        print("Articulo aniadido al carrito!")
    if articulos!='':
        conn = sqlite3.connect('database/mi_proyecto.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE articulos SET stock=stock-? WHERE id=?;',(unidades,id,))
        conn.commit()
        
        return redirect(url_for('carrito_inicio'))

@app.route('/eliminar_articulo_pedido/<int:id>')
def eliminar_articulo_carrito(id): 
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM carrito WHERE id=?;',(id,))
    articulos = cursor.fetchall()
    unidades = articulos[0][5]
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carrito WHERE id=?', (id,))
    conn.commit()
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE articulos SET stock=stock+? WHERE id=?;',(unidades,id,))
    conn.commit()
    
    print("Articulo borrado del carrito!")
    return redirect(url_for('carrito_inicio'))

@app.route('/tramitarPedido', methods=['GET','POST'])
def tramitarPedido():
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM (PrecioTotal) FROM carrito;')
    total_carrito = cursor.fetchall()
    cursor.execute('INSERT INTO compras (id, PrecioTotal,ComprasId) VALUES (NULL, ?, NULL);',(total_carrito[0][0],))
    conn.commit()
    cursor.execute('INSERT INTO ganancias_admin (id, PrecioTotal) VALUES (NULL, ?);',(total_carrito[0][0],))
    conn.commit()
    
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM carrito;')
    total = cursor.fetchall()
    
    if len(total) == 0:
        flash("El carrito esta vacio.")
        redirect(url_for('carrito_inicio'))
    else:
        cursor.execute('DELETE FROM carrito;')
        conn.commit()
        print("Pedido realizado!")
        
    return redirect(url_for('carrito_inicio'))

    
    
        


           #----------------------------------------- FUNCIONES REPONER STOCK ---------------------------------------------#


    
    
@app.route('/solicitar_stock/<int:id>') #BOTON DE ADMIN
def solicitar_stock(id):
    
    unidades = int(input("Cuantas unidades desea solicitar?"))  
    sql = 'SELECT * FROM articulos WHERE id=?;'
    parametros = (id,)
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql,parametros)
    articulos = cursor.fetchall()
    stock = articulos[0][6]
    if stock == 10:
        flash('El articulo ya ha alcanzado la capacidad maxima en el almacen.')
    else:  
        conn = sqlite3.connect('database/mi_proyecto.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articulos WHERE id=?;',(id,))
        articulos = cursor.fetchall()
        for item in articulos:
            cursor.execute('''INSERT INTO solicitudes (id, nombre, precio, coste_produccion, descripcion, image, Unidades, SolicitudId )
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?) ;''',(item[0], item[1], item[8], item[9], item[4], item[5],unidades, id,))
            conn.commit()
            print("Solicitud enviada a proveedor!")
            
        nombres = 'SELECT nombre FROM articulos WHERE id=?;'
        parametros = (id,)
        conn = sqlite3.connect('database/mi_proyecto.db')
        cursor = conn.cursor()
        cursor.execute(nombres,parametros)
        nombre = cursor.fetchall()
        flash("Se ha enviado una solicitud de {} unidad/es del articulo {}.".format(unidades,nombre[0][0]))
    
    return redirect(url_for('pagina_admin'))

@app.route('/enviar stock/<int:id>')   # BOTON ENVIAR STOCK
def enviar_stock(id):
    
    unidades = int(input("Cuantas unidades desea enviar?"))
    sql = 'SELECT * FROM articulos WHERE id=?;'
    parametros = (id,)
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute(sql,parametros)
    articulos = cursor.fetchall()
    stock = articulos[0][6]
    if stock == 10:
        flash('El articulo ya ha alcanzado la capacidad maxima en el almacen.')
    else:
        sql = 'UPDATE articulos SET stock=stock+? WHERE id=?;'
        parametros = (unidades,id,)
        conn = sqlite3.connect('database/mi_proyecto.db')
        cursor = conn.cursor()
        cursor.execute(sql,parametros)
        conn.commit()
    
        nombres = 'SELECT * FROM articulos WHERE id=?;'
        parametros = (id,)
        conn = sqlite3.connect('database/mi_proyecto.db')
        cursor = conn.cursor()
        cursor.execute(nombres,parametros)
        nombre = cursor.fetchall()
        flash("Se han enviado {} unidades del articulo {}".format(unidades,nombre[0][1]))
        print("Se han enviado {} unidades del articulo {}".format(unidades,nombre[0][1]))
        conn.commit()
        
        cantidades = unidades
        conn = sqlite3.connect('database/mi_proyecto.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articulos WHERE id=?;',(id,))
        articulos = cursor.fetchall()
        precio_sin_iva = articulos[0][8]
        cursor.execute('INSERT INTO perdidas_admin (id, PrecioTotal) VALUES (NULL, ?);',(precio_sin_iva*cantidades,))
        conn.commit()
        
        conn = sqlite3.connect('database/mi_proyecto.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articulos WHERE id=?;',(id,))
        articulos = cursor.fetchall()
        precio_sin_iva = articulos[0][8]
        cursor.execute('INSERT INTO ganancias_proveedor (id, PrecioTotal) VALUES (NULL, ?);',(precio_sin_iva*cantidades,))
        conn.commit()
        
        conn = sqlite3.connect('database/mi_proyecto.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articulos WHERE id=?;',(id,))
        articulos = cursor.fetchall()
        precio_produccion = articulos[0][9]
        cursor.execute('INSERT INTO perdidas_proveedor (id, PrecioTotal) VALUES (NULL, ?);',(precio_produccion*cantidades,))
        conn.commit()
    
    return redirect(url_for('pagina_proveedor'))



# REPONER IMPRESORAS-----------------------

@app.route('/reponer_impresora1')
def reponer_impresora1():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=1 AND id=1'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    imp1 = cursor.execute(sql)
    
    return render_template('suministros/impresoras/suministrar_impresora1.html', imp1 = imp1)

@app.route('/reponer_impresora2')
def reponer_impresora2():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=1 AND id=2'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    imp2 = cursor.execute(sql)
    
    return render_template('suministros/impresoras/suministrar_impresora2.html', imp2 = imp2)

@app.route('/reponer_impresora3')
def reponer_impresora3():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=1 AND id=3'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    imp3 = cursor.execute(sql)
    
    return render_template('suministros/impresoras/suministrar_impresora3.html', imp3 = imp3)

@app.route('/reponer_impresora4')
def reponer_impresora4():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=1 AND id=4'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    imp4 = cursor.execute(sql)
    
    return render_template('suministros/impresoras/suministrar_impresora4.html', imp4 = imp4)



# REPONER ARDUINOS-----------------------

@app.route('/reponer_ard1')
def reponer_ard1():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=2 AND id=5'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    ard1 = cursor.execute(sql)
    
    return render_template('suministros/arduinos/suministrar_arduino1.html', ard1 = ard1)

@app.route('/reponer_ard2')
def reponer_ard2():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=2 AND id=6'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    ard2 = cursor.execute(sql)
    
    return render_template('suministros/arduinos/suministrar_arduino2.html', ard2 = ard2)

@app.route('/reponer_ard3')
def reponer_ard3():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=2 AND id=7'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    ard3 = cursor.execute(sql)
    
    return render_template('suministros/arduinos/suministrar_arduino3.html', ard3 = ard3)

@app.route('/reponer_ard4')
def reponer_ard4():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=2 AND id=8'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    ard4 = cursor.execute(sql)
    
    return render_template('suministros/arduinos/suministrar_arduino4.html', ard4 = ard4)


# REPONER RASPBERRY PIS-----------------------

@app.route('/reponer_rasp1')
def reponer_rasp1():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=3 AND id=9'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    rasp1 = cursor.execute(sql)
    
    return render_template('suministros/rasp_pi/suministrar_rasp1.html', rasp1 = rasp1)

@app.route('/reponer_rasp2')
def reponer_rasp2():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=3 AND id=10'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    rasp2 = cursor.execute(sql)
    
    return render_template('suministros/rasp_pi/suministrar_rasp2.html', rasp2 = rasp2)

@app.route('/reponer_rasp3')
def reponer_rasp3():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=3 AND id=11'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    rasp3 = cursor.execute(sql)
    
    return render_template('suministros/rasp_pi/suministrar_rasp3.html', rasp3 = rasp3)

@app.route('/reponer_rasp4')
def reponer_rasp4():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=3 AND id=12'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    rasp4 = cursor.execute(sql)
    
    return render_template('suministros/rasp_pi/suministrar_rasp4.html', rasp4 = rasp4)


# REPONER CONSOLAS-----------------------

@app.route('/reponer_con1')
def reponer_con1():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=4 AND id=13'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    con1 = cursor.execute(sql)
    
    return render_template('suministros/consolas/suministrar_con1.html', con1 = con1)

@app.route('/reponer_con2')
def reponer_con2():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=4 AND id=14'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    con2 = cursor.execute(sql)
    
    return render_template('suministros/consolas/suministrar_con2.html', con2 = con2)

@app.route('/reponer_con3')
def reponer_con3():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=4 AND id=15'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    con3 = cursor.execute(sql)
    
    return render_template('suministros/consolas/suministrar_con3.html', con3 = con3)

@app.route('/reponer_con4')
def reponer_con4():
    sql = 'SELECT * FROM articulos WHERE CategoriaId=4 AND id=16'
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    con4 = cursor.execute(sql)
    
    return render_template('suministros/consolas/suministrar_con4.html', con4 = con4)




                           #-------------------------------------------------------------------------------#    

# JSON PARA LA GRAFICA DE COMPRAS DEL CLIENTE  

def crearJsonCliente():  
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM compras;')
    comprasCliente = cursor.fetchall()
    conn.commit()
    
    compras = []
    for item in comprasCliente:
        compras.append(
            {
                "id":'Compra N{}'.format(item[0]),
                "TotalPrecio":item[1]
            })

    with open('fichero_json/comprasCliente1.json','w',encoding='utf-8') as archivo:
        json.dump(compras, archivo, ensure_ascii=False)
        
def crearJsonAdminGanancias():  
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ganancias_admin;')
    gananciasAdmin = cursor.fetchall()
    conn.commit()
    
    ventas = []
    for item in gananciasAdmin:
        ventas.append(
            {
                "id":'Ingreso N{}'.format(item[0]),
                "TotalPrecio":item[1]
            })

    with open('fichero_json/gananciasAdmin.json','w',encoding='utf-8') as archivo:
        json.dump(ventas, archivo, ensure_ascii=False)
        
def crearJsonAdminPerdidas():  
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM perdidas_admin;')
    perdidasAdmin = cursor.fetchall()
    conn.commit()
    
    costes = []
    for item in perdidasAdmin:
        costes.append(
            {
                "id":'Solicitud N{}'.format(item[0]),
                "TotalPrecio":item[1]
            })

    with open('fichero_json/perdidasAdmin.json','w',encoding='utf-8') as archivo:
        json.dump(costes, archivo, ensure_ascii=False)
        
        
def crearJsonProveedorGanancias():  
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ganancias_proveedor;')
    gananciasProveedor = cursor.fetchall()
    conn.commit()
    
    ganancias = []
    for item in gananciasProveedor:
        ganancias.append(
            {
                "id":'Solicitud N{}'.format(item[0]),
                "TotalPrecio":item[1]
            })

    with open('fichero_json/gananciasProveedor.json','w',encoding='utf-8') as archivo:
        json.dump(ganancias, archivo, ensure_ascii=False)
        
        
def crearJsonProveedorPerdidas():  
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM perdidas_proveedor;')
    perdidasProveedor = cursor.fetchall()
    conn.commit()
    
    perdidas = []
    for item in perdidasProveedor:
        perdidas.append(
            {
                "id":'Coste Produccion N{}'.format(item[0]),
                "TotalPrecio":item[1]
            })

    with open('fichero_json/perdidasProveedor.json','w',encoding='utf-8') as archivo:
        json.dump(perdidas, archivo, ensure_ascii=False)
        
        
      
      
      
      
# FUNCION ELIMINAR CLIENTE  
@app.route('/eliminar_perfil', methods=['GET', 'POST'])
def eliminar_perfil():
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM compras;')
    conn.commit()
    print('Compras restauradas!') # Compras de la tabla 'compras', que registra SOLO las compras de un cliente.
    
    cursor.execute('DELETE FROM carrito;')
    conn.commit()
    print('Carrito eliminado!')
    
    cursor.execute('DELETE FROM cliente;')
    conn.commit()
    print('Cliente eliminado!')

    return redirect(url_for('home'))  


# FUNCION ELIMINAR PROVEEDOR 
@app.route('/eliminar_perfil_proveedor', methods=['GET', 'POST'])
def eliminar_perfil_proveedor():
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM solicitudes;')
    conn.commit()
    print('Lista de solicitudes eliminada!')
    
    cursor.execute('DELETE FROM ganancias_proveedor;')
    conn.commit()
    print('Historial de ganancias del proveedor eliminado!')
    
    cursor.execute('DELETE FROM perdidas_proveedor;')
    conn.commit()
    print('Historias de gastos del proveedor eliminado!')
    
    cursor.execute('DELETE FROM proveedor;')
    conn.commit()
    print('Proveedor eliminado!')

    return redirect(url_for('home')) 


# FUNCION ELIMINAR ADMINISTRADOR
@app.route('/eliminar_perfil_administrador', methods=['GET', 'POST'])
def eliminar_perfil_administrador():
    
    conn = sqlite3.connect('database/mi_proyecto.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM solicitudes;') # Las solicitudes llegan al proveedor, pero como son pedidos realizados por 
    conn.commit()                              # el usuario admin que se esta eliminando, se eliminan las solicitudes tambien.
    print('Lista de solicitudes eliminada!')
    
    cursor.execute('DELETE FROM ganancias_admin;')
    conn.commit()
    print('Historial de ganancias del proveedor eliminado!')
    
    cursor.execute('DELETE FROM perdidas_admin;')
    conn.commit()
    print('Historias de gastos del proveedor eliminado!')
    
    cursor.execute('DELETE FROM admin;')
    conn.commit()
    print('Proveedor eliminado!')

    return redirect(url_for('home')) 
    
    

if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
    