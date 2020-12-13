from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys, importlib, random
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
        self.Widget.SetWindowIcon (QtGui.QIcon(res.get(res.etc(self.AppName,'logo'))))

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
        self.new.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'text'))))
        self.new_page = self.file.addAction(res.get('@string/new_page'))
        self.new_page.triggered.connect (self.new_page_act)
        self.open = self.file.addAction(res.get('@string/open'))
        self.open.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'open'))))
        self.open.triggered.connect (self.open_act)
        self.save = self.file.addAction(res.get('@string/save'))
        self.save.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'save'))))
        self.save.triggered.connect (self.save_)
        self.saveas = self.file.addAction(res.get('@string/save_as'))
        self.saveas.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'save-as'))))
        self.saveas.triggered.connect (self.save_as)
        self.exit = self.file.addAction(res.get('@string/exit'))
        self.exit.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'exit'))))
        self.exit.triggered.connect (self.Widget.Close)

        # code menu
        self.code = self.menubar.addMenu('Code')
        self.run = self.code.addAction('Run')
        self.run.triggered.connect (self.run_)
        self.build = self.code.addAction('Build')
        self.build.setEnabled(False)

        self.insert_c = self.code.addMenu('Insert Code')

        # Codes #
        self.lang_c = self.insert_c.addAction('C')
        self.lang_c.setIcon(QtGui.QIcon(res.get('@icon/text-x-c')))
        self.lang_c.triggered.connect (self.langc)
        self.lang_cpp = self.insert_c.addAction('C++')
        self.lang_cpp.setIcon(QtGui.QIcon(res.get('@icon/text-x-c++')))
        self.lang_cpp.triggered.connect(self.langcpp)
        self.lang_cs = self.insert_c.addAction('C#')
        self.lang_cs.setIcon(QtGui.QIcon(res.get('@icon/text-csharp')))
        self.lang_cs.triggered.connect(self.langcs)
        self.lang_java = self.insert_c.addAction('Java')
        self.lang_java.setIcon(QtGui.QIcon(res.get('@icon/application-java')))
        self.lang_java.triggered.connect(self.langjava)
        self.lang_python = self.insert_c.addAction('Python')
        self.lang_python.triggered.connect(self.langpython)
        self.lang_python.setIcon(QtGui.QIcon(res.get('@icon/text-x-python3')))
        self.lang_pythongui = self.insert_c.addAction('Python GUI')
        self.lang_pythongui.triggered.connect(self.langpythonx)
        self.lang_pythongui.setIcon(QtGui.QIcon(res.get('@icon/text-x-python3')))
        self.lang_saye = self.insert_c.addAction('Saye')
        self.lang_saye.setIcon(QtGui.QIcon(res.get('@icon/application-x-executable-script')))
        self.lang_saye.triggered.connect(self.langsaye)
        self.lang_html = self.insert_c.addAction('HTML')
        self.lang_html.setIcon(QtGui.QIcon(res.get('@icon/html')))
        self.lang_html.triggered.connect(self.langhtml)
        self.lang_php = self.insert_c.addAction('PHP')
        self.lang_php.setIcon(QtGui.QIcon(res.get('@icon/application-x-php')))
        self.lang_php.triggered.connect(self.langphp)
        self.lang_js = self.insert_c.addAction('Java Script')
        self.lang_js.setIcon(QtGui.QIcon(res.get('@icon/application-javascript')))
        self.lang_js.triggered.connect(self.langjs)

        # set font size
        f = QtGui.QFont()
        f.setFamily('DejaVu Sans Mono')
        f.setPointSize(12)
        self.teEdit.setFont(f)

    def run_(self):
        control = Control()
        if self.Widget.WindowTitle()==res.get('@string/untitled'):
            self.save_('')

        ## Run it ##
        if self.Widget.WindowTitle().endswith (".c") or self.Widget.WindowTitle().endswith('.cpp') or self.Widget.WindowTitle().endswith('.cxx') or self.Widget.WindowTitle().endswith('.c++'):
            cmd.cc([self.Widget.WindowTitle()])
            self.Env.RunApp('commento',[self.Widget.WindowTitle().replace('.cpp','').replace('.cxx','').replace('.c++','').replace('.c',''),self.Widget.WindowTitle()])
            files.remove(self.Widget.WindowTitle())
        elif self.Widget.WindowTitle().endswith ('.py'):
            # check graphical PyQt5 #
            if files.readall(self.Widget.WindowTitle()).__contains__('from PyQt5') and files.readall(self.Widget.WindowTitle()).__contains__('MainApp'):
                rand = str (random.randint(1000,9999))
                files.create(f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('name[en]','Debug App',f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('name[fa]','برنامه تستی',f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('logo','@icon/app',f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('exec',f"debug_{rand}",f'/usr/share/applications/debug_{rand}.desk')
                cmd.cc([self.Widget.WindowTitle(),f'/usr/app/debug_{rand}.pyc'])
                self.Env.RunApp(f'debug_{rand}',[None])
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

    '''
    self.lang_c = self.insert_c.addAction('C')
        self.lang_cpp = self.insert_c.addAction('C++')
        self.lang_cs = self.insert_c.addAction('C#')
        self.lang_java = self.insert_c.addAction('Java')
        self.lang_python = self.insert_c.addAction('Python')
        self.lang_pythongui = self.insert_c.addAction('Python GUI')
        self.lang_saye = self.insert_c.addAction('Saye')
        self.lang_html = self.insert_c.addAction('HTML')
        self.lang_php = self.insert_c.addAction('PHP')
        self.lang_js = self.insert_c.addAction('Java Script')
    '''

    def langc (self):
        self.teEdit.setPlainText('''
#include <stdio.h>

int main ()
{
    printf ("Welcome to Barge!");
    return 0;
}
        ''')

    def langcpp (self):
        self.teEdit.setPlainText('''
#include <iostream>

using namespace std;

int main ()
{
    cout << "Welcome to Barge!";
    return 0;
}
        ''')

    def langjava (self):
        self.teEdit.setPlainText('''
class MainApp 
{
    pubic static void main (String[] args)
    {
        System.out.println ("Welcome to Barge!");
    }
}
        ''')

    def langpython (self):
        self.teEdit.setPlainText('''
from libabr import System, Control, Files, Colors, Script, App, Res

control = Control()
files = Files()
colors = Colors()
app = App()
res = Res()

class MainApp:
    def __init__ (self):
        print ("Welcome to Barge!")
        
MainApp ()
        ''')

    def langpythonx (self):
        self.teEdit.setPlainText('''
from libabr import System, Control, Files, Colors, Script, App, Res
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

control = Control()
files = Files()
colors = Colors()
app = App()
res = Res()

class MainApp (QMainWindow):
    def __init__ (self,ports):
        super(MainApp,self).__init__()
        
        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]
        
        self.Widget.Resize (self,500,300)
        self.Widget.SetWindowTitle ("Welcome to Barge!")
        self.Widget.SetWindowIcon (QIcon(res.get ('@icon/barge')))
        
        self.click_me = QPushButton ()
        self.click_me.setMaximumSize (300,300)
        self.layout().addWidget (self.click_me)
        
        ''')

    def langcs (self):
        self.teEdit.setPlainText('''
using System;

namespcae MyWelcomeApp
{
    public class MainApp
    {
        public static void Main (string[] args)
        {
            Console.WriteLine ("Welcome to Barge!");
        }
    }
}
        ''')

    def langsaye (self):
        self.teEdit.setPlainText('''
getv
echo Welcome to Barge!
        ''')

    def langhtml (self):
        self.teEdit.setPlainText('''
<!DOCTYPE HTML>
<html>
    <head>
        <title>Barge Example</title>
        <meta charset="utf-8"/>
    </head>
    <body>
        <p>Welcome to Barge!</p>
    </body>
</html>
        ''')

    def langphp (self):
        self.teEdit.setPlainText('''
<!DOCTYPE HTML>
<html>
    <head>
        <title>Barge Example</title>
        <meta charset="utf-8"/>
    </head>
    <body>
        <?php
            echo "<p>Welcome to Barge!</p>";
        ?>
    </body>
</html>
        ''')

    def langjs (self):
        self.teEdit.setPlainText('''
<!DOCTYPE HTML>
<html>
    <head>
        <title>Barge Example</title>
        <meta charset="utf-8"/>
    </head>
    <body>
        <script>
            window.alert ("Welcome to Barge!");
        </script>
    </body>
</html>
        ''')