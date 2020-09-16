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

from buildlibs import pack_archives as pack
from buildlibs import control
import shutil, os, sys, hashlib,getpass

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


pack.build('commento')
pack.unpack('commento')

# clean #
if os.path.isdir('app'): shutil.rmtree('app')
if os.path.isdir('build-packs'): shutil.rmtree('build-packs')
if os.path.isdir('stor'):
	shutil.make_archive('your-pyabr', 'zip', 'stor')
	shutil.rmtree('stor')