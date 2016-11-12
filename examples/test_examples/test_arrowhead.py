#!/usr/bin/env pyscript
# $Id$

# test script to test what the Arrowhead class should be able to do

__revision__ = '$Revision$'

from pyscript import *
import sys
sys.path.append('../../../pyscript/tests/')
from pyscriptTest import PyScriptTest

defaults.units=UNITS['cm']

arrowheads  = PyScriptTest()

# test init
arrowheads.test( ArrowHead(), "Arrowhead" ) 

# test internal scaling
arrowheads.test( ArrowHead(scalew=10, scaleh=10), "internal scale 10,10") 
arrowheads.test( ArrowHead(scalew=10, scaleh=5), "internal scale 10,5")
arrowheads.test( ArrowHead(scalew=5, scaleh=10), "internal scale 5,10")
# one would think this one should make it barf eh?
arrowheads.test( ArrowHead(scalew=-5, scaleh=-5), "internal scale -5,-5")
# test external scaling
arrowheads.test( ArrowHead().scale(10), "external scale 10")
arrowheads.test( ArrowHead().scale(10,10), "external scale 10,10")

# now add the scale option to each so can see them
arrowheads.test( ArrowHead(linewidth=2).scale(10), "linewidth=2")
arrowheads.test( ArrowHead(bg=Color("red")).scale(10), "bg = red")
arrowheads.test( ArrowHead(fg=Color("blue")).scale(10), "fg = blue")

# test angles
# should point north
arrowheads.test( ArrowHead(angle=0).scale(10), "angle=0")  
# should point east
arrowheads.test( ArrowHead(angle=90).scale(10), "angle=90") 
# should point south
arrowheads.test( ArrowHead(angle=180).scale(10), "angle=180") 
# should point west
arrowheads.test( ArrowHead(angle=270).scale(10), "angle=270") 
# should also point west
arrowheads.test( ArrowHead(angle=-90).scale(10), "angle=-90") 
# make sure can handle floats
arrowheads.test( ArrowHead(angle=83.71).scale(10), "angle=83.71") 

# test the tip position
arrowheads.test( ArrowHead(tip=P(0,0)).scale(10), "tip=P(0,0) default") 
# won't look much different on its own
arrowheads.test( ArrowHead(tip=P(1.5,6.2)).scale(10), "tip=P(1.5,6.2)") 

# test the other arrowheads
arrowheads.test( ArrowHead1().scale(10), "ArrowHead1")
arrowheads.test( ArrowHead2().scale(10), "ArrowHead2")
arrowheads.test( ArrowHead3().scale(10), "ArrowHead2")
arrowheads.test( ArrowHead4().scale(10), "ArrowHead4")

# render them
render(arrowheads, file="test_arrowhead.eps")

# vim: expandtab shiftwidth=4:
