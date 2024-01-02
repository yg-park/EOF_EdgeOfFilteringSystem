import sys
from PyQt5.QtWidgets import QApplication
from GUI import *


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainGUI()
    window.setGeometry(100, 100, 1200, 800)
    window.show()
    sys.exit(app.exec_())