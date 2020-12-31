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

# very basic terminal emulator in pyqt
# https://pythonbasics.org/pyqt/

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os, hashlib
import subprocess
from libabr import Res, System, Files, Control, Process, App, Commands

res = Res()
files = Files()
process = Process()
control = Control()
app = App()
commands = Commands()

class MainApp(QtWidgets.QMainWindow):
    username = ''
    password = ''
    confirm = ''
    def __init__(self,ports):
        super(MainApp, self).__init__()
        #uic.loadUi(res.get('@layout/commento'), self)

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.Widget.Resize(self,int(res.etc(self.AppName,"width")), int(res.etc(self.AppName,"height")))

        self.Widget.SetWindowTitle(res.get("@string/app_name"))
        self.Widget.DisableFloat()

        ## Set Icon ##
        self.Widget.SetWindowIcon(QIcon(res.get(res.etc(self.AppName,"logo"))))

        self.switch = process.processor()  # Switch the process
        process.check(self.switch)  # Check the switched process

        if self.switch == None:
            switch = 0

        files.write("/proc/info/sel", "/proc/" + str(self.switch))
        self.select = files.readall("/proc/info/sel")

        self.textBrowser = QTextBrowser()
        self.textBrowser.setStyleSheet(f'background-color:{res.etc(self.AppName,"bgcolor")};color:{res.etc(self.AppName,"fgcolor")};')
        self.textBrowser.setGeometry(0,0,self.width(),self.height()-40)
        f = QFont()
        f.setFamily('DejaVu Sans Mono')
        f.setPointSize(int(res.etc(self.AppName,"fontsize")))
        self.textBrowser.setFont(f)
        self.layout().addWidget(self.textBrowser)
        self.lineEdit = QLineEdit()
        f = QFont()
        f.setFamily('Monospace')
        f.setPointSize(11)
        self.lineEdit.setFont(f)
        self.lineEdit.setGeometry(0,self.height()-40,self.width(),40)

        self.layout().addWidget(self.lineEdit)

        self.lineEdit.returnPressed.connect(self.doCMD)

        if not self.External==None:
            self.lineEdit.hide()
            self.lineEdit.setStyleSheet('background-color: black;color: black;')
            result = subprocess.check_output(
                '"{0}" '.replace('{0}', sys.executable) + files.readall('/proc/info/boot') + ' exec ' + self.External[0], shell=True)
            self.textBrowser.setText(
                self.textBrowser.toPlainText() + "" + result.decode(
                    "utf-8") + '\n')
            self.Widget.SetWindowTitle(self.External[1])
            self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())

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
            self.Env.RunApp('commento',None)
        elif cmd==" clear":
            self.textBrowser.clear()
        elif cmd==" shutdown":
            self.Env.escape_act()
        elif cmd==" reboot":
            self.Env.reboot_act()
        elif cmd==" logout":
            self.Env.signout_act()
        elif cmd.startswith(' su'):
            split = cmd.split(' ')
            split.remove('')

            self.Env.switchuser_act()

        elif cmd.startswith(' uadd'):
            split = cmd.split(' ')
            split.remove('')

            if split == []:
                self.Env.RunApp('input', ['Pick a username', self._user_uadd])
            else:
                self._user_uadd(split[1])

        elif cmd.startswith(' udel'):
            split = cmd.split(' ')
            split.remove('')

            if split == []:
                self.Env.RunApp('input', ['Enter an username', self._user_del])
            else:
                self._user_del(split[1])

        elif cmd.startswith(' read'):
            split = cmd.split(' ')
            split.remove('')

            if split==[]:
                self.Env.RunApp('input', ['Enter a variable name', self._in])
            else:
                self._in(split[1])

        elif cmd.startswith(' @'):
            command = cmd.replace(' @','').split(' ')
            if app.exists(command[0]):
                self.Env.RunApp(command[0], command[1:])
        elif cmd.startswith(' #') or cmd.startswith(" ;") or cmd.startswith(" //") or (cmd.startswith(" /*")and cmd.endswith("*/")) or cmd=='' or cmd==' ' or cmd=='  ':
            self.textBrowser.setText(self.textBrowser.toPlainText() + "" + prompt_symbol + cmd + "\n")
            self.Widget.SetWindowTitle(space_username + space1 + space_hostname + space2)
            self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())
        else:
            result = subprocess.check_output('"{0}" '.replace('{0}',sys.executable)+files.readall('/proc/info/boot')+' exec '+cmd,shell=True)
            self.textBrowser.setText(self.textBrowser.toPlainText() + ""+prompt_symbol + cmd +"\n\n"+ result.decode("utf-8")+'\n\n')
            self.Widget.SetWindowTitle(space_username + space1 + space_hostname + space2 )
            self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())

        self.Widget.DisableFloat()

    def _user_uadd (self,username):
        if files.isfile(f'/etc/users/{username}'):
            self.Env.RunApp('text',['User exists', f'Cannot create {username} user account; because this user has already exists.'])
        elif username=='guest':
            self.Env.RunApp('text', ['Guest Account',
                                     f'Cannot create user account with guest name; because this user is a guest account.'])
        elif username=='root':
            self.Env.RunApp('text', ['Super Account',
                                     f'Cannot create user account with root name; because this user is a super account.'])
        else:
            self.username = username
            control.write_record('input.password_hint','Yes','/etc/configbox')
            self.Env.RunApp('input', ['Choose your a new password', self._user_uadd_passwd])

    def _user_uadd_passwd (self,password):
        self.password = password
        self.Env.RunApp('input', ['Confirm your password', self._user_uadd_passwd_confirm])
        control.write_record('input.password_hint', 'No', '/etc/configbox')

    def _user_uadd_passwd_confirm (self,confirm):
        if not self.password==confirm:
            self.Env.RunApp('text', ['Not match',
                                     f'Your new password and your confirm password are not match.'])
        else:
            hashname = hashlib.sha3_256(str(self.username).encode()).hexdigest()
            hashcode = hashlib.sha3_512(str(self.password).encode()).hexdigest()

            files.create("/etc/users/" + self.username)
            control.write_record("username", hashname, '/etc/users/' + self.username)
            control.write_record("code", hashcode, '/etc/users/' + self.username)
            control.write_record('/desk/' + self.username, "drwxr-x---/" + self.username, '/etc/permtab')

            self.Env.RunApp('text', ['Successfully created',
                                     f'Your new user with {self.username} successfully created.'])

    def _user_del (self,username):
        if not files.isfile(f'/etc/users/{username}'):
            self.Env.RunApp('text', ['User not found',
                                     f'Cannot remove {username} user account; because this user not found.'])
        elif username == 'guest':
            self.Env.RunApp('text', ['Guest Account',
                                     f'Cannot remove user account with guest name; because this user is a guest account.'])
        elif username == 'root':
            self.Env.RunApp('text', ['Super Account',
                                     f'Cannot remove user account with root name; because this user is a super account.'])
        else:
            self.username = username
            control.write_record('input.password_hint', 'Yes', '/etc/configbox')
            self.Env.RunApp('input', ['Enter this user password', self._user_del_passwd_])

    def _user_del_passwd_ (self,password):
        this_password = control.read_record('code',f'/etc/users/{self.username}')
        control.write_record('input.password_hint', 'No', '/etc/configbox')
        if not hashlib.sha3_512(password.encode()).hexdigest()==this_password:
            self.Env.RunApp('text', ['Wrong password',
                                     f'Cannot remove {self.username} user account; because your entered password is wrong.'])
        else:
            files.remove("/etc/users/" + self.username)
            if files.isdir('/desk/' + self.username):
                files.removedirs("/desk/" + self.username)
                control.remove_record('/desk/' + self.username, '/etc/permtab')

            self.Env.RunApp('text', ['Successfully removed',
                                     f'{self.username} user account successfully removed.'])

    def _in (self,name):
        self.name = name
        self.Env.RunApp('input', [f'Enter {name} value', self._in_value])

    def _in_value (self,value):
        commands.set([self.name+":",value])
