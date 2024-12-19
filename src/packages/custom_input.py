from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class custom_input(QWidget):
    def __init__(self, label_text, placeholder_text, hint_text=None):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Label
        self.label = QLabel(label_text)
        self.label.setMinimumWidth(50)
        self.label.setMaximumWidth(80)
        self.label.setMaximumHeight(22)
        self.label.setContentsMargins(0, 0, 0, 0)
        
        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setMinimumWidth(100)
        self.input_field.setMaximumWidth(150)
        self.input_field.setPlaceholderText(placeholder_text)
        self.input_field.setContentsMargins(0, 0, 0, 0)
        
        # Hint Label (optional)
        if hint_text:
            self.hint = QLabel(hint_text)
            self.hint.setMinimumWidth(50)
            self.hint.setMaximumWidth(100)
            self.hint.setMaximumHeight(22)
            self.hint.setContentsMargins(0, 0, 0, 0)
            # Add widgets to the layout
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.input_field)
            self.layout.addWidget(self.hint)
        else:
            # Add widgets to the layout without hint
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.input_field)
        
        self.setLayout(self.layout)
    
    def get_value(self):
        """
        Get input field value.

        :return: Value of input field.
        """
        return self.input_field.text()
        
    def set_value(self, value):
        """
        Set input field value.

        :param value: Value to set in input field.
        """
        self.input_field.setText(value)
