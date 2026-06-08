from extensions import db
from models import Curso

def obtener_todos():
    """Obtiene todos los cursos registrados en la base de datos."""
    return Curso.query.all()

def obtener_por_id(id_curso):
    """Busca un curso por su ID. Si no existe, devuelve un error 404."""
    return Curso.query.get_or_404(id_curso)

def agregar_curso(nombre, instructor, duracion):
    """Crea un nuevo curso y lo guarda en la base de datos."""
    nuevo_curso = Curso(nombre=nombre, instructor=instructor, duracion=duracion)
    db.session.add(nuevo_curso)
    db.session.commit()

def editar_curso(id_curso, nombre, instructor, duracion):
    """Actualiza los datos de un curso existente."""
    curso = obtener_por_id(id_curso)
    curso.nombre = nombre
    curso.instructor = instructor
    curso.duracion = duracion
    db.session.commit()

def eliminar_curso(id_curso):
    """Elimina un curso de la base de datos."""
    curso = obtener_por_id(id_curso)
    db.session.delete(curso)
    db.session.commit()