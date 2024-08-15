from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class custom_input (QWidget):
    def __init__(self,text = "Unnamed", hint = "", parent = None):
        """
        Create custom input field.
        """
        super().__init__(parent)
        self.setup_input(text, hint)
    
    def setup_input(self, text, hint):
        """
        Define essential elements in custom input field.
        """
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)

        # Label
        self.label = QLabel(text)
        self.label.setMinimumWidth(50)
        self.label.setMaximumWidth(80)
        self.label.setMaximumHeight(22)
        self.label.setContentsMargins(0,0,0,0)
        # self.label.setStyleSheet("background-color: green;")
        
        # Slider
        self.input = QLineEdit()
        self.input.setMinimumWidth(100)
        self.input.setMaximumWidth(150)
        self.input.setContentsMargins(0,0,0,0)
        # self.input.setStyleSheet("background-color: red;")
        
        # Hint
        self.hint = QLabel(hint)
        self.hint.setMinimumWidth(50)
        self.hint.setMaximumWidth(100)
        self.hint.setMaximumHeight(22)
        self.hint.setContentsMargins(0,0,0,0)
        # self.hint.setStyleSheet("background-color: blue;")
        
        # Add all to main layout
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.input)
        self.main_layout.addWidget(self.hint)

        self.setLayout(self.main_layout)
    
    def get_value(self):
        """
        Get input field value.

        :return: Value of input field.
        """
        return self.input.value()