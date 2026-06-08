import os
from flask import Flask, render_template, redirect, url_for, flash
from dotenv import load_dotenv
from extensions import db, migrate
import models

# Importamos las funciones de la capa de servicios
from services.curso_service import obtener_todos, agregar_curso, obtener_por_id, editar_curso, eliminar_curso
# Importamos nuestro formulario
from forms import CursoForm

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Construir la cadena de conexión a MySQL
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones con la app
db.init_app(app)
migrate.init_app(app, db)

# Ruta principal que renderiza el index
@app.route('/')
def index():
    cursos = obtener_todos()
    return render_template('index.html', cursos=cursos)

# Ruta para agregar un nuevo curso
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    form = CursoForm()
    if form.validate_on_submit():
        agregar_curso(form.nombre.data, form.instructor.data, form.duracion.data)
        flash('Curso agregado exitosamente.', 'success')
        return redirect(url_for('index'))
    
    return render_template('agregar_curso.html', form=form)

# Ruta para editar un curso existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    curso = obtener_por_id(id)
    form = CursoForm(obj=curso)
    
    if form.validate_on_submit():
        editar_curso(id, form.nombre.data, form.instructor.data, form.duracion.data)
        flash('Curso actualizado exitosamente.', 'success')
        return redirect(url_for('index'))
    
    return render_template('editar_curso.html', form=form, curso=curso)

# Ruta para eliminar un curso (Solo acepta POST por seguridad)
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminar_curso(id)
    flash('Curso eliminado exitosamente.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()