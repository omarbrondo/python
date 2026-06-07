from flask import Flask, url_for
from flask import render_template
from flask import redirect
from flask import flash

from cliente_dao import ClienteDAO
from cliente import Cliente
from cliente_forma import ClienteForma

app = Flask(__name__)

app.config["SECRET_KEY"] = "llave_secreta_123"

titulo_app = "Zona Fit (GYM)"


@app.route("/")
@app.route("/index.html")
def inicio():
    app.logger.debug("Entramos al path de inicio /")

    # Recuperamos los clientes de la BBDD
    clientes_db = ClienteDAO.seleccionar()
    # Creamos un objeto de formulario de cliente vacio

    cliente = Cliente()
    cliente_forma = ClienteForma(obj=cliente)

    return render_template(
        "index.html", titulo=titulo_app, clientes=clientes_db, forma=cliente_forma
    )


@app.route("/guardar", methods=["POST"])
def guardar():
    # Creamos los objetos de cliente inicialmente objetos vacios
    cliente = Cliente()
    cliente_forma = ClienteForma(obj=cliente)

    # Validamos el formulario
    if cliente_forma.validate_on_submit():
        # Si el formulario es valido, recuperamos los datos del formulario
        cliente_forma.populate_obj(cliente)
        

        if not cliente.id:
            ClienteDAO.insertar(cliente)
            flash("Cliente agregado correctamente", "success")
        else:
            ClienteDAO.actualizar(cliente)
            flash("Cliente actualizado correctamente", "info")
    return redirect(url_for("inicio"))


@app.route("/limpiar")
def limpiar():
    return redirect(url_for("inicio"))


@app.route("/editar/<int:id>")
def editar(id):
    cliente = ClienteDAO.seleccionar_por_id(id)
    cliente_forma = ClienteForma(obj=cliente)
    # Revuperar el listado de clientes para volver a mostrarlo
    clientes_db = ClienteDAO.seleccionar()
    return render_template(
        "index.html", titulo=titulo_app, clientes=clientes_db, forma=cliente_forma
    )

@app.route("/eliminar/<int:id>")
def eliminar(id):
    cliente = Cliente(id=id)
    ClienteDAO.eliminar(cliente)
    flash("Cliente eliminado correctamente", "error")
    return redirect(url_for("inicio"))



if __name__ == "__main__":
    app.run(debug=True)
