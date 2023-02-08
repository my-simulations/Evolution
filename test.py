from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
import time

import sys


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("wkng")
        self.setGeometry(300, 300, 300, 300)

        t0 = time.time()
        time.sleep(0.5)
        t = int(t0 - time.time())
        self.add_l(t)
        self.update()

    def add_l(self, t):
        self.main_t = QtWidgets.QLabel(self)
        self.main_t.setText("timer")
        self.main_t.move(10+t, 10+t)
        self.main_t.adjustSize()


def app():
    a = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(a.exec_())


if __name__ == "__main__":
    app()

