import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error


class Conexion:
    DATABASE = "zona_fit_db"
    USERNAME = "root"
    PASSWORD = "root"
    DB_PORT = 3306
    HOST = "localhost"
    POOL_SIZE = 5
    POOL_NAME = "zona_fit_pool"
    POOL = None

    @classmethod
    def obtener_pool(cls):
        if cls.POOL is None:
            try:
                cls.POOL = pooling.MySQLConnectionPool(
                    pool_name=cls.POOL_NAME,
                    pool_size=cls.POOL_SIZE,
                    pool_reset_session=True,
                    host=cls.HOST,
                    port=cls.DB_PORT,
                    user=cls.USERNAME,
                    password=cls.PASSWORD,
                    database=cls.DATABASE,
                )
                print(f"Pool de conexiones '{cls.POOL_NAME}' creado con éxito.")
            except Error as e:
                print(f"Error al crear el pool de conexiones: {e}")
        return cls.POOL

    @classmethod
    def obtener_conexion(cls):
        return cls.obtener_pool().get_connection()

    @classmethod
    def liberar_conexion(cls, conexion):
        conexion.close()


if __name__ == "__main__":
    pool = Conexion.obtener_pool()
    print(pool)
    conexion1 = pool.get_connection()
    print(conexion1)
    Conexion.liberar_conexion(conexion1)
    print("Conexión liberada.")
