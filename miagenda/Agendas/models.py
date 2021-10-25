from core.database import db


class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)


class Agenda(db.Model):
    __tablename__ = 'agendas'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)


class Cuenta(db.Model):
    __tablename__ = 'cuentas'

    id =  db.Column(db.BigInteger, primary_key=True, autoincrement=True)


