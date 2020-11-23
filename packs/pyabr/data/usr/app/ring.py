from libabr import Ring, Files

f = Files()
r = Ring()

r.write ('readme.rvd',r.TYPE_TEXT,'1234',"Hello")
print(r.read ('readme.rvd',r.TYPE_TEXT,'1234'))