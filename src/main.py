import sys
import os

from pprint import pprint
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore

from ui.main_window import Main_Window


def main(app):
    main_window = Main_Window(app)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
        QApplication.instance().exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main(app)
