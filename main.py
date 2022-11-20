import os
import sys

from PyQt6.QtWidgets import QApplication

from gui.main_window.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    else:
        app_path = os.path.dirname(os.path.abspath(__file__))
    window = MainWindow(app_path)
    app.exec()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
