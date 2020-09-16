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

from libabr import Res

res = Res()

from pyqtconsole.console import PythonConsole

class MainApp(PythonConsole):
    def __init__(self,args):
        super(MainApp, self).__init__()

        self.Backend = args[0]
        self.Env = args[1]
        self.Widget = args[2]

        self.Widget.resize (700,500)
        self.Widget.setWindowTitle (res.get("@string/app_name"))
        self.setStyleSheet('background-color:white;')

        self.eval_in_thread()