import sys
import cv2
from .webcam_driver import webcam_driver
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

        self.setup_window()
        self.setup_layout()
        self.add_video_options()
        self.add_rotation_options()
        

    def setup_window(self, geometry = (800,600), title = "Unnamed"):
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
        self.label = QLabel("Live preview (no webcam available)")
        self.label.setStyleSheet("color: #ffffff")
        self.right_top_layout.addWidget(self.label)
        self.right_column.addWidget(self.right_top_box)

        ## Right bottom box
        self.right_bottom_box = QWidget()
        self.right_bottom_box.setFixedSize(400,300)
        # self.right_bottom_box.setStyleSheet("background-color: lightblue;")
        
        self.right_bottom_layout = QVBoxLayout(self.right_bottom_box)
        self.right_bottom_layout.addWidget(QLabel("Right bottom box"))
        self.right_bottom_layout.setContentsMargins(25, 50, 25, 0)
        self.right_bottom_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.right_column.addWidget(self.right_bottom_box)

    def add_video_options(self):
        self.brightness_slider = custom_slider("Brightness")
        self.contrast_slider = custom_slider("Contrast")
        self.hue_slider = custom_slider("HUE")
        self.saturation_slider = custom_slider("saturation")
        self.sharpness_slider = custom_slider("Sharpness")

        self.left_top_layout.addWidget(self.brightness_slider)
        self.left_top_layout.addWidget(self.contrast_slider)
        self.left_top_layout.addWidget(self.hue_slider)
        self.left_top_layout.addWidget(self.saturation_slider)
        self.left_top_layout.addWidget(self.sharpness_slider)

    def add_rotation_options(self):
        self.mode_switch = custom_switch("Mode")
        self.frequency_input = custom_input("Frequency", "Degrees per photo")
        self.degrees_input = custom_input("Degrees", "Degrees to be rotated.")
        self.save_input = custom_input("Save As", "<browser>")

        self.start_button = QPushButton()
        self.start_button.setText("Start")
        self.reset_button = QPushButton()
        self.reset_button.setText("Reset")
        self.stop_button = QPushButton()
        self.stop_button.setText("Stop")

        self.left_bottom_layout.addWidget(self.mode_switch)
        self.left_bottom_layout.addWidget(self.frequency_input)
        self.left_bottom_layout.addWidget(self.degrees_input)
        self.left_bottom_layout.addWidget(self.save_input)
        self.left_bottom_layout.addWidget(self.start_button)
        self.left_bottom_layout.addWidget(self.reset_button)
        self.left_bottom_layout.addWidget(self.stop_button)

    def add_camera_view(self):
        return
    
    def add_zoom_options(self):
        return

    def display_window(self):
        """
        Show app window.
        """
        self.show()