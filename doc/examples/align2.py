#!/usr/bin/env pyscript

# $Id$

"""
Another example of aligning objects.  This time aligning boxes with numbers
inside around a circle.
"""

from pyscript import *

all=Align(angle=90,space=2)

for ii in range(10):
    rt=Rectangle(width=1,height=1)
    all.append(
        Group(rt,Text(str(ii),c=rt.c)),
            angle=all.angle+ii*360/10.)

render(
    all,
    file='align2.eps',
    )

# vim: expandtab shiftwidth=4:
