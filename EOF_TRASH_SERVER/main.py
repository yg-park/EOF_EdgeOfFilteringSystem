"""
프로그램 엔트리 포인트 모듈입니다.
"""
import sys
from PyQt5.QtWidgets import QApplication
from pyqtGUI.main_window import MainGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGUI()
    window.setGeometry(100, 100, 750, 800)
    window.show()
    sys.exit(app.exec_())
