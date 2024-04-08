import sys, time, os, logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from mysql_python import *

# Configuración de registro
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

driver = None

import logging

def iniciar_sesion_instagram(usuario, contrasena):
    global driver
    try:
        logging.info("Iniciando sesión en Instagram...")
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

        logging.info("Inicio de sesión exitoso.")
        return True
    except WebDriverException as e:
        logging.error(f"Error al iniciar sesión: {e}")
        print("Error al iniciar sesión:", e)
        return False


class VentanaInicioSesion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión en Instagram")
        self.setFixedSize(700, 500)

        # Establecer un estilo global para los widgets
        self.estilo_global()

        # Obtener la lista de usuarios desde la base de datos
        self.usuarios = obtener_usuarios()

        # Widgets
        self.titulo_label = QLabel("Usuarios de Instagram para iniciar sesión y ver videos")
        font = QFont()  # Crear un objeto QFont
        font.setPointSize(20)  # Establecer el tamaño de la fuente
        self.titulo_label.setFont(font)
        self.imagen_label = QLabel()
        self.imagen_label.setFixedSize(100, 100)  # Establecer tamaño fijo para la imagen
        self.imagen_label.setScaledContents(True)  # Escalar el contenido de la imagen
        self.lista_usuarios = QListWidget()
        self.lista_usuarios.addItems(self.usuarios)
        self.iniciar_sesion_btn = QPushButton("Iniciar Sesión")
        self.agregar_usuario_btn = QPushButton("Agregar Usuario")
        self.editar_usuario_btn = QPushButton("Editar Usuario")
        self.eliminar_usuario_btn = QPushButton("Eliminar Usuario")

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.titulo_label, 0, 1, 1, 3)  
        layout.addWidget(self.imagen_label, 0, 0, 1, 1)  
        layout.addWidget(self.lista_usuarios, 2, 0, 1, 4) 
        layout.addWidget(self.iniciar_sesion_btn, 3, 0)  
        layout.addWidget(self.agregar_usuario_btn, 3, 1) 
        layout.addWidget(self.editar_usuario_btn, 3, 2)  
        layout.addWidget(self.eliminar_usuario_btn, 3, 3)  
        self.setLayout(layout)

        self.titulo_label.setWordWrap(True)  # Habilitar el ajuste de texto automático
        self.titulo_label.setAlignment(Qt.AlignCenter)

        # Conexiones de señal
        self.iniciar_sesion_btn.setStyleSheet("border-radius: 10px; border: 2px solid gray; background:silver; color:black; font: bold 14px; max-width: 10em ; min-width: 8em; padding: 6px;")
        self.iniciar_sesion_btn.clicked.connect(self.solicitar_contrasena)
        self.agregar_usuario_btn.setStyleSheet("border-radius: 10px; border: 2px solid gray; background:silver; color:black; font: bold 14px; max-width: 10em ; min-width: 8em; padding: 6px;")
        self.agregar_usuario_btn.clicked.connect(self.abrir_modal_agregar_usuario)
        self.eliminar_usuario_btn.setStyleSheet("border-radius: 10px; border: 2px solid gray; background:silver; color:black; font: bold 14px; max-width: 10em ; min-width: 8em; padding: 6px;")
        self.eliminar_usuario_btn.clicked.connect(self.eliminar_usuario_seleccionado)
        self.editar_usuario_btn.setStyleSheet("border-radius: 10px; border: 2px solid gray; background:silver; color:black; font: bold 14px; max-width: 10em ; min-width: 8em; padding: 6px;")
        self.editar_usuario_btn.clicked.connect(self.abrir_modal_editar_usuario)

        # Configurar la imagen desde el archivo local
        self.configurar_imagen_desde_archivo(r"C:\Users\esteb\OneDrive\Documentos\PruebaPython\config\Ins.png")

    def abrir_modal_editar_usuario(self):
        dialogo = DialogoAgregarEditarUsuario(tipo="editar")
        if dialogo.exec_() == QDialog.Accepted:
            usuario_actual = self.lista_usuarios.currentItem().text()
            nuevo_usuario = dialogo.usuario_line_edit.text()
            nueva_contrasena = dialogo.contrasena_line_edit.text()
            editar_usuario(usuario_actual, nuevo_usuario, nueva_contrasena)
            # Actualizar la lista de usuarios
            self.usuarios = obtener_usuarios()
            self.lista_usuarios.clear()
            self.lista_usuarios.addItems(self.usuarios)
            logging.info(f"Usuario '{usuario_actual}' editado correctamente.")

    def eliminar_usuario_seleccionado(self):
        usuario_seleccionado = self.lista_usuarios.currentItem().text()
        respuesta = QMessageBox.question(self, "Confirmar Eliminación", f"¿Estás seguro de eliminar al usuario {usuario_seleccionado}?", QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            eliminar_usuario(usuario_seleccionado)
            # Actualizar la lista de usuarios
            self.usuarios = obtener_usuarios()
            self.lista_usuarios.clear()
            self.lista_usuarios.addItems(self.usuarios)
            logging.info(f"Usuario '{usuario_seleccionado}' eliminado correctamente.")

    def estilo_global(self):
        # Establecer un estilo global para los widgets
        QApplication.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.WindowText, QColor(251, 56, 14))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(128, 128, 128))  # Color gris para los botones
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # Color blanco para el texto de los botones
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(251, 56, 14))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(palette)
        font = QApplication.font()
        font.setPointSize(15)
        QApplication.setFont(font)

    def configurar_imagen_desde_archivo(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.imagen_label.setPixmap(pixmap.scaledToWidth(100))  # Escalar la imagen al ancho deseado
        else:
            logging.error("Error: No se pudo cargar la imagen desde el archivo.")

    @pyqtSlot()
    def solicitar_contrasena(self):
        usuario_seleccionado = self.lista_usuarios.currentItem()
        if usuario_seleccionado is None:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un usuario para iniciar sesión.")
            logging.warning("No se seleccionó ningún usuario para iniciar sesión.")
            return

        usuario = usuario_seleccionado.text()
        # Obtener las credenciales correspondientes al usuario seleccionado
        credenciales = obtener_credenciales(usuario)
        if credenciales:
            usuario, contrasena = credenciales
            iniciar_sesion_instagram(usuario, contrasena)
        else:
            QMessageBox.warning(self, "Error", "No se encontraron credenciales para el usuario seleccionado.")
            logging.warning(f"No se encontraron credenciales para el usuario '{usuario}'.")

    def abrir_modal_agregar_usuario(self):
        dialogo = DialogoAgregarEditarUsuario(tipo="agregar")
        if dialogo.exec_() == QDialog.Accepted:
            usuario = dialogo.usuario_line_edit.text()
            contrasena = dialogo.contrasena_line_edit.text()
            agregar_usuario(usuario, contrasena)
            self.usuarios.append(usuario)
            self.lista_usuarios.addItem(usuario)
            logging.info(f"Usuario '{usuario}' agregado correctamente.")

    def closeEvent(self, event):
        # Verificar si driver está definida
        global driver
        if driver:
            driver.quit()
        event.accept()


class DialogoAgregarEditarUsuario(QDialog):
    def __init__(self, tipo="agregar"):
        super().__init__()
        self.setWindowTitle("Agregar Usuario" if tipo == "agregar" else "Editar Usuario")
        self.setGeometry(200, 200, 500, 200)

        # Widgets
        self.usuario_label = QLabel("Usuario:")
        self.usuario_line_edit = QLineEdit()
        self.contrasena_label = QLabel("Contraseña:")
        self.contrasena_line_edit = QLineEdit()
        self.contrasena_line_edit.setEchoMode(QLineEdit.Password)  # Ocultar la contraseña
        self.mostrar_contrasena_btn = QPushButton("Mostrar Contraseña")
        self.aceptar_btn = QPushButton("Aceptar")
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
        btn_layout.addWidget(self.aceptar_btn)
        btn_layout.addWidget(self.cancelar_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Conexiones de señal
        self.aceptar_btn.clicked.connect(self.accept)
        self.aceptar_btn.setStyleSheet("border-radius: 10px; border: 2px solid gray; background:silver; color:black; font: bold 14px; max-width: 10em ; min-width: 8em; padding: 6px;")
        self.cancelar_btn.clicked.connect(self.reject)
        self.cancelar_btn.setStyleSheet("border-radius: 10px; border: 2px solid gray; background:silver; color:black; font: bold 14px; max-width: 10em ; min-width: 8em; padding: 6px;")
        self.mostrar_contrasena_btn.clicked.connect(self.toggle_mostrar_contrasena)
        self.mostrar_contrasena_btn.setStyleSheet("border-radius: 10px; border: 2px solid gray; background:silver; color:black; font: bold 14px; max-width: 10em ; min-width: 8em; padding: 6px;")

    def toggle_mostrar_contrasena(self):
        if self.contrasena_line_edit.echoMode() == QLineEdit.Password:
            self.contrasena_line_edit.setEchoMode(QLineEdit.Normal)
            self.mostrar_contrasena_btn.setText("Ocultar Contraseña")
            self.mostrar_contrasena_btn.setStyleSheet("border-radius: 10px; border: 2px solid gray; background:silver; color:black; font: bold 14px; max-width: 10em ; min-width: 8em; padding: 6px;")
        else:
            self.contrasena_line_edit.setEchoMode(QLineEdit.Password)
            self.mostrar_contrasena_btn.setText("Mostrar Contraseña")
            self.mostrar_contrasena_btn.setStyleSheet("border-radius: 10px; border: 2px solid gray; background:silver; color:black; font: bold 14px; max-width: 10em ; min-width: 8em; padding: 6px;")


if __name__ == "__main__":
    # Crear la aplicación de PyQt
    app = QApplication(sys.argv)

    # Crear la ventana de inicio de sesión
    ventana = VentanaInicioSesion()
    ventana.show()

    # Ejecutar la aplicación
    sys.exit(app.exec_())
