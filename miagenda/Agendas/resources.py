"""
Definición de las rutas de la aplicación
"""

from flask import render_template, request, redirect, make_response


from core.utils import debug
from . import models as m

# Utils
def login_required(function):
    """
    Función decoradora para confirmar que un usuario está logueado
    """
    def check_login(*args, **kwargs):
        if 'token' not in request.cookies:
            return redirect(f'/login?next={request.path}')
        else:
            return function(*args, **kwargs)
    # Renaming the function name:
    check_login.__name__ = function.__name__
    return check_login


def not_login_required(function):
    """
    Función decoradora para confirmar que un usuario no está logueado
    """
    def check_not_login(*args, **kwargs):
        if 'loggedIn' in request.cookies or 'token' in request.cookies:
            return redirect('/miagenda')
        else:
            return function(*args, **kwargs)
    # Renaming the function name:
    check_not_login.__name__ = function.__name__
    return check_not_login

# Rutas base
# Index
def index(): return render_template('index.html')

# Guía rápida
def guide(): return render_template('guide.html')

# Acerca de
def about(): return render_template('about.html')

# Creditos
def credits(): return render_template('credits.html')

# Agendas
@login_required
def mi_agenda():
    """
    Ruta que redirige a la agenda del usuario
    """
    id = m.Sesion.query.filter(m.Sesion.token==request.cookies.get('token')).first().cuenta.agenda.id
    return redirect(f'/agenda/{id}')
  
def agenda(id):
    """
    Ruta que renderea la agenda del usuario
    """
    # TODO:
    # Agenda query
    # Buttons for update and share agenda 
    return render_template('agendas/agenda.html')

# Accounts
@not_login_required
def login():
    """
    Ruta que inicia sesión
    """
    if request.method=="GET" : # Si es un GET regresa la página de login
        return render_template('accounts/login.html')
    
    # Sino hace la logica de log in

    # Obtiene el parametro next (sirva para redirigir a la ruta que se quiere despues del login)
    next_ = request.args.get('next')
    if str(next_) != 'None':
        response = make_response(redirect(next_))
    else:
        response = make_response(redirect('/miagenda'))
    
    data = request.form
    cuenta = m.Cuenta.query.filter(m.Cuenta.correo==data['correo'], m.Cuenta.contraseña==data['contrasena']).first()
    if cuenta: # si todo fue correcto crea una sesión en la db
        sesion = m.Sesion('IPhone 8', cuenta)
        response.set_cookie('token', sesion.token)
        m.db.session.add(sesion)
        m.db.session.commit()
        return response
    # si hubo un error muestra el mensaje de error
    return render_template('accounts/login.html', error='Contraseña o correo inválidos')

@login_required
def logout():
    """
    Ruta para hacer log out
    """

    # Pide el token de la sesión y elimina la sesión de la db
    response = make_response(redirect('/login'))
    token = request.cookies.get('token') 
    sesion = m.Sesion.query.filter(m.Sesion.token==token).first()
    m.db.session.delete(sesion)
    m.db.session.commit()
    # elimina el token de la cookie
    response.set_cookie('token', '', expires=0)
    return response

@not_login_required
def signup():
    """
    Ruta que registra un usuario
    """
    if request.method=="GET" : # Si es un GET regresa la página de registro
        return render_template('accounts/signup.html')
    # sino hace la logica de registro
    data = request.form
    print(data)
    # TODO: Agregar constraint de unique a correo de Cuenta

    cuenta_aux = m.Cuenta.query.filter(m.Cuenta.correo == data['correo']).first()
    if cuenta_aux:
        return render_template('accounts/signup.html', error='Correo ya registrado')
    agenda = m.Agenda(f'Agenda de {data["correo"][:data["correo"].find("@")]}')
    cuenta = m.Cuenta(data['contrasena'],
                      data['correo'],
                      data['escuela'],
                      agenda,
                )
    # TODO: Agregar nombre del dispositivo (user-agent)
    sesion = m.Sesion('IPhone 8', cuenta)
    
    # Agrega a la base de datos la agenda la cuenta y la sesión
    for model in [agenda, cuenta, sesion]:
        m.db.session.add(model)
    
    m.db.session.commit()
    response = make_response(redirect('/gestionar_agenda'))
    # Crea una cookie con el token de la sesión
    response.set_cookie('token', sesion.token)
    return response

@login_required
def gestionar_agenda():
    """
    Ruta que muestra la gestión de la agenda del usuario
    """
    return render_template('agendas/gestionar_agenda.html')