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
import  os, shutil, platform , hashlib, getpass
from buildlibs import  control, pack_archives as pack

if os.path.isdir("stor"): shutil.rmtree("stor")

if not os.path.isdir("app"):
    os.mkdir("app")
    os.mkdir("app/cache")
    os.mkdir("app/cache/archives")
    os.mkdir("app/cache/archives/data")
    os.mkdir("app/cache/archives/control")
    os.mkdir("app/cache/archives/code")
    os.mkdir("app/cache/archives/build")
    os.mkdir("app/cache/gets")

if not os.path.isdir("stor"):
    os.mkdir("stor")
    os.mkdir("stor/app")
    os.mkdir("stor/app/packages")

if not os.path.isdir("build-packs"): os.mkdir("build-packs")

pack.install()
pack.inst('baran')

os.remove('stor/vmabr.pyc')
shutil.copyfile('packs/pyabr/code/vmabr.py', 'stor/vmabr.py')

# clean #
if os.path.isdir('app'): shutil.rmtree('app')
if os.path.isdir('build-packs'): shutil.rmtree('build-packs')

## Setting up hostname ##
file = open("stor/etc/hostname", "w")
file.write(input('Enter a new hostname: '))
file.close()

## Setting up Root user ##
file = open("stor/etc/users/root", "w")
file.write("username: " + hashlib.sha3_256("root".encode()).hexdigest() + "\n")
file.write("code: " + hashlib.sha3_512(getpass.getpass('Choose a new root password: ').encode()).hexdigest() + "\n")
file.close()

## Setting up Standard user ##
u = input('Pick a username: ')
file = open("stor/etc/users/" + u, "w")
file.write("username: " + hashlib.sha3_256(u.encode()).hexdigest() + "\n")
file.write("code: " + hashlib.sha3_512(getpass.getpass('Choose a new user password:').encode()).hexdigest() + "\n")
file.close()

file = open("stor/etc/permtab", "a")
file.write("/desk/" + u + ": drwxr-x---/" + u + "\n")
file.close()

## Setting up Guest user ##
file = open("stor/etc/guest", "w")
guest = input('Unlock guest (Yes/No): ')
if guest == "No":
    file.write("enable_cli: No\nenable_gui: No\n")
elif guest == "Yes":
    file.write("enable_cli: Yes\nenable_gui: Yes\n")
else:
    file.write("enable_cli: No\nenable_gui: No\n")
file.close()

## Setting up interface ##
interface = input('Choose your interface (CLI/GUI): ')
file = open("stor/etc/interface", "w")
if interface.startswith("C"):
    file.write("CLI")
elif interface.startswith("G"):
    file.write("GUI")
file.close()

## Setting GUI Table ##
locale = input('Choose your language (fa/en/ar): ')
file = open("stor/etc/gui", "w")
file.write("locale: " + locale + "\n")
file.write('''
#!etcetra

desktop: baran
fullscreen: Yes
sides: No
width: 1280
height: 720
autosize: Yes
logo: @icon/pyabr-logo
locale: en

backend.color: black
backend.timeout: 1000

splash.timeout: 3000
splash.logo: @icon/pyabr-logo
splash.logo-size: 300
splash.color: #ABCDEF

login.bgcolor: #123456
login.background: @background/default
login.fgcolor: #FFFFFF

enter.bgcolor: #123456
enter.background: @background/default
enter.fgcolor: #FFFFFF

unlock.bgcolor: #123456
unlock.background: @background/default
unlock.fgcolor: #FFFFFF

loginw.bgcolor: white
loginw.fgcolor: black
loginw.round: Yes
loginw.round-size: 20 20
loginw.location: center
loginw.shadow: Yes
loginw.userlogo: @icon/account
loginw.userlogo.shadow: Yes
loginw.userlogo.color: white
loginw.userlogo.round: Yes
loginw.userlogo.round-size: 125 125
loginw.input.shadow: Yes
loginw.input.fgcolor: gray
loginw.input.bgcolor: white
loginw.input.round: Yes
loginw.input.round-size: 20 20
loginw.input.font-size: 12

taskbar.bgcolor: white
taskbar.fgcolor: black
taskbar.locked: No
taskbar.float: Yes

desktop.bgcolor: white
desktop.fgcolor: black
desktop.background: @background/default
lock.fgcolor: black
lock.bgcolor: black
lock.background: @background/default

loginw.login.round: Yes
loginw.login.round-size: 20
loginw.enter.round: Yes
loginw.enter.round-size: 20
loginw.unlock.round: Yes
loginw.unlock.round-size: 20

appw.bgcolor: #FFFFFF
appw.menubar.bgcolor: #FFFFFF
appw.menubar.shadow: Yes
            ''')
file.close()