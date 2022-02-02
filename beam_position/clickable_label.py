# Created by matveyev at 02.02.2022

from PyQt5 import QtWidgets, QtCore


class ClickableLabel(QtWidgets.QLabel):
    doubleClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent=parent)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()