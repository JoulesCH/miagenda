from core.database import db

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


class Sesion(db.Model):
    __tablename__ = 'sesiones'

    id =  db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    dispositivo = db.Column(db.String)

    token = db.Column(db.String)

    cuenta_id = db.Column(db.BigInteger, db.ForeignKey('cuentas.id'))
    cuenta = db.relationship("Cuenta", backref=db.backref("sesion", uselist=False))
