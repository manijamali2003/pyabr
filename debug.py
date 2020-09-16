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

pack.build ("pyabr")
pack.unpack ('pyabr')

pack.build ("baran")
pack.unpack ('baran')

pack.build ("paye")
pack.unpack ('paye')

pack.build('pyshell')
pack.unpack('pyshell')

pack.build('calendar')
pack.unpack('calendar')

pack.build('calculator')
pack.unpack('calculator')


pack.build('runapp')
pack.unpack('runapp')

pack.build('pysys')
pack.unpack('pysys')

pack.build('commento')
pack.unpack('commento')

# run #
i = input('Choose your kernel parameter ([G]UI, [C]Li, [R]OOT, G[U]ST, Default): ')
if os.path.isfile ('stor/proc/0'):  os.remove ('stor/proc/0')
if os.path.isfile ('stor/proc/id/desktop'): os.remove('stor/proc/id/desktop')

if os.path.isfile ('stor/vmabr.pyc'):
	if i.upper().startswith('C'):
		os.system('cd stor && "{0}" vmabr.pyc kernel'.replace('{0}', sys.executable))
	elif i.upper().startswith('G'):
		os.system('cd stor && "{0}" vmabr.pyc gui'.replace('{0}', sys.executable))
	elif i.upper().startswith('R'):
		os.system('cd stor && "{0}" vmabr.pyc user root toor'.replace('{0}', sys.executable))
	elif i.upper().startswith('U'):
		os.system('cd stor && "{0}" vmabr.pyc kernel'.replace('{0}', sys.executable))
	else:
		os.system('cd stor && "{0}" vmabr.pyc '.replace('{0}', sys.executable))
else:
	if i.upper().startswith('C'):
		os.system('cd stor && "{0}" vmabr.py kernel'.replace('{0}', sys.executable))
	elif i.upper().startswith('G'):
		os.system('cd stor && "{0}" vmabr.py gui'.replace('{0}', sys.executable))
	elif i.upper().startswith('R'):
		os.system('cd stor && "{0}" vmabr.py user root toor'.replace('{0}', sys.executable))
	elif i.upper().startswith('U'):
		os.system('cd stor && "{0}" vmabr.py kernel'.replace('{0}', sys.executable))
	else:
		os.system('cd stor && "{0}" vmabr.py '.replace('{0}', sys.executable))

# clean #
if os.path.isdir('app'): shutil.rmtree('app')
if os.path.isdir('build-packs'): shutil.rmtree('build-packs')
if os.path.isdir('stor'):
	shutil.rmtree('stor')