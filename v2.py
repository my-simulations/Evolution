from PyQt6 import QtCore, QtGui, QtWidgets
import sys


class MyWindow(object):

    def __init__(self, MainWindow):
        MainWindow.setWindowTitle('Evolution')
        MainWindow.resize(1100, 800)

        self.central_widget = QtWidgets.QWidget(MainWindow)

        self.grid = Grid(MainWindow)
        self.grid.setGeometry(QtCore.QRect(0, 0, ImageWidget.size[0]+1, ImageWidget.size[1]+1))
        # self.grid.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.grid.setStyleSheet('background-color: rgb(134, 230, 141);')

        self.game_widget = ImageWidget(MainWindow)
        self.game_widget.setGeometry(QtCore.QRect(0, 0, ImageWidget.size[0]+1, ImageWidget.size[1]+1))

        self.play_pause_btn = QtWidgets.QPushButton(MainWindow)
        self.play_pause_btn.setGeometry(QtCore.QRect(850, 670, 200, 80))
        self.play_pause_btn.setText('Start')
        self.play_pause_btn.pressed.connect(self.play_pause)

        MainWindow.setCentralWidget(self.central_widget)
        
        self.is_started = False
        self.is_playing = False

    def play_pause(self):
        if self.is_started:

            if self.is_playing:
                self.is_playing = False
                self.play_pause_btn.setText('Click to resume')
                self.game_widget.data_to_draw(Circle())
            else:
                self.is_playing = True
                self.play_pause_btn.setText('Click to stop')
                self.game_widget.clear()

        else:
            self.is_started = True
            self.is_playing = True
            self.play_pause_btn.setText('Click to stop')


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


class Cell:
    '''
    in progress

    directions:
    1 2 3
    0 8 4
    7 6 5
    this is closed by mod 8
    '''

    directions = {1: (-1, -1), 2: (0, -1), 3: (1, -1), 
                    0: (-1, 0), 8: (0, 0), 4: (1, 0),
                    7: (-1, 1), 6: (0, 1), 5: (1, 1)}

    def __init__(self, x, y, dir, type, energy):
        self.energy = energy
        self.type = type
        self.x = x
        self.y = y
        self.trend = dir % 8 #cell view direction
        self.eyes = ((self.trend + 1) % 8, self.trend, (self.trend + 7) % 8) #directions that cell sees
        self.vision = [(self.x + Cell.directions[self.eyes[0]][0], self.y + Cell.directions[self.eyes[0]][1]),
                         (self.x + Cell.directions[self.eyes[1]][0], self.y + Cell.directions[self.eyes[1]][1]),
                         (self.x + Cell.directions[self.eyes[2]][0], self.y + Cell.directions[self.eyes[2]][1])] #coordinates that cell sees : [(x1,y1), (x2,y2), (x3,y3)]
    
    def move(self):
        self.energy -= 1
        self.x = self.vision[1][0]
        self.y = self.vision[1][1]



    def rotate(self, direction):
        self.trend = direction % 8  # cell view direction
        self.eyes = ((self.trend + 1) % 8, self.trend, (self.trend + 7) % 8)  # directions that cell sees
        self.vision = [(self.x + Cell.directions[self.eyes[0]][0], self.y + Cell.directions[self.eyes[0]][1]),
                       (self.x + Cell.directions[self.eyes[1]][0], self.y + Cell.directions[self.eyes[1]][1]),
                       (self.x + Cell.directions[self.eyes[2]][0], self.y + Cell.directions[self.eyes[2]][1])]  # coordinates that cell sees : [(x1,y1), (x2,y2), (x3,y3)]


    def photosynthesis(self):
        self.energy += 1


    def eat(self, other_cell):
        self.energy += other_cell.energy



class Floor(): # тут что-то про ограничение коробки
    pass

class Circle:

    def __init__(self):
        self.x = 100
        self.y = 100
    
    def draw(self, painter):
        painter.setPen(QtGui.QColor(0x474747))
        painter.setBrush(QtGui.QColor(0x474747))
        painter.drawEllipse(self.x, self.y, 20, 20)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MyWindow(window)
    window.show()
    sys.exit(app.exec())
