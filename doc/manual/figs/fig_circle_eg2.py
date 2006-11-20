#!/usr/bin/env pyscript

from pyscript import *
from math import sqrt

g=Group(Rectangle(sw=P(0,0),width=2,height=2),
        Circle(r=1,sw=P(0,0)),
        Circle(r=sqrt(2)).locus(-135,P(0,0)),
        )
g.scale(1.5,.5)
render(g,
       file="fig_circle_eg2.eps")

# vim: expandtab shiftwidth=4:
