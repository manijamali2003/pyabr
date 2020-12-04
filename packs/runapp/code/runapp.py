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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, importlib
from libabr import Files, Res, App
files = Files()
res = Res()
app = App()

class MainApp(QLineEdit):
    def correct (self):
        self.setStyleSheet('background-color: white;color: black;')
        app.switch('runapp')
        self.Widget.SetWindowTitle(res.get('@string/app_name'))
        self.setEnabled(True)
        self.clear()

    def RunApp (self):
        command = self.text().split(' ')
        if app.exists(command[0]):
            self.Env.RunApp(command[0],command[1:])
            self.setEnabled(False)
            QTimer.singleShot(1000, self.correct)
        else:
            self.Widget.SetWindowTitle(res.get('@string/app_not_found').replace('{0}',self.text()))
            self.setStyleSheet('background-color: red;color: white;')
            self.setEnabled(False)
            QTimer.singleShot(1000, self.correct)

    def __init__(self,args):
        super(MainApp, self).__init__()

        self.Backend = args[0]
        self.Env = args[1]
        self.Widget = args[2]
        self.AppName = args[3]
        self.External = args[4]

        ## Widget configs ##
        self.Widget.SetWindowTitle (res.get('@string/app_name'))
        self.Widget.SetWindowIcon(QIcon(res.get('@icon/runner')))
        self.setStyleSheet('background-color:white;color: black;')
        self.Widget.Resize (self,600,40)
        self.returnPressed.connect(self.RunApp)  # https://pythonbasics.org/pyqt/ learn it

        f = QFont()
        f.setPointSize(12)
        self.setFont(f)

        self.Widget.DisableFloat()
