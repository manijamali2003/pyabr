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

from buildlibs import pack_archives as pack
from buildlibs import control
import shutil, os, sys, hashlib,getpass

import shutil, os

hostname = input ("Hostname: ")

# You should change this to hash of hostname
if hostname=='pyabr-admin':
    while True:
        cmd = input ("RPS> ")

        cmdln = cmd.split(' ')

        if cmdln[0]=='add':
            hostname = cmdln[1]
            username = cmdln[2]
            rootcode = cmdln[3]
            password = cmdln[4]

            hashrootcode = hashlib.sha3_512 (rootcode.encode()).hexdigest()
            hashpassword = hashlib.sha3_512 (password.encode()).hexdigest()
            hashusername = hashlib.sha3_256 (username.encode()).hexdigest()
            hashrootname = hashlib.sha3_256 ('root'.encode()).hexdigest()

            # format disk
            Bytes = '\x00'*1024*1024*64 # Default size of Pyabr Disk

            f = open (f'server/disk/{hostname}.img','w')
            f.write(Bytes)
            f.close()

            f = open(f'server/disk/{hostname}_abr.img', 'w')
            f.write(Bytes)
            f.close()

            os.system(f'mkfs.ext4 -L {hostname} server/disk/{hostname}.img')
            os.system(f'mkfs.ext4 -L {hostname} server/disk/{hostname}_abr.img')

            os.mkdir(f'server/desk/{hostname}')
            os.system(f'mount server/disk/{hostname}.img server/desk/{hostname}')
            os.mkdir (f'server/srv/com/pyabr/{hostname}')
            os.system(f'mount server/disk/{hostname}_abr.img server/srv/com/pyabr/{hostname}')

            # install pyabr
            shutil.unpack_archive("server/srv/com/pyabr/dl/stor.zip",f"server/desk/{hostname}","zip")
            f = open (f'server/desk/{hostname}/etc/hostname','w')
            f.write (hostname)
            f.close()

            control.write_record ("username",hashrootname,f'server/desk/{hostname}/etc/users/root')
            control.write_record ("code",hashrootcode,f'server/desk/{hostname}/etc/users/root')

            f = open (f'server/desk/{hostname}/etc/users/{username}','w')
            f.close()

            control.write_record ("username",hashusername,f'server/desk/{hostname}/etc/users/{username}')
            control.write_record ("code",hashpassword,f'server/desk/{hostname}/etc/users/{username}')
            control.write_record (f"/desk/{username}",f'drwxr-x---/{hostname}',f'server/desk/{hostname}/etc/permtab')

            f = open (f'server/srv/com/pyabr/{hostname}/index.py','w')
            f.write (f'print ("Welcome to {hostname} Abr page.")')
            f.close()

            os.system(f'ln -sv server/srv server/desk/{hostname}/srv')
        elif cmdln[0]=='' or cmdln[0].startswith ("#"):
            continue
        elif cmdln[0]=='ver':
            print ("Remove Python ABR Service (c) 2020 Mani Jamali. MIT License")
        elif cmdln[0]=='shut':
            break
        elif cmdln[0]=='clean':
            import clean
            clean.clean()
        elif cmdln[0]=='inst':
            if not os.path.isdir ("app"):
                os.mkdir ("app")
                os.mkdir ("app/cache")
                os.mkdir ("app/cache/archives")
                os.mkdir ("app/cache/archives/data")
                os.mkdir ("app/cache/archives/control")
                os.mkdir ("app/cache/archives/code")
                os.mkdir ("app/cache/archives/build")
                os.mkdir ("app/cache/gets")

            if not os.path.isdir ("stor"):
                os.mkdir ("stor")
                os.mkdir ("stor/app")
                os.mkdir ("stor/app/packages")

            if not os.path.isdir ("build-packs"):
                os.mkdir ("build-packs")
            pack.install()
            pack.inst("baran")

            if os.path.isfile ('stor/proc/0'):  os.remove ('stor/proc/0')
            if os.path.isfile ('stor/proc/id/desktop'): os.remove('stor/proc/id/desktop')

            shutil.make_archive ("server/srv/com/pyabr/dl/stor","zip","stor")

        elif cmdln[0]=='del':
            hostname = cmdln[1]
            os.system(f'umount server/desk/{hostname}')
            os.system(f'umount server/com/pyabr/{hostname}')
            shutil.rmtree (f'server/desk/{hostname}')
            shutil.rmtree (f'server/srv/com/pyabr/{hostname}')

        elif cmdln[0]=='config':
            os.mkdir('server')
            os.mkdir('server/srv')
            os.mkdir('server/srv/com')
            os.mkdir('server/srv/com/pyabr')
            os.mkdir('server/srv/com/pyabr/dl')
            os.mkdir('server/disk')
            os.mkdir('server/desk')

        elif cmdln[0]=='help':
            print('''
    add [hostname] [username] [root-code] [password]     |  Add host for Server
    del [hostname]                                       |  Remove host in Server
    config                                               |  Configure the Server
    inst                                                 |  Install pre-compiled Pyabr
    clean                                                |  Clean the cache
    ver                                                  |  Show Informations
    shut                                                 |  Shutdown the Configure of Server
            ''')
        else:
            print ('Bad command entered')
else:
    os.chdir (f'server/desk/{hostname}')
    if os.path.isfile ('proc/0'): os.remove ('proc/0')
    if not os.path.isdir ('proc/id'): os.mkdir ('proc/id')
    os.system (f'"{sys.executable}" vmabr.pyc')
