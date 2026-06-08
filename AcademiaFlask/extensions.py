from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instanciamos SQLAlchemy y Migrate
# Esto permite importarlos en otros archivos (como models.py) sin causar problemas.
db = SQLAlchemy()
migrate = Migrate()