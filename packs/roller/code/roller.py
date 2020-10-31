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

import sys , os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QBrush, QColor

from libabr import Files, Control, System, Res, Commands, Permissions

res = Res()
files = Files()
control = Control()
commands = Commands()
permissions = Permissions()

class FileListView (QtWidgets.QListView):
    def format(self, it, text):
        if files.isdir(self.dir + '/' + text):
            it.setIcon(QtGui.QIcon(res.get('@icon/folder')))
        else:
            format = it.whatsThis().split('.')
            format = max(format)
            if it.whatsThis().endswith(format):
                logo = control.read_record(format + '.icon', '/etc/ext')
                if not logo == None:
                    it.setIcon(QtGui.QIcon(res.get(logo)))
                else:
                    it.setIcon(QtGui.QIcon(res.get('@icon/gtk-file')))
            else:
                it.setIcon(QtGui.QIcon(res.get('@icon/gtk-file')))


    def mkdir (self,dirname):
        it = QtGui.QStandardItem(dirname)
        it.setWhatsThis(self.dir + "/" + dirname)
        it.setIcon(QtGui.QIcon(res.get('@icon/folder')))
        self.entry.appendRow(it)

        commands.mkdir([dirname])

    def mkfile (self,filename):
        it = QtGui.QStandardItem(filename)
        it.setWhatsThis(self.dir + "/" + filename)
        it.setIcon(QtGui.QIcon(res.get('@icon/gtk-file')))
        self.entry.appendRow(it)
        self.format(it, filename)
        commands.cat (['-c',filename])

    def __init__(self):
        super().__init__()
        self.entry = QtGui.QStandardItemModel()
        self.parentdir = QtGui.QStandardItem()
        self.parentdir.setIcon(QtGui.QIcon(res.get('@icon/folder')))
        self.entry.appendRow(self.parentdir)
        self.setModel(self.entry)
        self.setIconSize(QtCore.QSize(64,64))
        self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex()
        # on the given model index to get a pointer to the item

        self.setStyleSheet('background:white;')

        self.dir = files.readall('/proc/info/pwd')
        files.write('/proc/info/dsel', self.dir)
        self.listdir = (files.list(self.dir))
        self.listdir.sort()

        for text in self.listdir:
            it = QtGui.QStandardItem(text)
            it.setWhatsThis(self.dir+"/"+text)
            self.format(it,text)
            self.entry.appendRow(it)

        self.itemOld = QtGui.QStandardItem("text")

    def on_clicked(self, index):
        self.item = self.entry.itemFromIndex(index)

        x = hasattr(self.item,'whatsThis') # W3CSHCOOL.COM LEARN IT


        if x == True:

            if self.item.whatsThis() == "<parent>":
                commands.cd (['..'])
                self.dir = files.readall('/proc/info/pwd')
                files.write('/proc/info/dsel',self.dir)
                self.listdir = files.list(self.dir)
                self.listdir.sort() # Credit: https://www.geeksforgeeks.org/sort-in-python/

                self.entry = QtGui.QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QtCore.QSize(64, 64))
                self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
                self.parentdir = QtGui.QStandardItem()
                self.parentdir.setIcon(QtGui.QIcon(res.get('@icon/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    it = QtGui.QStandardItem(text)
                    it.setWhatsThis(self.dir + "/" + text)
                    self.format(it,text)
                    self.entry.appendRow(it)

            elif files.isdir(self.item.whatsThis()):
                files.write('/proc/info/dsel', self.item.whatsThis())  # Send Directory selected
                commands.cd ([self.item.whatsThis()])
                self.dir = files.readall("/proc/info/pwd")
                self.listdir = files.list(self.dir)
                self.listdir.sort()

                self.entry = QtGui.QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QtCore.QSize(64, 64))
                self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
                self.parentdir = QtGui.QStandardItem()
                self.parentdir.setIcon(QtGui.QIcon(res.get('@icon/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    it = QtGui.QStandardItem(text)
                    it.setWhatsThis(self.dir + "/" + text)
                    self.format(it,text)
                    self.entry.appendRow(it)

            elif files.isfile (self.item.whatsThis()):
                files.write ('/proc/info/fsel',self.item.whatsThis()) # Send File selected
                        
class MainApp (QtWidgets.QMainWindow):
    def format (self,it,text):
        if os.path.isdir(self.dir + '/' + text):
            it.setIcon(QtGui.QIcon(res.get('@icon/folder')))
        else:
            format = it.whatsThis().split('.')
            format = max(format)
            if it.whatsThis().endswith(format):
                logo = control.read_record(format + '.icon', '/etc/ext')
                if not logo==None:
                    it.setIcon(QtGui.QIcon(res.get(logo)))
                else:
                    it.setIcon(QtGui.QIcon(res.get('@icon/gtk-file')))
            else:
                it.setIcon(QtGui.QIcon(res.get('@icon/gtk-file')))

    def __init__(self,args):
        super().__init__()

        self.Backend = args[0]
        self.Env = args[1]
        self.Widget = args[2]
        self.AppName = args[3]
        self.External = args[4]

        if not self.External == None:
            if not self.External[0]==None:
                if permissions.check(files.output(self.External[0]), "r", files.readall("/proc/info/su")):
                    if files.isdir (files.output(self.External[0])):
                        files.write('/proc/info/pwd',files.output(self.External[0]))

        self.x = FileListView()

        ## Menubar ##

        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu("File")

        ## File menu

        self.new_file = self.file.addAction("New File")
        self.new_file.triggered.connect(self.New_File)

        self.new_folder = self.file.addAction("New Folder")
        self.new_folder.triggered.connect(self.New_Folder)

        self.exit = self.file.addAction("Exit")
        self.exit.triggered.connect(self.Widget.Close)

        ## end File menu

        ## end Menubar

        self.Widget.SetWindowTitle (res.get('@string/app_name'))
        self.Widget.SetWindowIcon (QtGui.QIcon(res.get('@icon/roller')))
        self.Widget.Resize (self,1000,600)

        self.setCentralWidget(self.x)

    def New_Folder (self):
        self.Env.RunApp('input',['Enter your folder name',self.x.mkdir])

    def New_File (self):
        self.Env.RunApp('input',['Enter your file name',self.x.mkfile])