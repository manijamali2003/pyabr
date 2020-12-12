#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Mani Jamali. GNU General Public License v3.0
#
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

import sys
import math
from libabr import Res
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

res = Res()

class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        style_numbtn = '''
           QToolButton {
                   background-color: white;
                   border-style: solid;
                   border-radius: 15% 15%;
                   border-color: silver;
                   border-width: 1%;
                   color: gray;
               }
           QToolButton::hover {
                   background-color: #ABCDEF;
                   border-style: solid;
                   border-radius: 15% 15%;
                   border-color: white;
                   border-width: 1%;
                   color: white;
           }
           '''
        self.setStyleSheet(style_numbtn)
        f = QFont()
        f.setPointSize(12)
        self.setFont(f)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 32)
        size.setWidth(max(size.width(), size.height()))
        return size


class Calc(QWidget):
    NumDigitButtons = 10

    style_opbtn = '''
        QToolButton {
            background-color: #ABCDEF;
            color: white;
            border-radius: 15% 15%;
        }
        QToolButton::hover {
            background-color: white;
            color: gray;
            border-color: silver;
            border-radius: 15% 15%;
            border-style: solid;
             border-width: 1%;
        }
    '''



    style_upbtn = '''
    QToolButton {
            background-color: blue;
            color: white;
            border-radius: 15% 15%;
        }
        QToolButton::hover {
            background-color: #ABCDEF;
            color: white;
            border-radius: 15% 15%;
        }
    '''

    def __init__(self,args):
        super(Calc, self).__init__()

        self.Backend = args[0]
        self.Env = args[1]
        self.Widget = args[2]

        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''

        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True

        self.display = QLineEdit(res.num('0'))
        self.display.setStyleSheet('''
        QLineEdit {
            background-color: white;
            color: gray;
            border-radius: 15% 15%;
        }
        ''')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        font = self.display.font()
        font.setPointSize(20)
        self.display.setFont(font)

        self.digitButtons = []

        for i in range(Calc.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i),
                                                       self.digitClicked))

        self.pointButton = self.createButton(".", self.pointClicked)
        self.changeSignButton = self.createButton(u"\N{PLUS-MINUS SIGN}",
                                                  self.changeSignClicked)

        self.backspaceButton = self.createButton(res.get('@string/backspace'),
                                                 self.backspaceClicked)
        self.backspaceButton.setStyleSheet(self.style_upbtn)
        self.clearButton = self.createButton(res.get('@string/clear'), self.clear)
        self.clearButton.setStyleSheet(self.style_upbtn)
        self.clearAllButton = self.createButton(res.get('@string/clearall'), self.clearAll)
        self.clearAllButton.setStyleSheet(self.style_upbtn)

        self.clearMemoryButton = self.createButton("MC", self.clearMemory)
        self.clearMemoryButton.setStyleSheet(self.style_opbtn)
        self.readMemoryButton = self.createButton("MR", self.readMemory)
        self.readMemoryButton.setStyleSheet(self.style_opbtn)
        self.setMemoryButton = self.createButton("MS", self.setMemory)
        self.setMemoryButton.setStyleSheet(self.style_opbtn)
        self.addToMemoryButton = self.createButton("M+", self.addToMemory)
        self.addToMemoryButton.setStyleSheet(self.style_opbtn)

        self.divisionButton = self.createButton(u"\N{DIVISION SIGN}",
                                                self.multiplicativeOperatorClicked)
        self.divisionButton.setStyleSheet(self.style_opbtn)
        self.timesButton = self.createButton(u"\N{MULTIPLICATION SIGN}",
                                             self.multiplicativeOperatorClicked)
        self.timesButton.setStyleSheet(self.style_opbtn)
        self.minusButton = self.createButton("-", self.additiveOperatorClicked)
        self.minusButton.setStyleSheet(self.style_opbtn)
        self.plusButton = self.createButton("+", self.additiveOperatorClicked)
        self.plusButton.setStyleSheet(self.style_opbtn)

        self.squareRootButton = self.createButton("Sqrt",
                                                  self.unaryOperatorClicked)
        self.squareRootButton.setStyleSheet(self.style_opbtn)
        self.powerButton = self.createButton(u"x\N{SUPERSCRIPT TWO}",
                                             self.unaryOperatorClicked)
        self.powerButton.setStyleSheet(self.style_opbtn)
        self.reciprocalButton = self.createButton("1/x",
                                                  self.unaryOperatorClicked)
        self.reciprocalButton.setStyleSheet(self.style_opbtn)
        self.equalButton = self.createButton("=", self.equalClicked)
        self.equalButton.setStyleSheet(self.style_opbtn)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addWidget(self.display, 0, 0, 1, 6)
        mainLayout.addWidget(self.backspaceButton, 1, 0, 1, 2)
        mainLayout.addWidget(self.clearButton, 1, 2, 1, 2)
        mainLayout.addWidget(self.clearAllButton, 1, 4, 1, 2)

        mainLayout.addWidget(self.clearMemoryButton, 2, 0)
        mainLayout.addWidget(self.readMemoryButton, 3, 0)
        mainLayout.addWidget(self.setMemoryButton, 4, 0)
        mainLayout.addWidget(self.addToMemoryButton, 5, 0)

        for i in range(1, Calc.NumDigitButtons):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3) + 1
            mainLayout.addWidget(self.digitButtons[i], row, column)

        mainLayout.addWidget(self.digitButtons[0], 5, 1)
        mainLayout.addWidget(self.pointButton, 5, 2)
        mainLayout.addWidget(self.changeSignButton, 5, 3)

        mainLayout.addWidget(self.divisionButton, 2, 4)
        mainLayout.addWidget(self.timesButton, 3, 4)
        mainLayout.addWidget(self.minusButton, 4, 4)
        mainLayout.addWidget(self.plusButton, 5, 4)

        mainLayout.addWidget(self.squareRootButton, 2, 5)
        mainLayout.addWidget(self.powerButton, 3, 5)
        mainLayout.addWidget(self.reciprocalButton, 4, 5)
        mainLayout.addWidget(self.equalButton, 5, 5)
        self.setLayout(mainLayout)

        self.Widget.SetWindowTitle(res.get("@string/app_name"))
        self.Widget.SetWindowIcon (QIcon(res.get(res.etc(self.AppName,"logo"))))

    def digitClicked(self):
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())

        if self.display.text() == res.num('0') and digitValue == 0.0:
            return

        if self.waitingForOperand:
            self.display.clear()
            self.waitingForOperand = False

        self.display.setText(self.display.text() + str(res.num(digitValue)))

    def unaryOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if clickedOperator == "Sqrt":
            if operand < 0.0:
                self.abortOperation()
                return

            result = math.sqrt(operand)
        elif clickedOperator == u"x\N{SUPERSCRIPT TWO}":
            result = math.pow(operand, 2.0)
        elif clickedOperator == "1/x":
            if operand == 0.0:
                self.abortOperation()
                return

            result = 1.0 / operand

        self.display.setText(str(res.num(result)))
        self.waitingForOperand = True

    def additiveOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            self.display.setText(res.num(str(self.factorSoFar)))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''

        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.display.setText(res.num(str(self.sumSoFar)))
        else:
            self.sumSoFar = operand

        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True

    def multiplicativeOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            self.display.setText(res.num(str(self.factorSoFar)))
        else:
            self.factorSoFar = operand

        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True

    def equalClicked(self):
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''

        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand

        self.display.setText(res.num(str(self.sumSoFar)))
        self.sumSoFar = 0.0
        self.waitingForOperand = True

    def pointClicked(self):
        if self.waitingForOperand:
            self.display.setText(res.num('0'))

        if "." not in self.display.text():
            self.display.setText(res.num(self.display.text() + "."))

        self.waitingForOperand = False

    def changeSignClicked(self):
        text = self.display.text()
        value = float(text)

        if value > 0.0:
            text = "-" + text
        elif value < 0.0:
            text = text[1:]

        self.display.setText(res.num(text))

    def backspaceClicked(self):
        if self.waitingForOperand:
            return

        text = self.display.text()[:-1]
        if not text:
            text = res.num('0')
            self.waitingForOperand = True

        self.display.setText(text)

    def clear(self):
        if self.waitingForOperand:
            return

        self.display.setText(res.num('0'))
        self.waitingForOperand = True

    def clearAll(self):
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.display.setText(res.num('0'))
        self.waitingForOperand = True

    def clearMemory(self):
        self.sumInMemory = 0.0

    def readMemory(self):
        self.display.setText(res.num(str(self.sumInMemory)))
        self.waitingForOperand = True

    def setMemory(self):
        self.equalClicked()
        self.sumInMemory = float(self.display.text())

    def addToMemory(self):
        self.equalClicked()
        self.sumInMemory += float(self.display.text())

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button

    def abortOperation(self):
        self.clearAll()
        self.display.setText("####")

    def calculate(self, rightOperand, pendingOperator):
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        elif pendingOperator == u"\N{MULTIPLICATION SIGN}":
            self.factorSoFar *= rightOperand
        elif pendingOperator == u"\N{DIVISION SIGN}":
            if rightOperand == 0.0:
                return False

            self.factorSoFar /= rightOperand

        return True

class MainApp (QMainWindow):
    def __init__(self,ports):
        super(MainApp, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.setStyleSheet(f'background-color:{res.etc(self.AppName,"bgcolor")};')
        self.Widget.Resize(self,int(res.etc(self.AppName,"width")),int(res.etc(self.AppName,"height")))
        self.calc = Calc(ports)
        self.setCentralWidget(self.calc)

        self.Widget.DisableFloat()