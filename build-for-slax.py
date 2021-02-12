#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Mani Jamali. GNU General Public License v3.0
#
#  Official Website: 		http://pyabr.rf.gd
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Gap channel: 			@pyabr
#  Gap group:   			@pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

import os,shutil,subprocess,sys

# This script install pyabr for slax as a slax module

# Generate Slax /usr/bin/pyabr

# config Pyabr env
print('Create env ...')
if not os.path.isdir ('/stor'): os.mkdir ('/stor')
if not os.path.isdir ('/stor/proc'): os.mkdir ('/stor/proc')
if not os.path.isdir ('/stor/proc/id'): os.mkdir ('/stor/proc/id')

# pyabr changes
print('Write Pyabr changes ...')

f = open('/etc/hostname','w')
f.write('pyabr')
f.close()

f = open('/etc/os-release','w')
f.write('''NAME="Pyabr"
VERSION="1 (Arvand)"
ID=pyabr
ID_LIKE=debian
PRETTY_NAME="Pyabr 1"
VERSION_ID="1"
VERSION_CODENAME=arvand''')
f.close()

f = open('/etc/issue','w')
f.write('Pyabr 1 \\n \\l')
f.close()

f = open('/etc/issue.net','w')
f.write('Pyabr 1')
f.close()

# set a startup
print('Setting as startup application ...')
f = open ('/root/.xinitrc','w')
f.write ('pyabr')
f.close()

# create desktop application file
print('Generate desktop file ...')
f = open('/usr/share/applications/pyabr.desktop','w')
f.write('''
[Desktop Entry]
Name=Pyabr
Comment=Pyabr Cloud Computing Startup Software
Exec=pyabr
Icon=/stor/usr/share/icons/pyabr-logo.svg
Terminal=false
Type=Application
StartupNotify=true
''')
f.close()

print('Generate startup script ...')
f = open('/usr/bin/pyabr')
f.write('''
#!/usr/bin/python3
#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Mani Jamali. GNU General Public License v3.0
#
#  Official Website: 		http://pyabr.rf.gd
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Gap channel: 			@pyabr
#  Gap group:   			@pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

import os,shutil,sys,subprocess as sub

os.chdir ('/stor')

if os.path.isfile ('pyabr-master.zip'):
    shutil.unpack_archive ('pyabr-master.zip','pyabr-master')
    os.chdir ('pyabr-master')
    sub.call ([sys.executable,'osinstaller.py'])
    
else:
    if not os.path.isdir ('proc/id'): os.mkdir ('proc/id')
    if not os.path.isdir ('proc/info'): os.mkdir ('proc/info')
    if os.path.isfile ('proc/0'): os.remove ('proc/0')
    
    sub.call ([sys.executable,'vmabr.pyc'])
''')
f.close()

subprocess.call(['chmod +x /usr/bin/pyabr'])

print('Install Requirements ...')

subprocess.call([sys.executable,'-m','pip','install','--upgrade','pip','setuptools'])
subprocess.call([sys.executable,'-m','pip','install','PyQt5','PyQtWebEngine','requests','pyqtconsole'])

print('Generate Squashfs disk ...')

subprocess.call(['savechanges','/run/initramfs/memory/data/slax/modules/pyabr.sb'])

print('Reboot the system ...')
subprocess.call(['systemctl','reboot'])