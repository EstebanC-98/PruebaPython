import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    #port = "3306",
    database = "login"
)
    
cursor = conn.cursor()
#cursor.execute("CREATE DATABASE login")


sql = """CREATE TABLE users (user VARCHAR (255), password VARCHAR(255))"""
cursor.execute(sql)
conn.commit()


cursor.execute("SHOW TABLES")

for dato in cursor:
    print(dato)

conn.close()