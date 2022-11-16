import sys

from PyQt6.QtWidgets import QApplication

from gui.main_window.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
