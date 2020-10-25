from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys, importlib
from libabr import System, App, Control, Files, Res

res = Res();files = Files();app = App();control=Control()

class MainApp(QtWidgets.QMainWindow):
    def __init__(self,args):
        super(MainApp, self).__init__()

        # ports
        self.Backend = args[0]
        self.Env = args[1]
        self.Widget = args[2]
        self.AppName = args[3]
        self.External = args[4]

        # resize
        self.Widget.Resize (self,700,500)
        self.Widget.SetWindowTitle(res.get('@string/app_name'))
        self.Widget.SetWindowIcon (QtGui.QIcon(res.get('@icon/barge')))

        # text box
        self.teEdit = QtWidgets.QTextEdit()
        self.setCentralWidget(self.teEdit)

        # set font size
        f = QtGui.QFont()
        f.setPointSize(12)
        self.teEdit.setFont(f)