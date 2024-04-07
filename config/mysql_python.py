import mysql.connector

def obtener_usuarios():
    # Establecer la conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="login"
    )
    
    # Crear el cursor para ejecutar consultas
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener los usuarios
    cursor.execute("SELECT user FROM users")
    usuarios = [usuario[0] for usuario in cursor.fetchall()]
    
    # Cerrar la conexión y retornar los usuarios
    conn.close()
    return usuarios


def agregar_usuario(usuario, contrasena):
    # Establecer la conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="login"
    )
    
    # Crear el cursor para ejecutar consultas
    cursor = conn.cursor()

    # Ejecutar la consulta para agregar el usuario
    sql = "INSERT INTO users (user, password) VALUES (%s, %s)"
    valores = (usuario, contrasena)
    cursor.execute(sql, valores)
    
    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def obtener_contrasena(usuario):
    # Establecer la conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="login"
    )
    
    # Crear el cursor para ejecutar consultas
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener la contraseña del usuario
    cursor.execute("SELECT password FROM users WHERE user = %s", (usuario,))
    resultado = cursor.fetchone()
    contrasena = resultado[0] if resultado else None
    
    # Cerrar la conexión y retornar la contraseña
    conn.close()
    return contrasena

def obtener_credenciales(usuario):
    # Establecer la conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="login"
    )
    
    # Crear el cursor para ejecutar consultas
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener las credenciales del usuario
    cursor.execute("SELECT user, password FROM users WHERE user = %s", (usuario,))
    resultado = cursor.fetchone()
    credenciales = resultado if resultado else None
    
    # Cerrar la conexión y retornar las credenciales
    conn.close()
    return credenciales