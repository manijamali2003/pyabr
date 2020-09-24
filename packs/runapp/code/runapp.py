#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Pasand team. GNU General Public License v3.0
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
from libabr import Files, Res
files = Files()
res = Res()

class MainApp(QLineEdit):
    def correct (self):
        self.setStyleSheet('background-color: white;color: black;')
        self.Widget.SetWindowTitle(res.get('@string/app_name'))
        self.setEnabled(True)
        self.clear()

    def RunApp (self):
        if files.isfile ("/usr/share/applications/"+self.text()+".desk"):
            self.Env.RunApp(self.text())
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

        ## Widget configs ##
        self.Widget.SetWindowTitle (res.get('@string/app_name'))
        self.Widget.SetWindowIcon(QIcon(res.get('@icon/runapp')))
        self.setStyleSheet('background-color:white;color: black;')
        self.Widget.Resize (600,40)
        self.setMaximumHeight(40)

        self.returnPressed.connect(self.RunApp)  # https://pythonbasics.org/pyqt/ learn it

