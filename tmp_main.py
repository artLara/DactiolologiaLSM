from Visor import Visor
import PyQt5.QtCore as QtCore, PyQt5.QtGui as QtGui, PyQt5.QtWidgets as QtWidgets
import sys
import os

app = QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
main=Visor()
main.show()
main.iniciar()
sys.exit(app.exec_())
