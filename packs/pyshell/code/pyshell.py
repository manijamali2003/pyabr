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

from libabr import Res
from PyQt5.QtGui import *

res = Res()

from pyqtconsole.console import PythonConsole

class MainApp(PythonConsole):
    def __init__(self,args):
        super(MainApp, self).__init__()

        self.Backend = args[0]
        self.Env = args[1]
        self.Widget = args[2]
        self.AppName = args[3]
        self.External = args[4]

        #self.Widget.Resize (700,500)
        self.Widget.Resize (self,700,500)
        self.Widget.SetWindowTitle (res.get("@string/app_name"))
        self.Widget.SetWindowIcon (QIcon(res.get('@icon/pyshell')))
        self.setStyleSheet('background-color:white;')

        self.eval_in_thread()
