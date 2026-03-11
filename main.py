import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from resource_path import resource_path
from views.mainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('icons/avatar.png')))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
