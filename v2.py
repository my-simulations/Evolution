from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class MyWindow(object):

    def __init__(self, MainWindow):
        MainWindow.setWindowTitle('Evolution')
        MainWindow.resize(1100, 800)

        self.central_widget = QtWidgets.QWidget(MainWindow)

        self.game_widget = Board(self.central_widget)
        self.game_widget.setGeometry(QtCore.QRect(0, 0, 800, 800))
        self.game_widget.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.game_widget.setStyleSheet('background-color: rgb(134, 230, 141);')

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
                self.game_widget.data_to_draw(Circle()) #
            else:
                self.is_playing = True
                self.play_pause_btn.setText('Click to stop')
                self.game_widget.clear() #
        else:
            self.is_started = True
            self.is_playing = True
            self.play_pause_btn.setText('Click to stop')



class Board(QtWidgets.QWidget):
    
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
