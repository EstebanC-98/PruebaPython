import mysql.connector

# Función para establecer la conexión a la base de datos
def conectar_base_datos():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )

# Función para crear la base de datos si no existe
def crear_base_datos():
    try:
        conn = conectar_base_datos()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS login")
        conn.commit()
    except mysql.connector.Error as error:
        print("Error al crear la base de datos:", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Función para crear la tabla users si no existe
def crear_tabla_usuarios():
    try:
        conn = conectar_base_datos()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS login.users ( user VARCHAR(255), password VARCHAR(255))")
        conn.commit()
    except mysql.connector.Error as error:
        print("Error al crear la tabla de usuarios:", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Llamar a las funciones para crear la base de datos y la tabla si no existen
crear_base_datos()
crear_tabla_usuarios()

# Función para obtener todos los usuarios de la tabla users
def obtener_usuarios():
    try:
        conn = conectar_base_datos()
        cursor = conn.cursor()
        cursor.execute("SELECT user FROM users")
        usuarios = [usuario[0] for usuario in cursor.fetchall()]
        return usuarios
    except mysql.connector.Error as error:
        print("Error al obtener usuarios:", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def agregar_usuario(usuario, contrasena):
    try:
        conn = conectar_base_datos()
        cursor = conn.cursor()
        sql = "INSERT INTO users (user, password) VALUES (%s, %s)"
        valores = (usuario, contrasena)
        cursor.execute(sql, valores)
        conn.commit()
    except mysql.connector.Error as error:
        print("Error al agregar usuario:", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def verificar_contrasena(usuario, contrasena):
    try:
        conn = conectar_base_datos()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE user = %s", (usuario,))
        resultado = cursor.fetchone()
        contrasena_guardada = resultado[0] if resultado else None
        return contrasena == contrasena_guardada
    except mysql.connector.Error as error:
        print("Error al verificar contraseña:", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def obtener_credenciales(usuario):
    try:
        conn = conectar_base_datos()
        cursor = conn.cursor()
        cursor.execute("SELECT user, password FROM users WHERE user = %s", (usuario,))
        resultado = cursor.fetchone()
        credenciales = resultado if resultado else None
        return credenciales
    except mysql.connector.Error as error:
        print("Error al obtener credenciales:", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def editar_usuario(usuario_actual, nuevo_usuario, nueva_contrasena):
    try:
        conn = conectar_base_datos()
        cursor = conn.cursor()
        sql = "UPDATE users SET user = %s, password = %s WHERE user = %s"
        valores = (nuevo_usuario, nueva_contrasena, usuario_actual)
        cursor.execute(sql, valores)
        conn.commit()
    except mysql.connector.Error as error:
        print("Error al editar usuario:", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def eliminar_usuario(usuario):
    try:
        conn = conectar_base_datos()
        cursor = conn.cursor()
        sql = "DELETE FROM users WHERE user = %s"
        cursor.execute(sql, (usuario,))
        conn.commit()
    except mysql.connector.Error as error:
        print("Error al eliminar usuario:", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
