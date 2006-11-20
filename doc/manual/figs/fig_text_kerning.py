from pyscript import *

t1=Text('SWEPT AWAY',kerning=0,size=20)
t2=Text('SWEPT AWAY',kerning=1,size=20,nw=t1.sw)

render(t1,t2,file="fig_text_kerning.eps")

# vim: expandtab shiftwidth=4:
