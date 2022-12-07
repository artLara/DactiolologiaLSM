# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dactiolologia_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(904, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.translate = QtWidgets.QLabel(self.centralwidget)
        self.translate.setGeometry(QtCore.QRect(20, 390, 341, 51))
        self.translate.setObjectName("translate")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(400, 430, 491, 61))
        self.textEdit.setObjectName("textEdit")
        self.delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_button.setGeometry(QtCore.QRect(150, 480, 89, 25))
        self.delete_button.setObjectName("delete_button")
        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(550, 510, 89, 25))
        self.play_button.setObjectName("play_button")
        self.live_sign = QtWidgets.QLabel(self.centralwidget)
        self.live_sign.setGeometry(QtCore.QRect(40, 80, 321, 291))
        self.live_sign.setObjectName("live_sign")
        self.image_sign = QtWidgets.QLabel(self.centralwidget)
        self.image_sign.setGeometry(QtCore.QRect(400, 40, 481, 381))
        self.image_sign.setObjectName("image_sign")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 904, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.translate.setText(_translate("MainWindow", "TextLabel"))
        self.delete_button.setText(_translate("MainWindow", "Borrar"))
        self.play_button.setText(_translate("MainWindow", "Play"))
        self.live_sign.setText(_translate("MainWindow", "<html><head/><body><p>LiveSign</p><p><br/></p></body></html>"))
        self.image_sign.setText(_translate("MainWindow", "<html><head/><body><p>LiveSign</p><p><br/></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
