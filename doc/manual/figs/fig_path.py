#!/usr/bin/env pyscript

from pyscript import *

p0=P(2,1)
p1=P(4,2)
c1=R(4,2)
c2=R(-4,-2)/2.
p2=P(4,4)
p3=P(6,5)

path=Path(p0,p1,C(c1,c2),p2,p3,fg=Color('red'),linewidth=.8)

d=R(0,.1)
g=Group()
for p in [p0,p1,p2,p3,p1+c1,p2+c2]:
    g.append(Dot(p))

render(
    path,
    Path(p1,p1+c1,dash="[3] 0 "),
    Path(p2,p2+c2,dash="[3] 0 "),
    g,
    Text("p0",n=p0-d),
    Text("p1",n=p1-d),
    Text("c1",n=p1+c1-d),
    Text("p2",s=p2+d),
    Text("p3",s=p3+d),
    Text("c2",s=p2+c2+d),
    file="fig_path.eps"
    )

# vim: expandtab shiftwidth=4:
