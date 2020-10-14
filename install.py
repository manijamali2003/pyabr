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
import shutil, os, sys, hashlib,getpass,platform

import shutil, os

os.system ('"{0}" -m pip install -r requirments.txt'.replace('{0}',sys.executable)) # install requirments

## pre build ##
if os.path.isdir ("stor"): shutil.rmtree("stor")

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

if not os.path.isdir ("build-packs"): os.mkdir ("build-packs")

plat = input('Choose your platform to install (Linux and Windows etc: 0, Termux: 1, PyDroid: 2, Server: 3): ')

if plat=='1':
	pack.inst('pyabr')
	pack.inst('pyabr_cli')
	pack.inst('paye')
	pack.inst('setup_cli')
	pack.inst('rachel')
	shutil.make_archive('pyabr-for-termux', 'zip', 'stor')
elif plat=='2':
	pack.inst('pyabr')
	pack.inst('paye')
	pack.inst('calculator')
	pack.inst('calendar')
	pack.inst('numix')
	pack.inst('commento')
	pack.inst('roller')
	pack.inst('runapp')
	pack.inst('paye')
	pack.inst('baran')
	pack.inst('setup')
	pack.inst('rachel')
	os.remove('stor/vmabr.pyc')
	shutil.copyfile('packs/pyabr/code/vmabr.py','stor/vmabr.py')
	shutil.make_archive('pyabr-for-pydroid', 'zip', 'stor')
elif plat=='3':
	pack.inst('pyabr')
	pack.inst('paye')
	pack.inst('calculator')
	pack.inst('calendar')
	pack.inst('numix')
	pack.inst('commento')
	pack.inst('roller')
	pack.inst('pyshell')
	pack.inst('pysys')
	pack.inst('runapp')
	pack.inst('paye')
	pack.inst('baran')
	pack.inst('setup_server')
	pack.inst('rachel')
	shutil.make_archive('pyabr-for-server', 'zip', 'stor')
else:
	pack.inst('pyabr')
	pack.inst('paye')
	pack.inst('calculator')
	pack.inst('calendar')
	pack.inst('numix')
	pack.inst('commento')
	pack.inst('roller')
	pack.inst('pyshell')
	pack.inst('pysys')
	pack.inst('runapp')
	pack.inst('paye')
	pack.inst('baran')
	pack.inst('setup')
	pack.inst('rachel')
	shutil.make_archive('pyabr', 'zip', 'stor')

# clean #
if os.path.isdir('app'): shutil.rmtree('app')
if os.path.isdir('build-packs'): shutil.rmtree('build-packs')
if os.path.isdir('stor'): shutil.rmtree('stor')