import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer
import sys
from classes import *
from random import randint


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
        self.play_pause_btn.setGeometry(QtCore.QRect(866, 670, 200, 80))

        self.play_pause_btn.setText('Start')
        self.play_pause_btn.pressed.connect(self.play_pause)

        MainWindow.setCentralWidget(self.central_widget)
        
        self.is_started = False
        self.is_playing = False

        self.tick_duration = 200

        self.game_field = Field()
        self.list_of_cells = []
        for i in range(8):
            self.list_of_cells.append(Herbivore(randint(1, 50), randint(1, 50), randint(0, 7), randint(5, 30)))
        for i in range(2):
            self.list_of_cells.append(Predator(randint(1, 50), randint(1, 50), randint(0, 7), randint(5, 30)))

        # for i in range(1):
        #     self.list_of_cells.append(Herbivore(1, 1, 3, 40))

        for i in self.list_of_cells:
            self.game_field.cell_born(i.type, i.x, i.y, i.trend)


    def play_pause(self):
        if self.is_started:

            if self.is_playing:
                self.is_playing = False
                self.play_pause_btn.setText('Click to resume')
                self.game_widget.timer.stop()
                # self.manager(0)
            else:
                self.is_playing = True
                self.play_pause_btn.setText('Click to stop')
                self.game_widget.timer.start(self.tick_duration)
                # self.manager(1)

        else:
            self.is_started = True
            self.is_playing = True
            self.play_pause_btn.setText('Click to stop')
            self.game_widget.timer.start(self.tick_duration)
            # self.manager(1)

    def manager(self):
        # print("man strt")
        i = 0
        cur_lenght = len(self.list_of_cells)
        # print(i, cur_lenght)
        while i < cur_lenght:
            # print('before')
            self.list_of_cells[i].get_vision_from_direction(self.list_of_cells[i].trend)
            self.list_of_cells[i].get_objects_for_vision(self.game_field.get_info()[:, :, 0])
            # print('after')
            decision = self.list_of_cells[i].step(self.game_widget.time)
            print(decision[0])
            print(self.list_of_cells[i].x, self.list_of_cells[i].y, self.list_of_cells[i].trend)
            print(self.list_of_cells[i].vision, self.list_of_cells[i].near_objects)
            # print('t, dec', self.game_widget.time, decision)
            # print('decis iter start')
            # print('decision', decision)
            if decision[0] == 'eat':
                t = decision[1]
                coords = decision[2]
                for k in self.list_of_cells:
                    if k.x == coords[2] and k.y == coords[3]:
                        self.list_of_cells.remove(k)
                        i -= 1
                        cur_lenght -= 1
                self.game_field.cell_step(t, coords[0], coords[1], coords[2], coords[3])
            elif decision[0] == 'reproduction':
                t = decision[1]
                coords = decision[2]
                self.game_field.cell_born(coords[0], coords[1], coords[2], coords[3])
                if coords[0] == 2:
                    self.list_of_cells.append(Herbivore(coords[1], coords[2], coords[3], coords[4]))
                else:
                    self.list_of_cells.append(Predator(coords[1], coords[2], coords[3], coords[4]))
            elif decision[0] == 'move':
                t = decision[1]
                coords = decision[2]
                self.game_field.cell_step(t, coords[0], coords[1], coords[2], coords[3])
                # print('move 3', i, cur_lenght)
            elif decision[0] == 'rotate':
                t = decision[1]
                coords = decision[2]
                self.game_field.rotate(coords[0], coords[1], coords[3])
                # print('none')
            else:
                pass
            self.list_of_cells[i].get_vision_from_direction(self.list_of_cells[i].trend)
            self.list_of_cells[i].get_objects_for_vision(self.game_field.get_info()[:, :, 0])
            i += 1

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


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

        self.time = 0
        self.x = 24
        self.y = 24

    def tick(self):
        self.time += 1

        print('time =', self.time)

        self.clear()
        self.data_to_draw()

        ui.manager()

        # print(self.x)
    
    def data_to_draw(self):
        self.data = ui.game_field.get_info()
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
                if self.data[x][y][0] == 1:
                    Square(x, y).draw(painter, 0x474747)
                elif self.data[x][y][0] == 2:
                    Circle(x, y, self.data[x][y][1]).draw(painter, 0x33FF33)
                elif self.data[x][y][0] == 3:
                    Circle(x, y, self.data[x][y][1]).draw(painter, 0xFF3300)




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
                         self.x+6 + round(6*np.cos(np.pi/8*self.direction)),
                         self.y+6 + round(6*np.sin(np.pi/8*self.direction)))



class Field:
    def __init__(self):
        self.field = np.zeros((52, 52, 2))
        # 0 - floor, 1 - wall, 2 - herbivore, 3 - predator
        self.field[0, :, 0] = 1
        self.field[:, 0, 0] = 1
        self.field[-1, :, 0] = 1
        self.field[:, -1, 0] = 1

    def cell_step(self, type, x_start, y_start, x_finish, y_finish):
        dir = self.field[x_start, y_start, 1]
        self.field[x_start, y_start] = [0, 0]
        self.field[x_finish, y_finish] = [type, dir]

    def cell_born(self, type, x_finish, y_finish, dir):
        self.field[x_finish, y_finish] = [type, dir]

    def rotate(self, x_start, y_start, dir):
        self.field[x_start, y_start, 1] = dir

    def get_info(self):
        return self.field




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MyWindow(window)
    window.show()
    sys.exit(app.exec()) #
