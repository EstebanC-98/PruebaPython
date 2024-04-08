# PruebaPython
Descripción del Proyecto
El objetivo de este proyecto es desarrollar una aplicación de gestión de usuarios y contraseñas que interactúe con una base de datos MySQL
y permita iniciar sesión en Instagram utilizando Selenium.
----------------------------------------------------------------

Herramientas y Bibliotecas Utilizadas
Python
Versión: 3.8.5
Descripción: Python es un lenguaje de programación de alto nivel ampliamente utilizado en el desarrollo de aplicaciones web, scripts, automatización, entre otros.

XAMPP
Versión: 3.3.0
Descripción: XAMPP es un paquete de software gratuito y de código abierto que incluye los componentes necesarios para configurar un servidor web local. Incluye Apache, MySQL, PHP y Perl, lo que lo convierte en una opción popular para el desarrollo y la prueba de aplicaciones web en entornos locales.

MySQL Connector/Python
Versión: 8.0.23
Descripción: MySQL Connector/Python es un conector oficial de MySQL para Python que proporciona una interfaz para conectar aplicaciones Python con bases de datos MySQL.

Selenium
Versión: 3.141.0
Descripción: Selenium es una herramienta de automatización de pruebas web que permite interactuar con navegadores web de manera programática. 
Se utiliza en este proyecto para realizar el inicio de sesión en Instagram.

PyQt5
Versión: 5.15.4
Descripción: PyQt5 es una biblioteca de Python que proporciona un conjunto de herramientas para el desarrollo de interfaces gráficas de usuario (GUI) 
utilizando el framework Qt.

------------------------------------------------------------------


Estructura del Proyecto
index.py: Archivo principal que contiene la lógica de la aplicación y la interfaz gráfica de usuario utilizando PyQt5.
mysql_python.py: Archivo que contiene funciones para interactuar con la base de datos MySQL, incluyendo la conexión, consulta y manipulación de datos.
app.log: Archivo de registro donde se registran los eventos y errores de la aplicación.
config/Ins.png: Imagen utilizada en la interfaz de usuario.


----------------------------------------------------------------------

Instalación y Ejecución
Instalar las bibliotecas requeridas ejecutando pip install -r requirements.txt.
Ejecutar el archivo index.py para iniciar la aplicación.
