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

import sys, os
from libabr import Files, Colors, Control, Res
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

files = Files()
colors = Colors()
control = Control()
res = Res()

# check option #
if sys.argv==[]:
    colors.show ("box",'fail',sys.argv+": option not found.")
    sys.exit(0)

# input box #
class InputDialog (QMainWindow):
    locale = control.read_record('locale','/etc/gui')
    mw = int(control.read_record('width','/etc/gui'))
    mh = int(control.read_record('height', '/etc/gui'))
    def __init__(self):
        super(InputDialog, self).__init__()

        uic.loadUi(res.get('@widget/input'),self)
        self.setStyleSheet('background-color: white;')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(int(self.mw/2-self.width()/2),int(self.mh/2-self.height()/2),self.width(),self.height())

        ## Finds ##

        self.lblInput = self.findChild(QLabel,'lblInput')
        self.leInput = self.findChild(QLineEdit, 'leInput')
        self.btnOK = self.findChild(QPushButton, 'btnOK')
        self.btnCancel = self.findChild(QPushButton,'btnCancel')
        self.btnOK.clicked.connect (self.inp)
        self.btnCancel.clicked.connect (self.cancel)

        self.lblInput.setText (control.read_record('input.title['+self.locale+"]",'/etc/configbox'))
        self.btnOK.setText (control.read_record('input.ok['+self.locale+"]",'/etc/configbox'))
        self.btnCancel.setText(control.read_record('cancel[' + self.locale + "]", '/etc/configbox'))

        self.show()

    def inp(self):
        files.write ('/proc/info/inp',self.leInput.text())
        self.close()

    def cancel (self):
        files.write('/proc/info/inp', '')
        self.close()

if sys.argv==['input']:
    appsv= QApplication([])
    w = InputDialog()
    appsv.exec_()