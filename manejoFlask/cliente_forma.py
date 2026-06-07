from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class ClienteForma(FlaskForm):
    id = HiddenField('id')
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    membresia = IntegerField('Membresia', validators=[DataRequired()])
    guardar = SubmitField('Guardar')

