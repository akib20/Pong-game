# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:13:48 2018

@author: Akib
"""

import sys
import time
import random
import winsound
import threading

from PyQt5.QtGui import QPainter, QColor, QImage, QPalette, QBrush,QFont, QIcon
from PyQt5.QtCore import Qt, QPoint, QBasicTimer, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow,QPushButton,QMessageBox 


# Keypad of the board
RIGHT = Qt.Key_Right
LEFT = Qt.Key_Left
UP = Qt.Key_Up 
DOWN = Qt.Key_Down



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # Setting the title and icon for main game window
        self.setWindowTitle('Pong')
        self.setWindowIcon(QIcon('pong.png'))

        # Background image
        oImage = QImage("test.png") 
        
        # Set the window size e.g. height and width               
        sImage = oImage.scaled(QSize(500,500))  
        palette = QPalette() 
        palette.setBrush(10, QBrush(sImage))          
        self.setPalette(palette)
        self.resize(500, 500)
        
        # Setting the size, position, font and color of the Pushbutton 
        btn1 = QPushButton('Play Games', self) 
        btn1.move(400, 350)  
        btn1.resize(100,50) 
        btn1.setStyleSheet("background-color: gray")
        btn1.setFont(QFont('SansSerif', 12))
        btn1.clicked.connect(self.openSecond)
        
        
        btn2 = QPushButton('Close', self)
        btn2.move(400, 450)
        btn2.resize(100,50)
        btn2.setStyleSheet("background-color: gray")
        btn2.setFont(QFont('SansSerif', 12))
        btn2.clicked.connect(self.CloseApp)

        
        btn3 = QPushButton('Help', self)
        btn3.move(400, 400)
        btn3.resize(100,50)
        btn3.setStyleSheet("background-color: gray")
        btn3.setFont(QFont('SansSerif', 12))
        btn3.clicked.connect(self.openHelp)
        
    
    def openSecond(self):
        # Opening Second Page 
        self.SW = App()
        self.SW.show()
      
    def CloseApp(self):
        # Closing the game
        reply = QMessageBox.question(self,"Close Message","Are You Sure to Close Window",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            

    
    def openHelp(self):
         # Opening help page        
         self.WW = Help()
         self.WW.show()
        
class Help(QMainWindow):
    
    # Setting the window size e.g. height and width   
    def __init__(self):
        super().__init__() 
        self.title = "Help"
        self.setWindowIcon(QIcon('help.png'))
        self.left = 435
        self.top = 115
        self.width = 500
        self.height = 500
        self.widget()

    def widget(self):
        
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFont(QFont('SansSerif', 12))
                
        #Setting the background image 
        oImage = QImage("test.png")
        sImage = oImage.scaled(QSize(500,500))                 
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))                   
        self.setPalette(palette)
        self.resize(500, 500)
        
        #Instruction
        label1 = QLabel("For Moving Left, press LEFT KEY", self)
        label1.resize(400, 30)

        label2 = QLabel("For Moving Right, press RIGHT KEY", self)
        label2.resize(400, 80)

        label3 = QLabel("For Stoping the paddle, press DOWN KEY", self)
        label3.resize(400, 130)

        label4 = QLabel("For Slow Motion, press UP KEY", self)
        label4.resize(400, 180)
        
        label5 = QLabel("For Going Back to Main Window, press ESCAPE", self)
        label5.resize(400, 230)
        
        label6 = QLabel("For Pausing, press SPACE or P", self)
        label6.resize(400, 280)
        
        self.show()
    
    
    
 
class App(QWidget):
    
    # Setting the User Interface, layout, scorce
    def __init__(self):
        super().__init__()
        self.padding = 500
        self.highScore = 0
        self.time = QBasicTimer()

        self.UI()
        self.start()
        

    
    def UI(self):
        
        # Setting the icon, background image, score  
        self.setWindowTitle('Pong')
        self.setFixedSize(self.padding, self.padding)
        self.setWindowIcon(QIcon('pong.png'))
        
        oImage = QImage("test.png")
        sImage = oImage.scaled(QSize(500,500))                 
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))                   
        self.setPalette(palette)
        
        
        self.scoreLabel = QLabel('Score: 000', self)
        self.scoreLabel.move(390,0)
        self.scoreLabel.setFont(QFont('SansSerif', 12))
        
        self.highScoreLabel = QLabel('Highscore: 000', self)
        self.highScoreLabel.move(390,15)
        self.highScoreLabel.setFont(QFont('SansSerif', 12))
        
        
        self.show()
        

        

    
    def paintEvent(self, e):
        
        # Setting paint color using painter
        painter = QPainter()
        painter.begin(self)
        self.paintBoard(painter)
        self.paintBall(painter)
        painter.end()
        
    def keyPressEvent(self, e):
        
        # Setting the key
        pressed = e.key()
        
        if pressed in (Qt.Key_P, Qt.Key_Space):
            self.pause()
        
        if self.paused:
            return

        if pressed == Qt.Key_Escape:
            self.pause()
            self.close()
        
        elif pressed in (DOWN, RIGHT, LEFT):
            self.direction = pressed
        
        elif pressed == UP:
            self.speedingBall()
        
        
            
    def start(self):
        
        # Starting the game after 20 microsecond
        self.time.start(20, self)

 
        mid = self.padding/2
        self.score = 0
        self.speed = 0
        
        # Setting the ball in the middle
        self.ball = QPoint(mid, mid)
    
        # Setting the ball direction
        x = random.choice([x for x in range(-2,3) if x])
        self.dirOfBall = QPoint(x, 3)

        self.pos = mid - 50
        self.direction = DOWN
        self.paused = False

        self.repaint()
        
    def pause(self):
        
        # Pausing the game
        if self.paused:
            self.paused = False
            self.time.start(20, self)
        else:
            self.paused = True
            self.time.stop()
   
    def speedingBall(self):
        
        # Increasing the speed
        if self.speed:
            self.speed = 0
            self.dirOfBall *= 0.5
            return
        self.dirOfBall *= 2
        self.speed = 1            
            
    def latestScore(self):
        
        # Updating the score
        self.scoreLabel.setText('Score: {}'.format(str(self.score).zfill(3)))
        
        if self.score > self.highScore:
            self.highScore = self.score
        
        self.highScoreLabel.setText('Highscore: {}'.format(str(self.highScore).zfill(3)))

        
    def paintBoard(self, painter):
        
        # Painting the board
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(self.pos, self.padding-60, 100, 10)

    def paintBall(self, painter):
        
        # Painting the ball
        painter.setBrush(QColor(51, 255, 51))
        painter.drawEllipse(self.ball, 6, 6)
     
    def kill(self):
        
        # After unsuccessful attempt, the game starts again
        self.time.stop()
        self.score = 0
        self.latestScore()
        time.sleep(0.5)
        self.start()
    
    def hitBoard(self):
        
        # After touching the board and the ball will go up  
        if self.padding-50 >= self.ball.y() + 6 >= self.padding-60:
            if self.pos <= self.ball.x() <= self.pos + 100:
                self.score += 1
                self.latestScore()
                
                
                soundThread = threading.Thread(target=self.playSound, args = ('circle.wav',))
                soundThread.start()
                return True
        return False
        
    def hitWall(self):
        
        # Hitting the wall and sending the details of the direction
        direction = False
         
        if self.ball.y() - 6 <= 0:
            direction = UP
        elif self.ball.y() + 6 >= self.padding:
            direction = DOWN
        elif self.ball.x() + 6 >= self.padding:
            direction = RIGHT
        elif self.ball.x() - 6 <= 0:
            direction = LEFT
            
        # Making sound when hit any side of the walls
        if direction != False:
            soundThread = threading.Thread(target=self.playSound, args = ('cross.wav',))
            soundThread.start()
           
        return direction
   
    
    def playSound(self, nameOfFile):
        
        # Playing the sound
        winsound.PlaySound(nameOfFile, winsound.SND_FILENAME)
        
    def timerEvent(self, e):
        
        # Changing the direction of the board
        if self.direction == RIGHT and self.pos < self.padding-100:
            self.pos += 6
        elif self.direction == LEFT and self.pos > 0:
            self.pos -= 6

        
        strike = self.hitWall()
        
        # Increasing the speed
        speed = self.speed + 1
        
        
        if strike:
            
            # Inrease the speed of the ball
            if strike == LEFT:
                self.dirOfBall.setX(random.randint(2, 4)*speed)
            elif strike == UP:
                self.dirOfBall.setY(random.randint(2, 4)*speed)           
            elif strike == RIGHT:
                self.dirOfBall.setX(random.randint(2, 4)*-1*speed)
            elif strike == DOWN:
                self.kill()
        
        if self.hitBoard():
            self.dirOfBall.setY(random.randint(2, 4)*-1*speed)
        
        
        self.ball += self.dirOfBall
        
        
        self.repaint()
        
if __name__ == "__main__":
     def run_app():   
        app = QApplication(sys.argv)
        ex = MainWindow()
        ex.show()
        app.exec()
     run_app() 
            

    
            
        

