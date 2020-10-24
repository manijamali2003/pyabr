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
import os, shutil
from buildlibs import  control

name =      control.read_record('name','packs/pyabr/data/etc/distro')
version =   control.read_record('version','packs/pyabr/data/etc/distro')
build =     control.read_record('build','packs/pyabr/data/etc/distro')

def clean():
    if os.path.isdir ('app'):                                           shutil.rmtree('app')
    if os.path.isdir ('build-packs'):                                   shutil.rmtree('build-packs')
    if os.path.isdir ('stor'):                                          shutil.rmtree('stor')
    if os.path.isdir ('pack-release'):                                  shutil.rmtree('pack-release')
    if os.path.isdir('wheel/src'):                                      shutil.rmtree('wheel/src')
    if os.path.isdir('wheel/setup'):                                    shutil.rmtree('wheel/setup')
    if os.path.isfile('pyabr.zip'):                                     os.remove    ('pyabr.zip')
    if os.path.isfile('pyabr-for-pydroid.zip'):                         os.remove    ('pyabr-for-pydroid.zip')
    if os.path.isfile('pyabr-for-termux.zip'):                          os.remove    ('pyabr-for-termux.zip')
    if os.path.isfile('Pyabr-'+version+'-'+build+'.zip'):               os.remove    ('Pyabr-'+version+'-'+build+'.zip')
clean()
