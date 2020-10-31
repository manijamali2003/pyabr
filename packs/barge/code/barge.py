from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys, importlib
from libabr import System, App, Control, Files, Res

res = Res();files = Files();app = App();control=Control()

class MainApp(QtWidgets.QMainWindow):
    def __init__(self,args):
        super(MainApp, self).__init__()

        # ports
        self.Backend = args[0]
        self.Env = args[1]
        self.Widget = args[2]
        self.AppName = args[3]
        self.External = args[4]

        # resize
        self.Widget.Resize (self,700,500)
        self.Widget.SetWindowTitle(res.get('@string/app_name'))
        self.Widget.SetWindowIcon (QtGui.QIcon(res.get('@icon/barge')))

        self.Widget.SetWindowTitle("Untitled - Barge")

        # text box
        self.teEdit = QtWidgets.QTextEdit()
        self.setCentralWidget(self.teEdit)

        # menubar
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu("File")

        # file menu #
        self.new = self.file.addAction("New")
        self.new.triggered.connect (self.new_act)
        self.new_page = self.file.addAction("New Page")
        self.new_page.triggered.connect (self.new_page_act)
        self.open = self.file.addAction("Open")
        self.open.triggered.connect (self.open_act)
        self.save = self.file.addAction("Save")
        self.save.triggered.connect (self.save_)
        self.saveas = self.file.addAction("Save As")
        self.saveas.triggered.connect (self.save_as)
        self.exit = self.file.addAction("Exit")
        self.exit.triggered.connect (self.Widget.Close)

        # set font size
        f = QtGui.QFont()
        f.setPointSize(12)
        self.teEdit.setFont(f)

    def new_page_act (self):
        self.Env.RunApp ('barge',None)

    def new_act (self):
        self.Widget.SetWindowTitle ("Untitled - Barge")
        self.teEdit.clear()

    def gettext (self,filename):
        self.teEdit.setText(files.readall(filename))
        self.Widget.SetWindowTitle(files.output(filename).replace('//',''))

    def saveas_ (self,filename):
        files.write(filename,self.teEdit.toPlainText())
        self.Widget.SetWindowTitle(files.output(filename).replace('//',''))

    def save_ (self,filename):
        if not self.Widget.WindowTitle()=='Untitled - Barge':
            files.write(files.output(self.Widget.WindowTitle()),self.teEdit.toPlainText())
        else:
            self.Env.RunApp('select', ['Save a file', 'save', self.saveas_])

    def open_act (self):
        self.Env.RunApp('select',['Choose a text file','open',self.gettext])

    def save_as (self):
        self.Env.RunApp('select', ['Save as file', 'save-as', self.saveas_])