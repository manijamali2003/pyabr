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

import sys

from libabr import Files, Control, Permissions, Colors, Process, Modules, Package

modules = Modules()
files = Files()
control = Control()
colors = Colors()
process = Process()
permissions = Permissions()
pack = Package()

## Check root ##
if not permissions.check_root (files.readall("/proc/info/su")):
    colors.show ("paye","perm","")
    sys.exit(0)

## Check inputs ##
if sys.argv[1:]==[]:
    colors.show ("paye","fail","no inputs.")
    sys.exit(0)

option = sys.argv[1]

if option=="-c":
    pack.clean()
    colors.show("", "ok", "Clean the cache.")

elif option=="-b":
    if files.isfile ("/app/cache/lock"):
        colors.show ("paye","fail","cache has already locked.")
        sys.exit(0)
    else:
        files.create ("/app/cache/lock")

    if sys.argv[2:]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)

    dir = sys.argv[2:]

    for i in dir:
        pack.build(i)
        colors.show("", "ok", "Build '" + i + "' source code.")

    pack.clean()


elif option=="-u":
    if files.isfile ("/app/cache/lock"):
        colors.show ("paye","fail","cache has already locked.")
        sys.exit(0)
    else:
        files.create ("/app/cache/lock")

    if sys.argv[1:]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)

    archive = sys.argv[2:]

    if archive[1:]==[]:
        y = input('Do you want to unpack {0} package? [Y/n]: '.replace('{0}', archive[0]))
        if not y.lower().startswith('y'):
            sys.exit(0)
    else:
        strv = ''
        for i in archive:
            strv+=','+i

        y = input('Do you want to unpack {0} packages? [Y/n]: '.replace('{0}', strv))
        if not y.lower().startswith('y'):
            sys.exit(0)

    for i in archive:
        if files.isfile(i):
            pack.unpack(i)
            colors.show("", "ok", "Unpack '" + i + "' archive package.")

        else:
            colors.show("paye", "fail", i + ": archive not found.")

    pack.clean()

elif option=="-r":
    if files.isfile ("/app/cache/lock"):
        colors.show ("paye","fail","cache has already locked.")
        sys.exit(0)
    else:
        files.create ("/app/cache/lock")

    if sys.argv[2]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)

    package = sys.argv[2:]

    if package[1:] == []:
        y = input('Do you want to uninstall {0} package? [Y/n]: '.replace('{0}', package[0]))
        if not y.lower().startswith('y'):
            sys.exit(0)
    else:
        strv = ''
        for i in package:
            strv += ',' + i

        y = input('Do you want to uninstall {0} packages? [Y/n]: '.replace('{0}', strv))
        if not y.lower().startswith('y'):
            sys.exit(0)

    for i in package:
        pack.uninstall(i.lower())
        colors.show("", "ok", "Uninstall '" + i.lower() + "' package.")

    pack.clean()

elif option=="-g":

    if sys.argv[2]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)

    package = sys.argv[2:]

    if package[1:] == []:
        y = input('Do you want to download {0} package? [Y/n]: '.replace('{0}', package[0]))
        if not y.lower().startswith('y'):
            sys.exit(0)
    else:
        strv = ''
        for i in package:
            strv += ',' + i

        y = input('Do you want to download {0} packages? [Y/n]: '.replace('{0}', strv))
        if not y.lower().startswith('y'):
            sys.exit(0)

    for i in package:
        colors.show ('',"ok","Download \'"+i+"\' archive package.")
        pack.download (i.lower())

elif option=="-i":
    if files.isfile ("/app/cache/lock"):
        colors.show ("paye","fail","cache has already locked.")
        sys.exit(0)
    else:
        files.create ("/app/cache/lock")

    if sys.argv[2]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)

    package = sys.argv[2:]

    if package[1:]==[]:
        y = input('Do you want to install {0} package? [Y/n]: '.replace('{0}', package[0]))
        if not y.lower().startswith('y'):
            sys.exit(0)
    else:
        strv = ''
        for i in package:
            strv+=','+i

        y = input('Do you want to install {0} packages? [Y/n]: '.replace('{0}', strv))
        if not y.lower().startswith('y'):
            sys.exit(0)

    for i in package:
        colors.show ('',"ok","Download \'"+i+"\' archive package.")
        pack.download(i.lower())

    for j in package:
        pack.unpack("/app/cache/gets/" + j.lower() + ".pa")
        colors.show("", "ok", "Unpack '.../" + j.lower() + ".pa' archive package.")

    pack.clean()

elif option=="-v":
    if sys.argv[2:]==[]:
        colors.show ('paye','fail','no inputs.')
        sys.exit(0)

    pack = "/app/packages/"+sys.argv[2]+".manifest"
    if files.isfile(pack):

        name = control.read_record ("name",pack)
        build = control.read_record("build", pack)
        version = control.read_record("version", pack)
        unpack = control.read_record("unpack", pack)
        description = control.read_record("description", pack)
        depends = control.read_record("depends", pack)
        license = control.read_record("license", pack)
        copyright = control.read_record("copyright", pack)
        arch = control.read_record("arch", pack)

        bold = colors.color(1, colors.get_bgcolor(), colors.get_fgcolor())
        if not (name == None or name == ""):  print(
            "\t      Package name: " + bold + name + colors.get_colors())
        if not (version == None or version == ""):  print(
            "\t   Package version: " + bold + version + colors.get_colors())
        if not (build == None or build == ""):  print(
            "\t        Build date: " + bold + build + colors.get_colors())
        if not (copyright == None or copyright == ""):  print(
            "\t         Copyright: " + bold + copyright + colors.get_colors())
        if not (license == None or license == ""):  print(
            "\t          Licensce: " + bold + license + colors.get_colors())
        if not (description == None or description == ""):  print(
            "\t       Description: " + bold + description + colors.get_colors())
        if not (depends == None or depends == ""):  print(
            "\t   Package depends: " + bold + depends + colors.get_colors())
        if not (unpack == None or unpack == ""):  print(
            "\t      Installed in: " + bold + unpack + colors.get_colors())
        if not (unpack == None or unpack == ""):  print(
            "\t      Architecture: " + bold + arch + colors.get_colors())
    else:
        colors.show ("paye","fail",sys.argv[2]+": package has not already installed.")

elif option=="-l":
    list = files.list ("/app/packages")
    bold = colors.color(1, colors.get_bgcolor(), colors.green)
    for i in list:
        if i.endswith (".manifest"):
            name = control.read_record("name", "/app/packages/"+i)
            build = control.read_record("build", "/app/packages/"+i)
            version = control.read_record("version", "/app/packages/"+i)
            print (bold+name+colors.get_colors()+"/"+colors.get_path()+version+colors.get_colors()+"/"+build)

elif option=='-a':
    if sys.argv[2:]==[] or sys.argv[3:]==[]:
        colors.show ('paye','fail','no inputs.')
        sys.exit(0)

    y = input ('Do you want to add {0} mirror? [Y/n]: '.replace('{0}',sys.argv[2]))
    if y.lower().startswith('y'):
        pack.add (sys.argv[2],sys.argv[3])
        colors.show ("",'ok','Add \''+sys.argv[2]+'\' mirror from ('+sys.argv[3]+").")
elif option=='-d':
    if sys.argv[2:]==[]:
        colors.show ('paye','fail','no inputs.')
        sys.exit(0)
    y = input('Do you want to remove {0} mirror? [Y/n]: '.replace('{0}', sys.argv[2]))
    if y.lower().startswith('y'):
        pack.remove (sys.argv[2])
        colors.show("", 'ok', 'Remove \'' + sys.argv[2] + '\' mirror.')
else:
    colors.show ("paye","fail",option+": option not found.")