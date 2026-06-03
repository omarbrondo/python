import mysql.connector

personas_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="personas_db"
)

cursor = personas_db.cursor()
sql = "DELETE FROM personas WHERE id = %s"
id_a_eliminar = input("Ingrese el ID de la persona a eliminar: ")
cursor.execute(sql, (id_a_eliminar,))
personas_db.commit()
print(f"Se ha eliminado el registro con ID: {id_a_eliminar}")
print(f"Filas afectadas: {cursor.rowcount}")    
cursor.close()
personas_db.close()