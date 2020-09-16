#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Pasand team. GNU General Public License v3.0
#
#  Offical website:         http://itpasand.com
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/pasandteam/pyabr
#
#######################################################################################

import os, shutil
from buildlibs import control

name = control.read_record('name','packs/pyabr/data/etc/distro')
build = control.read_record('build','packs/pyabr/data/etc/distro')
version = control.read_record('version','packs/pyabr/data/etc/distro')

if os.path.isdir ('pack-release'):
    shutil.rmtree('pack-release')
    os.mkdir('pack-release')

shutil.copytree('buildlibs','pack-release/buildlibs')
shutil.copytree('packs','pack-release/packs')
shutil.copyfile('debug.py','pack-release/debug.py')
shutil.copyfile('install.py','pack-release/install.py')
shutil.copyfile('LICENSE','pack-release/LICENSE')
shutil.copyfile('AUTHERS','pack-release/AUTHERS')
shutil.copyfile('pack.py','pack-release/pack.py')
shutil.copyfile('README.md','pack-release/README.md')
shutil.copyfile('requirments.txt','pack-release/requirments.txt')

shutil.make_archive(name+'-'+version+'-'+build,'zip','pack-release')
shutil.rmtree('pack-release')
