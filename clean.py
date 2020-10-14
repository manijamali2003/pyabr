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

def clean():
    if os.path.isdir ('app'):                    shutil.rmtree('app')
    if os.path.isdir ('build-packs'):            shutil.rmtree('build-packs')
    if os.path.isdir ('stor'):                   shutil.rmtree('stor')
    if os.path.isdir ('pack-release'):           shutil.rmtree('pack-release')
    if os.path.isfile('pyabr.zip'):              os.remove    ('pyabr.zip')
    if os.path.isfile('pyabr-for-pydroid.zip'):  os.remove('pyabr-for-pydroid.zip')
    if os.path.isfile('pyabr-for-termux.zip'):   os.remove('pyabr-for-termux.zip')
clean()
