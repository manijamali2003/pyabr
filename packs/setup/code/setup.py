from PyQt5 import QtGui, QtCore, QtWidgets, uic
import platform
import hashlib, shutil, os, sys
from buildlibs import pack_archives as pack
from pathlib import Path

class MainApp(QtWidgets.QWizard):
    def BrowseClick(self):
        self.leLocation.setText((QtWidgets.QFileDialog().getExistingDirectory()))

    def Finish(self):
        ## Get all configure information ##
        if not (
                self.leHostname.text() == None and
                self.leRootCode.text() == None and
                self.leConfirmRootCode.text() == None and
                self.leUsername.text() == None and
                self.lePassword.text() == None and
                self.leConfirmPassword.text() == None and
                self.leFirstName.text() == None and
                self.leLastName.text() == None and
                self.leEmail.text() == None and
                self.lePhone.text() == None and
                self.cmUI.currentText() == None and
                self.cmLang.currentText() == None and
                self.cmScreen.currentText() == None
        ):
            hostname = self.leHostname.text()
            rootcode = self.leRootCode.text()
            username = self.leUsername.text()
            password = self.lePassword.text()
            first_name = self.leFirstName.text()
            last_name = self.leLastName.text()
            email = self.leEmail.text()
            phone = self.lePhone.text()
            if self.chGuest.isChecked():
                guest = 'Yes'
            else:
                guest = 'No'

            interface = self.cmUI.currentText()
            if self.cmLang.currentText()=='English':
                locale = 'en'
            elif self.cmLang.currentText()=='فارسی':
                locale = 'fa'
            elif self.cmLang.currentText()=='عربی':
                locale = 'ar'
            else:
                locale = 'en'

            ## Setting up hostname ##
            file = open("etc/hostname", "w")
            file.write(hostname)
            file.close()

            ## Setting up Root user ##
            file = open("etc/users/root", "w")
            file.write("username: " + hashlib.sha3_256("root".encode()).hexdigest() + "\n")
            file.write("code: " + hashlib.sha3_512(rootcode.encode()).hexdigest() + "\n")
            file.close()

            ## Setting up Standard user ##
            file = open("etc/users/" + username, "w")
            file.write("username: " + hashlib.sha3_256(username.encode()).hexdigest() + "\n")
            file.write("code: " + hashlib.sha3_512(password.encode()).hexdigest() + "\n")
            file.write("first_name: " + first_name + "\n")
            file.write("last_name: " + last_name + "\n")
            file.write("email: " + email + "\n")
            file.write("phone: " + phone + "\n")
            file.close()

            file = open("etc/permtab", "a")
            file.write("/desk/" + username + ": drwxr-x---/" + username + "\n")
            file.close()

            ## Setting up Guest user ##
            file = open("etc/guest", "w")
            if guest == "No":
                file.write("enable_cli: No\nenable_gui: No\n")
            elif guest == "Yes":
                file.write("enable_cli: Yes\nenable_gui: Yes\n")
            else:
                file.write("enable_cli: No\nenable_gui: No\n")
            file.close()
            
            ## Setting up interface ##
            file = open("etc/interface", "w")
            if interface.startswith("C"):
                file.write("CLI")
            elif interface.startswith("G"):
                file.write("GUI")
            file.close()

            ## Setting GUI Table ##
            file = open("etc/gui", "w")
            file.write("locale: " + locale + "\n")
            file.write('''
desktop: baran
fullscreen: Yes
sides: No
width: 720
height: 1280
autosize: Yes
logo: @icon/pyabr-logo
locale: en
lock.clock.shadow: No
lock.clock.size: 30
lock.clock.color: white
lock.clock.location: center
submenu.hide: No
submenu.fgcolor: black
submenu.bgcolor: white
submenu.direction: ltr
submenu.fontsize: 12
titlebar.close: @icon/close
titlebar.close-hover: @icon/close-hover
titlebar.float: @icon/float
titlebar.float-hover: @icon/float-hover
titlebar.bgcolor: #123456
titlebar.fgcolor: white
taskbar.pins: calculator,calendar,pyshell,pysys,runapp
taskbar.location: left
taskbar.size: 140
taskbar.locked: Yes
taskbar.float: No
backend.color: #000000
backend.timeout: 100
splash.color: #ABCDEF
splash.timeout: 3000
fullscreen: Yes
autosize: Yes
login.fgcolor: #000000
login.background: @background/default
enter.fgcolor: #000000
enter.background: @background/default
unlock.fgcolor: #000000
unlock.background: @background/default
desktop.fgcolor: #000000
desktop.background: @background/default
lock.bgcolor: #FFFFFF
lock.fgcolor: #000000
lock.background: @background/default
taskbar.bgcolor: #FFFFFF
loginw.bgcolor: #FFFFFF
userlogo.color: #FFFFFF
input.bgcolor: #FFFFFF
input.fgcolor: #000000
loginw.fgcolor: #000000
loginw.round.size: 20
loginw.userlogo.round-size: 350
loginw.input.round-size: 20
loginw.location: center
loginw.input.fontsize: 16
loginw.login.bgcolor: #ABCDEF
loginw.login.fgcolor: #FFFFFF
loginw.login.hover-bgcolor: #123456
loginw.login.hover-fgcolor: #FFFFFF
loginw.login.fontsize: 12
loginw.login.round: Yes
loginw.login.round-size: 20
loginw.login.hide: No
loginw.login.width: 350
loginw.enter.bgcolor: pink
loginw.enter.fgcolor: #FFFFFF
loginw.enter.hover-bgcolor: purple
loginw.enter.hover-fgcolor: #FFFFFF
loginw.enter.fontsize: 12
loginw.enter.round: Yes
loginw.enter.round-size: 20
loginw.enter.hide: No
loginw.enter.width: 350
loginw.unlock.bgcolor: lime
loginw.unlock.fgcolor: green
loginw.unlock.hover-bgcolor: green
loginw.unlock.hover-fgcolor: lime
loginw.unlock.fontsize: 12
loginw.unlock.round: Yes
loginw.unlock.round-size: 20
loginw.unlock.hide: No
loginw.unlock.width: 350
loginw.shadow: Yes
loginw.userlogo.shadow: Yes
loginw.input.shadow: No
loginw.login.shadow: No
loginw.enter.shadow: No
loginw.unlock.shadow: No
loginw.input.width: 350
loginw.input.height: 60
loginw.login.height: 60
loginw.enter.height: 60
loginw.unlock.height: 60
loginw.userlogo: @icon/account
splash.logo: @icon/pyabr-logo
splash.logo-size: 300
            ''')
            file.close()

    os.remove('configure.pyc')
    os.remove('configure-inserver.pyc')
    shutil.rmtree('install')
    os.remove('app/packages/setup.compile')
    os.remove('app/packages/setup.list')
    os.remove('app/packages/setup.manifest')
    os.remove('setup.pyc')

    def __init__(self):
        super(MainApp, self).__init__()
        uic.loadUi('install/setup.ui', self)

        ## Finds ##
        self.leHostname = self.findChild(QtWidgets.QLineEdit, 'leHostname')
        self.leRootCode = self.findChild(QtWidgets.QLineEdit, 'leRootCode')
        self.leConfirmRootCode = self.findChild(QtWidgets.QLineEdit, 'leConfirmRootCode')
        self.leUsername = self.findChild(QtWidgets.QLineEdit, 'leUsername')
        self.lePassword = self.findChild(QtWidgets.QLineEdit, 'lePassword')
        self.leConfirmPassword = self.findChild(QtWidgets.QLineEdit, 'leConfirmPassword')
        self.chGuest = self.findChild(QtWidgets.QCheckBox, 'chGuest')
        self.cmUI = self.findChild(QtWidgets.QComboBox, 'cmUI')
        self.cmLang = self.findChild(QtWidgets.QComboBox, 'cmLang')
        self.leFirstName = self.findChild(QtWidgets.QLineEdit, 'leFirstName')
        self.leLastName = self.findChild(QtWidgets.QLineEdit, 'leLastName')
        self.leEmail = self.findChild(QtWidgets.QLineEdit, 'leEmail')
        self.lePhone = self.findChild(QtWidgets.QLineEdit, 'lePhone')

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.Finish)
        self.button(QtWidgets.QWizard.FinishButton).setText("Fast Install")

        ## Show setup ##
        self.show()

app = QtWidgets.QApplication([])
w = MainApp()
app.exec_()
