from extensions import db
from sqlalchemy import Numeric

class Empleado(db.Model):
    __tablename__ = "empleado"

    idEmpleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(100), nullable=False)
    sueldo = db.Column(Numeric(10,2), nullable=False)

    def __repr__(self) -> str:
        return f"<Empleado {self.idEmpleado} - {self.nombre}>"