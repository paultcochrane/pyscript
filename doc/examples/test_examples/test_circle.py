#!/usr/bin/env pyscript
# $Id$

# test script to test what the Circle class should be able to do

__revision__ = '$Revision$'

from pyscript import *

defaults.units=UNITS['cm']

circles = []
circles.append( Circle() )       # should be radius=1cm, black fg, None bg
circles.append( Circle(r=2.0) )  # should be radius=2cm, black fg, None bg
circles.append( Circle(linewidth=2) )
circles.append( Circle(bg=Color("red")) )  # radius=1cm, red bg, black fg
circles.append( Circle(fg=Color("blue")) ) # radius=1cm, blue fg, None bg
circles.append( Circle(start=90) )
circles.append( Circle(end=90) )
circles.append( Circle(start=90, end=270) )
circles.append( Circle(start=15.2, end=67.9) )

i = 0
for circle in circles:
    i = i + 1
    render(circle, file="test_circle%d.eps" % i)

# vim: expandtab shiftwidth=4:
