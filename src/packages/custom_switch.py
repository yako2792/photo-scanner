from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class custom_switch(QWidget):
    def __init__(self, text = "Unnamed", parent = None):
        """
        Create custom switch.
        """
        super().__init__(parent)
        self.setup_switch(text)
    
    def setup_switch(self, text):
        """
        Define essential elements in custom switch widget
        """
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Label
        self.label = QLabel(text)
        self.label.setMinimumWidth(50)
        self.label.setMaximumWidth(50)
        self.label.setMaximumHeight(22)
        self.label.setContentsMargins(0,0,0,0)
        # self.label.setStyleSheet("background-color: red;")

        # Checkbox
        self.switch = QCheckBox()
        self.switch.setMinimumSize(20,20)
        self.switch.setMaximumSize(20,20)
        # self.switch.setStyleSheet("background-color: blue;")

        # Add in layout

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.switch)

        self.setLayout(self.main_layout)