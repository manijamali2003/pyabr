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

import sys, os
from libabr import Files, Colors, Control, Res, Commands
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

files = Files()
colors = Colors()
control = Control()
res = Res()
commands = Commands()


class FileListView(QListView):
    def format(self, it, text):
        if files.isdir(self.dir + '/' + text):
            it.setIcon(QIcon(res.get('@icon/folder')))
        else:
            format = it.whatsThis().split('.')
            format = max(format)
            if it.whatsThis().endswith(format):
                logo = control.read_record(format + '.icon', '/etc/ext')
                if not logo == None:
                    it.setIcon(QIcon(res.get(logo)))
                else:
                    it.setIcon(QIcon(res.get('@icon/gtk-file')))
            else:
                it.setIcon(QIcon(res.get('@icon/gtk-file')))

    def mkdir(self, dirname):
        it = QStandardItem(dirname)
        it.setWhatsThis(self.dir + "/" + dirname)
        it.setIcon(QIcon(res.get('@icon/folder')))
        self.entry.appendRow(it)

        commands.mkdir([dirname])

    def __init__(self):
        super().__init__()
        self.entry = QStandardItemModel()
        self.parentdir = QStandardItem()
        self.parentdir.setIcon(QIcon(res.get('@icon/folder')))
        self.entry.appendRow(self.parentdir)
        self.setModel(self.entry)
        self.setIconSize(QSize(64, 64))
        self.clicked[QModelIndex].connect(self.on_clicked)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex()
        # on the given model index to get a pointer to the item

        self.setStyleSheet('background:white;')

        self.dir = files.readall('/proc/info/pwd')
        files.write('/proc/info/dsel', self.dir)
        self.listdir = (files.list(self.dir))
        self.listdir.sort()

        for text in self.listdir:
            it = QStandardItem(text)
            it.setWhatsThis(self.dir + "/" + text)
            self.format(it, text)
            self.entry.appendRow(it)

        self.itemOld = QStandardItem("text")

    def on_clicked(self, index):
        self.item = self.entry.itemFromIndex(index)

        x = hasattr(self.item, 'whatsThis')  # W3CSHCOOL.COM LEARN IT

        if x == True:

            if self.item.whatsThis() == "<parent>":
                commands.cd(['..'])
                self.dir = files.readall('/proc/info/pwd')
                files.write('/proc/info/dsel', self.dir)
                self.listdir = files.list(self.dir)
                self.listdir.sort()  # Credit: https://www.geeksforgeeks.org/sort-in-python/

                self.entry = QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QSize(64, 64))
                self.clicked[QModelIndex].connect(self.on_clicked)
                self.parentdir = QStandardItem()
                self.parentdir.setIcon(QIcon(res.get('@icon/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    it = QStandardItem(text)
                    it.setWhatsThis(self.dir + "/" + text)
                    self.format(it, text)
                    self.entry.appendRow(it)

            elif files.isdir(self.item.whatsThis()):
                files.write('/proc/info/dsel', self.item.whatsThis())  # Send Directory selected
                commands.cd([self.item.whatsThis()])
                self.dir = files.readall("/proc/info/pwd")
                self.listdir = files.list(self.dir)
                self.listdir.sort()

                self.entry = QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QSize(64, 64))
                self.clicked[QModelIndex].connect(self.on_clicked)
                self.parentdir = QStandardItem()
                self.parentdir.setIcon(QIcon(res.get('@icon/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    it = QStandardItem(text)
                    it.setWhatsThis(self.dir + "/" + text)
                    self.format(it, text)
                    self.entry.appendRow(it)

            elif files.isfile(self.item.whatsThis()):
                files.write('/proc/info/fsel', self.item.whatsThis())  # Send File selected


class DirListView(QListView):
    def format(self, it, text):
        if files.isdir(self.dir + '/' + text):
            it.setIcon(QIcon(res.get('@icon/folder')))

    def mkdir(self, dirname):
        it = QStandardItem(dirname)
        it.setWhatsThis(self.dir + "/" + dirname)
        it.setIcon(QIcon(res.get('@icon/folder')))
        self.entry.appendRow(it)

        commands.mkdir([dirname])

    def __init__(self):
        super().__init__()
        self.entry = QStandardItemModel()
        self.parentdir = QStandardItem()
        self.parentdir.setIcon(QIcon(res.get('@icon/folder')))
        self.entry.appendRow(self.parentdir)
        self.setModel(self.entry)
        self.setIconSize(QSize(64, 64))
        self.clicked[QModelIndex].connect(self.on_clicked)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex()
        # on the given model index to get a pointer to the item

        self.dir = files.readall('/proc/info/pwd')
        files.write('/proc/info/dsel', self.dir)
        self.listdir = (files.list(self.dir))
        self.listdir.sort()

        for text in self.listdir:
            if files.isdir(self.dir + "/" + text):
                it = QStandardItem(text)
                it.setWhatsThis(self.dir + "/" + text)
                self.format(it, text)
                self.entry.appendRow(it)

        self.itemOld = QStandardItem("text")

    def on_clicked(self, index):
        self.item = self.entry.itemFromIndex(index)

        x = hasattr(self.item, 'whatsThis')  # W3CSHCOOL.COM LEARN IT

        if x == True:

            if self.item.whatsThis() == "<parent>":
                commands.cd(['..'])
                self.dir = files.readall('/proc/info/pwd')
                files.write('/proc/info/dsel', self.dir)
                self.listdir = files.list(self.dir)
                self.listdir.sort()  # Credit: https://www.geeksforgeeks.org/sort-in-python/

                self.entry = QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QSize(64, 64))
                self.clicked[QModelIndex].connect(self.on_clicked)
                self.parentdir = QStandardItem()
                self.parentdir.setIcon(QIcon(res.get('@icon/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    if files.isdir(self.dir + "/" + text):
                        it = QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it, text)
                        self.entry.appendRow(it)

            elif files.isdir(self.item.whatsThis()):
                files.write('/proc/info/dsel', self.item.whatsThis())  # Send Directory selected
                commands.cd([self.item.whatsThis()])
                self.dir = files.readall("/proc/info/pwd")
                self.listdir = files.list(self.dir)
                self.listdir.sort()

                self.entry = QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QSize(64, 64))
                self.clicked[QModelIndex].connect(self.on_clicked)
                self.parentdir = QStandardItem()
                self.parentdir.setIcon(QIcon(res.get('@icon/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    if files.isdir(self.dir + "/" + text):
                        it = QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it, text)
                        self.entry.appendRow(it)


# select box #
class MainApp (QMainWindow):
    def __init__(self,ports):
        super(MainApp, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.External = ports[3]

        self.setStyleSheet('background-color: white;')
        ## Finds ##

        self.btnCancel = QPushButton()
        self.btnCancel.setText(res.get('@string/cancel'))
        self.btnCancel.setGeometry(0, int(self.Env.height() / 2) - 50, int(self.Env.width() / 4), 50)
        self.btnCancel.clicked.connect(self.Widget.Close)
        self.layout().addWidget(self.btnCancel)

        self.btnSelect = QPushButton()
        self.btnSelect.clicked.connect(self.inp)
        self.btnSelect.setGeometry(int(self.Env.width() / 4), int(self.Env.height() / 2) - 50,
                                   int(self.Env.width() / 4), 50)
        self.layout().addWidget(self.btnSelect)

        mode = control.read_record('select.mode', '/etc/configbox')
        self.mode = mode

        # widget #
        if self.External[0]==None or self.External[0]=="":
            if mode == 'select':
                self.Widget.SetWindowTitle(res.get('@string/dir'))
                self.btnSelect.setText(res.get('@string/choose'))
                self.x = DirListView()
            elif mode == 'open':
                self.Widget.SetWindowTitle(res.get('@string/file'))
                self.btnSelect.setText(res.get('@string/open'))
                self.x = FileListView()
            elif mode == 'save':
                self.Widget.SetWindowTitle(res.get('@string/dir'))
                self.btnSelect.setText(res.get('@string/save'))
                self.x = DirListView()
            elif mode == 'save-as':
                self.Widget.SetWindowTitle(res.get('@string/dir'))
                self.btnSelect.setText(res.get('@string/save-as'))
                self.x = DirListView()
        else:
            if mode == 'select':
                self.Widget.SetWindowTitle(self.External[0])
                self.btnSelect.setText(res.get('@string/choose'))
                self.x = DirListView()
            elif mode == 'open':
                self.Widget.SetWindowTitle(self.External[0])
                self.btnSelect.setText(res.get('@string/open'))
                self.x = FileListView()
            elif mode == 'save':
                self.Widget.SetWindowTitle(self.External[0])
                self.btnSelect.setText(res.get('@string/save'))
                self.x = DirListView()
            elif mode == 'save-as':
                self.Widget.SetWindowTitle(self.External[0])
                self.btnSelect.setText(res.get('@string/save-as'))
                self.x = DirListView()

        self.y = QMainWindow()
        self.y.resize(int(self.Env.width()/2),int(self.Env.height()/2)-50)
        self.y.setCentralWidget(self.x)
        self.layout().addWidget(self.y)

        self.Widget.Resize(self,int(self.Env.width()/2),int(self.Env.height()/2))

    def inp(self):
        if self.mode=='select' or self.mode=='save' or self.mode=='save-as':
            inputx = files.readall('/proc/info/dsel')
            self.External[1](inputx)
        else:
            inputx = files.readall('/proc/info/fsel')
            self.External[1](inputx)

        self.Widget.Close()