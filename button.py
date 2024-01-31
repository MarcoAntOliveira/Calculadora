from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber, convertToNumber
import math
from typing import TYPE_CHECKING# impede o erro de circular import
if TYPE_CHECKING:
    from display import Display
    from main_window import MainWindow
    from info  import Info


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75,75)
       

class ButtonGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: ' MainWindow' ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue =' Sua Conta'
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()
    @property
    def equation(self):
        return self._equation
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)
    def vouApagarVoce(self, *args):
        print(f"signal recebido em " ,type(self).__name__,
              args
              )    
       
    def _makeGrid (self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)
        for rowNumber, row in enumerate(self._gridMask):
            for columnNumber, text in enumerate(row):
                button = Button(text)

                if not isNumOrDot(text) and not isEmpty(text):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)
                self.addWidget(button, rowNumber, columnNumber)
                slot  = self._makeSlot(self._insertToDisplay,
                text
                )
                self._connectButtonSlot(button, slot)
    def _connectButtonSlot(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
        if text == 'C':
            self._connectButtonSlot(button, self._clear)
        if text == 'D':
            self._connectButtonSlot(
            button,
            self.display.backspace
            )
        if text == 'N':
            self._connectButtonSlot(button,self._invertNumber)
        if text in '+-/*^':
            self._connectButtonSlot(
            button,
            self._makeSlot(self._configLeftOp, text)
            )

        if text == '=':
            self._connectButtonSlot(
            button,
            self._eq
            )
        
    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)# decorator para o slot
        def realSlot(_):
            func( *args, **kwargs)
        return realSlot    
    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()
        if not isValidNumber(displayText):
            return 
        number = convertToNumber(displayText)
        self.display.setText(str(number))
        
        self.display.setText(str(number))
  
    @Slot()
    def _insertToDisplay(self,  text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return
        self.display.insert(text)
    @Slot() 
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()  
    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text() # deverá ser o _left
        self.display.clear()

        #se a pessoa clicou no operador
        # sem ter cliclado em nenhum numero antes
        if not isValidNumber(displayText) and self._left is None:
            self._showError('Voce nao digitou nada')
            return 
        
        # Se Houver algo na esquerda
        #aguardamos o numero da direita
        if self._left is None:
            self._left = float(displayText)

        self. _op = text
        self. equation = f'{self._left} {self._op}??'
    @Slot()
    def _eq(self):

        displayText = self.display.text()
        if not isValidNumber(displayText):
            self._showError('Conta imcompleta')
            return 
        if self._right  is None:
            self._right = float(displayText)
            self._left: float
        self.equation = f'{self._left} {self._op}{self._right} '  
        result = 'error'
        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left , self._right)
            else:    
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Divisao por zero')
        except OverflowError:
            self._showError('Essa conta não pode ser excutada')    
        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left= result
        self._right =  None
        if self._left == 'error':
            self._left == None

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox
    
    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()