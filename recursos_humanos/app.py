from flask import Flask
from flask_cors import CORS

from extensions import db, migrate, ma
from api import bp as api_bp

import api.empleados
import models

def create_app():
    app = Flask(__name__)

    #ajusta usuario/contraseña/host segun el entorno
    app.config["SQLALCHEMY_DATABASE_URI"]=(
        "mysql+pymysql://root:root@localhost/recursos_humanos_db?charset=utf8mb4"

    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["JSON_AS_ASCII"]=False

    db.init_app(app)
    migrate.init_app(app,db)
    ma.init_app(app)

    CORS(app, resources={r"/api/*": {"origins":"*"}})

    app.register_blueprint(api_bp)

    @app.get("/")
    def home():
        return "API de recursos Humanos (Flask)"
    
    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=8080)




