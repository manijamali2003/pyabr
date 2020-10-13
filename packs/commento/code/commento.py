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

# very basic terminal emulator in pyqt
# https://pythonbasics.org/pyqt/

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os
import subprocess
from libabr import Res, System, Files, Control, Process, App

res = Res()
files = Files()
process = Process()
control = Control()
app = App()

class MainApp(QtWidgets.QMainWindow):
    def __init__(self,ports):
        super(MainApp, self).__init__()
        uic.loadUi(res.get('@layout/commento'), self)

        self.setStyleSheet('background-color: black;color: white;')

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]

        self.Widget.Resize(self,700, 500)

        self.Widget.SetWindowTitle(res.get("@string/app_name"))

        ## Set Icon ##
        self.Widget.SetWindowIcon(QIcon(res.get('@icon/commento')))

        self.switch = process.processor()  # Switch the process
        process.check(self.switch)  # Check the switched process

        if self.switch == None:
            switch = 0

        files.write("/proc/info/sel", "/proc/" + str(self.switch))
        self.select = files.readall("/proc/info/sel")

        self.lineEdit.returnPressed.connect(self.doCMD)
        # self.pushButtonInstall.clicked.connect(self.onClick)

    def doCMD(self):
        cmd = self.lineEdit.text()
        self.lineEdit.setText("")


        ## Prompt data base ##

        show_username = control.read_record("show_username", "/etc/prompt")
        show_hostname = control.read_record("show_hostname", "/etc/prompt")
        show_path = control.read_record("show_path", "/etc/prompt")
        root_symbol = control.read_record("root", "/etc/prompt")
        user_symbol = control.read_record("user", "/etc/prompt")

        ## Setting up prompt data base 2 ##

        color_uh = ""
        color_path = ""
        prompt_symbol = ""

        if self.Env.username == "root":
            prompt_symbol = root_symbol
        else:
            prompt_symbol = user_symbol

        ## Setting up space of prompt ##

        if show_username == "Yes":
            space_username = self.Env.username
        else:
            space_username = ""

        if show_hostname == "Yes":
            space_hostname = files.readall('/proc/info/host')
        else:
            space_hostname = ""

        if show_path == "Yes":
            space_path = files.readall("/proc/info/pwd")
        else:
            space_path = ""

        if show_hostname == "Yes" and show_username == "Yes":
            space1 = "@"
        else:
            space1 = ""

        if (show_hostname == "Yes" or show_username == "Yes") and show_path == "Yes":
            space2 = ":"
        else:
            space2 = ""

        strcmdln = ''
        for i in cmd.split(" "):
            if str(i).startswith("$"):
                select = files.readall("/proc/info/sel")
                var = control.read_record(str(i).replace("$",""),select)
                if var==None:
                    strcmdln = strcmdln + " " + i
                else:
                    strcmdln = strcmdln + " " + var
            else:
                strcmdln = strcmdln + " " + i

        ## Process ##
        files.write ('/proc/info/su',self.Env.username)
        lastsel = files.readall('/proc/info/sel')
        if lastsel.startswith('/proc/'):
            files.write ('/proc/info/sel',self.select)
        files.write ('/proc/info/sp',str(self.switch))

        cmd = strcmdln

        if cmd==" shut":
            files.remove ('/proc/'+str(self.switch))
            self.Widget.close()
        elif cmd==" new":
            self.Env.RunApp('commento')
        elif cmd==" clear":
            self.textBrowser.clear()
        elif cmd==" shutdown":
            self.Env.escape_act()
        elif cmd==" reboot":
            self.Env.reboot_act()
        elif cmd==" logout":
            self.Env.signout_act()
        elif cmd.startswith(' #') or cmd.startswith(" ;") or cmd.startswith(" //") or (cmd.startswith(" /*")and cmd.endswith("*/")):
            pass
        elif cmd=='' or cmd==' ' or cmd=='  ':
            pass
        else:
            result = subprocess.check_output('"{0}" '.replace('{0}',sys.executable)+files.readall('/proc/info/boot')+' exec '+cmd,shell=True)
            self.textBrowser.setText(self.textBrowser.toPlainText() + ""+ space_username + space1 + space_hostname + space2  + space_path + prompt_symbol + cmd +"\n\n"+ result.decode("utf-8")+'\n')
            self.Widget.SetWindowTitle(space_username + space1 + space_hostname + space2 )
            self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())