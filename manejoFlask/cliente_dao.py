from conexion import Conexion
from cliente import Cliente

class ClienteDAO:
    SELECCIONAR = 'SELECT * FROM cliente ORDER BY id'
    SELECCIONAR_ID = 'SELECT * FROM cliente WHERE id=%s'
    INSERTAR = 'INSERT INTO cliente(nombre, apellido, membresia) VALUES(%s, %s, %s)'
    ACTUALIZAR = 'UPDATE cliente SET nombre=%s, apellido=%s, membresia=%s WHERE id=%s'
    ELIMINAR = 'DELETE FROM cliente WHERE id=%s'

    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR)
            registros = cursor.fetchall()
            clientes = []
            for registro in registros:
                cliente = Cliente(registro[0], registro[1], registro[2], registro[3])
                clientes.append(cliente)
            return clientes
        except Exception as e:
            print(f"Ocurrió un error al seleccionar los clientes: {e}")
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def seleccionar_por_id(cls, id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (id, )
            cursor.execute(cls.SELECCIONAR_ID, valores)
            registro = cursor.fetchone()
            cliente = Cliente(registro[0], registro[1], registro[2], registro[3])
            return cliente
        except Exception as e:
            print(f"Ocurrió un error al seleccionar un cliente por id: {e}")
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def insertar(cls, cliente):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.nombre, cliente.apellido, cliente.membresia)
            cursor.execute(cls.INSERTAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Ocurrió un error al insertar el cliente: {e}")
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def actualizar(cls, cliente):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.nombre, cliente.apellido, cliente.membresia, cliente.id)
            cursor.execute(cls.ACTUALIZAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Ocurrió un error al actualizar el cliente: {e}")
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def eliminar(cls, cliente):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.id,)
            cursor.execute(cls.ELIMINAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Ocurrió un error al eliminar el cliente: {e}")
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

if __name__ == "__main__":

    cliente1 = Cliente(nombre="Juan", apellido="Pérez", membresia=500)
    clientes_actualizados = ClienteDAO.insertar(cliente1)
    print(f"Clientes insertados: {clientes_actualizados}")
    clientes = ClienteDAO.seleccionar()
    for cliente in clientes:
        print(cliente)
