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

## pre build ##

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

# build #
y = input('Do you want to debug Pyabr? [Y/n]: ')
if y.lower().startswith('y'):
    pack.build ("pyabr")
    pack.unpack ('pyabr')

y = input('Do you want to debug Baran? [Y/n]: ')
if y.lower().startswith('y'):
    pack.build ("baran")
    pack.unpack ('baran')

y = input('Do you want to debug Paye? [Y/n]: ')
if y.lower().startswith('y'):
    pack.build ("paye")
    pack.unpack ('paye')

y = input('Do you want to debug PyShell [Y/n]: ')
if y.lower().startswith('y'):
	pack.build('pyshell')
	pack.unpack('pyshell')

y = input('Do you want to debug Calendar [Y/n]: ')
if y.lower().startswith('y'):
	pack.build('calendar')
	pack.unpack('calendar')

y = input('Do you want to debug Calculator [Y/n]: ')
if y.lower().startswith('y'):
	pack.build('calculator')
	pack.unpack('calculator')

y = input('Do you want to debug App Runner [Y/n]: ')
if y.lower().startswith('y'):
	pack.build('runapp')
	pack.unpack('runapp')

y = input('Do you want to debug Power Options [Y/n]: ')
if y.lower().startswith('y'):
	pack.build('pysys')
	pack.unpack('pysys')

y = input('Do you want to debug Terminal [Y/n]: ')
if y.lower().startswith('y'):
	pack.build('commento')
	pack.unpack('commento')

# run #
i = input('Choose your kernel parameter ([G]UI, [C]Li, [R]OOT, G[U]ST, Default): ')
if os.path.isfile ('stor/proc/0'):  os.remove ('stor/proc/0')
if os.path.isfile ('stor/proc/id/desktop'): os.remove('stor/proc/id/desktop')

if i.upper().startswith('C'):
	os.system('cd stor && "{0}" vmabr.pyc kernel'.replace('{0}',sys.executable))
elif i.upper().startswith('G'):
	os.system('cd stor && "{0}" vmabr.pyc gui'.replace('{0}',sys.executable))
elif i.upper().startswith('R'):
	os.system('cd stor && "{0}" vmabr.pyc user root toor'.replace('{0}',sys.executable))
elif i.upper().startswith('U'):
	os.system('cd stor && "{0}" vmabr.pyc kernel'.replace('{0}',sys.executable))
else:
	os.system('cd stor && "{0}" vmabr.pyc '.replace('{0}',sys.executable))