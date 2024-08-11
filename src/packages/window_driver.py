import sys
import cv2
from .webcam_driver import webcam_driver
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

    def setup_window(self, geometry = (800,600), title = "Unnamed"):
        """
        Setup window size and title.
        :param geometry: Size of window ((800,600) by default).
        :param title: Title of window ("Untitled" by default).
        """
        self.setWindowTitle(title)
        self.setGeometry(100,100, geometry[0], geometry[1])

    def setup_layout(self):
        """
        Create initial layout content in window.
        """
        # Horizontal layout as main container
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Creation of left container (sliders)
        self.left_column = QVBoxLayout()
        self.left_column.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.left_column.addWidget(QLabel("Header in LEFT column"))
        self.main_layout.addLayout(self.left_column)

        # Creation of right container (camera and buttons)
        self.right_column = QVBoxLayout()
        self.right_column.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.right_column.addWidget(QLabel("Header in RIGHT column"))
        self.main_layout.addLayout(self.right_column)
    
    def display_window(self):
        """
        Show app window.
        """
        self.show()