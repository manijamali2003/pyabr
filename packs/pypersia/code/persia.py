from PyQt5.QtGui import  *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtWidgets, QtCore
import sys, importlib, random,py_compile
from libabr import System, App, Control, Files, Res, Commands

res = Res();files = Files();app = App();control=Control();commands = Commands()

f = QtGui.QFont()
f.setFamily('DejaVu Sans Mono')
f.setPointSize(12)

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

    def mkfile (self,filename):
        it = QtGui.QStandardItem(filename)
        it.setWhatsThis(self.dir + "/" + filename)
        it.setIcon(QtGui.QIcon(res.get(res.etc('roller','file-icon'))))
        self.entry.appendRow(it)
        self.format(it, filename)
        commands.cat (['-c',filename])
        it.setFont(f)

    def mkc (self,filename):
        self.mkfile(filename+".c")
        files.write(self.dir + "/" + filename+'.c',files.readall(res.get('@temp/untitled.c')))

    def mkcpp (self,filename):
        self.mkfile(filename+".cpp")
        files.write(self.dir + "/" + filename+'.cpp',files.readall(res.get('@temp/untitled.cpp')))

    def mkjava (self,filename):
        self.mkfile(filename+".java")
        files.write(self.dir + "/" + filename+'.java',files.readall(res.get('@temp/untitled.java')).replace("MainApp",filename))

    def mkjs (self,filename):
        self.mkfile(filename+".js")
        files.write(self.dir + "/" + filename+'.js',files.readall(res.get('@temp/untitled.js')))

    def mkphp (self,filename):
        self.mkfile(filename+".php")
        files.write(self.dir + "/" + filename+".php",files.readall(res.get('@temp/untitled.php')))

    def mkhtml (self,filename):
        self.mkfile(filename+".html")
        files.write(self.dir + "/" + filename+".html",files.readall(res.get('@temp/untitled.html')))

    def mkcs (self,filename):
        self.mkfile(filename+".cs")
        files.write(self.dir + "/" + filename+".cs",files.readall(res.get('@temp/untitled.cs')))

    def mksa (self,filename):
        self.mkfile(filename+".sa")
        files.write(self.dir + "/" + filename+".sa",files.readall(res.get('@temp/untitled.sa')))

    def mkpy (self,filename):
        self.mkfile(filename+".py")
        files.write(self.dir + "/" + filename+".py",files.readall(res.get('@temp/untitled.py')))

    def mkpygui (self,filename):
        self.mkfile(filename+".py")
        files.write(self.dir + "/" + filename+".py",files.readall(res.get('@temp/untitled-gui.py')))

    def __init__(self,editor):
        super().__init__()
        self.editor = editor
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
            if files.isdir(self.dir+"/"+text):
                it = QStandardItem(text)
                it.setWhatsThis(self.dir + "/" + text)
                self.format(it, text)
                self.entry.appendRow(it)

        for text in self.listdir:
            if files.isfile(self.dir+"/"+text):
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
                    if files.isdir(self.dir+"/"+text):
                        it = QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it, text)
                        self.entry.appendRow(it)

                for text in self.listdir:
                    if files.isfile(self.dir+"/"+text):
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
                    if files.isdir(self.dir+"/"+text):
                        it = QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it, text)
                        self.entry.appendRow(it)

                for text in self.listdir:
                    if files.isfile(self.dir+"/"+text):
                        it = QStandardItem(text)
                        it.setWhatsThis(self.dir + "/" + text)
                        self.format(it, text)
                        self.entry.appendRow(it)

            elif files.isfile(self.item.whatsThis()):
                files.write('/proc/info/fsel', self.item.whatsThis())  # Send File selected
                self.editor.teEdit.setPlainText(files.readall(self.item.whatsThis()))

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
        self.Widget.Resize (self,self.Env.width(),self.Env.height())
        self.Widget.SetWindowTitle(res.get('@string/app_name'))
        self.Widget.SetWindowIcon (QtGui.QIcon(res.get(res.etc(self.AppName,'logo'))))

        if self.External==[] or self.External=='' or self.External==None:
            self.Widget.SetWindowTitle(res.get('@string/untitled'))
        else:
            self.Widget.SetWindowTitle(self.External)

        # text box
        self.teEdit = QtWidgets.QTextEdit()
        #self.teEdit.setText(files.readall('/proc/info/fsel'))
        self.teEdit.setGeometry(int(self.Env.width()/5),20,self.Env.width()-int(self.Env.width()/5),self.Env.height())
        self.layout().addWidget(self.teEdit)

        self.xfile = QMainWindow()
        self.x = FileListView(self)
        self.xfile.setCentralWidget(self.x)
        self.xfile.setGeometry(0,20,int(self.Env.width()/5),self.Env.height())
        self.layout().addWidget(self.xfile)

        # menubar
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu(res.get('@string/file'))

        # file menu #
        self.new_code = self.file.addMenu(res.get('@string/new'))
        self.new_code.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'text'))))

        ## new file
        self.new_c = self.new_code.addAction(res.get('@string/c'))
        self.new_c.triggered.connect(self.New_C)
        self.new_c.setIcon(QIcon(res.get(res.etc("persia", "c"))))

        self.new_cpp = self.new_code.addAction(res.get('@string/c++'))
        self.new_cpp.triggered.connect(self.New_Cpp)
        self.new_cpp.setIcon(QIcon(res.get(res.etc("persia", "c++"))))

        self.new_cs = self.new_code.addAction(res.get('@string/csharp'))
        self.new_cs.triggered.connect(self.New_Csharp)
        self.new_cs.setIcon(QIcon(res.get(res.etc("persia", "c#"))))

        self.new_html = self.new_code.addAction(res.get('@string/html'))
        self.new_html.triggered.connect(self.New_Html)
        self.new_html.setIcon(QIcon(res.get(res.etc("persia", "html"))))

        self.new_java = self.new_code.addAction(res.get('@string/java'))
        self.new_java.triggered.connect(self.New_Java)
        self.new_java.setIcon(QIcon(res.get(res.etc("persia", "java"))))

        self.new_js = self.new_code.addAction(res.get('@string/javascript'))
        self.new_js.triggered.connect(self.New_Js)
        self.new_js.setIcon(QIcon(res.get(res.etc("persia", "js"))))

        self.new_Php = self.new_code.addAction(res.get('@string/php'))
        self.new_Php.triggered.connect(self.New_Php)
        self.new_Php.setIcon(QIcon(res.get(res.etc("persia", "php"))))

        self.new_py = self.new_code.addAction(res.get('@string/python'))
        self.new_py.triggered.connect(self.New_Py)
        self.new_py.setIcon(QIcon(res.get(res.etc("persia", "py"))))

        self.new_sa = self.new_code.addAction(res.get('@string/saye'))
        self.new_sa.triggered.connect(self.New_Sa)
        self.new_sa.setIcon(QIcon(res.get(res.etc("persia", "sa"))))

        self.new_pygui = self.new_code.addAction(res.get('@string/pythongui'))
        self.new_pygui.triggered.connect(self.New_PyGui)
        self.new_pygui.setIcon(QIcon(res.get(res.etc("persia", "py"))))
        ##

        self.new_project = self.file.addMenu(res.get('@string/new_page'))
        self.new_project.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName, 'py'))))

        self.new_page = self.new_project.addAction(res.get('@string/empty'))
        self.new_page.triggered.connect(self.new_empty_act)
        self.new_page.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName, 'py'))))

        self.new_gui = self.new_project.addAction(res.get('@string/gui'))
        self.new_gui.triggered.connect(self.new_gui_act)
        self.new_gui.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName, 'py'))))

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

        self.run = self.code.addAction('Run Project')
        self.run.triggered.connect (self.run_project_)

        self.insert_c = self.code.addMenu('Insert Code')

        # Codes #
        self.lang_c = self.insert_c.addAction(res.get('@string/c'))
        self.lang_c.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'c'))))
        self.lang_c.triggered.connect (self.langc)
        self.lang_cpp = self.insert_c.addAction(res.get('@string/c++'))
        self.lang_cpp.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'c++'))))
        self.lang_cpp.triggered.connect(self.langcpp)
        self.lang_cs = self.insert_c.addAction(res.get('@string/csharp'))
        self.lang_cs.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'c#'))))
        self.lang_cs.triggered.connect(self.langcs)
        self.lang_java = self.insert_c.addAction(res.get('@string/java'))
        self.lang_java.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'java'))))
        self.lang_java.triggered.connect(self.langjava)
        self.lang_python = self.insert_c.addAction(res.get('@string/python'))
        self.lang_python.triggered.connect(self.langpython)
        self.lang_python.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'py'))))
        self.lang_pythongui = self.insert_c.addAction(res.get('@string/pythongui'))
        self.lang_pythongui.triggered.connect(self.langpythonx)
        self.lang_pythongui.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'py'))))
        self.lang_saye = self.insert_c.addAction(res.get('@string/saye'))
        self.lang_saye.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'sa'))))
        self.lang_saye.triggered.connect(self.langsaye)
        self.lang_html = self.insert_c.addAction(res.get('@string/html'))
        self.lang_html.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'html'))))
        self.lang_html.triggered.connect(self.langhtml)
        self.lang_php = self.insert_c.addAction(res.get('@string/php'))
        self.lang_php.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'php'))))
        self.lang_php.triggered.connect(self.langphp)
        self.lang_js = self.insert_c.addAction(res.get('@string/javascript'))
        self.lang_js.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'js'))))
        self.lang_js.triggered.connect(self.langjs)

        # set font size
        self.teEdit.setFont(f)

    def run_(self):
        control = Control()
        file = files.readall('/proc/info/fsel')

        ## Run it ##
        if file.endswith (".c") or file.endswith('.cpp') or file.endswith('.cxx') or file.endswith('.c++'):
            commands.cc([file])
            self.Env.RunApp('commento',[file.replace('.cpp','').replace('.cxx','').replace('.c++','').replace('.c',''),'PyPersia Console'])
            files.remove(file.replace('.c','').replace('.cpp','').replace('.cxx','').replace('.c++',''))
        elif file.endswith ('.py'):
            # check graphical PyQt5 #
            if files.readall(file).__contains__('from PyQt5') and files.readall(file).__contains__('MainApp'):
                rand = str (random.randint(1000,9999))
                files.create(f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('name[en]','Debug App',f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('name[fa]','برنامه تستی',f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('logo','@icon/runner',f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('exec',f"debug_{rand}",f'/usr/share/applications/debug_{rand}.desk')
                py_compile.compile(files.input(file),files.input(f'/usr/app/debug_{rand}.pyc'))
                self.Env.RunApp(f'debug_{rand}',[None])
                files.remove(f'/usr/share/applications/debug_{rand}.desk')
                files.remove(f'/usr/app/debug_{rand}.pyc')
            else:
                self.Env.RunApp('commento', [file.replace('.py',''),'PyPersia Console'])
        elif file.endswith ('.sa'):
            self.Env.RunApp('commento', [file.replace('.sa',''), 'PyPersia Console'])

    def run_project_(self):
        pass

    def new_empty_act (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.project_create])

    def new_gui_act (self):
        self.Env.RunApp('input', [res.get('@string/filename'), self.project_create_gui])

    def project_create (self,projectname):
        su = files.readall('/proc/info/su')

        if not su=='root':
            System (f"paye crt empty /desk/{su}/Projects/{projectname}")
            commands.cd([f'/desk/{su}/Projects/{projectname}'])
        else:
            System(f"paye crt empty /root/Projects/{projectname}")
            commands.cd([f'/root/Projects/{projectname}'])

        commands.mv(['packs/app', f'packs/{projectname}'])
        commands.mv([f'packs/{projectname}/data/usr/share/docs/hello',
                     f'packs/{projectname}/data/usr/share/docs/{projectname}'])
        commands.mv([f'packs/{projectname}/code/hello.py', f'packs/{projectname}/code/{projectname}.py'])
        files.write(f'packs/{projectname}/control/manifest', f'name: {projectname}\ncopyright: (c) 2020 Your name\nlicense: Your license\nunpack: /\nbuild: year-month-day\nversion: 0.0.1\ndescription: Your application description\ncompile: Yes')

        files.write(f'packs/{projectname}/control/compile', f'{projectname}.py:usr/app/{projectname}.pyc')
        files.write(f'packs/{projectname}/control/list', f'/usr/app/{projectname}.pyc\n/usr/share/docs/{projectname}')

        files.write('/proc/info/psel', projectname)
        files.create(".pypersia")

        control.write_record('name', projectname, ".pypersia")
        control.write_record('type', 'empty', ".pypersia")
        control.write_record('lang', 'python', '.pypersia')

        self.Env.RunApp ('persia',projectname)

    def project_create_gui (self,projectname):
        su = files.readall('/proc/info/su')

        if not su=='root':
            System (f"paye crt empty /desk/{su}/Projects/{projectname}")
            commands.cd([f'/desk/{su}/Projects/{projectname}'])
        else:
            System(f"paye crt gui /root/Projects/{projectname}")
            commands.cd([f'/root/Projects/{projectname}'])

        commands.mv(['packs/app',f'packs/{projectname}'])
        commands.mv([f'packs/{projectname}/data/usr/share/docs/hello',f'packs/{projectname}/data/usr/share/docs/{projectname}'])
        commands.mv([f'packs/{projectname}/code/hello.py',f'packs/{projectname}/code/{projectname}.py'])
        commands.mv([f'packs/{projectname}/data/usr/share/applications/hello.desk',f'packs/{projectname}/data/usr/share/applications/{projectname}.desk'])
        files.write (f'packs/{projectname}/control/manifest',f'name: {projectname}\ncopyright: (c) 2020 Your name\nlicense: Your license\nunpack: /\nbuild: year-month-day\nversion: 0.0.1\ndescription: Your application description\ncompile: Yes')
        files.write(f'packs/{projectname}/control/compile', f'{projectname}.py:usr/app/{projectname}.pyc')
        files.write(f'packs/{projectname}/control/list',f'/usr/app/{projectname}.pyc\n/usr/share/docs/{projectname}')
        files.write(f'packs/{projectname}/data/usr/share/applications/{projectname}.desk',f'name[en]: {projectname}\nlogo: @icon/runner\nexec: {projectname}')

        files.write('/proc/info/psel', projectname)
        files.create(".pypersia")

        control.write_record('name', projectname, ".pypersia")
        control.write_record('type', 'gui', ".pypersia")
        control.write_record('lang','python','.pypersia')

        self.Env.RunApp ('persia',projectname)

    def new_act (self):
        self.Widget.SetWindowTitle (res.get('@string/untitled'))
        self.teEdit.clear()

    def gettext (self,filename):
        self.teEdit.setPlainText(files.readall(filename))
        self.Widget.SetWindowTitle(files.output(filename).replace('//',''))

        if self.Widget.WindowTitle()=='': self.Widget.SetWindowTitle (res.get('@string/untitled'))

    def saveas_ (self,filename):
        files.write(filename,self.teEdit.toPlainText())
        files.write('/proc/info/fsel',filename)

    def save_ (self,filename):
        if not self.Widget.WindowTitle()==res.get('@string/untitled'):
            files.write(files.readall('/proc/info/fsel'),self.teEdit.toPlainText())
        else:
            self.Env.RunApp('select', [res.get('@string/saveafile'), 'save', self.saveas_])

    def open_act (self):
        self.Env.RunApp('select',[res.get('@string/chooseafile'),'open',self.gettext])

    def save_as (self):
        self.Env.RunApp('select', [res.get('@string/saveasfile'), 'save-as', self.saveas_])

    def langc (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.c')))

    def langcpp (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.cpp')))

    def langjava (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.java')))

    def langpython (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.py')))

    def langpythonx (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled-gui.py')))

    def langcs (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.cs')))

    def langsaye (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.sa')))

    def langhtml (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.html')))

    def langphp (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.php')))

    def langjs (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.js')))

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