#!/usr/bin/env pyscript
# $Id$

# test script to test what the Circle class should be able to do

__revision__ = '$Revision$'

from pyscript import *
import sys
sys.path.append('../../../pyscript/tests/')
from pyscriptTest import PyScriptTest

defaults.units=UNITS['cm']

rects = PyScriptTest()

# test init
rects.test( Rectangle() ) 

# test linewidth
rects.test( Rectangle(linewidth=1), "linewidth=1" )
rects.test( Rectangle(linewidth=2.0), "linewidth=2.0" )

# test colour
rects.test( Rectangle(fg=Color("blue")), "fg = blue" )
rects.test( Rectangle(bg=Color("red")), "bg = red" )

# test dash
rects.test( Rectangle(dash=Dash()), "dash=Dash()" )

# test radius of corners
rects.test( Rectangle(r=0), "r=0" )  # default
rects.test( Rectangle(r=0.1), "r=0.1" )
rects.test( Rectangle(r=0.25), "r=0.25" )
rects.test( Rectangle(r=0.5), "r=0.5" )
rects.test( Rectangle(r=0.75), "r=0.75" )
rects.test( Rectangle(r=1.0), "r=1.0" )

# test width
rects.test( Rectangle(width=1.0), "width=1.0" ) # default
rects.test( Rectangle(width=2.0), "width=2.0" )
rects.test( Rectangle(width=0.25), "width=0.25" )

# test height
rects.test( Rectangle(height=1.0), "height=1.0" ) # default
rects.test( Rectangle(height=2.0), "height=2.0" )
rects.test( Rectangle(height=0.25), "height=0.25" )

# test width and height
rects.test( Rectangle(width=1.0, height=1.0), "width=1.0, height=1.0" )
rects.test( Rectangle(width=0.5, height=2.0), "width=0.5, height=2.0" )
rects.test( Rectangle(width=2.0, height=0.3), "width=2.0, height=0.3" )


# render them
render(rects, file="test_rectangle.eps")

# vim: expandtab shiftwidth=4:
