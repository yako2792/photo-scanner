import cv2
import serial
import time
import json
import os
from .webcam_driver import webcam_driver
from .custom_dropdown import custom_dropdown
from .custom_switch import custom_switch
from .custom_input import custom_input
from .custom_slider import custom_slider
from .custom_file_browser import custom_file_browser
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class SerialWorker(QThread):
    image_captured = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, ser, serial_array, capture_images_callback):
        super().__init__()
        self.ser = ser
        self.serial_array = serial_array
        self.capture_images_callback = capture_images_callback
        self.is_running = True

    def run(self):
        message = str(self.serial_array[0]) + "," + str(self.serial_array[1]) + "\n"
        print(f"Sending message to Arduino: {message.encode()}")
        self.ser.write(message.encode())

        buffer = ''
        pictures = 0
        while self.is_running and pictures < self.serial_array[1]:
            data = self.ser.read(self.ser.in_waiting or 1)
            if data:
                buffer += data.decode(errors='ignore')
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if line:
                        print(f"Received from Arduino: {line}")
                        if line == '1':
                            pictures += 1
                            self.capture_images_callback(pictures)
                            self.image_captured.emit(pictures)
                            print(f"Picture {pictures} taken")
            else:
                QThread.msleep(100)  # Esperar 100 ms para reducir uso de CPU
        self.finished.emit()


class window_driver(QMainWindow):
    def __init__(self):
        """
        Initialize window driver with window title.
        """
        super().__init__()

        # Cargar configuración desde puertos.conf
        self.load_configuration()

        # Cargar configuración principal desde main.conf
        self.load_main_configuration()

        # Camera settings
        self.selected_camera = self.main_config.get('selected_camera', 0)
        self.camera0_index = int(self.config.get('camera_1', 0))
        self.camera1_index = int(self.config.get('camera_2', 1))
        self.camera2_index = int(self.config.get('camera_3', 2))
        self.fps = 15

        # Live preview siempre activo
        self.preview = True

        # Serial message
        selected_port = self.config.get('selected_port', 'COM3')
        self.ser = serial.Serial(selected_port, 9600, timeout=0)  # Establecer timeout=0 para modo no bloqueante
        self.capture_frequency = 0
        self.degrees_movement = 0
        self.serial_array = [0, 0]

        # Setup app
        self.setup_window()
        self.setup_layout()
        self.add_video_options()
        self.add_rotation_options()
        self.add_zoom_options()
        self.add_camera_view()
        self.load_stylesheet('style.qss')

        # Establecer valores desde main.conf
        self.apply_main_configuration()

    def load_configuration(self):
        """
        Load configuration from puertos.conf file.
        """
        try:
            with open('puertos.conf', 'r') as conf_file:
                self.config = json.load(conf_file)
        except FileNotFoundError:
            print("Configuration file puertos.conf not found. Using default settings.")
            self.config = {}
        except json.JSONDecodeError:
            print("Error decoding puertos.conf. Using default settings.")
            self.config = {}

    def load_main_configuration(self):
        """
        Load main configuration from main.conf file.
        If it doesn't exist, create it with default values.
        """
        if os.path.exists('main.conf'):
            try:
                with open('main.conf', 'r') as conf_file:
                    self.main_config = json.load(conf_file)
            except json.JSONDecodeError:
                print("Error decoding main.conf. Using default settings.")
                self.main_config = {}
        else:
            print("main.conf not found. Creating default configuration.")
            # Default configuration
            self.main_config = {
                'selected_camera': 0,
                'camera_settings': {
                    '0': {
                        'brightness': 50,
                        'contrast': 10.0,
                        'hue': 0,
                        'saturation': 10.0,
                        'gain': 0,
                        'exposure': -6
                    },
                    '1': {
                        'brightness': 50,
                        'contrast': 10.0,
                        'hue': 0,
                        'saturation': 10.0,
                        'gain': 0,
                        'exposure': -6
                    },
                    '2': {
                        'brightness': 50,
                        'contrast': 10.0,
                        'hue': 0,
                        'saturation': 10.0,
                        'gain': 0,
                        'exposure': -6
                    }
                },
                'save_folder': 'src\\test-images',
                'file_name': '',
                'live_preview': True,  # Siempre activo
                'capture_frequency': 0,
                'degrees_movement': 0
            }
            self.save_main_configuration()

    def save_main_configuration(self):
        """
        Save current configuration to main.conf file.
        """
        with open('main.conf', 'w') as conf_file:
            json.dump(self.main_config, conf_file, indent=4)

    # Setup window and layout
    def setup_window(self, geometry=(800, 600), title="Photo Scanner"):
        """
        Setup window size and title.
        :param geometry: Size of window ((800,600) by default).
        :param title: Title of window ("Untitled" by default).
        """
        self.setWindowTitle(title)
        # Habilitar redimensionamiento de la ventana
        self.setMinimumSize(800, 600)
        self.resize(800, 600)
        self.setStyleSheet("background-color: #d6d0d4")

        # Deshabilitar el botón de cerrar
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        # Crear el widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Establecer fuente global
        font = QFont()
        font.setPointSize(15)
        self.setFont(font)

    def setup_layout(self):
        """
        Create initial layout content in window.
        """
        # Crear el layout principal
        self.main_vertical_layout = QVBoxLayout(self.central_widget)
        self.main_vertical_layout.setContentsMargins(10, 10, 10, 10)
        self.main_vertical_layout.setSpacing(10)

        # Crear el layout horizontal principal
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.main_vertical_layout.addLayout(self.main_layout)

        # Añadir los layouts de columnas
        self.setup_left_column()
        self.setup_right_column()

        # Añadir el botón "Guardar y Cerrar"
        self.save_close_button = QPushButton("Guardar y Cerrar")
        self.save_close_button.setObjectName("saveCloseButton")
        self.save_close_button.clicked.connect(self.on_save_and_close)
        self.save_close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.main_vertical_layout.addWidget(self.save_close_button, alignment=Qt.AlignRight)

    def setup_left_column(self):
        """
        Create left column in layout.
        """
        # Left column
        self.left_column = QVBoxLayout()
        self.left_column.setContentsMargins(10, 10, 10, 10)
        self.left_column.setSpacing(10)
        self.main_layout.addLayout(self.left_column, 1)

        ## Left upper box
        self.left_top_box = QWidget()
        # Eliminar tamaño fijo
        self.left_top_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.left_top_box.setStyleSheet("background-color: lightblue;")

        self.left_top_layout = QVBoxLayout(self.left_top_box)
        self.left_top_layout.setContentsMargins(25, 25, 25, 25)
        self.left_top_layout.setSpacing(10)
        self.left_top_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.left_top_title = QLabel("Process video options")
        self.left_top_title.setFont(QFont(self.font().family(), 15, QFont.Bold))
        self.left_top_layout.addWidget(self.left_top_title)

        self.left_column.addWidget(self.left_top_box)

        ## Left bottom box
        self.left_bottom_box = QWidget()
        self.left_bottom_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.left_bottom_box.setStyleSheet("background-color: blue;")

        self.left_bottom_layout = QVBoxLayout(self.left_bottom_box)
        self.left_bottom_layout.setContentsMargins(25, 25, 25, 25)
        self.left_bottom_layout.setSpacing(10)
        self.left_bottom_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.left_bottom_title = QLabel("Rotation option")
        self.left_bottom_title.setFont(QFont(self.font().family(), 15, QFont.Bold))
        self.left_bottom_layout.addWidget(self.left_bottom_title)

        self.left_column.addWidget(self.left_bottom_box)

    def setup_right_column(self):
        """
        Create right column in layout.
        """
        # Right column
        self.right_column = QVBoxLayout()
        self.right_column.setContentsMargins(10, 10, 10, 10)
        self.right_column.setSpacing(10)
        self.main_layout.addLayout(self.right_column, 2)

        ## Right top box
        self.right_top_box = QWidget()
        self.right_top_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_top_box.setStyleSheet("background-color: black;")

        self.right_top_layout = QVBoxLayout(self.right_top_box)
        self.right_top_layout.setContentsMargins(0, 0, 0, 0)
        self.right_top_layout.setSpacing(0)
        self.right_top_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.right_column.addWidget(self.right_top_box)

        ## Right bottom box
        self.right_bottom_box = QWidget()
        self.right_bottom_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.right_bottom_box.setStyleSheet("background-color: lightblue;")

        self.right_bottom_layout = QVBoxLayout(self.right_bottom_box)
        self.right_bottom_layout.setContentsMargins(25, 25, 25, 25)
        self.right_bottom_layout.setSpacing(10)
        self.right_bottom_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.right_bottom_title = QLabel("Camera control options")
        self.right_bottom_title.setFont(QFont(self.font().family(), 15, QFont.Bold))
        self.right_bottom_layout.addWidget(self.right_bottom_title)

        self.right_column.addWidget(self.right_bottom_box)

    # Add elements to layout
    def add_video_options(self):
        self.brightness_slider = custom_slider("Brightness")
        self.contrast_slider = custom_slider("Contrast")
        self.hue_slider = custom_slider("HUE")
        self.saturation_slider = custom_slider("Saturation")

        self.left_top_layout.addWidget(self.brightness_slider)
        self.left_top_layout.addWidget(self.contrast_slider)
        self.left_top_layout.addWidget(self.hue_slider)
        self.left_top_layout.addWidget(self.saturation_slider)

        # Set custom minimum and maximum values
        self.brightness_slider.set_min_max_values(0, 100)
        self.contrast_slider.set_min_max_values(0, 30)
        self.hue_slider.set_min_max_values(0, 100)
        self.saturation_slider.set_min_max_values(0, 30)

        # Set default values
        self.brightness_slider.slider.setValue(0)
        self.contrast_slider.slider.setValue(10)
        self.hue_slider.slider.setValue(0)
        self.saturation_slider.slider.setValue(10)

        self.brightness_slider.slider.valueChanged.connect(self.on_brightness_changed)
        self.contrast_slider.slider.valueChanged.connect(self.on_contrast_changed)
        self.hue_slider.slider.valueChanged.connect(self.on_hue_changed)
        self.saturation_slider.slider.valueChanged.connect(self.on_saturation_changed)

    def add_rotation_options(self):
        self.frequency_input = custom_dropdown("Frequency", "Capture interval.")
        self.degrees_input = custom_dropdown("Degrees", "Rotation degrees.")
        self.file_name_input = custom_input("ID", "Part number.")
        self.path_input = custom_file_browser("Path", "Browse")

        # Botón "Start" deshabilitado por defecto
        self.start_button = QPushButton()
        self.start_button.setText("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setEnabled(False)

        # Setup dropdown content
        self.frequency_input.add_item("Select")
        self.frequency_input.add_item("5 Degs")
        self.frequency_input.add_item("10 Degs")
        self.frequency_input.add_item("15 Degs")
        self.frequency_input.add_item("25 Degs")

        self.degrees_input.dropdown.setEnabled(False)
        self.degrees_input.add_item("Select")
        self.degrees_input.add_item("45 Degs")
        self.degrees_input.add_item("90 Degs")
        self.degrees_input.add_item("180 Degs")
        self.degrees_input.add_item("360 Degs")

        self.left_bottom_layout.addWidget(self.frequency_input)
        self.left_bottom_layout.addWidget(self.degrees_input)
        self.left_bottom_layout.addWidget(self.file_name_input)
        self.left_bottom_layout.addWidget(self.path_input)
        self.left_bottom_layout.addWidget(self.start_button)

        self.frequency_input.dropdown.currentIndexChanged.connect(self.on_frequency_changed)
        self.degrees_input.dropdown.currentIndexChanged.connect(self.on_degrees_changed)
        self.start_button.clicked.connect(self.on_start_button_pressed)
        self.path_input.button.clicked.connect(self.on_browse_pressed)

    def add_zoom_options(self):
        self.live_preview_switch = custom_switch("Live view")
        self.gain_slider = custom_slider("Gain")
        self.exposure_slider = custom_slider("Exposure")
        self.camera_selection_input = custom_dropdown("Camera No.", "Available cameras")
        self.default_button = QPushButton()
        self.default_button.setText("Default")

        # Configurar sliders
        self.gain_slider.set_min_max_values(0, 100)
        self.gain_slider.slider.setValue(0)
        self.exposure_slider.set_min_max_values(-13, -1)
        self.exposure_slider.slider.setValue(-6)

        self.camera_selection_input.add_item("Camera 1")
        self.camera_selection_input.add_item("Camera 2")
        self.camera_selection_input.add_item("Camera 3")

        # Configurar live preview siempre activo y deshabilitado
        self.live_preview_switch.switch.setChecked(True)
        self.live_preview_switch.switch.setEnabled(False)
        self.preview = True  # Asegurar que la vista previa está activa

        self.right_bottom_layout.addWidget(self.live_preview_switch)
        # Eliminado el botón de captura
        self.right_bottom_layout.addWidget(self.gain_slider)
        self.right_bottom_layout.addWidget(self.exposure_slider)
        self.right_bottom_layout.addWidget(self.camera_selection_input)
        self.right_bottom_layout.addWidget(self.default_button)

        self.camera_selection_input.dropdown.currentIndexChanged.connect(self.on_camera_dropdown_changed)
        self.default_button.clicked.connect(self.on_default_button_clicked)
        self.gain_slider.slider.valueChanged.connect(self.on_gain_changed)
        self.exposure_slider.slider.valueChanged.connect(self.on_exposure_changed)
        # Eliminada la conexión del interruptor de vista previa
        return

    def add_camera_view(self):
        # Create camera objects
        self.camera0 = webcam_driver(self.camera0_index, 1920, 1080)
        self.camera1 = webcam_driver(self.camera1_index, 1920, 1080)
        self.camera2 = webcam_driver(self.camera2_index, 1920, 1080)

        # Init camera objects
        self.camera0.start()
        self.camera1.start()
        self.camera2.start()

        self.camera_timer = QTimer()

        self.video_label = QLabel()
        self.video_label.setContentsMargins(0, 0, 0, 0)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_top_layout.addWidget(self.video_label)

        self.camera_timer.timeout.connect(self.update_frame)
        self.camera_timer.start(int(1000 / self.fps))

        return

    # Action/functionalities methods
    def update_frame(self):
        """
        Camera frame update
        """
        if self.preview:
            match self.selected_camera:
                case 0:
                    frame = self.camera0.get_frame()
                    pixmap = self.camera0.to_pixmap(frame)
                case 1:
                    frame = self.camera1.get_frame()
                    pixmap = self.camera1.to_pixmap(frame)
                case 2:
                    frame = self.camera2.get_frame()
                    pixmap = self.camera2.to_pixmap(frame)

            self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_camera_dropdown_changed(self):
        option = self.camera_selection_input.dropdown.currentText()

        match option:
            case "Camera 1":
                self.selected_camera = 0
                camera = self.camera0
            case "Camera 2":
                self.selected_camera = 1
                camera = self.camera1
            case "Camera 3":
                self.selected_camera = 2
                camera = self.camera2

        self.brightness_slider.slider.setValue(camera.brightness)
        self.contrast_slider.slider.setValue(int(camera.contrast * 10))
        self.saturation_slider.slider.setValue(int(camera.saturation * 10))
        self.hue_slider.slider.setValue(camera.hue_shift)
        self.exposure_slider.slider.setValue(camera.exposure)
        self.gain_slider.slider.setValue(int(camera.gain))

    def on_capture_button_clicked(self):
        # Método eliminado ya que el botón de captura ha sido eliminado
        pass

    def on_default_button_clicked(self):

        default_brightness = self.camera0.default_brightness
        default_contrast = self.camera0.default_contrast
        default_saturation = self.camera0.default_saturation
        default_hue_shift = self.camera0.default_hue_shift
        default_exposure = self.camera0.default_exposure
        default_gain = self.camera0.default_gain

        match self.selected_camera:
            case 0:
                self.camera0.set_brightness(default_brightness)
                self.camera0.set_contrast(default_contrast)
                self.camera0.set_saturation(default_saturation)
                self.camera0.set_hue_shift(default_hue_shift)
                self.camera0.set_exposure(default_exposure)
                self.camera0.set_gain(default_gain)
            case 1:
                self.camera1.set_brightness(default_brightness)
                self.camera1.set_contrast(default_contrast)
                self.camera1.set_saturation(default_saturation)
                self.camera1.set_hue_shift(default_hue_shift)
                self.camera1.set_exposure(default_exposure)
                self.camera1.set_gain(default_gain)
            case 2:
                self.camera2.set_brightness(default_brightness)
                self.camera2.set_contrast(default_contrast)
                self.camera2.set_saturation(default_saturation)
                self.camera2.set_hue_shift(default_hue_shift)
                self.camera2.set_exposure(default_exposure)
                self.camera2.set_gain(default_gain)

        self.brightness_slider.slider.setValue(default_brightness)
        self.contrast_slider.slider.setValue(default_contrast * 10)
        self.saturation_slider.slider.setValue(default_saturation * 10)
        self.hue_slider.slider.setValue(default_hue_shift)
        self.exposure_slider.slider.setValue(default_exposure)
        self.gain_slider.slider.setValue(default_gain)

    def on_gain_changed(self):
        value = float(self.gain_slider.get_value())
        match self.selected_camera:
            case 0:
                self.camera0.set_gain(value)
            case 1:
                self.camera1.set_gain(value)
            case 2:
                self.camera2.set_gain(value)

    def on_exposure_changed(self):
        value = self.exposure_slider.get_value()

        match(self.selected_camera):
            case 0:
                self.camera0.set_exposure(value)
            case 1:
                self.camera1.set_exposure(value)
            case 2:
                self.camera2.set_exposure(value)

    def on_brightness_changed(self):
        value = self.brightness_slider.slider.value()
        match self.selected_camera:
            case 0:
                self.camera0.set_brightness(value)
            case 1:
                self.camera1.set_brightness(value)
            case 2:
                self.camera2.set_brightness(value)

    def on_contrast_changed(self):
        value = (self.contrast_slider.slider.value()) / 10
        match self.selected_camera:
            case 0:
                self.camera0.set_contrast(value)
            case 1:
                self.camera1.set_contrast(value)
            case 2:
                self.camera2.set_contrast(value)

    def on_hue_changed(self):
        value = self.hue_slider.slider.value()
        match self.selected_camera:
            case 0:
                self.camera0.set_hue_shift(value)
            case 1:
                self.camera1.set_hue_shift(value)
            case 2:
                self.camera2.set_hue_shift(value)

    def on_live_preview_changed(self, state):
        # Método eliminado ya que live_preview está siempre activo y deshabilitado
        pass

    def on_saturation_changed(self):
        value = (self.saturation_slider.slider.value()) / 10
        match self.selected_camera:
            case 0:
                self.camera0.set_saturation(value)
            case 1:
                self.camera1.set_saturation(value)
            case 2:
                self.camera2.set_saturation(value)

    def on_frequency_changed(self):
        option = self.frequency_input.dropdown.currentText()
        self.degrees_input.dropdown.setEnabled(True)

        match option:
            case "Select":
                self.degrees_input.dropdown.setEnabled(False)
                self.degrees_input.dropdown.setCurrentIndex(0)
                self.capture_frequency = 0  # Asegurarse de restablecer el valor
            case "5 Degs":
                self.capture_frequency = 5
            case "10 Degs":
                self.capture_frequency = 10
            case "15 Degs":
                self.capture_frequency = 15
            case "25 Degs":
                self.capture_frequency = 25

        if self.capture_frequency != 0:
            pulse_frequency = int(self.capture_frequency * 16000 / 360)
            self.serial_array[0] = pulse_frequency
        else:
            self.serial_array[0] = 0  # Asegurarse de restablecer el valor

    def on_degrees_changed(self):
        option = self.degrees_input.dropdown.currentText()

        match option:
            case "Select":
                self.start_button.setEnabled(False)
                self.degrees_movement = 0  # Asegurarse de restablecer el valor
            case "45 Degs":
                self.degrees_movement = 45
            case "90 Degs":
                self.degrees_movement = 90
            case "180 Degs":
                self.degrees_movement = 180
            case "360 Degs":
                self.degrees_movement = 360

        if self.capture_frequency != 0 and self.degrees_movement != 0:
            times_to_move = int(self.degrees_movement / self.capture_frequency)
            self.serial_array[1] = times_to_move
            self.start_button.setEnabled(True)
        else:
            self.serial_array[1] = 0
            self.start_button.setEnabled(False)

    def on_start_button_pressed(self):
        # Deshabilitar el botón de inicio
        self.start_button.setEnabled(False)

        # Crear el hilo del trabajador
        self.serial_worker = SerialWorker(
            ser=self.ser,
            serial_array=self.serial_array,
            capture_images_callback=self.capture_images
        )

        # Conectar las señales del trabajador a los métodos de la GUI
        self.serial_worker.image_captured.connect(self.on_image_captured)
        self.serial_worker.finished.connect(self.on_serial_worker_finished)

        # Iniciar el hilo
        self.serial_worker.start()

    def on_image_captured(self, picture_number):
        print(f"Image {picture_number} captured.")

    def on_serial_worker_finished(self):
        print("Serial worker finished.")
        # Rehabilitar el botón de inicio
        self.start_button.setEnabled(True)

    def on_browse_pressed(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select destination folder")
        if folder_path:
            self.path_input.set_value(folder_path)

        self.start_button.setEnabled(True)

    def capture_images(self, image_number):
        path_input = self.path_input.get_value()
        file_name = self.file_name_input.get_value().upper()
        time_stamp = datetime.now().strftime("%d%m%y")
        image_format = "jpg"

        # Verificar que el nombre del producto no esté vacío
        if not file_name:
            QMessageBox.warning(self, "Error", "Por favor, ingrese el código del producto (ID).")
            return

        # Crear carpeta para el producto
        product_folder = os.path.join(path_input, file_name)
        try:
            os.makedirs(product_folder, exist_ok=True)
            print(f"Carpeta creada o existente: {product_folder}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear la carpeta: {e}")
            return

        # Construir rutas de archivos
        camera0_file_path = os.path.join(product_folder, f"{file_name}_CAM0_{time_stamp}_{image_number}.{image_format}")
        camera1_file_path = os.path.join(product_folder, f"{file_name}_CAM1_{time_stamp}_{image_number}.{image_format}")
        camera2_file_path = os.path.join(product_folder, f"{file_name}_CAM2_{time_stamp}_{image_number}.{image_format}")

        # Guardar imágenes
        try:
            cv2.imwrite(camera0_file_path, self.camera0.get_frame())
            cv2.imwrite(camera1_file_path, self.camera1.get_frame())
            cv2.imwrite(camera2_file_path, self.camera2.get_frame())
            print(f"Imágenes guardadas en: {product_folder}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron guardar las imágenes: {e}")

    def load_stylesheet(self, file_name):
        try:
            with open(file_name, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Stylesheet file {file_name} not found.")

        self.left_top_title.setStyleSheet("""font-weight: bold;margin-bottom: 10px;""")
        self.left_bottom_title.setStyleSheet("""font-weight: bold;margin-bottom: 10px;""")
        self.right_bottom_title.setStyleSheet("""font-weight: bold;margin-bottom: 10px;""")

    def display_window(self):
        """
        Show app window.
        """
        self.show()

    def apply_main_configuration(self):
        """
        Apply the configuration loaded from main.conf to the UI elements and variables.
        """
        # Establecer la cámara seleccionada
        self.selected_camera = self.main_config.get('selected_camera', 0)
        self.camera_selection_input.dropdown.setCurrentIndex(self.selected_camera)

        # Establecer valores de los sliders y ajustes de cámara
        for camera_index in ['0', '1', '2']:
            settings = self.main_config['camera_settings'].get(camera_index, {})
            camera = getattr(self, f'camera{camera_index}')
            if camera:
                camera.set_brightness(settings.get('brightness', 50))
                camera.set_contrast(settings.get('contrast', 1.0))
                camera.set_saturation(settings.get('saturation', 1.0))
                camera.set_hue_shift(settings.get('hue', 0))
                camera.set_gain(settings.get('gain', 0))
                camera.set_exposure(settings.get('exposure', -6))

        # Actualizar los sliders de la interfaz con los valores de la cámara seleccionada
        self.on_camera_dropdown_changed()

        # Establecer la carpeta donde se guardarán los archivos
        save_folder = self.main_config.get('save_folder', 'src\\test-images')
        self.path_input.set_value(save_folder)

        # Establecer el nombre de archivo
        file_name = self.main_config.get('file_name', '')
        self.file_name_input.set_value(file_name)

        # Establecer el estado de live preview (siempre True)
        self.live_preview_switch.switch.setChecked(True)
        self.live_preview_switch.switch.setEnabled(False)
        self.preview = True

        # Cargar la configuración de grados y frecuencia
        self.capture_frequency = self.main_config.get('capture_frequency', 0)
        self.degrees_movement = self.main_config.get('degrees_movement', 0)

        # Establecer el índice seleccionado en los dropdowns basados en los valores de frecuencia y grados
        frequency_options = ["Select", "5 Degs", "10 Degs", "15 Degs", "25 Degs"]
        degrees_options = ["Select", "45 Degs", "90 Degs", "180 Degs", "360 Degs"]

        # Encontrar el índice correspondiente a la frecuencia guardada
        if self.capture_frequency in [5, 10, 15, 25]:
            frequency_text = f"{self.capture_frequency} Degs"
            frequency_index = frequency_options.index(frequency_text)
        else:
            frequency_index = 0  # "Select"

        self.frequency_input.dropdown.setCurrentIndex(frequency_index)
        self.on_frequency_changed()  # Llamar manualmente para actualizar variables

        # Encontrar el índice correspondiente a los grados guardados
        if self.degrees_movement in [45, 90, 180, 360]:
            degrees_text = f"{self.degrees_movement} Degs"
            degrees_index = degrees_options.index(degrees_text)
        else:
            degrees_index = 0  # "Select"

        self.degrees_input.dropdown.setCurrentIndex(degrees_index)
        self.on_degrees_changed()  # Llamar manualmente para actualizar variables

    def on_save_and_close(self):
        """
        Save the current configuration to main.conf and close the application.
        """
        # Actualizar la configuración con los valores actuales
        self.main_config['selected_camera'] = self.selected_camera

        # Guardar los ajustes de cada cámara
        for idx in [0, 1, 2]:
            camera = getattr(self, f'camera{idx}')
            if camera:
                self.main_config['camera_settings'][str(idx)] = {
                    'brightness': camera.brightness,
                    'contrast': camera.contrast,
                    'hue': camera.hue_shift,
                    'saturation': camera.saturation,
                    'gain': camera.gain,
                    'exposure': camera.exposure
                }

        # Guardar la carpeta donde se guardarán los archivos
        save_folder = self.path_input.get_value()
        self.main_config['save_folder'] = save_folder

        # Guardar el nombre de archivo
        file_name = self.file_name_input.get_value()
        self.main_config['file_name'] = file_name

        # Guardar el estado de live preview (siempre True)
        self.main_config['live_preview'] = True

        # Guardar la configuración de grados y frecuencia
        self.main_config['capture_frequency'] = self.capture_frequency
        self.main_config['degrees_movement'] = self.degrees_movement

        # Guardar la configuración en main.conf
        self.save_main_configuration()

        # Cerrar la aplicación
        self.close()

    def closeEvent(self, event):
        """
        Override closeEvent to ensure the worker thread is stopped.
        """
        if hasattr(self, 'serial_worker') and self.serial_worker.isRunning():
            self.serial_worker.is_running = False
            self.serial_worker.wait()
        event.accept()
