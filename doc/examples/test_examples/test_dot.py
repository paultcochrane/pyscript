#!/usr/bin/env pyscript
# $Id$

# test script to test what the Circle class should be able to do

__revision__ = '$Revision$'

from pyscript import *
import sys
sys.path.append('../../../pyscript/tests/')
from pyscriptTest import PyScriptTest

defaults.units=UNITS['cm']

dots = PyScriptTest()

# test init
dots.test( Dot() ) 

# test radius
dots.test( Dot(r=1.0), "r=1.0" ) 

# test colours
dots.test( Dot(bg=Color("red")), "bg = red" )  # radius=1cm, red bg, black fg
dots.test( Dot(fg=Color("blue")), "fg = blue" ) # radius=1cm, blue fg, None bg

# test colours at a decent size
dots.test( Dot(bg=Color("red"), r=1.0), "bg = red, r=1.0" )
dots.test( Dot(fg=Color("blue"), r=1.0), "fg = blue, r=1.0" )

# render them
render(dots, file="test_dot.eps")

# vim: expandtab shiftwidth=4:
