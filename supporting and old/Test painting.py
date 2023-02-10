from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
import time


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.startTimer(1000)
        self.title = "PyQt5 Drawing Tutorial"
        self.top= 150
        self.left= 150
        self.width = 500
        self.height = 500
        self.init_window()
        self.x_0 = 10

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    # def timerEvent(self, event):
    #     if event.timerId() == self.timer.timerId():
    #         self.update()
    #     else:
    #         super(Window, self).timerEvent(event)
    #         self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green, 8, Qt.DashLine))
        self.paint_line(painter)

    def paint_line(self, painter):
        self.x_0 += 10
        x = self.x_0
        painter.drawEllipse(x, x, 40, 40)
        # time.sleep(1)
        # self.update()
        print(x)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())