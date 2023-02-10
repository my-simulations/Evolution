from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class MyWindow(object):

    def __init__(self, MainWindow):
        MainWindow.setWindowTitle('Evolution')
        MainWindow.resize(1100, 800)

        self.central_widget = QtWidgets.QWidget(MainWindow)

        self.grid = Grid(self.central_widget)
        self.grid.setGeometry(QtCore.QRect(0, 0, ImageWidget.size[0]+1, ImageWidget.size[1]+1))
        self.grid.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.grid.setStyleSheet('background-color: rgb(134, 230, 141);')

        self.game_widget = ImageWidget(self.grid)
        self.game_widget.setGeometry(QtCore.QRect(0, 0, ImageWidget.size[0]+1, ImageWidget.size[1]+1))

        self.play_pause_btn = QtWidgets.QPushButton(self.central_widget)
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
    8 0 4
    7 6 5
    this is closed by mod 8
    '''

    directions = {1: (-1, -1), 2: (0, -1), 3: (1, -1), 
                    8: (-1, 0), 0: (0, 0), 4: (1, 0),
                    7: (-1, 1), 6: (0, 1), 5: (1, 1)}

    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.trend = dir % 8 #cell view direction
        self.eyes = ( (self.eye + 1) % 8, self.eye, (self.eye + 7) % 8 ) #directions that cell sees
        self.vision = [(self.x + Cell.directions[self.eyes[0]][0], self.y + Cell.directions[self.eyes[0]][1]),
                         (self.x + Cell.directions[self.eyes[1]][0], self.y + Cell.directions[self.eyes[1]][1]),
                         (self.x + Cell.directions[self.eyes[2]][0], self.y + Cell.directions[self.eyes[2]][1])] #coordinates that cell sees : [(x1,y1), (x2,y2), (x3,y3)]
    
    def move(self):
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
    sys.exit(app.exec_())
