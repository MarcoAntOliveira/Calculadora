import sys
from PySide6.QtWidgets import (QApplication,  QLabel)
from variables import WINDOW_ICON_PATH
from main_window import MainWindow
from display import Display
from PySide6.QtGui import QIcon
from styles import setupTheme
from button import Button, ButtonGrid
from info import Info
def temp_label(texto):
    label1 = QLabel(texto)
    label1.setStyleSheet('font-size: 50px')
    return label1

if __name__ =="__main__":

    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    #define icone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    #Info
    info = Info('sua conta')
    window.addWidgetToVLayout(info)

    #display
    display = Display()
    display.setPlaceholderText("Digite Algo")
    window.addWidgetToVLayout(display)
    #grid
    buttonsGrid = ButtonGrid(display,info, window)
    window.vLayout.addLayout(buttonsGrid)

    
#
    window.adjustFixedSize()
    window.show()
    app.exec()