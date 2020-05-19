
from PySide2.QtWidgets import QApplication
from src.mainwindow import MainWindow
import sys

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
