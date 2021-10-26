# Builtin packages
import string
import random

from core.database import db

letters = string.ascii_lowercase + string.ascii_uppercase + string.digits

agenda_materia = db.Table('agenda_materia', db.Model.metadata,
                           db.Column('agenda_id', db.BigInteger, db.ForeignKey('agendas.id'), primary_key=True),
                           db.Column('materia_id', db.BigInteger, db.ForeignKey('materias.id'), primary_key=True),
                           )

class Agenda(db.Model):
    __tablename__ = 'agendas'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    nombre = db.Column(db.String)
    materias = db.relationship('Materia', secondary=agenda_materia, lazy='subquery',
                                 backref=db.backref('horario', lazy=True))
    def __init__(self, nombre):
        self.nombre = nombre

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    
    nombre = db.Column(db.String)
    color = db.Column(db.String)
    descripcion = db.Column(db.String)

    profesor = db.Column(db.String)
    enlaces = db.Column(db.JSON)
    horarios = db.relationship("Horario", backref="materia_horario", lazy='dynamic')

class Horario(db.Model):
    __tablename__ = 'horarios'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    inicio = db.Column(db.Float)
    final = db.Column(db.Float)
    duracion = db.Column(db.Float)
    dias = db.Column(db.String)

    materia_id = db.Column(db.BigInteger, db.ForeignKey('materias.id'))
    materia  = db.relationship('Materia')


# Usuarios
class Cuenta(db.Model):
    __tablename__ = 'cuentas'

    id =  db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    
    contraseña = db.Column(db.String)
    correo = db.Column(db.String)

    escuela = db.Column(db.String)

    agenda_id = db.Column(db.BigInteger, db.ForeignKey('agendas.id'))
    agenda = db.relationship("Agenda", backref=db.backref("cuenta", uselist=False))

    def __init__(self, contraseña, correo, escuela, agenda):
        self.contraseña = contraseña
        self.correo = correo
        self.escuela = escuela
        self.agenda = agenda # Agenda(f'Agenda de {correo[:correo.find("@")]}')
        self.agenda_id = self.agenda.id

class Sesion(db.Model):
    __tablename__ = 'sesiones'

    id =  db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    dispositivo = db.Column(db.String)

    token = db.Column(db.String)

    cuenta_id = db.Column(db.BigInteger, db.ForeignKey('cuentas.id'))
    cuenta = db.relationship("Cuenta", backref=db.backref("sesion", uselist=False))
    
    def __init__(self, dispositivo, cuenta):
        self.dispositivo = dispositivo
        self.cuenta = cuenta
        self.cuenta_id = self.cuenta.id
        self.token = ''.join(random.choice(letters) for i in range(10))
