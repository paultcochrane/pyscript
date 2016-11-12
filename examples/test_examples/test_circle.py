#!/usr/bin/env pyscript
# $Id$

# test script to test what the Circle class should be able to do

__revision__ = '$Revision$'

from pyscript import *
import sys
sys.path.append('../../../pyscript/tests/')
from pyscriptTest import PyScriptTest

defaults.units=UNITS['cm']

circles = PyScriptTest()

# test init
circles.test( Circle() )       # should be radius=1cm, black fg, None bg

# test radius
circles.test( Circle(r=2.0), "r=2.0" )  # should be radius=2cm, black fg, None bg

# test linewidth
circles.test( Circle(linewidth=2), "linewidth=2" )

# test colours
circles.test( Circle(bg=Color("red")), "bg = red" )  # radius=1cm, red bg, black fg
circles.test( Circle(fg=Color("blue")), "fg = blue" ) # radius=1cm, blue fg, None bg

# test starting and ending
circles.test( Circle(start=90), "start=90" )
circles.test( Circle(end=90), "end=90" )
circles.test( Circle(start=90, end=270), "start=90, end=270" )
circles.test( Circle(start=15.2, end=67.9), "start=15.2, end=67.9" )

# render them
render(circles, file="test_circle.eps")

# vim: expandtab shiftwidth=4:
