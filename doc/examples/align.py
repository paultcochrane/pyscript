#!/usr/bin/env pyscript

from pyscript import *

defaults.units=UNITS['cm']

r1=Rectangle(width=2,height=1,c=P(0,0))
r2=Rectangle(width=1,height=2,c=P(2,1))
c1=Circle(c=P(3,2))
c2=Circle(r=2,c=P(6,3))

# record where they started in red
orig=Group(r1.copy(fg=Color('Red')),
           r2.copy(fg=Color('Red')),
           c1.copy(fg=Color('Red')),
           c2.copy(fg=Color('Red')),
)


a=Group(r1,r2,c1,c2).apply(linewidth=2)
Align(a,a1="e",a2="w",space=None,angle=90)

render(
    orig,
    a,
    file="align.eps",
    )
    
