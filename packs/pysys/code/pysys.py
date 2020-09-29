#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Pasand team. GNU General Public License v3.0
#
#  Offical website:         http://itpasand.com
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/pasandteam/pyabr
#
#######################################################################################
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

import sys

from libabr import Files, Control, Permissions, Colors, Process, Modules, Package, Res

modules = Modules()
files = Files()
control = Control()
colors = Colors()
process = Process()
permissions = Permissions()
pack = Package()
res = Res()

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainApp (QWidget):
    def __init__(self,ports):
        super(MainApp, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]

        self.Widget.setStyleSheet('background-color:white;')

        self.Widget.SetWindowTitle (res.get('@string/app_name'))
        self.Widget.SetWindowIcon(QIcon(res.get('@icon/pysys')))
        self.Widget.Resize (self,850,400)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        styles = '''
        QToolButton {
            background-color: #ABCDEF;
            border-radius: 64% 64%;
        }
        QToolButton:hover {
            background-color: #123456;
            border-radius: 64% 64%;
        }
        '''

        self.btnEscape = QToolButton()
        self.btnEscape.setIconSize(QSize(128,128))
        self.btnEscape.setIcon(QIcon(res.get('@icon/pysys_escape')))
        self.btnEscape.setStyleSheet(styles)
        self.btnEscape.setFixedSize(128,128)
        self.btnEscape.clicked.connect (self.Env.escape_act)
        self.layout.addWidget(self.btnEscape)

        self.btnLock = QToolButton()
        self.btnLock.setFixedSize(128, 128)
        self.btnLock.setIconSize(QSize(128,128))
        self.btnLock.setIcon(QIcon(res.get('@icon/pysys_lock')))
        self.btnLock.setStyleSheet(styles)
        self.btnLock.clicked.connect(self.Env.lock_act)
        self.layout.addWidget(self.btnLock)

        self.btnLogout = QToolButton()
        self.btnLogout.setFixedSize(128, 128)
        self.btnLogout.setIconSize(QSize(128,128))
        self.btnLogout.setIcon(QIcon(res.get('@icon/pysys_logout')))
        self.btnLogout.setStyleSheet(styles)
        self.btnLogout.clicked.connect(self.Env.signout_act)
        self.layout.addWidget(self.btnLogout)

        self.btnRestart = QToolButton()
        self.btnRestart.setFixedSize(128, 128)
        self.btnRestart.setIconSize(QSize(128,128))
        self.btnRestart.setIcon(QIcon(res.get('@icon/pysys_restart')))
        self.btnRestart.clicked.connect(self.Env.reboot_act)
        self.btnRestart.setStyleSheet(styles)
        self.layout.addWidget(self.btnRestart)

        self.btnSuspend = QToolButton()
        self.btnSuspend.setFixedSize(128, 128)
        self.btnSuspend.setIconSize(QSize(128,128))
        self.btnSuspend.setIcon(QIcon(res.get('@icon/pysys_suspend')))
        self.btnSuspend.setStyleSheet(styles)
        self.btnSuspend.clicked.connect(self.Env.sleep_act)
        self.layout.addWidget(self.btnSuspend)

        self.btnSwitchuser = QToolButton()
        self.btnSwitchuser.setFixedSize(128, 128)
        self.btnSwitchuser.setIconSize(QSize(128,128))
        self.btnSwitchuser.setIcon(QIcon(res.get('@icon/pysys_switchuser')))
        self.btnSwitchuser.setStyleSheet(styles)
        self.btnSwitchuser.clicked.connect(self.Env.switchuser_act)
        self.layout.addWidget(self.btnSwitchuser)