import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer
import sys
from Cells import *


class MyWindow(object):

    def __init__(self, MainWindow):
        MainWindow.setWindowTitle('Evolution')
        MainWindow.resize(1100, 800)

        self.central_widget = QtWidgets.QWidget(MainWindow)

        self.grid = Grid(MainWindow)
        self.grid.setGeometry(QtCore.QRect(0, 0, ImageWidget.size[0]+1, ImageWidget.size[1]+1))
        # self.grid.setStyleSheet('background-color: rgb(134, 230, 141);')

        self.game_widget = ImageWidget(MainWindow)
        self.game_widget.setGeometry(QtCore.QRect(0, 0, ImageWidget.size[0]+1, ImageWidget.size[1]+1))

        self.play_pause_btn = QtWidgets.QPushButton(MainWindow)
        self.play_pause_btn.setGeometry(QtCore.QRect(850, 670, 200, 80))
        self.play_pause_btn.setText('Start')
        self.play_pause_btn.pressed.connect(self.play_pause)

        MainWindow.setCentralWidget(self.central_widget)
        
        self.is_started = False
        self.is_playing = False

        self.tick_duration = 1000


    def play_pause(self):
        if self.is_started:

            if self.is_playing:
                self.is_playing = False
                self.play_pause_btn.setText('Click to resume')
                self.game_widget.timer.stop()
            else:
                self.is_playing = True
                self.play_pause_btn.setText('Click to stop')
                self.game_widget.timer.start(self.tick_duration)

        else:
            self.is_started = True
            self.is_playing = True
            self.play_pause_btn.setText('Click to stop')
            self.game_widget.timer.start(self.tick_duration)




class Grid(QtWidgets.QWidget):

    def __init__(self, widget):
        super().__init__(widget)

        self.x_blocks = 50
        self.y_blocks = 50
        self.x_size = ImageWidget.size[0] // self.x_blocks
        self.y_size = ImageWidget.size[1] // self.y_blocks

    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        for row in range(self.x_blocks+1):
            painter.drawLine(row*self.x_size, 0, row*self.x_size, self.y_blocks*self.y_size)
        
        for column in range(self.y_blocks+1):
            painter.drawLine(0, column*self.y_size, self.x_blocks*self.x_size, column*self.y_size)



    
class ImageWidget(QtWidgets.QWidget):

    size = (800, 800)
    
    def __init__(self, widget):
        super().__init__(widget)
        self.data=[]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

        self.x = 100
        self.y = 100

    def tick(self):
        self.x += 10
        self.y += 10

        self.clear()
        self.data_to_draw(Circle(self.x, self.y))

        print(self.x)
    
    def data_to_draw(self, data):
        self.data.append(data)
        self.update()
    
    def clear(self):
        self.data = []
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        for object in self.data:
            object.draw(painter)


class Circle:

    def __init__(self, x=100, y=100):
        self.x = x
        self.y = y
    
    def draw(self, painter, color=0x474747):
        painter.setPen(QtGui.QColor(color))
        painter.setBrush(QtGui.QColor(color))
        painter.drawEllipse(self.x, self.y, 15, 15)


class Floor(): # тут что-то про ограничение коробки
    field = np.zeros()
    field.reshape(50, 50)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MyWindow(window)
    window.show()
    sys.exit(app.exec())