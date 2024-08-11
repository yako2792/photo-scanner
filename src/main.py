# src/main.py
import sys
from packages.window_driver import window_driver
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    driver = window_driver()
    driver.display_window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
