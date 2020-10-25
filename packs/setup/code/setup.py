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
#!etcetra

desktop: baran
fullscreen: Yes
sides: No
width: 1280
height: 720
autosize: Yes
logo: @icon/pyabr-logo
locale: en

backend.color: black
backend.timeout: 1000

splash.timeout: 3000
splash.logo: @icon/pyabr-logo
splash.logo-size: 300
splash.color: #ABCDEF

login.bgcolor: #123456
login.background: @background/default
login.fgcolor: #FFFFFF

enter.bgcolor: #123456
enter.background: @background/default
enter.fgcolor: #FFFFFF

unlock.bgcolor: #123456
unlock.background: @background/default
unlock.fgcolor: #FFFFFF

loginw.bgcolor: white
loginw.fgcolor: black
loginw.round: Yes
loginw.round-size: 20 20
loginw.location: center
loginw.shadow: Yes
loginw.userlogo: @icon/account
loginw.userlogo.shadow: Yes
loginw.userlogo.color: white
loginw.userlogo.round: Yes
loginw.userlogo.round-size: 125 125
loginw.input.shadow: Yes
loginw.input.fgcolor: gray
loginw.input.bgcolor: white
loginw.input.round: Yes
loginw.input.round-size: 20 20
loginw.input.font-size: 12

taskbar.bgcolor: white
taskbar.fgcolor: black
taskbar.locked: No
taskbar.float: Yes

desktop.bgcolor: white
desktop.fgcolor: black
desktop.background: @background/default
lock.fgcolor: black
lock.bgcolor: black
lock.background: @background/default

loginw.login.round: Yes
loginw.login.round-size: 20
loginw.enter.round: Yes
loginw.enter.round-size: 20
loginw.unlock.round: Yes
loginw.unlock.round-size: 20

appw.bgcolor: #FFFFFF
appw.menubar.bgcolor: #FFFFFF
appw.menubar.shadow: Yes
            ''')
            file.close()

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
