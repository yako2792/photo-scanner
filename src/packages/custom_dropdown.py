from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class custom_dropdown(QWidget):
    def __init__(self, text = "Unnamed", hint = "", parent = None):
        """
        Create custom dropdown.
        """
        super().__init__(parent)
        self.setup_dropdown(text, hint)

    def setup_dropdown(self, text, hint):
        """
        Define essential elements in custom dropdown menu.
        """
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Label
        self.label = QLabel(text)
        self.label.setMinimumWidth(50)
        self.label.setMaximumWidth(100)
        self.label.setMaximumHeight(22)
        self.label.setContentsMargins(0, 0, 0, 0)
        # self.label.setStyleSheet("background-color: green;")

        # Dropdown
        self.dropdown = QComboBox()
        self.dropdown.addItem("Camera 1")
        self.dropdown.addItem("Camera 2")
        self.dropdown.addItem("Camera 3")

        self.dropdown.setMinimumWidth(100)
        self.dropdown.setMaximumWidth(150)
        self.dropdown.setContentsMargins(0, 0, 0, 0)
        # self.label.setStyleSheet("background-color: red;")

        # Hint
        self.hint = QLabel(hint)
        self.hint.setMinimumWidth(50)
        self.hint.setMaximumWidth(100)
        self.hint.setMaximumHeight(22)
        self.hint.setContentsMargins(0, 0, 0, 0)
        # self.hint.setStyleSheet("background-color: blue;")

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.dropdown)
        self.main_layout.addWidget(self.hint)

        self.setLayout(self.main_layout)
    
    def get_value(self):
        """
        Get dropdown selection/value.

        :return: Actual selection of dropdown menu.
        """
        value = None
        return value