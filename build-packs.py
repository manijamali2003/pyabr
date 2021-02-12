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

## pre build ##

mode = input('choose your mode (stable,latest): ')

for i in os.listdir('packs'):pack.manifest(i)

os.removedirs('stor/tmp')
shutil.copytree('packs',f'stor/tmp')
f = open('stor/pack.sa','w')
f.write(f'''mkdir /tmp/all
paye pak /tmp/baran
mv /tmp/baran.pa /tmp/all/baran.pa
paye pak /tmp/barge
mv /tmp/barge.pa /tmp/all/barge.pa
paye pak /tmp/browser
mv /tmp/browser.pa /tmp/all/browser.pa
paye pak /tmp/calculator
mv /tmp/calculator.pa /tmp/all/calculator.pa
paye pak /tmp/calendar
mv /tmp/calendar.pa /tmp/all/calendar.pa
paye pak /tmp/commento
mv /tmp/commento.pa /tmp/all/commento.pa
paye pak /tmp/gap
mv /tmp/gap.pa /tmp/all/gap.pa
paye pak /tmp/help
mv /tmp/help.pa /tmp/all/help.pa
paye pak /tmp/{mode}
mv /tmp/{mode}.pa /tmp/all/{mode}.pa
paye pak /tmp/lightword
mv /tmp/lightword.pa /tmp/all/lightword.pa
paye pak /tmp/mines
mv /tmp/mines.pa /tmp/all/mines.pa
paye pak /tmp/numix
mv /tmp/numix.pa /tmp/all/numix.pa
paye pak /tmp/paint
mv /tmp/paint.pa /tmp/all/paint.pa
paye pak /tmp/paye
mv /tmp/paye.pa /tmp/all/paye.pa
paye pak /tmp/persia
mv /tmp/persia.pa /tmp/all/persia.pa
paye pak /tmp/pyabr
mv /tmp/pyabr.pa /tmp/all/pyabr.pa
paye pak /tmp/pyshell
mv /tmp/pyshell.pa /tmp/all/pyshell.pa
paye pak /tmp/pysys
mv /tmp/pysys.pa /tmp/all/pysys.pa
paye pak /tmp/roller
mv /tmp/roller.pa /tmp/all/roller.pa
paye pak /tmp/runapp
mv /tmp/runapp.pa /tmp/all/runapp.pa
paye pak /tmp/ubuntu-theme
mv /tmp/ubuntu-theme.pa /tmp/all/ubuntu-theme.pa
paye pak /tmp/windows-theme
mv /tmp/windows-theme.pa /tmp/all/windows-theme.pa
''')
shutil.rmtree(mode)

input('Are sure copy all package? press enter')

shutil.copytree('stor/tmp/all',mode)