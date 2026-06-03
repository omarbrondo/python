import mysql.connector

personas_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="personas_db"
)

#ejecutar la sentencia select

cursor = personas_db.cursor()
cursor.execute("SELECT * FROM personas")
resultado = cursor.fetchall()

print(resultado)

for fila in resultado:
    print(f"ID: {fila[0]}, Nombre: {fila[1]}, Apellido: {fila[2]}, Edad: {fila[3]}")

#cerrar la conexion
cursor.close()
personas_db.close()

