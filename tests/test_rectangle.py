#!/usr/bin/env pyscript

import sys
sys.path.insert(0,"../")
from pyscript import *

defaults.units=UNITS['cm']

r=Rectangle().rotate(60)

g=VAlign(
    r,

    Rectangle(linewidth=2.0),

    Rectangle(fg=Color("green"),bg=Color("red")),

    Rectangle(dash=Dash(4),width=2,height=.5),

    Rectangle(r=0.25),
    Rectangle(r=0.6),
    )


render(g, 
    Dot(r.ne), Dot(r.n), Dot(r.nw), Dot(r.w), Dot(r.sw), Dot(r.s), Dot(r.se), Dot(r.e), Dot(r.c), 

    file="test_rectangle.eps")

# vim: expandtab shiftwidth=4:
