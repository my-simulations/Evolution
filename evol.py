from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QFrame, QWidget, QPushButton, QDesktopWidget, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import random
import sys


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Evolution')
        self.setFixedWidth(1100)
        self.setFixedHeight(800)

        self.board = Board()

        self.widget = QWidget(self.board)
        self.widget.setGeometry(QRect(0,0,800,800))
        self.widget.setStyleSheet('background-color: rgb(134, 230, 141);')

        self.play_pause_btn = QPushButton(self.board)
        self.play_pause_btn.setGeometry(QRect(850, 670, 200, 80))
        self.play_pause_btn.setText('Start')
        self.play_pause_btn.clicked.connect(self.play_pause)
        

        self.setCentralWidget(self.board)
        self.board.start()

        self.show()

    
    def play_pause(self):
        timer = self.board.timer
        if timer.isActive():
            timer.stop()
            self.play_pause_btn.setText('Resume')
        else:
            timer.timeout.connect(self.board.play)
            self.play_pause_btn.setText('Pause')
            timer.start()




class Board(QFrame):

    BoardWidth = 800
    BoardHeight = 800
    Speed = 300

    def __init__(self):
        super().__init__()
        self.colors_for_drawing = {1: 0x474747}

        self.timer = QTimer()
    
    def start(self):
        self.field = np.random.randint(0, 2, size=(Board.BoardWidth, Board.BoardHeight))
        self.field[0,:] = 1
        self.field[-1,:] = 1
        self.field[:,0] = 1
        self.field[:,-1] = 1
        self.play
    
    def paintEvent(self, event):
        painter = QPainter()
        for i in range(2):
            for j in range(2):
                number = self.field[i,j]
                if number != 0:
                    painter.begin(self)
                    self.drawPoint(event, painter, number, i, j)
                    painter.end()
    def drawPoint(self, event, painter, number, x, y):

        painter.setPen(QColor(self.colors_for_drawing[number]))
        painter.drawPoint(x, y)

    
    def play(self):
        # self.paintEvent()
        

        # self.start() #test
        pass






if __name__ == "__main__":
    app = QApplication(sys.argv)
    evolution = Ui_MainWindow()
    sys.exit(app.exec_())
