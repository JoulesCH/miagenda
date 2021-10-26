from flask import render_template, request, redirect, make_response

from core.utils import debug
from . import models as m

# Utils
def login_required(function):
    def check_login(*args, **kwargs):
        if 'token' not in request.cookies:
            return redirect(f'/login?next={request.path}')
        else:
            return function(*args, **kwargs)
    # Renaming the function name:
    check_login.__name__ = function.__name__
    return check_login


def not_login_required(function):
    def check_not_login(*args, **kwargs):
        if 'loggedIn' in request.cookies or 'token' in request.cookies:
            return redirect('/miagenda/')
        else:
            return function(*args, **kwargs)
    # Renaming the function name:
    check_not_login.__name__ = function.__name__
    return check_not_login

# Base
def index(): return render_template('index.html')

def guide(): return render_template('guide.html')

def about(): return render_template('about.html')

def credits(): return render_template('credits.html')

# Agendas
@login_required
def mi_agenda():
    id = m.Sesion.query.filter(m.Sesion.token==request.cookies.get('token')).first().cuenta.agenda.id
    return redirect(f'/agenda/{id}')

def agenda(id):
    return 'Hola mundo'

# Accounts
@not_login_required
def login():
    if request.method=="GET" :
        return render_template('accounts/login.html')
    response = make_response(redirect('/miagenda'))
    
    data = request.form
    cuenta = m.Cuenta.query.filter(m.Cuenta.correo==data['correo'], m.Cuenta.contraseña==data['contrasena']).first()
    if cuenta:
        sesion = m.Sesion('IPhone 8', cuenta)
        response.set_cookie('token', sesion.token)
        m.db.session.add(sesion)
        m.db.session.commit()
        return response
    return render_template('accounts/login.html', error='Contraseña o correo inválidos')

@login_required
def logout():
    response = make_response(redirect('/login'))
    token = request.cookies.get('token') 
    sesion = m.Sesion.query.filter(m.Sesion.token==token).first()
    m.db.session.delete(sesion)
    m.db.session.commit()
    response.set_cookie('token', '', expires=0)
    return response

@not_login_required
def signup():
    if request.method=="GET" :
        return render_template('accounts/signup.html')
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

    for model in [agenda, cuenta, sesion]:
        m.db.session.add(model)
    
    m.db.session.commit()
    response = make_response(redirect('/miagenda'))
    response.set_cookie('token', sesion.token)
    return response