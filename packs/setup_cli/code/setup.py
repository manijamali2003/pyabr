#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Pasand team. GNU General Public License v3.0
#
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

import getpass, hashlib,sys, os, shutil, subprocess, platform

# hostname
hostname = input('Enter a new hostname: ')

# root password
while True:
    root_password = getpass.getpass ('Enter a new root password: ')
    confirm = getpass.getpass('Confirm the new root password: ')

    if root_password==confirm: break

# username
username = input('Enter a new username: ')

# password
while True:
    password = getpass.getpass('Enter a new '+username+'\'s password: ')
    confirm = getpass.getpass('Confirm the new password: ')

    if password == confirm: break

# enable guest

guest = input('Do you want to enable guest user? [Y/n]: ')

if guest.lower()=='n': guest='No'
else: guest='Yes'

# save

save = input ('Do you want to save changes? [Y/n]: ')

if not save.lower()=='y':
    sys.exit(0)

# hostname and users

file = open('etc/hostname','w');file.write(hostname);file.close()
file = open('etc/users/'+username,'w');file.write('username: {0}\ncode: {1}'.replace('{0}',hashlib.sha3_256(username.encode()).hexdigest()).replace('{1}',hashlib.sha3_512(password.encode()).hexdigest()));file.close()
file = open('etc/users/root','w');file.write('username: {0}\ncode: {1}'.replace('{0}',hashlib.sha3_256('root'.encode()).hexdigest()).replace('{1}',hashlib.sha3_512(root_password.encode()).hexdigest()));file.close()

# permissions
file = open('etc/permtab','w')
file.write('''
#!etcetra

/: dr--r-----/root
/desk/guest: drw----rw-/guest
/root: drwx------/root
/tmp: drw-rw----/root
/usr/app: dr-xr-x--x/root
/usr/games: dr-xr-x--x/root
/desk/{username}: drwxr-x---/{username}
'''.replace('{username}',username))
file.close()

# sudo
file = open('etc/sudoers','w')
file.write(username)
file.close()

# guest
file = open ('etc/guest','w')
if guest=='y': guest='Yes'
else: guest='No'
file.write('enable_cli: '+guest+"\nenable_gui: "+guest)
file.close()

# remove the setup
if os.path.isfile ('app/packages/setup.compile'): os.remove('app/packages/setup.compile')
if os.path.isfile ('app/packages/setup.list'): os.remove('app/packages/setup.list')
if os.path.isfile ('app/packages/setup.manifest'): os.remove('app/packages/setup.manifest')

# theme

if platform.node()=='localhost' and platform.system()=="Linux":
    file = open ('etc/gui','w')
    file.write('''
desktop: baran
fullscreen: Yes
sides: No
width: 720
height: 1280
autosize: Yes
logo: @icon/pyabr-logo
locale: en
lock.clock.shadow: No
lock.clock.size: 30
lock.clock.color: white
lock.clock.location: center
submenu.hide: No
submenu.fgcolor: black
submenu.bgcolor: white
submenu.direction: ltr
submenu.fontsize: 12
titlebar.close: @icon/close
titlebar.close-hover: @icon/close-hover
titlebar.float: @icon/float
titlebar.float-hover: @icon/float-hover
titlebar.bgcolor: #123456
titlebar.fgcolor: white
taskbar.pins: calculator,calendar,pyshell,pysys,runapp
taskbar.location: left
taskbar.size: 140
taskbar.locked: Yes
taskbar.float: No
backend.color: #000000
backend.timeout: 100
splash.color: #ABCDEF
splash.timeout: 3000
fullscreen: Yes
autosize: Yes
login.fgcolor: #000000
login.background: @background/default-phone
enter.fgcolor: #000000
enter.background: @background/default-phone
unlock.fgcolor: #000000
unlock.background: @background/default-phone
desktop.fgcolor: #000000
desktop.background: @background/default-phone
lock.bgcolor: #FFFFFF
lock.fgcolor: #000000
lock.background: @background/default-phone
taskbar.bgcolor: #FFFFFF
loginw.bgcolor: #FFFFFF
userlogo.color: #FFFFFF
input.bgcolor: #FFFFFF
input.fgcolor: #000000
loginw.fgcolor: #000000
loginw.round.size: 20
loginw.userlogo.round-size: 350
loginw.input.round-size: 20
loginw.location: center
loginw.input.fontsize: 16
loginw.login.bgcolor: #ABCDEF
loginw.login.fgcolor: #FFFFFF
loginw.login.hover-bgcolor: #123456
loginw.login.hover-fgcolor: #FFFFFF
loginw.login.fontsize: 12
loginw.login.round: Yes
loginw.login.round-size: 20
loginw.login.hide: No
loginw.login.width: 350
loginw.enter.bgcolor: pink
loginw.enter.fgcolor: #FFFFFF
loginw.enter.hover-bgcolor: purple
loginw.enter.hover-fgcolor: #FFFFFF
loginw.enter.fontsize: 12
loginw.enter.round: Yes
loginw.enter.round-size: 20
loginw.enter.hide: No
loginw.enter.width: 350
loginw.unlock.bgcolor: lime
loginw.unlock.fgcolor: green
loginw.unlock.hover-bgcolor: green
loginw.unlock.hover-fgcolor: lime
loginw.unlock.fontsize: 12
loginw.unlock.round: Yes
loginw.unlock.round-size: 20
loginw.unlock.hide: No
loginw.unlock.width: 350
loginw.shadow: Yes
loginw.userlogo.shadow: Yes
loginw.input.shadow: No
loginw.login.shadow: No
loginw.enter.shadow: No
loginw.unlock.shadow: No
loginw.input.width: 350
loginw.input.height: 60
loginw.login.height: 60
loginw.enter.height: 60
loginw.unlock.height: 60
splash.logo: @icon/pyabr-logo
splash.logo-size: 300
    ''')
    file.close()
# finish

finish = input('Installaction of Pyabr was done; do you want to reboot? [Y/n]: ')

if finish.lower()=='y':
    os.remove('setup.pyc')
    subprocess.call([sys.executable,'vmabr.pyc'])
    sys.exit(0)
else:
    os.remove('setup.pyc')
    sys.exit(0)