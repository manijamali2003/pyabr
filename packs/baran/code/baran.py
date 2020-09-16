
#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Pasand team. GNU General Pucdic License v3.0
#
#  Offical website:         http://itpasand.com
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/pasandteam/pyabr
#
#######################################################################################

## Imports ##
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, hashlib, os, importlib, subprocess
from libabr import Files, Control, Permissions, Colors, Process, Modules, App, System, Res, Commands

modules = Modules()
files = Files()
control = Control()
colors = Colors()
process = Process()
permissions = Permissions()
app = App()
res = Res()
commands = Commands()

## Main entry ##
application = QApplication (sys.argv)
app.start('desktop')
## https://www.cdog.pythonlibrary.org/2015/08/18/getting-your-screen-resolution-with-python/ Get screen model ##
screen_resolution = application.desktop().screenGeometry()
width, height = screen_resolution.width(), screen_resolution.height()

## variables ##

class variables:
    lock_clock_shadow = 'Yes'
    lock_clock_size = 100
    lock_clock_color = 'white'
    lock_clock_location = 'bottom/left'
    locale = 'en'
    submenu_hide = 'No'
    submenu_fgcolor = 'black'
    submenu_bgcolor = 'white'
    submenu_direction = 'ltr'
    submenu_fontsize = 12
    titlebar_close = '@icon/close'
    titlebar_close_hover = '@icon/close-hover'
    titlebar_float = '@icon/float'
    titlebar_float_hover = '@icon/float-hover'
    titlebar_bgcolor = '#123456'
    titlebar_fgcolor = 'white'
    taskbar_pins = 'calculator,pyshell,calendar'
    taskbar_location = 'bottom'
    taskbar_size = 70
    taskbar_locked = 'Yes'
    taskbar_float = 'Yes'
    backend_color = '#000000'
    backend_timeout = 1000
    splash_color = '#ABCDEF'
    splash_timeout = 3000
    fullscreen = True
    width = width
    height = height
    sides = False
    login_bgcolor = '#123456'
    login_fgcolor = '#000000'
    login_background = ''
    enter_bgcolor = ''
    enter_fgcolor = '#000000'
    enter_background = ''
    unlock_bgcolor = ''
    unlock_fgcolor = '#000000'
    unlock_background = ''
    username = ''
    password = ''
    desktop_bgcolor = '#FFFFFF'
    desktop_fgcolor = '#000000'
    desktop_background = ''
    lock_bgcolor = '#FFFFFF'
    lock_fgcolor = '#000000'
    lock_background = ''
    taskbar_bgcolor = '#FFFFFF'
    loginw_bgcolor = '#FFFFFF'
    userlogo_color = '#FFFFFF'
    input_bgcolor = '#FFFFFF'
    input_fgcolor = '#000000'
    loginw_fgcolor = '#000000'
    loginw_round_size = 20
    loginw_userlogo_round_size = 125
    loginw_input_round_size = 20
    loginw_location = 'center'
    loginw_input_fontsize = 12
    loginw_login_bgcolor = '#ABCDEF'
    loginw_login_fgcolor = '#FFFFFF'
    loginw_login_hover_bgcolor = '#123456'
    loginw_login_hover_fgcolor = '#FFFFFF'
    loginw_login_fontsize = 12
    loginw_login_round = 'Yes'
    loginw_login_round_size = 20
    loginw_login_hide = 'No'
    loginw_login_width = 300
    loginw_enter_bgcolor = 'pink'
    loginw_enter_fgcolor = '#FFFFFF'
    loginw_enter_hover_bgcolor = 'purple'
    loginw_enter_hover_fgcolor = '#FFFFFF'
    loginw_enter_fontsize = 12
    loginw_enter_round = 'Yes'
    loginw_enter_round_size = 20
    loginw_enter_hide = 'No'
    loginw_enter_width = 300
    loginw_unlock_bgcolor = 'lime'
    loginw_unlock_fgcolor = 'green'
    loginw_unlock_hover_bgcolor = 'green'
    loginw_unlock_hover_fgcolor = 'lime'
    loginw_unlock_fontsize = 12
    loginw_unlock_round = 'Yes'
    loginw_unlock_round_size = 20
    loginw_unlock_hide = 'No'
    loginw_unlock_width = 300
    loginw_shadow = 'Yes'
    loginw_userlogo_shadow = 'Yes'
    loginw_input_shadow = 'Yes'
    loginw_login_shadow = 'No'
    loginw_enter_shadow = 'No'
    loginw_unlock_shadow = 'No'
    loginw_input_width = 300
    loginw_input_height = 40
    loginw_login_height = 40
    loginw_enter_height = 40
    loginw_unlock_height = 40

## ## ## ## ##

## Get data ##
def getdata (name):
    return control.read_record (name,'/etc/gui')

## Backend ##
class Backend (QMainWindow):
    ## Run splash page ##
    def runSplash (self):
        self.setCentralWidget(Splash([self]))

    def runLogin (self):
        self.setCentralWidget(Login([self,self]))

    def runEnter (self):
        self.setCentralWidget(Enter([self,self],self.gui_params[1]))

    def runDesktop (self):
        self.setCentralWidget(Desktop([self],self.gui_params[1],self.gui_params[2]))

    def __init__(self):
        super(Backend, self).__init__()

        ## Set port name ##
        self.setObjectName('Backend')

        ## Get informations ##
        cs = files.readall ('/proc/info/cs')
        ver = files.readall('/proc/info/ver')
        cd = files.readall('/proc/info/cd')

        self.setWindowTitle(cs+' '+ver+' ('+cd+")")

        ## Get app logo ##
        applogo = getdata('logo')
        if not applogo == None:
            self.setWindowIcon(QIcon(res.get(applogo)))

        ## Get backend color ##
        color = getdata('backend.color')

        ## Set color ##
        if not color==None:
            variables.backend_color = color

        self.setStyleSheet('background-color: ' + variables.backend_color+";color: black;")

        ## Set size ##
        autosize = getdata('autosize')
        width = getdata('width')
        height = getdata('height')

        if not width==None and not autosize=='Yes':
            variables.width = int(width)

        if not height==None and not autosize=='Yes':
            variables.height = int(height)

        self.resize(variables.width, variables.height)

        ## Set sides ##
        ## Set sides ##
        sides = getdata('sides')

        if sides == 'Yes':
            variables.sides = True
        else:
            variables.sides = False

        if variables.sides == False:
            self.setWindowFlag(Qt.FramelessWindowHint)

        ## Show ##

            ## Get data ##
        fullscreen = getdata('fullscreen')

        if fullscreen == 'Yes':
            variables.fullscreen = True
        else:
            variables.fullscreen = False

        if variables.fullscreen == True:
            self.showFullScreen()
        else:
            self.show()

        ## Run backend after showing backend ##
        timeout = getdata('backend.timeout')
        if timeout == None:
            variables.backend_timeout = 1000
        else:
            variables.backend_timeout = int(timeout)

        self.gui_params = getdata('params')

        if self.gui_params==None: self.gui_params=[]
        else:
            self.gui_params = self.gui_params.split(',')

        if self.gui_params==[]:
            control.write_record('params','splash','/etc/gui')
            QTimer.singleShot(variables.backend_timeout, self.runSplash)  ## Run splash after 1s
        elif self.gui_params[0]=='splash':
            control.write_record('params','splash','/etc/gui')
            QTimer.singleShot(variables.backend_timeout, self.runSplash)
        elif self.gui_params[0]=='login':
            control.write_record('params','splash','/etc/gui')
            QTimer.singleShot(variables.backend_timeout, self.runLogin)
        elif self.gui_params[0]=='enter':
            control.write_record('params','splash','/etc/gui')
            QTimer.singleShot(variables.backend_timeout, self.runEnter)
        elif self.gui_params[0]=='desktop':
            control.write_record('params','splash','/etc/gui')
            QTimer.singleShot(variables.backend_timeout, self.runDesktop)
        else:
            sys.exit(0)

## Splash ##
class Splash (QMainWindow):

    ## Run login page ##
    def runLogin(self):
        self.setCentralWidget(Login([self.Backend]))

    def __init__(self,ports):
        super(Splash, self).__init__()

        ## Set port name ##
        self.setObjectName('Splash')

        ## Get informations ##
        cs = files.readall('/proc/info/cs')
        ver = files.readall('/proc/info/ver')
        cd = files.readall('/proc/info/cd')

        self.setWindowTitle(cs + ' ' + ver + ' (' + cd + ")")

        ## Get app logo ##
        applogo = getdata('logo')
        if not applogo == None:
            self.setWindowIcon(QIcon(res.get(applogo)))

        ## Get app logo ##
        applogo = getdata('logo')
        if not applogo==None:
            self.setWindowIcon(QIcon(res.get(applogo)))

        ## Ports ##

        self.Backend = ports[0]

        ## Get backend color ##
        color = getdata('splash.color')

        ## Set color ##
        if not color==None:
            variables.splash_color = color

        self.setStyleSheet('background-color: {0}'.replace('{0}',variables.splash_color))

        ## Set size ##
        width = getdata('width')
        height = getdata('height')
        autosize =getdata('autosize')

        if not width == None  and not autosize=='Yes':
            variables.width = int(width)

        if not height == None and not autosize=='Yes':
            variables.height = int(height)

        self.resize(variables.width, variables.height)

        ## Set sides ##
        sides = getdata('sides')

        if sides=='Yes':
            variables.sides = True
        else:
            variables.sides = False

        if variables.sides == False:
            self.setWindowFlag(Qt.FramelessWindowHint)

        ## Show ##
        ## Get data ##
        fullscreen = getdata('fullscreen')

        if fullscreen == 'Yes':
            variables.fullscreen = True
        else:
            variables.fullscreen = False

        if variables.fullscreen == True:
            self.showFullScreen()
        else:
            self.show()

        ## Splash Logo ##

        logo = getdata('splash.logo')

        self.logo = QToolButton()
        self.layout().addWidget (self.logo)

        ## Set logo ##
        if not logo==None:
            self.logo.setIcon(QIcon(res.get(logo)))

        logo_size = getdata('splash.logo-size')

        if not logo_size==None:
            self.w = int(logo_size)
        else:
            self.w = 300

        self.logo.setMaximumSize(self.w,self.w) ## Set size
        self.logo.setIconSize(QSize(self.w,self.w))

        self.logo.setStyleSheet('border:none;')

        self.logo.setGeometry(int(self.width()/2)-int(self.w/2),int(self.height()/2)-int(self.w/2),self.w,self.w)

        ## Run splash after showing backend ##
        timeout = getdata('splash.timeout')
        if timeout==None:
            variables.splash_timeout = 3000
        else:
            variables.splash_timeout = int(timeout)

        QTimer.singleShot(variables.splash_timeout, self.runLogin) ## Run login

## LoginW ##
class LoginWidget (QMainWindow):
    def __init__(self,ports):
        super(LoginWidget, self).__init__()

        ## ports ##

        self.Backend = ports[0]
        self.Env = ports[1]

        ######

        loginw_bgcolor = getdata('loginw.bgcolor')
        loginw_fgcolor = getdata('loginw.fgcolor')
        loginw_width = getdata('loginw.width')
        loginw_height = getdata('loginw.height')
        loginw_round = getdata('loginw.round')
        loginw_round_size = getdata('loginw.round-size')
        loginw_location = getdata('loginw.location')
        loginw_shadow = getdata('loginw.shadow')
        loginw_userlogo = getdata('loginw.userlogo')
        loginw_userlogo_shadow = getdata('loginw.userlogo.shadow')
        loginw_userlogo_color = getdata('loginw.userlogo.color')
        loginw_input_bgcolor = getdata('loginw.input.bgcolor')
        loginw_input_fgcolor = getdata('loginw.input.fgcolor')
        loginw_input_shadow = getdata('loginw.input.shadow')
        loginw_input_round = getdata('loginw.input.round')
        loginw_input_width = getdata('loginw.input.width')
        loginw_input_round_size = getdata('loginw.input.round-size')
        loginw_userlogo_round = getdata('loginw.userlogo.round')
        loginw_userlogo_round_size = getdata('loginw.userlogo.round-size')
        loginw_input_fontsize = getdata('loginw.input.fontsize')
        loginw_login_bgcolor = getdata('loginw.login.bgcolor')
        loginw_login_fgcolor = getdata('loginw.login.fgcolor')
        loginw_login_fontsize = getdata('loginw.login.fontsize')
        loginw_login_round = getdata('loginw.login.round')
        loginw_login_round_size = getdata('loginw.login.round-size')
        loginw_login_hide = getdata ('loginw.login.hide')
        loginw_login_hover_fgcolor = getdata('loginw.login.hover-fgcolor')
        loginw_login_hover_bgcolor = getdata('loginw.login.hover-bgcolor')
        loginw_login_width = getdata('loginw.login.width')
        loginw_login_shadow = getdata('loginw.login.shadow')
        loginw_enter_bgcolor = getdata('loginw.enter.bgcolor')
        loginw_enter_fgcolor = getdata('loginw.enter.fgcolor')
        loginw_enter_fontsize = getdata('loginw.enter.fontsize')
        loginw_enter_round = getdata('loginw.enter.round')
        loginw_enter_round_size = getdata('loginw.enter.round-size')
        loginw_enter_hide = getdata('loginw.enter.hide')
        loginw_enter_hover_fgcolor = getdata('loginw.enter.hover-fgcolor')
        loginw_enter_hover_bgcolor = getdata('loginw.enter.hover-bgcolor')
        loginw_enter_width = getdata('loginw.enter.width')
        loginw_enter_shadow = getdata('loginw.enter.shadow')
        loginw_unlock_bgcolor = getdata('loginw.unlock.bgcolor')
        loginw_unlock_fgcolor = getdata('loginw.unlock.fgcolor')
        loginw_unlock_fontsize = getdata('loginw.unlock.fontsize')
        loginw_unlock_round = getdata('loginw.unlock.round')
        loginw_unlock_round_size = getdata('loginw.unlock.round-size')
        loginw_unlock_hide = getdata('loginw.unlock.hide')
        loginw_unlock_hover_fgcolor = getdata('loginw.unlock.hover-fgcolor')
        loginw_unlock_hover_bgcolor = getdata('loginw.unlock.hover-bgcolor')
        loginw_unlock_width = getdata('loginw.unlock.width')
        loginw_unlock_shadow = getdata('loginw.unlock.shadow')
        loginw_input_height = getdata('loginw.input.height')
        loginw_login_height = getdata('loginw.login.height')
        loginw_enter_height = getdata('loginw.enter.height')
        loginw_unlock_height = getdata('loginw.unlock.height')

        ## Check data ##
        if loginw_bgcolor == None:
            loginw_bgcolor = variables.loginw_bgcolor

        if loginw_input_height == None:
            loginw_input_height = variables.loginw_input_height
        else:
            loginw_input_height = int(loginw_input_height)

        if loginw_login_height == None:
            loginw_login_height = variables.loginw_login_height
        else:
            loginw_login_height = int(loginw_login_height)

        if loginw_enter_height == None:
            loginw_enter_height = variables.loginw_enter_height
        else:
            loginw_enter_height = int(loginw_enter_height)

        if loginw_unlock_height == None:
            loginw_unlock_height = variables.loginw_unlock_height
        else:
            loginw_unlock_height = int(loginw_unlock_height)

        if loginw_login_width == None:
            loginw_login_width = variables.loginw_login_width
        else:
            loginw_login_width = int(loginw_login_width)

        if loginw_input_width == None:
            loginw_input_width = variables.loginw_input_width
        else:
            loginw_input_width = int(loginw_input_width)

        if loginw_enter_width == None:
            loginw_enter_width = variables.loginw_enter_width
        else:
            loginw_enter_width = int(loginw_enter_width)

        if loginw_unlock_width == None:
            loginw_unlock_width = variables.loginw_unlock_width
        else:
            loginw_unlock_width = int(loginw_unlock_width)

        if loginw_fgcolor == None:
            loginw_fgcolor = variables.loginw_fgcolor

        if loginw_login_bgcolor == None:
            loginw_login_bgcolor = variables.loginw_login_bgcolor

        if loginw_login_fgcolor == None:
            loginw_login_fgcolor = variables.loginw_login_fgcolor

        if loginw_login_hover_bgcolor == None:
            loginw_login_hover_bgcolor = variables.loginw_login_hover_bgcolor

        if loginw_login_hover_fgcolor == None:
            loginw_login_hover_fgcolor = variables.loginw_login_hover_fgcolor

        if loginw_enter_bgcolor == None:
            loginw_enter_bgcolor = variables.loginw_enter_bgcolor

        if loginw_enter_fgcolor == None:
            loginw_enter_fgcolor = variables.loginw_enter_fgcolor

        if loginw_enter_hover_bgcolor == None:
            loginw_enter_hover_bgcolor = variables.loginw_enter_hover_bgcolor

        if loginw_enter_hover_fgcolor == None:
            loginw_enter_hover_fgcolor = variables.loginw_enter_hover_fgcolor

        if loginw_unlock_bgcolor == None:
            loginw_unlock_bgcolor = variables.loginw_unlock_bgcolor

        if loginw_unlock_fgcolor == None:
            loginw_unlock_fgcolor = variables.loginw_unlock_fgcolor

        if loginw_unlock_hover_bgcolor == None:
            loginw_unlock_hover_bgcolor = variables.loginw_unlock_hover_bgcolor

        if loginw_unlock_hover_fgcolor == None:
            loginw_unlock_hover_fgcolor = variables.loginw_unlock_hover_fgcolor

        if loginw_width == None:
            loginw_width = self.width()

        if loginw_height == None:
            loginw_height = self.height()

        if loginw_round_size == None:
            loginw_round_size = str(variables.loginw_round_size)+'% '+str(variables.loginw_round_size)+'%'
        else:
            loginw_round_size = loginw_round_size.replace(' ','% ')+'%'

        if loginw_userlogo_round_size == None:
            loginw_userlogo_round_size = str(variables.loginw_userlogo_round_size)+'% '+str(variables.loginw_userlogo_round_size)+'%'
        else:
            loginw_userlogo_round_size = loginw_userlogo_round_size.replace(' ','% ')+'%'

        if loginw_input_round_size == None:
            loginw_input_round_size = str(variables.loginw_input_round_size)+'% '+str(variables.loginw_input_round_size)+'%'
        else:
            loginw_input_round_size = loginw_input_round_size.replace(' ','% ')+'%'

        if loginw_login_round_size == None:
            loginw_login_round_size = str(variables.loginw_login_round_size)+'% '+str(variables.loginw_login_round_size)+'%'
        else:
            loginw_login_round_size = loginw_login_round_size.replace(' ','% ')+'%'

        if loginw_enter_round_size == None:
            loginw_enter_round_size = str(variables.loginw_enter_round_size)+'% '+str(variables.loginw_enter_round_size)+'%'
        else:
            loginw_enter_round_size = loginw_enter_round_size.replace(' ','% ')+'%'

        if loginw_unlock_round_size == None:
            loginw_unlock_round_size = str(variables.loginw_unlock_round_size)+'% '+str(variables.loginw_unlock_round_size)+'%'
        else:
            loginw_unlock_round_size = loginw_unlock_round_size.replace(' ','% ')+'%'

        if loginw_round == 'Yes':
            loginw_round = loginw_round_size
        else:
            loginw_round ='0% 0%'

        if loginw_userlogo_round == 'Yes':
            loginw_userlogo_round = loginw_userlogo_round_size
        else:
            loginw_userlogo_round = '0% 0%'

        if loginw_input_round == 'Yes':
            loginw_input_round = loginw_input_round_size
        else:
            loginw_input_round = '0% 0%'

        if loginw_login_round == 'Yes':
            loginw_login_round = loginw_login_round_size
        else:
            loginw_login_round = '0% 0%'

        if loginw_enter_round == 'Yes':
            loginw_enter_round = loginw_enter_round_size
        else:
            loginw_enter_round = '0% 0%'

        if loginw_unlock_round == 'Yes':
            loginw_unlock_round = loginw_unlock_round_size
        else:
            loginw_unlock_round = '0% 0%'

        if loginw_location == None:
            loginw_location = variables.loginw_location

        if loginw_input_fontsize==None:
            loginw_input_fontsize = variables.loginw_input_fontsize
        else:
            loginw_input_fontsize = int(loginw_input_fontsize)

        if loginw_login_fontsize==None:
            loginw_login_fontsize = variables.loginw_login_fontsize
        else:
            loginw_login_fontsize = int(loginw_login_fontsize)

        if loginw_login_hide == None: loginw_login_hide = variables.loginw_login_hide

        if loginw_enter_fontsize==None:
            loginw_enter_fontsize = variables.loginw_enter_fontsize
        else:
            loginw_enter_fontsize = int(loginw_enter_fontsize)

        if loginw_enter_hide == None: loginw_enter_hide = variables.loginw_enter_hide

        if loginw_unlock_fontsize==None:
            loginw_unlock_fontsize = variables.loginw_unlock_fontsize
        else:
            loginw_unlock_fontsize = int(loginw_unlock_fontsize)

        if loginw_unlock_hide == None: loginw_unlock_hide = variables.loginw_unlock_hide

        self.setMaximumSize(int(loginw_width), int(loginw_height))  ## Set size of loginw

        ## Locations ##

        if loginw_location == 'center':
            self.setGeometry(int(self.Env.width() / 2) - int(self.width() / 2),
                             int(self.Env.height() / 2) - int(self.height() / 2), self.width(),
                             self.height())  ## Geometric
        elif loginw_location == 'top':
            self.setGeometry(int(self.Env.width() / 2) - int(self.width() / 2), int(self.height() / 20), self.width(),
                             self.height())  ## Geometric
        elif loginw_location == 'left':
            self.setGeometry(int(self.width() / 20), int(self.Env.height() / 2) - int(self.height() / 2), self.width(),
                             self.height())  ## Geometric
        elif loginw_location == 'right':
            self.setGeometry(self.Env.width() - int(self.width() / 20) - self.width(),
                             int(self.Env.height() / 2) - int(self.height() / 2), self.width(),
                             self.height())  ## Geometric
        elif loginw_location == 'bottom':
            self.setGeometry(int(self.Env.width() / 2) - int(self.width() / 2),
                             self.Env.height() - int(self.height() / 20) - self.height(), self.width(),
                             self.height())  ## Geometric

        if loginw_shadow==None: loginw_shadow = variables.loginw_shadow
        if loginw_userlogo_shadow == None: loginw_userlogo_shadow = variables.loginw_userlogo_shadow
        if loginw_input_shadow == None: loginw_input_shadow = variables.loginw_input_shadow
        if loginw_login_shadow == None: loginw_login_shadow = variables.loginw_login_shadow
        if loginw_enter_shadow == None: loginw_enter_shadow = variables.loginw_enter_shadow
        if loginw_unlock_shadow == None: loginw_unlock_shadow = variables.loginw_unlock_shadow

        if loginw_shadow=='Yes':
            ## Shadow ##
            # Copy right shadow box: medium.com/@rekols/qt-button-box-shadow-property-c47c7bf58721 ##
            shadow = QGraphicsDropShadowEffect()
            shadow.setColor(QColor(10, 2, 34, 255 * 0.8))
            shadow.setOffset(0)
            shadow.setBlurRadius(10)
            self.setGraphicsEffect(shadow)

            ## BackgroudcolorButton ##
        self.btnColorButton = QPushButton()
        self.btnColorButton.setGeometry(0,0,self.width(),self.height())
        self.layout().addWidget(self.btnColorButton)
            ##

            ## Set colors ##
        self.setStyleSheet('color:{0};border-radius:{1};'
            .replace('{0}', loginw_fgcolor)
            .replace('{1}', loginw_round)
        )  ## Set color white as default
        self.btnColorButton.setStyleSheet('background-color:{0};'
            .replace('{0}',loginw_bgcolor)
        )

        ## Userlogo ##

        self.userlogo = QToolButton()

            ## Set size & location ##
        self.userlogo.setMaximumSize(250,250)
        self.userlogo.setGeometry(int(self.width()/2)-int(self.userlogo.width()/2),int(self.height()/4)-int(self.userlogo.height()/4),self.userlogo.width(),self.userlogo.height())

        if loginw_userlogo_color == None: loginw_userlogo_color = variables.userlogo_color

        if not loginw_userlogo == None:
            if self.Env.objectName()=='Enter' or self.Env.objectName()=='Unlock':
                logo = control.read_record ('loginw.userlogo','/etc/users/'+self.Env.username)
                if not logo == None: loginw_userlogo = logo

            self.userlogo.setStyleSheet('background-color: {0};border-radius: {1};background-image: url({2});'
                .replace('{0}', loginw_userlogo_color)
                .replace('{1}',loginw_userlogo_round)
                .replace('{2}', res.get(loginw_userlogo))
            )

            ## Shadow for userlogo ##
        ## Shadow ##
        if loginw_userlogo_shadow=='Yes':
            # Copy right shadow box: medium.com/@rekols/qt-button-box-shadow-property-c47c7bf58721 ##
            shadow = QGraphicsDropShadowEffect()
            shadow.setColor(QColor(10, 2, 34, 255 * 0.8))
            shadow.setOffset(0)
            shadow.setBlurRadius(10)
            self.userlogo.setGraphicsEffect(shadow)

            ## Default userlogo ##
        self.layout().addWidget (self.userlogo)

            ## leInput username ##

        self.leInput = QLineEdit()

            ## Size & Location of leInput ##
        self.leInput.setMaximumSize(loginw_input_width,loginw_input_height)
        self.leInput.setGeometry(int(self.width()/2)-int(self.leInput.width()/2),self.height()-int(self.height()/4)-self.leInput.height(),self.leInput.width(),self.leInput.height())

            ## Shadow of leInput ##
        ## Shadow ##
        if loginw_input_shadow=='Yes':
            # Copy right shadow box: medium.com/@rekols/qt-button-box-shadow-property-c47c7bf58721 ##
            shadow = QGraphicsDropShadowEffect()
            shadow.setColor(QColor(10, 2, 34, 255 * 0.8))
            shadow.setOffset(0)
            shadow.setBlurRadius(10)
            self.leInput.setGraphicsEffect(shadow)

            ## Colors of leInput ##
        if loginw_input_bgcolor==None: loginw_input_bgcolor=variables.input_bgcolor
        if loginw_input_fgcolor==None: loginw_input_fgcolor=variables.input_fgcolor

            ## Setting up all colors ##
        self.leInput.setStyleSheet('padding-left: 10%;padding-right: 10%;background-color: '+loginw_input_bgcolor+';color: '+loginw_input_fgcolor+";border-width: 3%;border-radius: "+loginw_input_round)

            ## Place holder in input ##

        if self.Env.objectName()=='Login':
            self.leInput.setPlaceholderText(res.get('@string/username_placeholder')) # See https://stackoverflow.com/questions/24274318/placeholder-text-not-showing-pyside-pyqt
        else:
            self.leInput.setEchoMode(QLineEdit.Password)
            self.leInput.setPlaceholderText(res.get('@string/password_placeholder').replace("{0}",self.Env.username))

            ## Setting up font settings ##
        f = QFont()
        f.setPointSize(int(loginw_input_fontsize))
        self.leInput.setFont(f)

            ## Connect to action ##

        self.leInput.returnPressed.connect (self.actions)

        ## Add leInput Widget ##
        self.layout().addWidget(self.leInput)

            ## Enter button ##
        if self.Env.objectName()=='Login':
            self.btnLogin = QPushButton()

            ## Shadow ##
            if loginw_login_shadow == 'Yes':
                ## Shadow ##
                # Copy right shadow box: medium.com/@rekols/qt-button-box-shadow-property-c47c7bf58721 ##
                shadow = QGraphicsDropShadowEffect()
                shadow.setColor(QColor(10, 2, 34, 255 * 0.8))
                shadow.setOffset(0)
                shadow.setBlurRadius(10)
                self.btnLogin.setGraphicsEffect(shadow)

            self.btnLogin.clicked.connect (self.actions)
            self.btnLogin.setStyleSheet('''
                    QPushButton {
                        background-color: ''' + loginw_login_bgcolor + """;
                        color: """ + loginw_login_fgcolor + """;
                        border-radius: """ + loginw_login_round + '''
                    } 
                    QPushButton:hover {
                        background-color:''' + loginw_login_hover_bgcolor + ''';
                        color:''' + loginw_login_hover_fgcolor + ''';
                        border-radius: ''' + loginw_login_round + ''';
                    }
                    ''')

            f = QFont()
            f.setPointSize(int(loginw_login_fontsize))
            self.btnLogin.setFont(f)
            if loginw_login_hide == 'Yes':
                self.btnLogin.hide()
            self.btnLogin.setText(res.get('@string/next_text'))
            self.btnLogin.setMaximumSize(loginw_login_width, loginw_login_height)
            self.btnLogin.setGeometry(int(self.width() / 2) - int(self.btnLogin.width() / 2),
                                      self.height() - int(self.height() / 4) - int(self.btnLogin.height() / 4) + int(self.btnLogin.height()/2),
                                      self.btnLogin.width(), self.btnLogin.height())
            self.layout().addWidget(self.btnLogin)

        elif self.Env.objectName() == 'Enter':
            self.btnEnter = QPushButton()
            ## Shadow ##
            if loginw_enter_shadow == 'Yes':
                ## Shadow ##
                # Copy right shadow box: medium.com/@rekols/qt-button-box-shadow-property-c47c7bf58721 ##
                shadow = QGraphicsDropShadowEffect()
                shadow.setColor(QColor(10, 2, 34, 255 * 0.8))
                shadow.setOffset(0)
                shadow.setBlurRadius(10)
                self.btnEnter.setGraphicsEffect(shadow)

            self.btnEnter.clicked.connect (self.actions)
            self.btnEnter.setStyleSheet('''
                    QPushButton {
                        background-color: ''' + loginw_enter_bgcolor + """;
                        color: """ + loginw_enter_fgcolor + """;
                        border-radius: """ + loginw_enter_round + '''
                    } 
                    QPushButton:hover {
                        background-color:''' + loginw_enter_hover_bgcolor + ''';
                        color:''' + loginw_enter_hover_fgcolor + ''';
                        border-radius: ''' + loginw_enter_round + ''';
                    }
                    ''')

            f = QFont()
            f.setPointSize(int(loginw_enter_fontsize))
            self.btnEnter.setFont(f)
            if loginw_enter_hide == 'Yes':
                self.btnEnter.hide()
            self.btnEnter.setText(res.get('@string/enter_text'))
            self.btnEnter.setMaximumSize(loginw_enter_width, loginw_enter_height)
            self.btnEnter.setGeometry(int(self.width() / 2) - int(self.btnEnter.width() / 2),
                                      self.height() - int(self.height() / 4) - int(self.btnEnter.height() / 4) + int(self.btnEnter.height()/2),
                                      self.btnEnter.width(), self.btnEnter.height())
            self.layout().addWidget(self.btnEnter)
        elif self.Env.objectName()=='Unlock':
            self.btnUnlock = QPushButton()
            ## Shadow ##
            if loginw_unlock_shadow == 'Yes':
                ## Shadow ##
                # Copy right shadow box: medium.com/@rekols/qt-button-box-shadow-property-c47c7bf58721 ##
                shadow = QGraphicsDropShadowEffect()
                shadow.setColor(QColor(10, 2, 34, 255 * 0.8))
                shadow.setOffset(0)
                shadow.setBlurRadius(10)
                self.btnUnlock.setGraphicsEffect(shadow)

            self.btnUnlock.clicked.connect(self.actions)
            self.btnUnlock.setStyleSheet('''
                                QPushButton {
                                    background-color: ''' + loginw_unlock_bgcolor + """;
                                    color: """ + loginw_unlock_fgcolor + """;
                                    border-radius: """ + loginw_unlock_round + '''
                                } 
                                QPushButton:hover {
                                    background-color:''' + loginw_unlock_hover_bgcolor + ''';
                                    color:''' + loginw_unlock_hover_fgcolor + ''';
                                    border-radius: ''' + loginw_unlock_round + ''';
                                }
                                ''')

            f = QFont()
            f.setPointSize(int(loginw_unlock_fontsize))
            self.btnUnlock.setFont(f)
            if loginw_enter_hide == 'Yes':
                self.btnUnlock.hide()
            self.btnUnlock.setText(res.get('@string/unlock_text'))
            self.btnUnlock.setMaximumSize(loginw_unlock_width, loginw_unlock_height)
            self.btnUnlock.setGeometry(int(self.width() / 2) - int(self.btnUnlock.width() / 2),
                                      self.height() - int(self.height() / 4) - int(self.btnUnlock.height() / 4) + int(
                                          self.btnUnlock.height() / 2),
                                      self.btnUnlock.width(), self.btnUnlock.height())
            self.layout().addWidget(self.btnUnlock)

    def actions (self):
        if self.Env.objectName() == 'Login':
            username = self.leInput.text().lower()  ## Get username

            if self.Env.guest == 'Yes' and username == 'guest':
                self.Env.setCentralWidget(Desktop([self.Backend,self],username,'*'))

            elif not files.isfile('/etc/users/' + username):
                self.leInput.clear()
                self.leInput.setEnabled(False)
                message = res.get('@string/user_not_found')
                if not message==None: message = message.replace("{0}",username)
                self.leInput.setPlaceholderText(message)
                QTimer.singleShot(2500, self.clean)
            else:
                ## Check user ##
                hashname = hashlib.sha3_256(username.encode()).hexdigest()  ## Get hashname
                name = control.read_record ('username','/etc/users/'+username)

                if not hashname==name:
                    self.leInput.clear()
                    self.leInput.setEnabled(False)
                    message = res.get('@string/user_not_found')
                    if not message == None: message = message.replace("{0}", username)
                    self.leInput.setPlaceholderText(message)
                    QTimer.singleShot(2500, self.clean)

                else:
                    ## Setting up switched user ##

                    self.Env.setCentralWidget(Enter ([self.Backend,self],username)) ## Switch user
        elif self.Env.objectName()=='Enter':

            username = self.Env.username
            password = self.leInput.text()

            ## Check password ##
            hashcode = hashlib.sha3_512(password.encode()).hexdigest() ## Create hashcode for password
            code = control.read_record('code','/etc/users/'+username)

            if not code==hashcode:
                self.leInput.clear()
                self.leInput.setEnabled(False)
                message = res.get('@string/wrong_password')
                self.leInput.setPlaceholderText(message)
                QTimer.singleShot(2500, self.clean)
            else:
                self.Env.setCentralWidget(Desktop([self.Backend,self],username,password))

        elif self.Env.objectName()=='Unlock':

            username = self.Env.username
            password = self.leInput.text()

            ## Check password ##
            hashcode = hashlib.sha3_512(password.encode()).hexdigest()  ## Create hashcode for password
            code = control.read_record('code', '/etc/users/' + username)

            if not code == hashcode:
                self.leInput.clear()
                self.leInput.setEnabled(False)
                message = res.get('@string/wrong_password')
                self.leInput.setPlaceholderText(message)
                QTimer.singleShot(2500, self.clean)
            else:
                self.hide()
                self.Env.hide()

    def clean (self):
        self.leInput.setEnabled(True)
        if self.Env.objectName()=='Login':
            self.leInput.setPlaceholderText(res.get('@string/username_placeholder')) # See https://stackoverflow.com/questions/24274318/placeholder-text-not-showing-pyside-pyqt
        else:
            self.leInput.setPlaceholderText(res.get('@string/password_placeholder').replace('{0}',self.Env.username))

## Login ##
class Login (QMainWindow):
    def __init__(self,ports):
        super(Login, self).__init__()

        ## Guest user ##
        self.guest = control.read_record('enable_gui','/etc/guest')

        ## Set port name ##
        self.setObjectName('Login')

        ## Get informations ##
        cs = files.readall('/proc/info/cs')
        ver = files.readall('/proc/info/ver')
        cd = files.readall('/proc/info/cd')

        self.setWindowTitle(cs + ' ' + ver + ' (' + cd + ")")

        ## Get app logo ##
        applogo = getdata('logo')
        if not applogo == None:
            self.setWindowIcon(QIcon(res.get(applogo)))

        ## Ports ##

        self.Backend = ports[0]

        bgcolor = getdata('login.bgcolor')
        background = getdata('login.background')
        fgcolor = getdata('login.fgcolor')

        ## Widget for bgcolor or background ##
        self.backgroundButton = QPushButton()
        self.backgroundButton.setGeometry(0,0,variables.width,variables.height)
        self.layout().addWidget(self.backgroundButton)

        ## Set bgcolor and background ##

        if background==None and bgcolor==None and not fgcolor==None:
            variables.login_fgcolor = fgcolor
            ## Set colors ##
            self.setStyleSheet('color: {0};'.replace('{0}',variables.login_fgcolor))
            self.backgroundButton.setStyleSheet('border:none;background-color: {0};'.replace('{0}',variables.login_bgcolor))

        elif background==None and not fgcolor==None:

            ## Set colors ##
            variables.login_bgcolor = bgcolor
            variables.login_fgcolor = fgcolor

            self.setStyleSheet('color: {0};'.replace('{0}', variables.login_fgcolor))

            self.backgroundButton.setStyleSheet('border:none;background-color: {0};'.replace('{0}', variables.login_bgcolor))
        elif not background==None and not fgcolor==None:
            ## Set bgcolor ##

            variables.login_background = res.get(background)
            self.setStyleSheet('color: {0};'.replace('{0}', variables.login_fgcolor))
            self.backgroundButton.setStyleSheet('border:none;background-image: url({0});'.replace('{0}', variables.login_background))
        else:
            self.setStyleSheet('background-color:{1};color: {0};'.replace('{0}', variables.login_fgcolor).replace('{1}',variables.login_bgcolor))

        ## Set size ##
        width = getdata('width')
        height = getdata('height')
        autosize =getdata('autosize')

        if not width == None  and not autosize=='Yes':
            variables.width = int(width)

        if not height == None and not autosize=='Yes':
            variables.height = int(height)

        self.resize(variables.width, variables.height)

        ## Set sides ##
        ## Set sides ##
        sides = getdata('sides')

        if sides == 'Yes':
            variables.sides = True
        else:
            variables.sides = False
        if variables.sides == False:
            self.setWindowFlag(Qt.FramelessWindowHint)

        ## Login widget ##

        self.loginw = LoginWidget([self.Backend,self])
        self.layout().addWidget (self.loginw)

        ## Show ##
        ## Get data ##
        fullscreen = getdata('fullscreen')

        if fullscreen == 'Yes':
            variables.fullscreen = True
        else:
            variables.fullscreen = False

        if variables.fullscreen == True:
            self.showFullScreen()
        else:
            self.show()

## Enter ##
class Enter (QMainWindow):
    def __init__(self,ports,username):
        super(Enter, self).__init__()

        ## username ##
        self.username = username.lower()

        ## Ports ##
        self.Backend = ports[0]
        self.Env = ports[1]

        ## Set port name ##
        self.setObjectName('Enter')

        ## Get informations ##
        cs = files.readall('/proc/info/cs')
        ver = files.readall('/proc/info/ver')
        cd = files.readall('/proc/info/cd')

        self.setWindowTitle(cs + ' ' + ver + ' (' + cd + ")")

        ## Get app logo ##
        applogo = getdata('logo')
        if not applogo == None:
            self.setWindowIcon(QIcon(res.get(applogo)))

        bgcolor = getdata('enter.bgcolor')
        background = getdata('enter.background')
        fgcolor = getdata('enter.fgcolor')

        if not self.username=='guest':
            value = control.read_record('enter.bgcolor','/etc/users/'+self.username)
            if not value==None: bgcolor = value

        if not self.username=='guest':
            value = control.read_record('enter.background','/etc/users/'+self.username)
            if not value==None: background = value

        if not self.username=='guest':
            value = control.read_record('enter.fgcolor','/etc/users/'+self.username)
            if not value==None: fgcolor = value

        ## Widget for bgcolor or background ##
        self.backgroundButton = QPushButton()
        self.backgroundButton.setGeometry(0, 0, variables.width, variables.height)
        self.layout().addWidget(self.backgroundButton)

        ## Set bgcolor and background ##

        if background == None and bgcolor == None and not fgcolor == None:
            variables.enter_fgcolor = fgcolor
            ## Set colors ##
            self.setStyleSheet('color: {0};'.replace('{0}', variables.enter_fgcolor))
            self.backgroundButton.setStyleSheet(
                'border:none;background-color: {0};'.replace('{0}', variables.enter_bgcolor))

        elif background == None and not fgcolor == None:

            ## Set colors ##
            variables.enter_bgcolor = bgcolor
            variables.enter_fgcolor = fgcolor

            self.setStyleSheet('color: {0};'.replace('{0}', variables.enter_fgcolor))

            self.backgroundButton.setStyleSheet(
                'border:none;background-color: {0};'.replace('{0}', variables.enter_bgcolor))
        elif not background == None and not fgcolor == None:
            ## Set bgcolor ##

            variables.enter_background = res.get(background)
            self.setStyleSheet('color: {0};'.replace('{0}', variables.enter_fgcolor))
            self.backgroundButton.setStyleSheet(
                'border:none;background-image: url({0});'.replace('{0}', variables.enter_background))
        else:
            self.setStyleSheet('background-color:{1};color: {0};'.replace('{0}', variables.enter_fgcolor).replace('{1}',variables.enter_bgcolor))

        ## Set size ##
        width = getdata('width')
        height = getdata('height')
        autosize =getdata('autosize')

        if not width == None  and not autosize=='Yes':
            variables.width = int(width)

        if not height == None and not autosize=='Yes':
            variables.height = int(height)

        self.resize(variables.width, variables.height)

        ## Set sides ##
        ## Set sides ##
        sides = getdata('sides')

        if sides == 'Yes':
            variables.sides = True
        else:
            variables.sides = False
        if variables.sides == False:
            self.setWindowFlag(Qt.FramelessWindowHint)

        ## Login widget ##

        self.loginw = LoginWidget([self.Backend,self])
        self.layout().addWidget (self.loginw)

        ## Show ##
        ## Get data ##
        fullscreen = getdata('fullscreen')

        if fullscreen == 'Yes':
            variables.fullscreen = True
        else:
            variables.fullscreen = False

        if variables.fullscreen == True:
            self.showFullScreen()
        else:
            self.show()

## Enter ##
class Unlock (QMainWindow):
    def __init__(self,ports,username):
        super(Unlock, self).__init__()

        ## username ##
        self.username = username.lower()

        ## Ports ##
        self.Backend = ports[0]
        self.Env = ports[1]

        ## Set port name ##
        self.setObjectName('Unlock')

        ## Get informations ##
        cs = files.readall('/proc/info/cs')
        ver = files.readall('/proc/info/ver')
        cd = files.readall('/proc/info/cd')

        self.setWindowTitle(cs + ' ' + ver + ' (' + cd + ")")

        ## Get app logo ##
        applogo = getdata('logo')
        if not applogo == None:
            self.setWindowIcon(QIcon(res.get(applogo)))

        bgcolor = getdata('unlock.bgcolor')
        background = getdata('unlock.background')
        fgcolor = getdata('unlock.fgcolor')

        if not self.username=='guest':
            value = control.read_record('unlock.bgcolor','/etc/users/'+self.username)
            if not value==None: bgcolor = value

        if not self.username=='guest':
            value = control.read_record('unlock.background','/etc/users/'+self.username)
            if not value==None: background = value

        if not self.username=='guest':
            value = control.read_record('unlock.fgcolor','/etc/users/'+self.username)
            if not value==None: fgcolor = value

        ## Widget for bgcolor or background ##
        self.backgroundButton = QPushButton()
        self.backgroundButton.setGeometry(0, 0, variables.width, variables.height)
        self.layout().addWidget(self.backgroundButton)

        ## Set bgcolor and background ##

        if background == None and bgcolor == None and not fgcolor == None:
            variables.unlock_fgcolor = fgcolor
            ## Set colors ##
            self.setStyleSheet('color: {0};'.replace('{0}', variables.unlock_fgcolor))
            self.backgroundButton.setStyleSheet(
                'border:none;background-color: {0};'.replace('{0}', variables.unlock_bgcolor))

        elif background == None and not fgcolor == None:

            ## Set colors ##
            variables.unlock_bgcolor = bgcolor
            variables.unlock_fgcolor = fgcolor

            self.setStyleSheet('color: {0};'.replace('{0}', variables.unlock_fgcolor))

            self.backgroundButton.setStyleSheet(
                'border:none;background-color: {0};'.replace('{0}', variables.unlock_bgcolor))
        elif not background == None and not fgcolor == None:
            ## Set bgcolor ##

            variables.unlock_background = res.get(background)
            self.setStyleSheet('color: {0};'.replace('{0}', variables.unlock_fgcolor))
            self.backgroundButton.setStyleSheet(
                'border:none;background-image: url({0});'.replace('{0}', variables.unlock_background))
        else:
            self.setStyleSheet('background-color:{1};color: {0};'.replace('{0}', variables.unlock_fgcolor).replace('{1}',variables.unlock_bgcolor))

        ## Set size ##
        width = getdata('width')
        height = getdata('height')
        autosize =getdata('autosize')

        if not width == None  and not autosize=='Yes':
            variables.width = int(width)

        if not height == None and not autosize=='Yes':
            variables.height = int(height)

        self.resize(variables.width, variables.height)

        ## Set sides ##
        ## Set sides ##
        sides = getdata('sides')

        if sides == 'Yes':
            variables.sides = True
        else:
            variables.sides = False
        if variables.sides == False:
            self.setWindowFlag(Qt.FramelessWindowHint)

        ## Login widget ##

        self.loginw = LoginWidget([self.Env,self])
        self.layout().addWidget (self.loginw)

        ## Show ##
        ## Get data ##
        fullscreen = getdata('fullscreen')

        if fullscreen == 'Yes':
            variables.fullscreen = True
        else:
            variables.fullscreen = False

        if variables.fullscreen == True:
            self.showFullScreen()
        else:
            self.show()

## Taskbar ##
class TaskBar (QToolBar):
    def __init__(self,ports):
        super(TaskBar,self).__init__()

        ## Ports ##
        self.Backend = ports[0]
        self.Env = ports[1]

        ## Set username ##
        self.username = self.Env.username

            ## Get DATAS ###################

        ## Set bgcolor ##
        bgcolor = getdata('taskbar.bgcolor')
        if not self.Env.username=='guest':
            value = control.read_record('taskbar.bgcolor','/etc/users/'+self.username)
            if not value==None: bgcolor = value
        if bgcolor == None: bgcolor = variables.taskbar_bgcolor

        ## Set fgcolor ##
        fgcolor = getdata('taskbar.fgcolor')
        if not self.Env.username=='guest':
            value = control.read_record('taskbar.fgcolor','/etc/users/'+self.username)
            if not value==None: fgcolor = value
        if fgcolor == None: fgcolor = 'black'

        ## Set location ##
        location = getdata('taskbar.location')
        if not self.Env.username == 'guest':
            value = control.read_record('taskbar.location', '/etc/users/' + self.username)
            if not value == None: location = value
        if location == None: location = variables.taskbar_location

        ## locked ##
        locked = getdata('taskbar.locked')
        if not self.Env.username == 'guest':
            value = control.read_record('taskbar.locked', '/etc/users/' + self.username)
            if not value == None: locked = value
        if locked == None: locked = variables.taskbar_locked

        ## locked ##
        size = getdata('taskbar.size')
        if not self.Env.username == 'guest':
            value = control.read_record('taskbar.size', '/etc/users/' + self.username)
            if not value == None: locked = int(value)
        if size == None: size = variables.taskbar_size

        # float #
        float = getdata('taskbar.float')
        if not self.Env.username == 'guest':
            value = control.read_record('taskbar.float', '/etc/users/' + self.username)
            if not value == None: float = value
        if float == None: float = variables.taskbar_float

        # pins #
        pins = getdata('taskbar.pins')
        if not self.Env.username == 'guest':
            value = control.read_record('taskbar.pins', '/etc/users/' + self.username)
            if not value == None: pins = value
        if pins == None: pins = variables.taskbar_pins

        # styles #

        self.setStyleSheet('background-color: '+bgcolor+";color: "+fgcolor+";")

        # location #
        if location=='top':
            self.Env.addToolBar (Qt.TopToolBarArea,self)
        elif location=='left':
            self.Env.addToolBar(Qt.LeftToolBarArea, self)
        elif location=='right':
            self.Env.addToolBar(Qt.RightToolBarArea, self)
        elif location=='bottom':
            self.Env.addToolBar(Qt.BottomToolBarArea, self)

        # locked #
        if locked=='Yes':
            self.setMovable(False)
        else:
            self.setMovable(True)

        # float #
        if float=='Yes':
            self.setFloatable(True)
        else:
            self.setFloatable(False)

        # size #
        self.setMinimumSize(QSize(int(size),int(size)))
        self.setIconSize(QSize(int(size), int(size))) # https://stackoverflow.com/questions/21133612/how-to-change-iconsize-of-qtoolbutton

        # pins #
        pins = pins.split (',')

        for i in pins:
            find = '/usr/share/applications/'+i+'.desk'
            if files.isfile (find):
                # app logo
                applogo = control.read_record('logo', find)
                # design
                self.btnApp = QToolButton()
                if not applogo==None:
                    self.btnApp.setIcon(QIcon(res.get(applogo)))
                self.btnApp.setMinimumSize(int(size),int(size))
                self.btnApp.setObjectName(i)
                self.btnApp.clicked.connect (self.RunApplication)
                self.addWidget(self.btnApp)

    def RunApplication (self):
        sender = self.sender().objectName()
        self.Env.RunApp (sender)

## Application ##
class Application (QDockWidget):
    def __init__(self,ports):
        super(Application, self).__init__()

        self.Backend = ports[0]
        self.Env = ports[1]
        self.App = ports[2]

        self.username = self.Env.username

        app.start(self.App) # start the application

        self.setObjectName(self.App)

        exec = control.read_record('exec','/usr/share/applications/'+self.App+".desk")

        if not exec==None:
            exec = importlib.import_module(exec)
        else:
            self.close()

        self.setWidget(exec.MainApp([self.Backend,self.Env,self]))

        close = getdata('titlebar.close')
        if not self.Env.username == 'guest':
            value = control.read_record('titlebar.close', '/etc/users/' + self.username)
            if not value == None: close = value
        if close == None: close = variables.titlebar_close

        close_hover = getdata('titlebar.close-hover')
        if not self.Env.username == 'guest':
            value = control.read_record('titlebar.close-hover', '/etc/users/' + self.username)
            if not value == None: close_hover = value
        if close_hover == None: close_hover = variables.titlebar_close_hover

        float = getdata('titlebar.float')
        if not self.Env.username == 'guest':
            value = control.read_record('titlebar.float', '/etc/users/' + self.username)
            if not value == None: float = value
        if float == None: float = variables.titlebar_float

        float_hover = getdata('titlebar.float-hover')
        if not self.Env.username == 'guest':
            value = control.read_record('titlebar.float-hover', '/etc/users/' + self.username)
            if not value == None: float_hover = value
        if float_hover == None: float_hover = variables.titlebar_float_hover

        bgcolor = getdata('titlebar.bgcolor')
        if not self.Env.username == 'guest':
            value = control.read_record('titlebar.bgcolor', '/etc/users/' + self.username)
            if not value == None: bgcolor = value
        if bgcolor == None: bgcolor = variables.titlebar_bgcolor

        fgcolor = getdata('titlebar.fgcolor')
        if not self.Env.username == 'guest':
            value = control.read_record('titlebar.fgcolor', '/etc/users/' + self.username)
            if not value == None: fgcolor = value
        if fgcolor == None: fgcolor = variables.titlebar_fgcolor

        self.setStyleSheet('''
/* see: https://stackoverflow.com/questions/32145080/qdockwidget-float-close-button-hover-images */
QDockWidget { 
    background: rgb(36,38,41);
    titlebar-close-icon: url({close});
    titlebar-normal-icon: url({float});
    color: {fgcolor}; 
}

QDockWidget::title {
    background-color: {bgcolor}; 
    color: {fgcolor}; 
    text-align: center;
    border: none;
}

QDockWidget::close-button, QDockWidget::float-button {
    border: none;
    background: transparent;
    icon-size: 30px;
    padding: 1px;
    color: {fgcolor}; 
}

QDockWidget::float-button {
    image: url({float});
    color: {fgcolor}; 
}

QDockWidget::close-button {
    image: url({close});
    color: {fgcolor}; 
}

QDockWidget::float-button:hover {
    image: url({float:hover});
    color: {fgcolor}; 
}

QDockWidget::close-button:hover {
    image: url({close:hover});
    color: {fgcolor}; 
}
        '''
.replace('{bgcolor}', bgcolor)
.replace('{fgcolor}', fgcolor)
.replace('{close}',res.get(close))
.replace('{float}',res.get(float))
.replace('{close:hover}', res.get(close_hover))
.replace('{float:hover}', res.get(float_hover))
)

## Shell ##
class Shell (QWidget):
    def __init__(self,ports):
        super(Shell, self).__init__()

        self.boxl = QVBoxLayout() # layout
        self.setLayout(self.boxl)

        # ports #
        self.Backend = ports[0]
        self.Env = ports[1]

        # shells #
        shells = files.list('/usr/share/shells')

        for i in shells:
            exec = control.read_record ('exec','/usr/share/shells/'+i)
            self.shell = importlib.import_module(exec)
            self.shell = self.shell.MainApp ([self.Backend,self.Env,self])
            self.boxl.addWidget(self.shell)

## Desktop ##
class Desktop (QMainWindow):
    locale = control.read_record("locale", "/etc/gui")

    def RunApp (self,appname):
        self.addDockWidget(Qt.TopDockWidgetArea, Application([self.Backend, self, appname]))

    def RunApplication (self):
        sender = self.sender().objectName()
        self.RunApp (sender.replace('.desk',''))

    def escape_act (self):
        app.endall()
        app.switch('desktop')
        commands.shutdown([])
        sys.exit(0)

    def reboot_act (self):
        app.endall()
        self.Backend.hide()
        commands.reboot([])
        sys.exit(0)

    def wakeup_act (self):
        self.submenu.show()
        self.BtnWakeUp.hide()

    def sleep_act (self):
        self.submenu.hide()
        self.BtnWakeUp = QPushButton()
        self.BtnWakeUp.setStyleSheet('background: black;color: black;border: black;')
        self.BtnWakeUp.setText('')

        ## Get informations ##
        cs = files.readall('/proc/info/cs')
        ver = files.readall('/proc/info/ver')
        cd = files.readall('/proc/info/cd')

        self.BtnWakeUp.setWindowTitle(cs + ' ' + ver + ' (' + cd + ")")

        ## Get app logo ##
        applogo = getdata('logo')
        if not applogo == None:
            self.BtnWakeUp.setWindowIcon(QIcon(res.get(applogo)))

        ## Set size ##
        width = getdata('width')
        height = getdata('height')
        autosize = getdata('autosize')

        if not width == None and not autosize == 'Yes':
            variables.width = int(width)

        if not height == None and not autosize == 'Yes':
            variables.height = int(height)

        self.BtnWakeUp.resize(variables.width, variables.height)

            ## Set sides ##
            ## Set sides ##
        sides = getdata('sides')

        if sides == 'Yes':
            variables.sides = True
        else:
            variables.sides = False
        if variables.sides == False:
             self.BtnWakeUp.setWindowFlag(Qt.FramelessWindowHint)

        fullscreen = getdata('fullscreen')

        if fullscreen == 'Yes':
            variables.fullscreen = True
        else:
            variables.fullscreen = False

        if variables.fullscreen == True:
            self.BtnWakeUp.showFullScreen()
        else:
            self.BtnWakeUp.show()

        self.BtnWakeUp.setCursor(Qt.BlankCursor)
        self.BtnWakeUp.clicked.connect (self.wakeup_act)

    def signout_act (self):
        app.endall()
        commands.shutdown([])
        subprocess.call(['./'+files.readall('/proc/info/boot'),"gui-login"])
        sys.exit(0)

    def switchuser_act (self):
        files.create('/tmp/switched-user')
        subprocess.call(['./' + files.readall('/proc/info/boot'), "gui-login"]) # just run the login

    def unlock_act (self):
        if self.username == 'guest':
            self.submenu.show()
            self.taskbar.show()
            self.backgroundButton.show()
            self.BtnUnlock.hide()
            self.lock.hide()
        else:
            self.BtnUnlock.hide()
            self.lock.hide()
            self.w = Unlock([self.Backend,self],self.username)
            self.submenu.show()
            self.taskbar.show()
            self.backgroundButton.show()

    def showTime_lock (self):
        # getting current time
        current_time = QTime.currentTime()

        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')

        # showing it to the label
        self.lblClock.setText(res.num(label_time))

    def lock_act (self):
        self.lock = QMainWindow()

        self.submenu.hide()
        self.taskbar.hide()
        self.backgroundButton.hide()
        self.BtnUnlock = QPushButton()
        self.BtnUnlock.setText('')
        self.lock.setCentralWidget(self.BtnUnlock)

        bgcolor = getdata('lock.bgcolor')
        background = getdata('lock.background')
        fgcolor = getdata('lock.fgcolor')
        clock_shadow = getdata('lock.clock.shadow')
        clock_size = getdata('lock.clock.size')
        clock_location = getdata('lock.clock.location')
        clock_color = getdata('lock.clock.color')

        ## Check background or bgcolor in users ##
        if not self.username == 'guest':
            value = control.read_record('lock.bgcolor', '/etc/users/' + self.username)
            if not value == None: bgcolor = value

        if bgcolor==None: bgcolor = variables.lock_bgcolor

        if not self.username == 'guest':
            value = control.read_record('lock.background', '/etc/users/' + self.username)
            if not value == None: background = value

        if background == None:
            background = variables.lock_background

        if not self.username == 'guest':
            value = control.read_record('lock.fgcolor', '/etc/users/' + self.username)
            if not value == None: fgcolor = value

        if fgcolor == None:
            fgcolor = variables.lock_fgcolor

        if not self.username == 'guest':
            value = control.read_record('lock.clock.shadow', '/etc/users/' + self.username)
            if not value == None: clock_shadow = variables.lock_clock_shadow

        if clock_shadow == None:
            clock_shadow = variables.lock_clock_shadow

        if not self.username == 'guest':
            value = control.read_record('lock.clock.color', '/etc/users/' + self.username)
            if not value == None: clock_color =  variables.lock_clock_color

        if clock_color == None:
            clock_color = variables.lock_clock_color

        if not self.username == 'guest':
            value = control.read_record('lock.clock.size', '/etc/users/' + self.username)
            if not value == None: clock_size =  variables.lock_clock_size

        if clock_size == None:
            clock_size =   variables.lock_clock_size

        if not self.username == 'guest':
            value = control.read_record('lock.clock.location', '/etc/users/' + self.username)
            if not value == None: clock_location =   variables.lock_clock_location

        if clock_location==None: clock_location = variables.lock_clock_location

            ## Set bgcolor and background ##

        if background == None and bgcolor == None and not fgcolor == None:
            variables.lock_fgcolor = fgcolor
            ## Set colors ##
            self.BtnUnlock.setStyleSheet(
                'border:none;background-color: {0};color:{1};'.replace('{0}', variables.lock_bgcolor).replace('{0}', variables.lock_fgcolor))

        elif background == None and not fgcolor == None:

            ## Set colors ##
            variables.lock_bgcolor = bgcolor
            variables.lock_fgcolor = fgcolor

            self.BtnUnlock.setStyleSheet(
                'border:none;background-color: {0};color:{1};'.replace('{0}', variables.lock_bgcolor).replace('{0}', variables.lock_fgcolor))
        elif not background == None and not fgcolor == None:
            ## Set bgcolor ##

            variables.lock_background = res.get(background)
            self.BtnUnlock.setStyleSheet(
                'border:none;background-image: url({0});color: {1};'.replace('{0}', variables.lock_background).replace('{1}', variables.lock_fgcolor))
        else:
            self.BtnUnlock.setStyleSheet(
                'background-color:{1};color: {0};'.replace('{0}', variables.lock_fgcolor).replace('{1}',
                                                                                                     variables.lock_bgcolor))

        ## Get informations ##
        cs = files.readall('/proc/info/cs')
        ver = files.readall('/proc/info/ver')
        cd = files.readall('/proc/info/cd')

        self.lock.setWindowTitle(cs + ' ' + ver + ' (' + cd + ")")

        ## Clock ##
        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.showTime_lock)

        # update the timer every second
        timer.start(1000)

        ## Get app logo ##
        applogo = getdata('logo')
        if not applogo == None:
            self.lock.setWindowIcon(QIcon(res.get(applogo)))

        ## Set size ##
        width = getdata('width')
        height = getdata('height')
        autosize = getdata('autosize')

        if not width == None and not autosize == 'Yes':
            variables.width = int(width)

        if not height == None and not autosize == 'Yes':
            variables.height = int(height)

        self.lock.resize(variables.width, variables.height)
        self.BtnUnlock.resize(variables.width, variables.height)

        ## Set sides ##
        ## Set sides ##
        sides = getdata('sides')

        if sides == 'Yes':
            variables.sides = True
        else:
            variables.sides = False
        if variables.sides == False:
            self.lock.setWindowFlag(Qt.FramelessWindowHint)

        fullscreen = getdata('fullscreen')

        if fullscreen == 'Yes':
            variables.fullscreen = True
        else:
            variables.fullscreen = False

        if variables.fullscreen == True:
            self.lock.showFullScreen()
        else:
            self.lock.show()

        # lbl Clock #
        self.lblClock = QLabel()
        self.lock.layout().addWidget(self.lblClock)

        # shadow #
        if clock_shadow=='Yes':
            ## Shadow ##
            # Copy right shadow box: medium.com/@rekols/qt-button-box-shadow-property-c47c7bf58721 ##
            shadow = QGraphicsDropShadowEffect()
            shadow.setColor(QColor(10, 2, 34, 255 * 0.8))
            shadow.setOffset(0)
            shadow.setBlurRadius(10)
            self.lblClock.setGraphicsEffect(shadow)

        # font size clock #

        f = QFont()
        f.setPointSize(int(clock_size))

        self.lblClock.setFont(f)

        # color clock #
        self.lblClock.setStyleSheet('color:'+clock_color)

        # set lbl Clock location #
        if clock_location == 'top':
            self.lblClock.setGeometry(int(self.BtnUnlock.width() / 2) - int(self.lblClock.width() / 2), 0,
                                          self.lblClock.width(), self.lblClock.height())
        elif clock_location == 'center':
            self.lblClock.setGeometry(int(self.BtnUnlock.width() / 2) - int(self.lblClock.width() / 2),
                                          int(self.lock.height() / 2) - int(self.lblClock.height() / 2),
                                          self.lblClock.width(),
                                          self.lblClock.height())

        elif clock_location == 'left':
            self.lblClock.setGeometry(0,
                                          int(self.lock.height() / 2) - int(self.lblClock.height() / 2),
                                          self.lblClock.width(),
                                          self.lblClock.height())

        elif clock_location == 'right':
            self.lblClock.setGeometry(self.BtnUnlock.width()-self.lblClock.width(),
                                          int(self.lock.height() / 2) - int(self.lblClock.height() / 2),
                                          self.lblClock.width(),
                                          self.lblClock.height())
        elif clock_location == 'bottom':
            self.lblClock.setGeometry(int(self.BtnUnlock.width() / 2) - int(self.lblClock.width() / 2),
                                          self.lock.height() -self.lblClock.height(),
                                          self.lblClock.width(),
                                          self.lblClock.height())

        elif clock_location == 'top/left':
            self.lblClock.setGeometry(0,
                                          0,
                                          self.lblClock.width(),
                                          self.lblClock.height())

        elif clock_location == 'top/right':
            self.lblClock.setGeometry(self.BtnUnlock.width()-self.lblClock.width(),
                                          0,
                                          self.lblClock.width(),
                                          self.lblClock.height())

        elif clock_location == 'bottom/left':
            self.lblClock.setGeometry(0,
                                      self.BtnUnlock.height()-self.lblClock.height(),
                                      self.lblClock.width(),
                                      self.lblClock.height())

        elif clock_location == 'bottom/right':
            self.lblClock.setGeometry(self.BtnUnlock.width() - self.lblClock.width(),
                                      self.BtnUnlock.height()-self.lblClock.height(),
                                      self.lblClock.width(),
                                      self.lblClock.height())

        self.BtnUnlock.clicked.connect(self.unlock_act)

    def __init__(self,ports,username,password):
        super(Desktop, self).__init__()

        ## Set port name ##
        self.setObjectName('Desktop')

        ## ports ##
        self.Backend = ports[0]

        ## username ##
        self.username = username.lower()
        self.password = password

        ## Get informations ##
        cs = files.readall('/proc/info/cs')
        ver = files.readall('/proc/info/ver')
        cd = files.readall('/proc/info/cd')

        self.setWindowTitle(cs + ' ' + ver + ' (' + cd + ")")

        ## Get app logo ##
        applogo = getdata('logo')
        if not applogo == None:
            self.setWindowIcon(QIcon(res.get(applogo)))

        ## Menu ##

            # hide the menu #
        submenu_hide = getdata('submenu.hide')
        if not self.username == 'guest':
            value = control.read_record('submenu.hide', '/etc/users/' + self.username)
            if not value == None: submenu_hide = value
        if submenu_hide == None: submenu_hide = variables.submenu_hide

        submenu_bgcolor = getdata('submenu.bgcolor')
        if not self.username == 'guest':
            value = control.read_record('submenu.bgcolor', '/etc/users/' + self.username)
            if not value == None: submenu_bgcolor = value
        if submenu_bgcolor == None: submenu_bgcolor = variables.submenu_bgcolor

        submenu_fgcolor = getdata('submenu.fgcolor')
        if not self.username == 'guest':
            value = control.read_record('submenu.fgcolor', '/etc/users/' + self.username)
            if not value == None: submenu_fgcolor = value
        if submenu_fgcolor == None: submenu_fgcolor = variables.submenu_fgcolor

        submenu_direction = getdata('submenu.direction')
        if not self.username == 'guest':
            value = control.read_record('submenu.direction', '/etc/users/' + self.username)
            if not value == None: submenu_direction = value
        if submenu_direction == None: submenu_direction = variables.submenu_direction

        submenu_fontsize = getdata('submenu.fontsize')
        if not self.username == 'guest':
            value = control.read_record('submenu.fontsize', '/etc/users/' + self.username)
            if not value == None: submenu_fontsize = value
        if submenu_fontsize == None: submenu_fontsize = variables.submenu_fontsize
        ## menu section

        self.submenu =QMenuBar() # Sub menu
        self.Backend.setMenuBar(self.submenu)

        self.submenu.setStyleSheet('background-color:none;color:{1};'.replace('{0}',submenu_bgcolor).replace("{1}",submenu_fgcolor))

        if submenu_direction=='ltr': self.submenu.setLayoutDirection(Qt.LeftToRight)
        elif submenu_direction=='rtl': self.submenu.setLayoutDirection(Qt.RightToLeft)

        f = QFont()
        f.setPointSize(int(submenu_fontsize))

        self.submenu.setFont(f)

        ## Shell ##

        self.submenu.setCornerWidget(Shell([self.Backend,self]))

        ## Menu Applications #

        self.appmenu = QMenu (res.get('@string/appmenu'))
        self.submenu.addMenu(self.appmenu)

        apps = files.list('/usr/share/applications')

        # default language
        if self.locale==None: self.locale = variables.locale

        # menu action

        for i in apps:
            find = '/usr/share/applications/' + i
            # data
            # app name
            appname = control.read_record('name['+self.locale+"]", find)
            shortcut = control.read_record('shortcut',find)

            if appname == None:
                appname = i.replace('.desk','')

            # app logo
            applogo = control.read_record('logo', find)

            # design
            self.actApp = self.appmenu.addAction(i)
            self.actApp.setObjectName(i)
            self.actApp.setText(appname)

            if not applogo==None:
                self.actApp.setIcon(QIcon(res.get(applogo)))

            if not shortcut==None:
                self.actApp.setShortcut(shortcut)

            self.actApp.setFont(f) # set font actions

            self.actApp.triggered.connect(self.RunApplication)

        ## Etcetra menu ##
        self.etcmenu = QMenu()
        self.etcmenu.setFont(f)
        self.etcmenu.setTitle (res.get('@string/etcmenu'))
        self.submenu.addMenu(self.etcmenu)

        # Account menu #
        self.usermenu = QMenu()
        self.usermenu.setFont(f)
        self.etcmenu.addMenu(self.usermenu)

        # get username first + lastname
        fullname = ''

        if username=='guest':
            fullname = res.get('@string/guest')
        else:
            first_name = control.read_record('first_name','/etc/users/'+username)
            last_name = control.read_record('last_name','/etc/users/'+username)

            if first_name==None and last_name==None:
                fullname = username
            elif not first_name==None and last_name==None:
                fullname = first_name
            elif not first_name==None and not last_name==None:
                fullname = first_name +" "+last_name
            else:
                fullname = last_name

        self.usermenu.setTitle(fullname)

        # Power menu #
        self.powermenu = QMenu()
        self.powermenu.setFont(f)
        self.etcmenu.addMenu(self.powermenu)
        self.powermenu.setTitle(res.get('@string/powermenu'))

        # all actions in menus #

        self.accoutsettings = QAction(res.get('@string/accountsettings'))
        self.usermenu.addAction(self.accoutsettings)

        self.signout = QAction(res.get('@string/signout'))
        self.signout.triggered.connect (self.signout_act)
        self.usermenu.addAction(self.signout)

        self.switchuser = QAction(res.get('@string/switchuser'))
        self.switchuser.triggered.connect (self.switchuser_act)
        self.usermenu.addAction(self.switchuser)

        self.locks = QAction(res.get('@string/lock'))
        self.locks.triggered.connect (self.lock_act)
        self.usermenu.addAction(self.locks)

        self.escape = QAction(res.get('@string/escape'))
        self.escape.triggered.connect (self.escape_act)
        self.powermenu.addAction(self.escape)

        self.restart = QAction(res.get('@string/restart'))
        self.restart.triggered.connect (self.reboot_act)
        self.powermenu.addAction(self.restart)

        self.sleep = QAction(res.get('@string/sleep'))
        self.sleep.triggered.connect (self.sleep_act)
        self.powermenu.addAction(self.sleep)

        ## Widget for bgcolor or background ##
        self.backgroundButton = QPushButton()
        self.backgroundButton.setGeometry(0, 0, variables.width, variables.height)
        self.layout().addWidget(self.backgroundButton)

        bgcolor = getdata('desktop.bgcolor')
        background = getdata('desktop.background')
        fgcolor = getdata('desktop.fgcolor')


        ## Check background or bgcolor in users ##
        if not self.username=='guest':
            value = control.read_record('desktop.bgcolor','/etc/users/'+self.username)
            if not value==None: bgcolor = value

        if not self.username=='guest':
            value = control.read_record('desktop.background','/etc/users/'+self.username)
            if not value==None: background = value

        if not self.username=='guest':
            value = control.read_record('desktop.fgcolor','/etc/users/'+self.username)
            if not value==None: fgcolor = value

            ## Set bgcolor and background ##

        if background == None and bgcolor == None and not fgcolor == None:
            variables.desktop_fgcolor = fgcolor
            ## Set colors ##
            self.setStyleSheet('color: {0};'.replace('{0}', variables.desktop_fgcolor))
            self.backgroundButton.setStyleSheet(
                'border:none;background-color: {0};'.replace('{0}', variables.desktop_bgcolor))

        elif background == None and not fgcolor == None:

            ## Set colors ##
            variables.desktop_bgcolor = bgcolor
            variables.desktop_fgcolor = fgcolor

            self.setStyleSheet('color: {0};'.replace('{0}', variables.desktop_fgcolor))

            self.backgroundButton.setStyleSheet(
                'border:none;background-color: {0};'.replace('{0}', variables.desktop_bgcolor))
        elif not background == None and not fgcolor == None:
            ## Set bgcolor ##

            variables.desktop_background = res.get(background)
            self.setStyleSheet('color: {0};'.replace('{0}', variables.desktop_fgcolor))
            self.backgroundButton.setStyleSheet(
                'border:none;background-image: url({0});'.replace('{0}', variables.desktop_background))
        else:
            self.setStyleSheet(
                'background-color:{1};color: {0};'.replace('{0}', variables.desktop_fgcolor).replace('{1}',
                                                                                                     variables.desktop_bgcolor))

        ## Set size ##
        width = getdata('width')
        height = getdata('height')
        autosize =getdata('autosize')

        if not width == None  and not autosize=='Yes':
            variables.width = int(width)

        if not height == None and not autosize=='Yes':
            variables.height = int(height)

        self.resize(variables.width, variables.height)

        ## Set sides ##
        ## Set sides ##
        sides = getdata('sides')

        if sides == 'Yes':
            variables.sides = True
        else:
            variables.sides = False
        if variables.sides == False:
            self.setWindowFlag(Qt.FramelessWindowHint)

        ## Taskbar ##
        self.taskbar = TaskBar ([Backend,self])

        ## Show ##
        ## Get data ##
        fullscreen = getdata('fullscreen')

        if fullscreen == 'Yes':
            variables.fullscreen = True
        else:
            variables.fullscreen = False

        if variables.fullscreen == True:
            self.showFullScreen()
        else:
            self.show()

    ## Run baran as Backend ##
if sys.argv[1:]==[]:
    mainApp = Backend()
else:
    sys.exit(0)

sys.exit(application.exec_())
