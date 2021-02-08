from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import os
import sys

from libabr import Res, Control, Files

res = Res()
control = Control()
files = Files()

class MainApp(QMainWindow):
    def RunGap (self):
        self.Widget.close()
        self.Env.RunApp('wapp', ['https://web.gap.im'])

    def __init__(self,ports, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.Widget.SetWindowTitle (res.get('@string/app_name'))
        self.Widget.SetWindowIcon(QIcon(res.get(res.etc(self.AppName,"logo"))))
        self.Widget.Resize(self,560,390)
        self.setStyleSheet(f'background-image: url({res.get("@image/about_bg")});')

        QTimer.singleShot(3000,self.RunGap)

