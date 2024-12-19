from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class custom_file_browser(QWidget):
    def __init__(self, label_text, button_text):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 15)

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
        self.input_field.setContentsMargins(0, 0, 0, 0)
        self.input_field.setDisabled(True)  # Si deseas que sea editable, puedes cambiar esto a False

        # Button
        self.button = QPushButton(button_text)
        self.button.setMinimumWidth(50)
        self.button.setMaximumWidth(100)
        self.button.setMaximumHeight(22)
        self.button.setContentsMargins(0, 0, 0, 0)

        # Add all to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def set_value(self, value):
        """
        Set the text of the input field.
        """
        self.input_field.setText(value)

    def get_value(self):
        """
        Get the text from the input field.
        """
        return self.input_field.text()
