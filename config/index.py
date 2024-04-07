from cProfile import label
import sys, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from mysql_python import obtener_usuarios, obtener_credenciales, agregar_usuario

driver = None

# Función para iniciar sesión en Instagram
def iniciar_sesion_instagram(usuario, contrasena):
    global driver
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.instagram.com")

        # Esperar a que el campo de usuario sea visible
        campo_usuario = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username")))
        # Esperar a que el campo de contraseña sea visible
        campo_contrasena = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "password")))

        # Ingresar el usuario y la contraseña
        campo_usuario.send_keys(usuario)
        campo_contrasena.send_keys(contrasena)

        # Hacer clic en el botón de inicio de sesión
        boton_inicio_sesion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"loginForm\"]/div/div[3]")))
        boton_inicio_sesion.click()

        
        # Esperar a que se haya iniciado sesión correctamente
        WebDriverWait(driver, 10).until(EC.url_contains("https://www.instagram.com/"))

        time.sleep(7)

        # Navegar a la página de reels
        driver.get("https://www.instagram.com/reels")


    except WebDriverException as e:
        print("Error al iniciar sesión:", e)
        # Aquí puedes manejar la excepción de acuerdo a tus necesidades


class VentanaInicioSesion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión en Instagram")
        self.setFixedSize(700,500)
        

        # Obtener la lista de usuarios desde la base de datos
        self.usuarios = obtener_usuarios()

        # Widgets
        self.usuario_label = QLabel("Usuarios:")
        self.lista_usuarios = QListWidget()
        self.lista_usuarios.addItems(self.usuarios)
        self.iniciar_sesion_btn = QPushButton("Iniciar Sesión")
        self.agregar_usuario_btn = QPushButton("Agregar Usuario")

        # Layout
        layout = QVBoxLayout()
    
        layout.addWidget(self.usuario_label)
        layout.addWidget(self.lista_usuarios)
        layout.addWidget(self.iniciar_sesion_btn)
        layout.addWidget(self.agregar_usuario_btn)
        self.setLayout(layout)

        # Conexiones de señal
        self.iniciar_sesion_btn.clicked.connect(self.solicitar_contrasena)
        self.agregar_usuario_btn.clicked.connect(self.abrir_modal_agregar_usuario)

    @pyqtSlot()
    def solicitar_contrasena(self):
        usuario_seleccionado = self.lista_usuarios.currentItem()
        if usuario_seleccionado is None:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un usuario para iniciar sesión.")
            return

        usuario = usuario_seleccionado.text()
        # Obtener las credenciales correspondientes al usuario seleccionado
        credenciales = obtener_credenciales(usuario)
        if credenciales:
            usuario, contrasena = credenciales
            iniciar_sesion_instagram(usuario, contrasena)
        else:
            QMessageBox.warning(self, "Error", "No se encontraron credenciales para el usuario seleccionado.")

    def abrir_modal_agregar_usuario(self):
        dialogo = DialogoAgregarUsuario()
        if dialogo.exec_() == QDialog.Accepted:
            usuario = dialogo.usuario_line_edit.text()
            contrasena = dialogo.contrasena_line_edit.text()
            agregar_usuario(usuario, contrasena)
            self.usuarios.append(usuario)
            self.lista_usuarios.addItem(usuario)

    def closeEvent(self, event):
        # Verificar si driver está definida
        global driver
        if driver:
            driver.quit()
        event.accept()

class DialogoAgregarUsuario(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Usuario")
        self.setGeometry(200, 200, 300, 100)

        # Widgets
        self.usuario_label = QLabel("Usuario:")
        self.usuario_line_edit = QLineEdit()
        self.contrasena_label = QLabel("Contraseña:")
        self.contrasena_line_edit = QLineEdit()
        self.contrasena_line_edit.setEchoMode(QLineEdit.Password)  # Ocultar la contraseña
        self.mostrar_contrasena_btn = QPushButton("Mostrar Contraseña")
        self.agregar_btn = QPushButton("Agregar")
        self.cancelar_btn = QPushButton("Cancelar")

        # Layout
        layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.usuario_label)
        form_layout.addWidget(self.usuario_line_edit)
        layout.addLayout(form_layout)
        form_layout2 = QHBoxLayout()
        form_layout2.addWidget(self.contrasena_label)
        form_layout2.addWidget(self.contrasena_line_edit)
        form_layout2.addWidget(self.mostrar_contrasena_btn)
        layout.addLayout(form_layout2)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.agregar_btn)
        btn_layout.addWidget(self.cancelar_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Conexiones de señal
        self.agregar_btn.clicked.connect(self.accept)
        self.cancelar_btn.clicked.connect(self.reject)
        self.mostrar_contrasena_btn.clicked.connect(self.toggle_mostrar_contrasena)

    def toggle_mostrar_contrasena(self):
        if self.contrasena_line_edit.echoMode() == QLineEdit.Password:
            self.contrasena_line_edit.setEchoMode(QLineEdit.Normal)
            self.mostrar_contrasena_btn.setText("Ocultar Contraseña")
        else:
            self.contrasena_line_edit.setEchoMode(QLineEdit.Password)
            self.mostrar_contrasena_btn.setText("Mostrar Contraseña")

if __name__ == "__main__":
    # Crear la aplicación de PyQt
    app = QApplication(sys.argv)

    # Crear la ventana de inicio de sesión
    ventana = VentanaInicioSesion()
    ventana.show()

    # Ejecutar la aplicación
    sys.exit(app.exec_())