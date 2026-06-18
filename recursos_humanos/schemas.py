from extensions import ma, db
from marshmallow import fields, validate
from models import Empleado

class EmpleadoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Empleado
        load_instance = True 
        sqla_session = db.session

    idEmpleado = ma.auto_field(dump_only=True)
    nombre = ma.auto_field(required=True, validate=validate.Length(min=1, max=100))
    departamento = ma.auto_field(required=True, validate=validate.Length(min=1, max=100))
    #Guardamos DECIMAl en BD pero exponemos float en JSON para facilitar consumo
    sueldo = fields.Float(required=True, validate=validate.Range(min=0))

empleado_schema = EmpleadoSchema()
empleados_schema = EmpleadoSchema(many=True)




