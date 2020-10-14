from libabr import Files, Control

files = Files()
control = Control()

user = files.readall ('/proc/info/su')

name = control.read_record ('first_name','/etc/users/'+user)
family = control.read_record ('last_name','/etc/users/'+user)

username = ""

if not name==None and not family == None:
    username = name+" "+family
elif not name==None:
    username = name
elif not family==None:
    username = family
else:
    username = user