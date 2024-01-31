import sys
from PySide6.QtWidgets import ( QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox)


class MainWindow (QMainWindow):
    def __init__(self, parent:QWidget | None = None, *args , **kwargs ):
        super().__init__(parent, *args, **kwargs)
        #configurando o layout basico
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)
        


        # Titulo
        self.setWindowTitle('Calculadora')

        #define Icone
    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)    

    def makeMsgBox(self):
        return QMessageBox(self)