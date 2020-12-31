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
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from libabr import Files, Control, System, Res, Commands, Permissions

res = Res()
files = Files()
control = Control()
commands = Commands()
permissions = Permissions()

f = QtGui.QFont()
f.setPointSize(int(res.etc("roller","fontsize")))

class FileListView (QtWidgets.QListView):
    AppName = "roller"
    def format(self, it, text):
        if files.isdir(self.dir + '/' + text):
            it.setIcon(QtGui.QIcon(res.get(res.etc("roller","folder-icon"))))
        else:
            format = it.whatsThis().split('.')
            format = max(format)
            if it.whatsThis().endswith(format):
                logo = control.read_record(format + '.icon', '/etc/ext')
                if not logo == None:
                    it.setIcon(QtGui.QIcon(res.get(logo)))
                else:
                    it.setIcon(QtGui.QIcon(res.get(res.etc("roller",'file-icon'))))
            else:
                it.setIcon(QtGui.QIcon(res.get(res.etc("roller",'file-icon'))))

    def mkdir (self,dirname):
        if files.isfile(dirname): self.Env.RunApp('text', ['Is a file',f'Cannot create {dirname} beacause it is a file.'])
        else:
            it = QtGui.QStandardItem(dirname)
            it.setWhatsThis(self.dir + "/" + dirname)
            it.setIcon(QtGui.QIcon(res.get(res.etc("roller",'folder-icon'))))
            self.entry.appendRow(it)
            commands.mkdir([dirname])
            it.setFont(f)

    def mkfile (self,filename):
        if files.isdir(filename ): self.Env.RunApp('text', ['Is a directory',
                                                                         f'Cannot create {filename} beacause it is a directory.'])
        else:
            it = QtGui.QStandardItem(filename)
            it.setWhatsThis(self.dir + "/" + filename)
            it.setIcon(QtGui.QIcon(res.get(res.etc('roller','file-icon'))))
            self.entry.appendRow(it)
            self.format(it, filename)
            commands.cat (['-c',filename])
            it.setFont(f)

    def mkc (self,filename):
        if files.isdir(filename + ".c"): self.Env.RunApp('text', ['Is a directory',
                                                                         f'Cannot create {filename + ".c"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".c")
            files.write(self.dir + "/" + filename+'.c',files.readall(res.get('@temp/untitled.c')))

    def mkcpp (self,filename):
        if files.isdir(filename + ".cpp"): self.Env.RunApp('text', ['Is a directory',
                                                                         f'Cannot create {filename + ".cpp"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".cpp")
            files.write(self.dir + "/" + filename+'.cpp',files.readall(res.get('@temp/untitled.cpp')))

    def mkjava (self,filename):
        if files.isdir(filename + ".java"): self.Env.RunApp('text', ['Is a directory',f'Cannot create {filename + ".java"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".java")
            files.write(self.dir + "/" + filename+'.java',files.readall(res.get('@temp/untitled.java')).replace("MainApp",filename))

    def mkjs (self,filename):
        if files.isdir(filename + ".js"): self.Env.RunApp('text', ['Is a directory',f'Cannot create {filename + ".js"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".js")
            files.write(self.dir + "/" + filename+'.js',files.readall(res.get('@temp/untitled.js')))

    def mkphp (self,filename):
        if files.isdir(filename + ".php"): self.Env.RunApp('text', ['Is a directory',f'Cannot create {filename + ".php"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".php")
            files.write(self.dir + "/" + filename+".php",files.readall(res.get('@temp/untitled.php')))

    def mkhtml (self,filename):
        if files.isdir(filename + ".html"): self.Env.RunApp('text', ['Is a directory',f'Cannot create {filename + ".html"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".html")
            files.write(self.dir + "/" + filename+".html",files.readall(res.get('@temp/untitled.html')))

    def mkcs (self,filename):
        if files.isdir(filename + ".cs"): self.Env.RunApp('text', ['Is a directory',f'Cannot create {filename + ".cs"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".cs")
            files.write(self.dir + "/" + filename+".cs",files.readall(res.get('@temp/untitled.cs')))

    def mksa (self,filename):
        if files.isdir(filename + ".sa"): self.Env.RunApp('text', ['Is a directory',f'Cannot create {filename + ".sa"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".sa")
            files.write(self.dir + "/" + filename+".sa",files.readall(res.get('@temp/untitled.sa')))

    def mkpy (self,filename):
        if files.isdir(filename + ".py"): self.Env.RunApp('text', ['Is a directory',f'Cannot create {filename + ".py"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".py")
            files.write(self.dir + "/" + filename+".py",files.readall(res.get('@temp/untitled.py')))

    def mkpygui (self,filename):
        if files.isdir(filename + ".py"): self.Env.RunApp('text', ['Is a directory',f'Cannot create {filename + ".py"} beacause it is a directory.'])
        else:
            self.mkfile(filename+".py")
            files.write(self.dir + "/" + filename+".py",files.readall(res.get('@temp/untitled-gui.py')))

    def __init__(self,ports):
        super().__init__()
        self.Env = ports[0]
        self.entry = QtGui.QStandardItemModel()
        self.parentdir = QtGui.QStandardItem()
        self.parentdir.setIcon(QtGui.QIcon(res.get(res.etc("roller",'folder-icon'))))
        self.entry.appendRow(self.parentdir)
        self.setModel(self.entry)
        iconsize = int(res.etc("roller","icon-size"))
        self.setIconSize(QtCore.QSize(iconsize,iconsize))


        self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex()
        # on the given model index to get a pointer to the item

        self.setStyleSheet(f'background:{res.etc("roller","bgcolor")};')

        self.dir = files.readall('/proc/info/pwd')
        files.write('/proc/info/dsel', self.dir)
        self.listdir = (files.list(self.dir))
        self.listdir.sort()

        for text in self.listdir:
            if files.isdir(self.dir+"/"+text):
                it = QtGui.QStandardItem(text)
                it.setWhatsThis(self.dir + "/" + text)
                self.format(it, text)
                self.entry.appendRow(it)
                it.setFont(f)

        for text in self.listdir:
            if files.isfile(self.dir + "/" + text):
                it = QtGui.QStandardItem(text)
                it.setWhatsThis(self.dir + "/" + text)
                self.format(it, text)
                self.entry.appendRow(it)
                it.setFont(f)

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
                self.setIconSize(QtCore.QSize(int(res.etc(self.AppName,"icon-size")), int(res.etc(self.AppName,"icon-size"))))
                self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
                self.parentdir = QtGui.QStandardItem()
                self.parentdir.setIcon(QtGui.QIcon(res.get(res.etc("roller","folder-icon"))))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    if files.isdir(self.dir+"/"+text):
                        it = QtGui.QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it, text)
                        self.entry.appendRow(it)
                        it.setFont(f)

                for text in self.listdir:
                    if files.isfile(self.dir+"/"+text):
                        it = QtGui.QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it, text)
                        self.entry.appendRow(it)
                        it.setFont(f)

            elif files.isdir(self.item.whatsThis()):
                files.write('/proc/info/dsel', self.item.whatsThis())  # Send Directory selected
                commands.cd ([self.item.whatsThis()])
                self.dir = files.readall("/proc/info/pwd")
                self.listdir = files.list(self.dir)
                self.listdir.sort()

                self.entry = QtGui.QStandardItemModel()
                self.setModel(self.entry)
                self.setIconSize(QtCore.QSize(int(res.etc(self.AppName,"icon-size")), int(res.etc(self.AppName,"icon-size"))))
                self.clicked[QtCore.QModelIndex].connect(self.on_clicked)
                self.parentdir = QtGui.QStandardItem()
                self.parentdir.setIcon(QtGui.QIcon(res.get(res.etc("roller","folder-icon"))))
                self.parentdir.setWhatsThis('<parent>')
                self.entry.appendRow(self.parentdir)

                for text in self.listdir:
                    if files.isdir(self.dir+"/"+text):
                        it = QtGui.QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it, text)
                        self.entry.appendRow(it)
                        it.setFont(f)
                for text in self.listdir:
                    if files.isfile(self.dir+"/"+text):
                        it = QtGui.QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it, text)
                        self.entry.appendRow(it)
                        it.setFont(f)

            elif files.isfile (self.item.whatsThis()):
                files.write ('/proc/info/fsel',self.item.whatsThis()) # Send File selected
                        
class MainApp (QtWidgets.QMainWindow):
    def format (self,it,text):
        if os.path.isdir(self.dir + '/' + text):
            it.setIcon(QtGui.QIcon(res.get(res.etc("roller","folder-icon"))))
        else:
            format = it.whatsThis().split('.')
            format = max(format)
            if it.whatsThis().endswith(format):
                logo = control.read_record(format + '.icon', '/etc/ext')
                if not logo==None:
                    it.setIcon(QtGui.QIcon(res.get(logo)))
                else:
                    it.setIcon(QtGui.QIcon(res.get(res.etc("roller","file-icon"))))
            else:
                it.setIcon(QtGui.QIcon(res.get(res.etc("roller","file-icon"))))

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

        ## Menubar ##

        self.x = FileListView([self.Env])

        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu(res.get('@string/file'))

        ## File menu

        self.new_file = self.file.addAction(res.get('@string/newfile'))
        self.new_file.triggered.connect(self.New_File)
        self.new_file.setIcon(QIcon(res.get(res.etc("roller","file-icon"))))

        self.new_code = self.file.addMenu(res.get('@string/newcode'))
        self.new_code.setIcon(QIcon(res.get(res.etc('roller','c'))))

        ##
        self.new_c = self.new_code.addAction(res.get('@string/c'))
        self.new_c.triggered.connect(self.New_C)
        self.new_c.setIcon(QIcon(res.get(res.etc("roller", "c"))))

        self.new_cpp = self.new_code.addAction(res.get('@string/c++'))
        self.new_cpp.triggered.connect(self.New_Cpp)
        self.new_cpp.setIcon(QIcon(res.get(res.etc("roller", "c++"))))

        self.new_cs = self.new_code.addAction(res.get('@string/csharp'))
        self.new_cs.triggered.connect(self.New_Csharp)
        self.new_cs.setIcon(QIcon(res.get(res.etc("roller", "c#"))))

        self.new_html = self.new_code.addAction(res.get('@string/html'))
        self.new_html .triggered.connect(self.New_Html)
        self.new_html.setIcon(QIcon(res.get(res.etc("roller", "html"))))

        self.new_java = self.new_code.addAction(res.get('@string/java'))
        self.new_java.triggered.connect(self.New_Java)
        self.new_java.setIcon(QIcon(res.get(res.etc("roller", "java"))))

        self.new_js = self.new_code.addAction(res.get('@string/javascript'))
        self.new_js.triggered.connect(self.New_Js)
        self.new_js.setIcon(QIcon(res.get(res.etc("roller", "js"))))

        self.new_Php = self.new_code.addAction(res.get('@string/php'))
        self.new_Php.triggered.connect(self.New_Php)
        self.new_Php.setIcon(QIcon(res.get(res.etc("roller", "php"))))

        self.new_py = self.new_code.addAction(res.get('@string/python'))
        self.new_py.triggered.connect(self.New_Py)
        self.new_py.setIcon(QIcon(res.get(res.etc("roller", "py"))))

        self.new_sa = self.new_code.addAction(res.get('@string/saye'))
        self.new_sa.triggered.connect(self.New_Sa)
        self.new_sa.setIcon(QIcon(res.get(res.etc("roller", "sa"))))

        self.new_pygui = self.new_code.addAction(res.get('@string/pythongui'))
        self.new_pygui.triggered.connect(self.New_PyGui)
        self.new_pygui.setIcon(QIcon(res.get(res.etc("roller", "py"))))
        ##

        self.new_folder = self.file.addAction(res.get('@string/newfolder'))
        self.new_folder.triggered.connect(self.New_Folder)
        self.new_folder.setIcon(QIcon(res.get(res.etc("roller","folder-icon"))))

        self.exit = self.file.addAction(res.get('@string/exit'))
        self.exit.triggered.connect(self.Widget.Close)
        self.exit.setIcon(QIcon(res.get(res.etc("roller","exit-icon"))))

        ## end File menu

        ## end Menubar

        self.Widget.SetWindowTitle (res.get('@string/app_name'))
        self.Widget.SetWindowIcon (QtGui.QIcon(res.get(res.etc(self.AppName,"logo"))))
        self.Widget.Resize (self,int(res.etc(self.AppName,"width")),int(res.etc(self.AppName,"height")))

        self.setCentralWidget(self.x)

    def New_Folder (self):
        self.Env.RunApp('input',[res.get('@string/foldername'),self.x.mkdir])

    def New_File (self):
        self.Env.RunApp('input',[res.get('@string/filename'),self.x.mkfile])

    def New_C (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mkc])

    def New_Cpp (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mkcpp])

    def New_Csharp (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mkcs])

    def New_Html (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mkhtml])

    def New_Java (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mkjava])

    def New_Js (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mkjs])

    def New_Php (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mkphp])

    def New_Py (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mkpy])

    def New_PyGui (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mkpygui])

    def New_Sa (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.x.mksa])