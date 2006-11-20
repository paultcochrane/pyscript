#!/usr/bin/env pyscript

from pyscript import *

p0=P(2,1)
p1=P(4,2)
c1=R(4,2)
c2=R(-4,-2)/2.
#c2=R(-1,-.5)
p2=P(4,4)
p3=P(6,5)

path=Path(p0,p1,C(c1,c2),p2,p3,fg=Color('red'),linewidth=.8)

g=Group()
delta=1/20.
for p in range(21):
    g.append(Dot(path.P(p*delta)))

render(
    path,
    g,
    file="fig_path_eg.eps"
    )

# vim: expandtab shiftwidth=4:
