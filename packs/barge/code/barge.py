from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys, importlib
from libabr import System, App, Control, Files, Res, Commands

res = Res();files = Files();app = App();control=Control();cmd = Commands()

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

        self.Widget.SetWindowTitle(res.get('@string/untitled'))

        # text box
        self.teEdit = QtWidgets.QTextEdit()
        self.setCentralWidget(self.teEdit)

        # menubar
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu(res.get('@string/file'))

        # file menu #
        self.new = self.file.addAction(res.get('@string/new'))
        self.new.triggered.connect (self.new_act)
        self.new_page = self.file.addAction(res.get('@string/new_page'))
        self.new_page.triggered.connect (self.new_page_act)
        self.open = self.file.addAction(res.get('@string/open'))
        self.open.triggered.connect (self.open_act)
        self.save = self.file.addAction(res.get('@string/save'))
        self.save.triggered.connect (self.save_)
        self.saveas = self.file.addAction(res.get('@string/save_as'))
        self.saveas.triggered.connect (self.save_as)
        self.exit = self.file.addAction(res.get('@string/exit'))
        self.exit.triggered.connect (self.Widget.Close)

        # code menu
        self.code = self.menubar.addMenu('Code')
        self.run = self.code.addAction('Run')
        self.run.triggered.connect (self.run_)
        self.build = self.code.addAction('Build')
        self.build.setEnabled(False)

        # set font size
        f = QtGui.QFont()
        f.setPointSize(12)
        self.teEdit.setFont(f)

    def run_(self):
        control = Control()
        if self.Widget.WindowTitle().endswith (".c") or self.Widget.WindowTitle().endswith('.cpp') or self.Widget.WindowTitle().endswith('.cxx') or self.Widget.WindowTitle().endswith('.c++'):
            cmd.cc([self.Widget.WindowTitle()])
            self.Env.RunApp('commento',[self.Widget.WindowTitle().replace('.cpp','').replace('.cxx','').replace('.c++','').replace('.c',''),self.Widget.WindowTitle()])
            files.remove(self.Widget.WindowTitle())
        elif self.Widget.WindowTitle().endswith ('.py'):
            # check graphical PyQt5 #
            if files.readall(self.Widget.WindowTitle()).__contains__('from PyQt5'):
                files.create('/usr/share/applications/debug.desk')
                cmd.cc([self.Widget.WindowTitle(),'/usr/app/debug_app.pyc'])
                self.Env.RunApp('debug',[None])
            else:
                self.Env.RunApp('commento', [self.Widget.WindowTitle().replace('.py',''),self.Widget.WindowTitle()])
        elif self.Widget.WindowTitle().endswith ('.sa'):
            self.Env.RunApp('commento', [self.Widget.WindowTitle().replace('.sa', ''), self.Widget.WindowTitle()])


    def new_page_act (self):
        self.Env.RunApp ('barge',None)

    def new_act (self):
        self.Widget.SetWindowTitle (res.get('@string/untitled'))
        self.teEdit.clear()

    def gettext (self,filename):
        self.teEdit.setText(files.readall(filename))
        self.Widget.SetWindowTitle(files.output(filename).replace('//',''))

        if self.Widget.WindowTitle()=='': self.Widget.SetWindowTitle (res.get('@string/untitled'))

    def saveas_ (self,filename):
        files.write(filename,self.teEdit.toPlainText())
        self.Widget.SetWindowTitle(files.output(filename).replace('//',''))

    def save_ (self,filename):
        if not self.Widget.WindowTitle()==res.get('@string/untitled'):
            files.write(files.output(self.Widget.WindowTitle()),self.teEdit.toPlainText())
        else:
            self.Env.RunApp('select', [res.get('@string/saveafile'), 'save', self.saveas_])

    def open_act (self):
        self.Env.RunApp('select',[res.get('@string/chooseafile'),'open',self.gettext])

    def save_as (self):
        self.Env.RunApp('select', [res.get('@string/saveasfile'), 'save-as', self.saveas_])