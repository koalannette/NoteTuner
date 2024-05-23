import sys

from PyQt5.QtWidgets import QApplication
from widgets.mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    wid = MainWindow()
    wid.show()
    
    sys.exit(app.exec())