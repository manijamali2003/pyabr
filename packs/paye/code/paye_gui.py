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

import sys, subprocess,os

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

class PackageListView (QListView):
    def format(self, it, text):
        if files.isfile (f'/usr/share/applications/{it.text()}.desk'):
            self.application = control.read_record('application',f'/usr/share/applications/{it.text()}.desk')
            if self.application=='Yes':
                self.logo = control.read_record('logo',f'/usr/share/applications/{it.text()}.desk')
                self.locale = control.read_record('locale', '/etc/gui')
                it.setText(control.read_record(f'name[{self.locale}]', f'/usr/share/applications/{it.text()}.desk'))
                it.setIcon(QIcon(res.get(self.logo)))
            else:
                it.setIcon(QIcon(res.get('@icon/runner')))
        else:
            it.setIcon(QIcon(res.get('@icon/application-x-pak')))

        #it.setIcon(QIcon(res.get('@icon/application-x-pak')))

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

        self.listdir = files.list('/app/packages')
        self.listdir.sort()

        for text in self.listdir:
            if files.isfile(f'/app/packages/{text}') and text.endswith('.manifest'):
                it = QStandardItem(text.replace('.manifest',''))
                it.setWhatsThis(text.replace('.manifest',''))
                self.format(it, text.replace('.manifest',''))
                self.entry.appendRow(it)

        self.itemOld = QStandardItem("text")

    def on_clicked(self, index):
        self.item = self.entry.itemFromIndex(index)

        x = hasattr(self.item, 'whatsThis')  # W3CSHCOOL.COM LEARN IT

        if x == True:
            w = ShowPackageInformation([self.Backend,self.Env,self.Widget,self.AppName,[self.item.whatsThis(),self]])
            w.setGeometry(0,0,self.Env.width(),self.Env.height())
            self.Widget.layout().addWidget (w)

class ShowPackageInformation (QMainWindow):
    def __init__(self,ports):
        super(ShowPackageInformation, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.XShowpackages = self.External[1]
        self.XShowpackages.hide()

        self.path = f'/app/packages/{self.External[0]}'

        self.manifest = self.path+".manifest"
        self.compile = self.path+".compile"
        self.list = self.path+".list"
        self.preremove = self.path+".preremove"
        self.postremove= self.path+".postremove"
        self.preinstall = self.path+".preinstall"
        self.postinstall = self.path+".postinstall"

        self.name = control.read_record('name',self.manifest)
        self.version = control.read_record('version',self.manifest)
        self.build = control.read_record('build',self.manifest)
        self.unpack = control.read_record('unpack',self.manifest)
        self.license = control.read_record('license',self.manifest)
        self.copyright = control.read_record('copyright',self.manifest)
        self.description = control.read_record('description',self.manifest)
        self.Env.SetWindowTitle(self.External[0]+" package")
        self.resize(self.Env.width(),self.Env.height())

        self.btnBack = QPushButton()
        self.btnBack.clicked.connect(self.xhide)
        self.btnBack.setText('Back')
        self.btnBack.setGeometry(0, 0, self.Env.width(), 50)
        self.btnBack.setStyleSheet('background-color: #123456;color:white;')
        self.layout().addWidget(self.btnBack)

        self.btnImage = QToolButton()
        self.btnImage.setIconSize(QSize(128,128))

        self.namex = self.name

        if files.isfile (f'/usr/share/applications/{self.name}.desk'):
            self.application = control.read_record('application',f'/usr/share/applications/{self.name}.desk')
            if self.application=='Yes':
                self.logo = control.read_record('logo',f'/usr/share/applications/{self.name}.desk')
                self.locale = control.read_record('locale','/etc/gui')
                self.namex =  control.read_record(f'name[{self.locale}]',f'/usr/share/applications/{self.name}.desk')
                self.Env.SetWindowTitle(self.namex + " application")
                self.btnImage.setIcon(QIcon(res.get(self.logo)))
            else:
                self.btnImage.setIcon(QIcon(res.get('@icon/runner')))
        else:
            self.btnImage.setIcon(QIcon(res.get('@icon/application-x-pak')))


        self.btnImage.setStyleSheet('background-color:white;border-radius: 64% 64%;')
        self.btnImage.setGeometry(30, 70, 128, 128)
        self.layout().addWidget (self.btnImage)

        self.lblName = QLabel()
        self.lblName.setText(self.namex)
        self.lblName.setGeometry(60 + 128, 128 - 25, self.width(), 50)
        f = QFont()
        f.setPointSize(20)
        self.lblName.setFont(f)
        self.layout().addWidget(self.lblName)

        self.btnUninstall = QPushButton()
        self.btnUninstall.clicked.connect(self.xuni)
        self.btnUninstall.setText('Uninstall')
        self.btnUninstall.setGeometry(self.width()-260, 128-25, 100, 50)
        self.layout().addWidget(self.btnUninstall)

        self.btnUpdate = QPushButton()
        self.btnUpdate.clicked.connect(self.xup)
        self.btnUpdate.setText('Update')
        self.btnUpdate.setGeometry(self.width()-150, 128 - 25, 100, 50)
        self.layout().addWidget(self.btnUpdate)

    def xhide (self):
        self.hide()
        self.XShowpackages.show()
        self.Env.SetWindowTitle("Package Manager")

    # un install pack #
    def xuni (self):
        self.Backend.RunApp('bool', [f'Uninstall {self.External[0]}', f'Do you want to uninstall {self.External[0]} package?', self.xuni_])

    def xup (self):
        self.Backend.RunApp('bool', [f'Uninstall {self.External[0]}', f'Do you want to uninstall {self.External[0]} package?', self.xuni_])

    def xuni_(self,yes):
        if yes:
            System(f"paye rm {self.External[0]}")
            self.Env.Close()
            self.Backend.RunApp ('paye',[None])

    def xup_(self,yes):
        if yes:
            pass

class MainApp (QMainWindow):
    def __init__(self,ports):
        super(MainApp, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        self.Widget.SetWindowIcon (QIcon(res.get('@icon/paye')))
        self.Widget.SetWindowTitle ("Package Manager")
        self.Widget.Resize(self,720,640)

        self.x = PackageListView([self.Env,self.Widget,self,self.AppName,self.External])
        self.setCentralWidget(self.x)