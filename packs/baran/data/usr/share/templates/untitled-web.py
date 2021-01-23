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

# Your URL for your webview project 
URL = "https://google.com"

class MainApp(QMainWindow):
    def __init__(self,ports, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)
        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.Widget.SetWindowTitle ("Hello World!")
        self.Widget.SetWindowIcon (QIcon(res.get('@icon/web-browser')))
        self.Widget.Resize(self,int(self.Env.width())/1.5,int(self.Env.height())/1.5)

        self.add_new_tab(QUrl(URL), 'Homepage')

    def add_new_tab(self, qurl=None, label="Blank"):

        self.browser = QWebEngineView()
        self.browser.setUrl(qurl)

        self.setCentralWidget(self.browser)
        self.Loop()

    def Loop(self):
        self.browser.update()
        QTimer.singleShot(200,self.Loop)

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

