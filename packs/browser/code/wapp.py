from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import os,subprocess
import sys,markdown

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

        if self.External==[]:
            self.add_new_tab(QUrl(URL), 'Homepage')
        else:
            if self.External[0]==None:
                self.add_new_tab(QUrl(URL), 'Homepage')
            else:
                if self.External[0].startswith ('http://') or self.External[0].startswith ('https://'):
                    self.add_new_tab(QUrl(self.External[0]), 'Homepage')

                elif self.External[0].startswith ('abr://'):
                    protocol = self.External[0].replace('abr://','/srv/')
                    prspl = protocol.split('/')
                    prspl.remove('')

                    proto = prspl[0]
                    try:
                        domain = prspl[1]
                    except:
                        domain = control.read_record('abr.default','/etc/webconfig')

                    try:
                        filename = prspl[2]
                    except:
                        filename = control.read_record('abr.index','/etc/webconfig')

                    revspl = domain.split('.')
                    revspl.reverse()

                    package = ''
                    for i in revspl:
                        package+='/'+i

                    if not files.isdir(f'/srv/{package}'):
                        result = subprocess.check_output(f'"{sys.executable}" {files.readall("/proc/info/boot")} exec /srv/com/pyabr/error/DomainNotExists', shell=True)
                        html = result.decode('utf-8')
                        self.abr(html)
                    else:
                        if files.isfile(f'/srv/{package}/{filename}.py') or files.isfile(f'/srv/{package}/{filename}.sa') or files.isfile(f'/srv/{package}/{filename}') or files.isfile(f'/srv/{package}/{filename}.exe') or files.isfile(f'/srv/{package}/{filename}.jar'):
                            result = subprocess.check_output(f'"{sys.executable}" {files.readall("/proc/info/boot")} exec /srv/{package}/{filename}',shell=True)
                            html = result.decode('utf-8')
                            self.abr(html)
                        elif files.isfile(f'/srv/{package}/{filename}.html'):
                            html = files.readall(f'/srv/{package}/{filename}.html')
                            self.abr(html)
                        elif files.isfile(f'/srv/{package}/{filename}.md'):
                            html = markdown.markdown(files.readall(f'/srv/{package}/{filename}.md'))
                            self.abr(html)
                        else:
                            result = subprocess.check_output(
                                f'"{sys.executable}" {files.readall("/proc/info/boot")} exec /srv/com/pyabr/error/PageNotFound',
                                shell=True)
                            html = result.decode('utf-8')
                            self.abr(html)
                else:
                    result = subprocess.check_output(
                        f'"{sys.executable}" {files.readall("/proc/info/boot")} exec /srv/com/pyabr/error/InvalidURL',
                        shell=True)
                    html = result.decode('utf-8')
                    self.abr(html)

    def add_new_tab(self, qurl=None, label="Blank"):

        self.browser = QWebEngineView()
        self.browser.setUrl(qurl)

        self.setCentralWidget(self.browser)
        self.Loop()

    def abr (self, data):

        self.browser = QWebEngineView()
        self.browser.setHtml(data)
        self.Widget.SetWindowTitle(self.browser.title())
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
