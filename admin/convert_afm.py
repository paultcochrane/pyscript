import os,sys
sys.path.insert(0,'../')

from pyscript import afm


for file in sys.argv[1:]:

    f=afm.ConvertAFM(file)

    fontname,ext=os.path.splitext(file)

    f.write(fontname+".font")
    print "converted",fontname
