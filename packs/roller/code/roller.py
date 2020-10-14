import sys , os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QBrush, QColor

from libabr import Files, Control, System, Res

res = Res()
files = Files()
control = Control()

class FileListView (QtWidgets.QListView):
    def format(self, it, text):
        if files.isdir(self.dir + '/' + text):
            it.setIcon(QtGui.QIcon(res.get('@icon/folder')))
        else:
            format = it.whatsThis().split('.')
            format = max(format)
            if it.whatsThis().endswith(format):
                logo = control.read_record(format + '.logo', '/etc/ext')
                if not logo == None:
                    it.setIcon(QtGui.QIcon(res.get(logo)))
                else:
                    it.setIcon(QtGui.QIcon(res.get('@logo/gtk-file')))
            else:
                it.setIcon(QtGui.QIcon(res.get('@logo/gtk-file')))


    def mkdir (self,dirname):
        it = QtGui.QStandardItem(dirname)
        it.setWhatsThis(self.dir + "/" + dirname)
        it.setIcon(QtGui.QIcon(res.get('@logo/folder')))
        self.entry.appendRow(it)

        core.system ("mkdir '"+dirname+"'")

    def __init__(self):
        super().__init__()
        self.entry = QtGui.QStandardItemModel()
        self.parentdir = QtGui.QStandardItem()
        self.parentdir.setIcon(QtGui.QIcon(res.get('@logo/folder')))
        self.entry.appendRow(self.parentdir)
        self.setModel(self.entry)
        self.setIconSize(QtCore.QSize(64,64))
        self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex()
        # on the given model index to get a pointer to the item

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
                core.system('cd ..')
                self.dir = files.readall('/proc/info/pwd')
                files.write('/proc/info/dsel',self.dir)
                self.listdir = files.list(self.dir)
                self.listdir.sort() # Credit: https://www.geeksforgeeks.org/sort-in-python/

                self.entry = QtGui.QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QtCore.QSize(64, 64))
                self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
                self.parentdir = QtGui.QStandardItem()
                self.parentdir.setIcon(QtGui.QIcon(res.get('@logo/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    it = QtGui.QStandardItem(text)
                    it.setWhatsThis(self.dir + "/" + text)
                    self.format(it,text)
                    self.entry.appendRow(it)

            elif files.isdir(self.item.whatsThis()):
                files.write('/proc/info/dsel', self.item.whatsThis())  # Send Directory selected
                core.system ('cd "'+self.item.whatsThis()+'"')
                self.dir = files.readall("/proc/info/pwd")
                self.listdir = files.list(self.dir)
                self.listdir.sort()

                self.entry = QtGui.QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QtCore.QSize(64, 64))
                self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
                self.parentdir = QtGui.QStandardItem()
                self.parentdir.setIcon(QtGui.QIcon(res.get('@logo/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                print (files.output(files.output(self.dir)))

                for text in self.listdir:
                    it = QtGui.QStandardItem(text)
                    it.setWhatsThis(self.dir + "/" + text)
                    self.format(it,text)
                    self.entry.appendRow(it)

            elif files.isfile (self.item.whatsThis()):
                files.write ('/proc/info/fsel',self.item.whatsThis()) # Send File selected


class DirListView (QtWidgets.QListView):
    def format(self, it, text):
        if files.isdir(self.dir + '/' + text):
            it.setIcon(QtGui.QIcon(res.get('@logo/folder')))

    def mkdir (self,dirname):
        it = QtGui.QStandardItem(dirname)
        it.setWhatsThis(self.dir + "/" + dirname)
        it.setIcon(QtGui.QIcon(res.get('@logo/folder')))
        self.entry.appendRow(it)

        core.system ("mkdir '"+dirname+"'")

    def __init__(self):
        super().__init__()
        self.entry = QtGui.QStandardItemModel()
        self.parentdir = QtGui.QStandardItem()
        self.parentdir.setIcon(QtGui.QIcon(res.get('@logo/folder')))
        self.entry.appendRow(self.parentdir)
        self.setModel(self.entry)
        self.setIconSize(QtCore.QSize(64,64))
        self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex()
        # on the given model index to get a pointer to the item

        self.dir = files.readall('/proc/info/pwd')
        files.write('/proc/info/dsel', self.dir)
        self.listdir = (files.list(self.dir))
        self.listdir.sort()

        for text in self.listdir:
            if files.isdir (self.dir+"/"+text):
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
                core.system('cd ..')
                self.dir = files.readall('/proc/info/pwd')
                files.write('/proc/info/dsel',self.dir)
                self.listdir = files.list(self.dir)
                self.listdir.sort() # Credit: https://www.geeksforgeeks.org/sort-in-python/

                self.entry = QtGui.QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QtCore.QSize(64, 64))
                self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
                self.parentdir = QtGui.QStandardItem()
                self.parentdir.setIcon(QtGui.QIcon(res.get('@logo/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    if files.isdir(self.dir + "/" + text):
                        it = QtGui.QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it,text)
                        self.entry.appendRow(it)

            elif files.isdir(self.item.whatsThis()):
                files.write('/proc/info/dsel', self.item.whatsThis())  # Send Directory selected
                core.system ('cd "'+self.item.whatsThis()+'"')
                self.dir = files.readall("/proc/info/pwd")
                self.listdir = files.list(self.dir)
                self.listdir.sort()

                self.entry = QtGui.QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QtCore.QSize(64, 64))
                self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
                self.parentdir = QtGui.QStandardItem()
                self.parentdir.setIcon(QtGui.QIcon(res.get('@logo/folder')))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                print (files.output(files.output(self.dir)))

                for text in self.listdir:
                    if files.isdir (self.dir + "/" + text):
                        it = QtGui.QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it,text)
                        self.entry.appendRow(it)