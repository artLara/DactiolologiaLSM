from PyQt5.QtWidgets import*
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

from oyente_main_ui import Ui_MainWindow
from time import sleep

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.play_button.clicked.connect(self.playButton)
        # self.pixmap = QPixmap('/home/lara/Desktop/DactiolologiaLSM/oyente/ImagenesAbecedario/a.jpg')

        # self.pixmap = QPixmap('/ImagenesAbecedario/'+'a.jpg')
        # adding image to label
        # self.image_sign.setPixmap(self.pixmap)
        # self.pixmap = QPixmap('frame0.jpg')
        # # adding image to label
        # self.image_sign.setPixmap(self.pixmap)

    def spanish2lsm(self, sentence):
        for word in sentence.split(" "):
            for letter in word:
                print(letter)
                self.pixmap = QPixmap('/home/lara/Desktop/DactiolologiaLSM/oyente/ImagenesAbecedario/'+letter+'.jpg')
                # adding image to label
                self.pixmap = self.pixmap.scaled(340, 340, QtCore.Qt.KeepAspectRatio)
                self.image_sign.setPixmap(self.pixmap)

                loop = QEventLoop()
                QTimer.singleShot(1000, loop.quit)
                loop.exec_()
            loop = QEventLoop()
            QTimer.singleShot(2000, loop.quit)
            loop.exec_()

    def playButton(self):
        msg = self.textEdit.toPlainText()
        # self.thread = Thread(target=self.spanish2lsm, args=msg)
        # self.thread.start()
        # self.thread.join()
        self.spanish2lsm(msg+" ")
        self.textEdit.setText("")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
