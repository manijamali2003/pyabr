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

from buildlibs import pack_archives as pack
from buildlibs import control
import shutil, os, sys, hashlib,getpass

import shutil, os

if not os.path.isfile (".termux"):
    open ('.termux','w')
    ## pre build ##

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

    # build #

    pack.build("pyabr")
    pack.unpack('pyabr')

    pack.build("paye")
    pack.unpack('paye')

    if os.path.isfile('stor/proc/0'):  os.remove('stor/proc/0')
    if os.path.isfile('stor/proc/id/desktop'): os.remove('stor/proc/id/desktop')

    # hostname
    hostname = input('Enter a new hostname: ')

    # root password
    while True:
        root_password = getpass.getpass('Enter a new root password: ')
        confirm = getpass.getpass('Confirm the new root password: ')

        if root_password == confirm: break

    # username
    username = input('Enter a new username: ')

    # password
    while True:
        password = getpass.getpass('Enter a new ' + username + '\'s password: ')
        confirm = getpass.getpass('Confirm the new password: ')

        if password == confirm: break

    # enable guest

    guest = input('Do you want to enable guest user? [Y/n]: ')

    if guest.lower() == 'n':
        guest = 'No'
    else:
        guest = 'Yes'

    # save

    save = input('Do you want to save changes? [Y/n]: ')

    if not save.lower() == 'y':
        sys.exit(0)

    # hostname and users

    file = open('stor/etc/hostname', 'w');
    file.write(hostname);
    file.close()
    file = open('stor/etc/users/' + username, 'w');
    file.write('username: {0}\ncode: {1}'.replace('{0}', hashlib.sha3_256(username.encode()).hexdigest()).replace('{1}',
                                                                                                                  hashlib.sha3_512(
                                                                                                                      password.encode()).hexdigest()));
    file.close()
    file = open('stor/etc/users/root', 'w');
    file.write('username: {0}\ncode: {1}'.replace('{0}', hashlib.sha3_256('root'.encode()).hexdigest()).replace('{1}',
                                                                                                                hashlib.sha3_512(
                                                                                                                    root_password.encode()).hexdigest()));
    file.close()

    # permissions
    file = open('stor/etc/permtab', 'w')
    file.write('''
    #!etcetra

    /: dr--r-----/root
    /desk/guest: drw----rw-/guest
    /root: drwx------/root
    /tmp: drw-rw----/root
    /usr/app: dr-xr-x--x/root
    /usr/games: dr-xr-x--x/root
    /desk/{username}: drwxr-x---/{username}
    '''.replace('{username}', username))
    file.close()

    # sudo
    file = open('stor/etc/sudoers', 'w')
    file.write(username)
    file.close()

    # guest
    file = open('stor/etc/guest', 'w')
    if guest == 'y':
        guest = 'Yes'
    else:
        guest = 'No'
    file.write('enable_cli: ' + guest + "\nenable_gui: " + guest)
    file.close()

    shutil.copyfile('termux.py','../pyabr.py')

if os.path.isfile ('stor/vmabr.py'):
    os.system('cd stor && python vmabr.py kernel')
elif os.path.isdir ('stor/vmabr.pyc'):
    os.system('cd stor && python vmabr.py kernel')