import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer
import sys
from Cells import *


class MyWindow(object):

    def __init__(self, MainWindow):
        MainWindow.setWindowTitle('Evolution')
        MainWindow.resize(1100, 850)

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

        self.x_blocks = 52
        self.y_blocks = 52
        self.x_size = ImageWidget.size[0] // self.x_blocks
        self.y_size = ImageWidget.size[1] // self.y_blocks

    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        for row in range(self.x_blocks+1):
            painter.drawLine(row*self.x_size, 0, row*self.x_size, self.y_blocks*self.y_size)
        
        for column in range(self.y_blocks+1):
            painter.drawLine(0, column*self.y_size, self.x_blocks*self.x_size, column*self.y_size)



    
class ImageWidget(QtWidgets.QWidget):

    size = (832, 832)
    
    def __init__(self, widget):
        super().__init__(widget)

        self.data = []
        self.game_field = Field()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

        self.time = 0
        self.x = 1
        self.y = 1

    def tick(self):
        self.x += 1
        self.y += 1
        self.time += 1

        print(self.time)

        self.game_field.cell_step(2, self.x - 1, self.y - 1, self.x, self.y)
        self.clear()
        self.data_to_draw()

        print(self.x)
    
    def data_to_draw(self):
        self.data = self.game_field.get_info()
        self.update()
    
    def clear(self):
        self.data = []
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        for x in range(len(self.data)):
            for y in range(len(self.data)):
                # if self.data[x][y] == 0:
                #     Square(x, y).draw(painter, 0x009)
                if self.data[x][y] == 1:
                    Square(x, y).draw(painter, 0x474747)
                elif self.data[x][y] == 2:
                    Circle(x, y, 3).draw(painter, 0x090)
                elif self.data[x][y] == 3:
                    Circle(x, y, 3).draw(painter, 0x474747)




class Square:
    def __init__(self, x=100, y=100):
        self.x = x * 16
        self.y = y * 16

    def draw(self, painter, color=0x474747):
        painter.setPen(QtGui.QColor(color))
        painter.setBrush(QtGui.QColor(color))
        painter.drawRect(self.x, self.y, 14, 14)

class Circle:

    def __init__(self, x, y, direction):
        self.x = x * 16 + 2
        self.y = y * 16 + 2
        self.direction = direction
    
    def draw(self, painter, color=0x474747):
        painter.setPen(QtGui.QColor(color))
        painter.setBrush(QtGui.QColor(color))
        painter.drawEllipse(self.x, self.y, 12, 12)

        painter.setPen(QtGui.QColor(0x009))
        painter.setBrush(QtGui.QColor(0x009))
        painter.drawLine(self.x+6, self.y+6,
                         self.x+6 + round(6*np.cos(np.pi/8*self.direction)), self.y+6 + round(6*np.sin(np.pi/8*self.direction)))



class Field:
    def __init__(self):
        self.field = np.zeros(2704)
        self.field = self.field.reshape(52, 52)
        # 0 - floor, 1 - wall, 2 - herbivore, 3 - predator
        self.field[0, :] = np.array([1]*52)
        self.field[:, 0] = np.array([1]*52)
        self.field[-1, :] = np.array([1]*52)
        self.field[:, -1] = np.array([1]*52)

    def cell_step(self, type, x_start, y_start, x_finish, y_finish):
        self.field[x_start, y_start] = 0
        self.field[x_finish, y_finish] = type

    def get_info(self):
        return self.field




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MyWindow(window)
    window.show()
    sys.exit(app.exec()) #
