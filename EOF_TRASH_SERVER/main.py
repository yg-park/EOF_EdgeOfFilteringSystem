"""
프로그램 엔트리 포인트 모듈입니다.
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt_framework.GUI import MainGUI

IP_ADDRESS = "10.10.15.58"
IMG_PORT = 5555
STR_PORT = 6666
WAV_PORT = 7777
TMP_PORT = 8888

if __name__ == "__main__":
    port = {"IMG_PORT": IMG_PORT, "STR_PORT": STR_PORT,
            "WAV_PORT": WAV_PORT, "TMP_PORT": TMP_PORT}

    app = QApplication(sys.argv)
    window = MainGUI(IP_ADDRESS, port)
    window.setGeometry(100, 100, 1200, 800)
    window.show()
    sys.exit(app.exec_())
