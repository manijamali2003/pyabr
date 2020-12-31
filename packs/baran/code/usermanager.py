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

import sys, subprocess,os,shutil

from libabr import Files, Control, Permissions, Colors, Process, Modules, Package, Commands, Res, System

modules = Modules()
files = Files()
control = Control()
colors = Colors()
process = Process()
permissions = Permissions()
pack = Package()
commands = Commands()
res = Res()

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

f = QFont()

class PackageListView (QListView):
    def format(self, it, text):

        first_name = control.read_record('first_name',f'/etc/users/{it.text()}')
        last_name = control.read_record('last_name',f'/etc/users/{it.text()}')
        logo = control.read_record('loginw.userlogo',f'/etc/users/{it.text()}')

        if not (first_name==None and last_name==None):
            namex = first_name+" "+last_name
        elif not first_name==None:
            namex = last_name
        elif not last_name==None:
            namex = first_name
        else:
            namex = it.text()

        it.setText(namex)
        self.setIconSize(QSize(128,128))
        if logo==None:
            it.setIcon(QIcon(res.get('@icon/account')))
        else:
            it.setIcon(QIcon(res.get(logo)))


    def __init__(self,ports):
        super().__init__()
        self.ports = ports

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.entry = QStandardItemModel()
        self.setModel(self.entry)
        self.setIconSize(QSize(80, 80))
        self.clicked[QModelIndex].connect(self.on_clicked)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex()
        # on the given model index to get a pointer to the item

        self.listdir = files.list('/etc/users')
        self.listdir.sort()

        for text in self.listdir:
            it = QStandardItem(text)
            it.setWhatsThis(text)
            self.format(it, text)
            self.entry.appendRow(it)

        self.itemOld = QStandardItem("text")

    def on_clicked(self, index):
        self.item = self.entry.itemFromIndex(index)

        x = hasattr(self.item, 'whatsThis')  # W3CSHCOOL.COM LEARN IT

        if x == True:
            w = ShowUserInformation([self.Backend,self.Env,self.Widget,self.AppName,[self.item.whatsThis(),self]])
            w.setGeometry(0,0,self.Env.width(),self.Env.height())
            self.Widget.layout().addWidget (w)

class ShowUserInformation (QMainWindow):
    def __init__(self,ports):
        super(ShowUserInformation, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.XShowpackages = self.External[1]
        self.XShowpackages.hide()

        self.path = f'/etc/users/{self.External[0]}'

        self.btnBack = QPushButton()
        self.btnBack.clicked.connect(self.xhide)
        self.btnBack.setText('Back')
        self.btnBack.setGeometry(0, 0, self.Env.width(), 50)
        self.btnBack.setStyleSheet('background-color: #123456;color:white;')
        self.layout().addWidget(self.btnBack)

        first_name = control.read_record('first_name', self.path)
        last_name = control.read_record('last_name', self.path)
        logo = control.read_record('loginw.userlogo', self.path)

        if not (first_name == None and last_name == None):
            namex = first_name + " " + last_name
        elif not first_name == None:
            namex = last_name
        elif not last_name == None:
            namex = first_name
        else:
            namex = self.External[0]

        self.Env.SetWindowTitle(namex)

        self.fullname = namex
        self.email = control.read_record('email',self.path)
        self.phone = control.read_record('phone', self.path)
        self.blood_type = control.read_record('blood_type', self.path)
        self.company = control.read_record('company', self.path)
        self.gender = control.read_record('gender', self.path)
        self.website = control.read_record('website', self.path)
        self.birthday = control.read_record('birthday', self.path)

        self.w = QWidget()
        self.w.setGeometry(30, 200, self.width() - 60, 275)
        self.hbox = QHBoxLayout()
        self.w.setLayout(self.hbox)
        f.setPointSize(12)
        self.text1 = QTextBrowser()
        self.text1.setAlignment(Qt.AlignRight)
        self.text1.append('\nFull name:\n')
        if not self.company==None:
            self.text1.append('Company name:\n')
        if not self.email == None :
            self.text1.append('Email address:\n')
        if not self.phone == None:
            self.text1.append('Phone number:\n')
        if not self.gender == None:
            self.text1.append('Gender:\n')
        if not self.birthday == None :
            self.text1.append('Birthday:\n')
        if not self.blood_type == None:
            self.text1.append('Blood type:\n')
        self.text1.setFont(f)
        self.hbox.addWidget(self.text1)

        self.text2 = QTextBrowser()
        self.text2.append("\n" + self.fullname + "\n")
        if not self.company == None:
            self.text2.append(self.company + "\n")
        if not self.email == None:
            self.text2.append(self.email + "\n")
        if not self.phone == None:
            self.text2.append(self.phone + "\n")
        if not self.gender == None:
            self.text2.append(self.gender + "\n")
        if not self.birthday == None:
            self.text2.append(self.birthday + "\n")
        if not self.blood_type == None:
            self.text2.append(self.blood_type + "\n")
        self.text2.setAlignment(Qt.AlignLeft)
        self.text2.setFont(f)
        self.hbox.addWidget(self.text2)
        self.layout().addWidget(self.w)

    def xhide (self):
        self.hide()
        self.XShowpackages.show()
        self.Env.SetWindowTitle("Account Manager")

class MainApp (QMainWindow):
    def __init__(self,ports):
        super(MainApp, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.Widget.SetWindowIcon (QIcon(res.get('@icon/help-about')))
        self.Widget.SetWindowTitle ("Account Managers")
        self.Widget.Resize(self,720,640)
        self.x = PackageListView([self.Env,self.Widget,self,self.AppName,self.External])
        self.setCentralWidget(self.x)
