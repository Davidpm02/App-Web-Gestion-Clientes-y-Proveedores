from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre:', validators=[ InputRequired() ])
    edad = StringField('Edad:', validators=[ InputRequired() ])
    email = StringField ('E-mail:', validators=[ InputRequired() ])
    contrasenia = PasswordField('Contraseña:', validators=[ InputRequired(), EqualTo('confirmar') ])
    confirmar = PasswordField('Confirmar Contraseña:', validators=[ InputRequired() ])

class LoginForm(FlaskForm):
    email = StringField ('E-mail:')
    contrasenia = PasswordField('Contraseña:')


class ProveedorRegisterForm(FlaskForm):
    nombre_empresa = StringField('Nombre Empresa:', validators=[ InputRequired() ])
    telefono = StringField('Telefono:', validators=[ InputRequired() ])
    direccion = StringField('Direccion:', validators=[ InputRequired() ])
    cif = StringField('CIF:', validators=[ InputRequired() ])
    email = StringField ('E-mail:', validators=[ InputRequired() ])
    contrasenia = PasswordField('Contraseña:', validators=[ InputRequired(), EqualTo('confirmar') ])
    confirmar = PasswordField('Confirmar Contraseña:', validators=[ InputRequired() ])
