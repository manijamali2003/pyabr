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
if os.path.isfile ('app/packages/setup_cli.compile'): os.remove('app/packages/setup_cli.compile')
if os.path.isfile ('app/packages/setup_cli.list'): os.remove('app/packages/setup_cli.list')
if os.path.isfile ('app/packages/setup_cli.manifest'): os.remove('app/packages/setup_cli.manifest')
# finish

finish = input('Installaction of Pyabr was done; do you want to reboot? [Y/n]: ')

if finish.lower()=='y':
    shutil.rmtree('install')
    os.remove('app/packages/setup_cli.compile')
    os.remove('app/packages/setup_cli.list')
    os.remove('app/packages/setup_cli.manifest')
    os.remove('setup.pyc')
    subprocess.call([sys.executable,'vmabr.pyc'])
    sys.exit(0)
else:
    shutil.rmtree('install')
    os.remove('app/packages/setup_cli.compile')
    os.remove('app/packages/setup_cli.list')
    os.remove('app/packages/setup_cli.manifest')
    os.remove('setup.pyc')
    sys.exit(0)