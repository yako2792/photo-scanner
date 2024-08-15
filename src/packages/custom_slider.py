from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class custom_slider(QWidget):
    def __init__(self, text = "Unnamed", hint = "", parent = None):
        """
        Create custom horizontal slider.
        """
        super().__init__(parent)
        self.setup_slider(text, hint)
    
    def setup_slider(self, text, hint):
        """
        Define essential elements in custom slider widget.
        """
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)

        # Label
        self.label = QLabel(text)
        self.label.setMinimumWidth(50)
        self.label.setMaximumWidth(100)
        self.label.setMaximumHeight(22)
        self.label.setContentsMargins(0,0,0,0)
        # self.label.setStyleSheet("background-color: green;")
        
        # Slider
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimumWidth(100)
        self.slider.setMaximumWidth(150)
        self.slider.setContentsMargins(0,0,0,0)
        # self.slider.setStyleSheet("background-color: red;")
        
        # Hint
        self.hint = QLabel(hint)
        self.hint.setMinimumWidth(50)
        self.hint.setMaximumWidth(100)
        self.hint.setMaximumHeight(22)
        self.hint.setContentsMargins(0,0,0,0)
        # self.hint.setStyleSheet("background-color: blue;")
        
        # Add all to main layout
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.slider)
        self.main_layout.addWidget(self.hint)

        self.setLayout(self.main_layout)
    
    def get_value(self):
        """
        Get slider value/position.

        :return: Int value of slider position.
        """
        return self.slider.value()