from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class custom_file_browser (QWidget):
    def __init__(self,text = "Unnamed", hint = "", parent = None):
        super().__init__(parent)
        self.setup_browser(text, hint)
    
    def setup_browser(self, text, hint):
        """
        Define essential elements in custom file browser.
        """
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 15)

        # Label
        self.label = QLabel(text)
        self.label.setMinimumWidth(50)
        self.label.setMaximumWidth(80)
        self.label.setMaximumHeight(22)
        self.label.setContentsMargins(0, 0, 0, 0)

        # Slider
        self.input = QLineEdit()
        self.input.setMinimumWidth(100)
        self.input.setMaximumWidth(150)
        self.input.setContentsMargins(0, 0, 0, 0)
        self.input.setDisabled(True)

        # Hint
        self.button = QPushButton(hint)
        self.button.setMinimumWidth(50)
        self.button.setMaximumWidth(100)
        self.button.setMaximumHeight(22)
        self.button.setContentsMargins(0, 0, 0, 0)

        # Add all to main layout
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.input)
        self.main_layout.addWidget(self.button)

        self.setLayout(self.main_layout)
    
    def set_input_field_text(self, text):
        """
        Add text to input filed.

        :param text: Value to insert in text field.
        """
        self.input.setText(text)
    
    def get_value(self):
        """
        Get input field value.

        :return: Value of input field.
        """
        return self.input.text()