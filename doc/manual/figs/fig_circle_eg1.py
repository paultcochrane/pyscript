from pyscript import *

c=Circle(r=.5,bg=Color('gold'))

g=Group(c)
for ii in range(0,360,30):
    g.append(
        Circle(r=.2,bg=Color('white')).locus(180+ii,c.locus(ii))
        )

render(g,file="fig_circle_eg1.eps")

# vim: expandtab shiftwidth=4:
