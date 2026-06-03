import mysql.connector

personas_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="personas_db"
)

#ejecutar la sentencia insert
cursor = personas_db.cursor()
sql = "INSERT INTO personas (nombre, apellido, edad) VALUES (%s, %s, %s)"
valores = ("Omar", "Brondo", 30)

cursor.execute(sql, valores)
personas_db.commit()

print(f"Se ha insertado un nuevo registro con ID: {cursor.lastrowid}")
print(f"Filas afectadas: {cursor.rowcount}")
print(f"Valores: {valores}")
cursor.close()
personas_db.close()