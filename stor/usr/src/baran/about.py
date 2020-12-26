from libabr import System, Control, Files, Colors, Script, App, Res
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

control = Control()
files = Files()
colors = Colors()
app = App()
res = Res()


class MainApp(QWidget):
    def __init__(self, ports):
        super(MainApp, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        f = QFont()
        f.setPointSize(12)

        self.Widget.Resize(self, 600, 500)
        self.Widget.SetWindowTitle(res.get('@string/app_name'))
        self.Widget.SetWindowIcon(QIcon(res.get('@icon/help-about')))
        self.vmbox = QVBoxLayout()
        self.btnInfo = QToolButton()
        self.btnInfo.setMinimumSize(128,128)
        self.btnInfo.setIconSize(QSize(128,128))
        self.btnInfo.setStyleSheet(f'background-color: #ABCDEF;border-radius: 64% 64%;margin-left: {str(int(self.width()/2.666666))}%;')
        self.btnInfo.setIcon(QIcon(res.get(control.read_record('logo','/etc/gui'))))
        self.vmbox.addWidget(self.btnInfo)
        self.extral = QWidget()
        self.vmbox.addWidget(self.extral)
        self.hbox = QHBoxLayout()
        self.setLayout(self.vmbox)
        self.extral.setLayout(self.hbox)
        self.text1 = QTextBrowser()
        self.text1.setAlignment(Qt.AlignRight)
        self.text1.append('Static hostname:\n')
        self.text1.append('Cloud software:\n')
        self.text1.append('Desktop Enviroment:\n')
        self.text1.append('Kernel:\n')
        self.text1.append('Build date:\n')
        self.text1.append('Operating System:\n')
        self.text1.append('Switched user:\n')
        self.text1.append('Interface:\n')
        self.text1.setFont(f)
        self.hbox.addWidget(self.text1)

        self.text2 = QTextBrowser()
        self.text2.append(files.readall('/proc/info/host')+"\n")
        self.text2.append(files.readall('/proc/info/cs')+' '+files.readall('/proc/info/ver')+' ('+files.readall('/proc/info/cd')+")\n")
        self.text2.append(files.readall('/proc/info/de')+"\n")
        self.text2.append(files.readall('/proc/info/kname')+" "+files.readall('/proc/info/kver')+"\n")
        self.text2.append(files.readall('/proc/info/bl')+"\n")
        self.text2.append(files.readall('/proc/info/os')+"\n")
        self.text2.append(files.readall('/proc/info/su')+"\n")
        self.text2.append(files.readall('/proc/info/inter')+"\n")
        self.text2.setAlignment(Qt.AlignLeft)
        self.text2.setFont(f)
        self.hbox.addWidget(self.text2)

        self.Widget.DisableFloat()
