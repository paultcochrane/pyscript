# test script to test what the Circle class should be able to do
import sys
sys.path.insert(0,"../")

from pyscript import *

c=Circle()
g=VAlign( 
    c,
    Circle(r=2.0,dash=Dash(3)),
    Circle(bg=Color("red")),
    Circle(fg=Color("blue"),linewidth=3).scale(2,.5),
    Circle(start=90, end=270),
    space=.2)

g2=Group()
for ii in range(0,360,30):
    g2.append(Dot(c.locus(ii)))

g2.append(Dot(c.c))
# render them
render(g,g2, file="test_circle.eps")

# vim: expandtab shiftwidth=4:
