import cv2
import serial
import time
from .webcam_driver import webcam_driver
from .custom_dropdown import custom_dropdown
from .custom_switch import custom_switch
from .custom_input import custom_input
from .custom_slider import custom_slider
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class window_driver(QMainWindow):
    def __init__(self):
        """
        Initialize window driver with window title.
        """
        super().__init__()

        # Camera settings
        self.selected_camera = 0
        self.camera0_index = 0
        self.camera1_index = 1
        self.fps = 5

        self.preview = False

        # Serial message
        self.ser = serial.Serial("COM7", 9600, timeout=1)
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
        
    # Setup window and layout
    def setup_window(self, geometry = (800, 600), title = "Photo Scanner"):
        """
        Setup window size and title.
        :param geometry: Size of window ((800,600) by default).
        :param title: Title of window ("Untitled" by default).
        """
        self.setWindowTitle(title)
        self.setFixedSize(geometry[0], geometry[1])
        self.setStyleSheet("background-color: #d6d0d4")

        # Horizontal layout as main container
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def setup_layout(self):
        """
        Create initial layout content in window.
        """
        self.setup_left_column()
        self.setup_right_column()
    
    def setup_left_column(self):
        """
        Create left column in layout.
        """
        # Left column
        self.left_column = QVBoxLayout()
        self.main_layout.addLayout(self.left_column)
        
        ## Left upper box
        self.left_top_box = QWidget()
        self.left_top_box.setFixedSize(400,300)
        # self.left_top_box.setStyleSheet("background-color: lightblue;")
        
        self.left_top_layout = QVBoxLayout(self.left_top_box)
        self.left_top_layout.addWidget(QLabel("Process video options"))
        self.left_top_layout.setContentsMargins(25, 50, 25, 0)
        self.left_top_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.left_column.addWidget(self.left_top_box)

        ## Left bottom box
        self.left_bottom_box = QWidget()
        self.left_bottom_box.setFixedSize(400,300)
        # self.left_bottom_box.setStyleSheet("background-color: blue;")
        
        self.left_bottom_layout = QVBoxLayout(self.left_bottom_box)
        self.left_bottom_layout.addWidget(QLabel("Rotation options"))
        self.left_bottom_layout.setContentsMargins(25, 50, 25, 0)
        self.left_bottom_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.left_column.addWidget(self.left_bottom_box)

    def setup_right_column(self):
        """
        Create right column in layout.
        """
        # Right column
        self.right_column = QVBoxLayout()
        self.main_layout.addLayout(self.right_column)

        ## Right top box
        self.right_top_box = QWidget()
        self.right_top_box.setFixedSize(400,300)
        self.right_top_box.setStyleSheet("background-color: black;")
        
        self.right_top_layout = QVBoxLayout(self.right_top_box)
        # self.label = QLabel("Live preview (no webcam available)")
        # self.label.setStyleSheet("color: #ffffff")
        # self.right_top_layout.addWidget(self.label)
        self.right_top_layout.setContentsMargins(0, 0, 0, 0)
        self.right_top_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.right_column.addWidget(self.right_top_box)

        ## Right bottom box
        self.right_bottom_box = QWidget()
        self.right_bottom_box.setFixedSize(400,300)
        # self.right_bottom_box.setStyleSheet("background-color: lightblue;")
        
        self.right_bottom_layout = QVBoxLayout(self.right_bottom_box)
        self.right_bottom_layout.addWidget(QLabel("Camera control options"))
        self.right_bottom_layout.setContentsMargins(25, 50, 25, 0)
        self.right_bottom_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.right_column.addWidget(self.right_bottom_box)

    # Add elements to layout
    def add_video_options(self):
        self.brightness_slider = custom_slider("Brightness")
        self.contrast_slider = custom_slider("Contrast")
        self.hue_slider = custom_slider("HUE")
        self.saturation_slider = custom_slider("saturation")
        # self.sharpness_slider = custom_slider("Sharpness")

        self.left_top_layout.addWidget(self.brightness_slider)
        self.left_top_layout.addWidget(self.contrast_slider)
        self.left_top_layout.addWidget(self.hue_slider)
        self.left_top_layout.addWidget(self.saturation_slider)
        # self.left_top_layout.addWidget(self.sharpness_slider)

        # Set custom minimum and maximum values
        self.brightness_slider.set_min_max_values(0, 100)
        self.contrast_slider.set_min_max_values(0, 30)
        self.hue_slider.set_min_max_values(0,100)
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
        self.path_input = custom_input("Path", "File save path.")

        # Buttons and setup
        self.start_button = QPushButton()
        self.start_button.setText("Start")
        self.start_button.setEnabled(False)

        self.stop_button = QPushButton()
        self.stop_button.setText("Stop")
        self.stop_button.setEnabled(False)

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
        self.left_bottom_layout.addWidget(self.stop_button)

        self.frequency_input.dropdown.currentIndexChanged.connect(self.on_frequency_changed)
        self.degrees_input.dropdown.currentIndexChanged.connect(self.on_degrees_changed)
        self.start_button.clicked.connect(self.on_start_button_pressed)
        self.stop_button.clicked.connect(self.on_stop_button_pressed)

    def add_camera_view(self):
        # Create camera objects
        self.camera0 = webcam_driver(self.camera0_index, 3840, 2160)
        self.camera1 = webcam_driver(self.camera1_index, 1920, 1080)
        
        # Init camera objects
        self.camera0.start()
        self.camera1.start()

        self.camera_timer = QTimer()

        self.video_label = QLabel()
        self.video_label.setContentsMargins(0, 0, 0, 0)
        self.video_label.setFixedSize(400, 300)
        self.right_top_layout.addWidget(self.video_label)

        self.camera_timer.timeout.connect(self.update_frame)
        self.camera_timer.start(int(1000/self.fps))

        return
    
    def add_zoom_options(self):
        self.live_preview_switch = custom_switch("Live view")
        self.capture_button = QPushButton(); self.capture_button.setText("Capture")
        self.zoom_slider = custom_slider("Zoom")
        self.focus_slider = custom_slider("Focus")
        self.exposure_slider = custom_slider("Exposure")
        self.camera_selection_input = custom_dropdown("Camera No.", "Available cameras")
        self.default_button = QPushButton(); self.default_button.setText("Default")

        self.camera_selection_input.add_item("Camera 1")
        self.camera_selection_input.add_item("Camera 2")

        self.right_bottom_layout.addWidget(self.live_preview_switch)
        self.right_bottom_layout.addWidget(self.capture_button)
        self.right_bottom_layout.addWidget(self.zoom_slider)
        self.right_bottom_layout.addWidget(self.focus_slider)
        self.right_bottom_layout.addWidget(self.exposure_slider)
        self.right_bottom_layout.addWidget(self.camera_selection_input)
        self.right_bottom_layout.addWidget(self.default_button)

        self.camera_selection_input.dropdown.currentIndexChanged.connect(self.on_camera_dropdown_changed)
        self.capture_button.clicked.connect(self.on_capture_button_clicked)
        self.default_button.clicked.connect(self.on_default_button_clicked)
        self.zoom_slider.slider.valueChanged.connect(self.on_zoom_changed)
        self.live_preview_switch.switch.stateChanged.connect(self.on_live_preview_changed)
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
        
            self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_camera_dropdown_changed(self):
        """
        Change camera index based on dropdown selection.
        """
        option = self.camera_selection_input.dropdown.currentText()
        
        match option:
            case "Camera 1":
                self.selected_camera = 0
            case "Camera 2":
                self.selected_camera = 1
            case "Camera 3":
                self.selected_camera = 2 

    def on_capture_button_clicked(self):
        match self.selected_camera:
            case 0:
                frame = self.camera0.get_frame()
                path_extension = "CAM0"
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            case 1:
                frame = self.camera1.get_frame()
                path_extension = "CAM1"
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        path = f"src\\test-images\\{path_extension}.jpg"
        cv2.imwrite(path, frame)
        pixmap = QPixmap(path)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_default_button_clicked(self):
        match self.selected_camera:
            case 0:
                default_brightness = self.camera0.default_brightness
                default_contrast = self.camera0.default_contrast
                default_saturation = self.camera0.default_saturation
                default_hue_shift = self.camera0.default_hue_shift

                self.camera0.set_brightness(default_brightness)
                self.camera0.set_contrast(default_contrast)
                self.camera0.set_saturation(default_saturation)
                self.camera0.set_hue_shift(default_hue_shift)
            case 1:
                default_brightness = self.camera1.default_brightness
                default_contrast = self.camera1.default_contrast
                default_saturation = self.camera1.default_saturation
                default_hue_shift = self.camera1.default_hue_shift

                self.camera1.set_brightness(default_brightness)
                self.camera1.set_contrast(default_contrast)
                self.camera1.set_saturation(default_saturation)
                self.camera1.set_hue_shift(default_hue_shift)
        
        self.brightness_slider.slider.setValue(default_brightness)
        self.contrast_slider.slider.setValue(default_contrast*10)
        self.saturation_slider.slider.setValue(default_saturation*10)
        self.hue_slider.slider.setValue(default_hue_shift)

    def on_zoom_changed(self):
        value = float(self.zoom_slider.slider.value())
        # print(f"[Zoom Slider] value {value}")
        match self.selected_camera:
            case 0:
                self.camera0.set_zoom(value)
            case 1:
                self.camera1.set_zoom(value)

    def on_brightness_changed(self):
        value = self.brightness_slider.slider.value()
        match self.selected_camera:
            case 0:
                self.camera0.set_brightness(value)
            case 1:
                self.camera1.set_brightness(value)   

    def on_contrast_changed(self):
        value = (self.contrast_slider.slider.value())/10
        match self.selected_camera:
            case 0:
                self.camera0.set_contrast(value)
            case 1:
                self.camera1.set_contrast(value) 

    def on_hue_changed(self):
        value = self.hue_slider.slider.value()
        match self.selected_camera:
            case 0:
                self.camera0.set_hue_shift(value)
            case 1:
                self.camera1.set_hue_shift(value)
    
    def on_live_preview_changed(self, state):
        match state:
            case 0:
                self.capture_button.setEnabled(True)
                self.preview = False
            case 2:
                self.capture_button.setEnabled(False)
                self.preview = True

    def on_saturation_changed(self):
        value = (self.saturation_slider.slider.value())/10
        match self.selected_camera:
            case 0:
                self.camera0.set_saturation(value)
            case 1:
                self.camera1.set_saturation(value) 

    def on_frequency_changed(self):
        option = self.frequency_input.dropdown.currentText()
        self.degrees_input.dropdown.setEnabled(True)

        match option:
            case "Select":
                self.degrees_input.dropdown.setEnabled(False)
                self.degrees_input.dropdown.setCurrentIndex(0)
            case "5 Degs":
                self.capture_frequency = 5

            case "10 Degs":
                self.capture_frequency = 10

            case "15 Degs":
                self.capture_frequency = 15

            case "25 Degs":
                self.capture_frequency = 25
        
        pulse_frequency = int(self.capture_frequency*16000/360)
        self.serial_array[0] = pulse_frequency
        
    def on_degrees_changed(self):
        option = self.degrees_input.dropdown.currentText()
        self.start_button.setEnabled(True)

        match option:
            case "Select":
                self.start_button.setEnabled(False)

            case "45 Degs":
                self.degrees_movement = 45
            case "90 Degs":
                self.degrees_movement = 90
            case "180 Degs":
                self.degrees_movement = 180
            case "360 Degs":
                self.degrees_movement = 360

        times_to_move = int(self.degrees_movement/self.capture_frequency)
        self.serial_array[1] = times_to_move

    def on_start_button_pressed(self):
        self.stop_button.setEnabled(True)

        message = str(self.serial_array[0]) + "," + str(self.serial_array[1]) + "\n"
        print(message.encode())
        self.ser.write(message.encode())
    
    def on_stop_button_pressed(self):
        message = str(1) + "\n"
        print(message.encode())
        self.ser.write(message.encode())

    def display_window(self):
        """
        Show app window.
        """
        self.show()