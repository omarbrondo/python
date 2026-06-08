from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired

class CursoForm(FlaskForm):
    nombre = StringField('Nombre del Curso', validators=[DataRequired(message="El nombre es obligatorio.")])
    instructor = StringField('Instructor', validators=[DataRequired(message="El instructor es obligatorio.")])
    duracion = DecimalField('Duración (Meses)', validators=[DataRequired(message="La duración es obligatoria.")])
    submit = SubmitField('Guardar Curso')