#!/usr/bin/env pyscript
# $Id$

# test script to test what the Arrowhead class should be able to do

__revision__ = '$Revision$'

from pyscript import *
import sys
sys.path.append('../../../pyscript/tests/')
from pyscriptTest import PyScriptTest

defaults.units=UNITS['cm']

arrows  = PyScriptTest()

# test init
arrows.test(Arrowhead(), "Arrowhead") 

# test internal scaling
arrows.test(Arrowhead(scalew=10, scaleh=10), "internal scale 10,10") 
arrows.test(Arrowhead(scalew=10, scaleh=5), "internal scale 10,5")
arrows.test(Arrowhead(scalew=5, scaleh=10), "internal scale 5,10")
# one would think this one should make it barf eh?
arrows.test(Arrowhead(scalew=-5, scaleh=-5), "internal scale -5,-5")
# test external scaling
arrows.test(Arrowhead().scale(10), "external scale 10")
arrows.test(Arrowhead().scale(10,10), "external scale 10,10")

# now add the scale option to each so can see them
arrows.test(Arrowhead(linewidth=2).scale(10), "linewidth=2")
arrows.test(Arrowhead(bg=Color("red")).scale(10), "bg = red")
arrows.test(Arrowhead(fg=Color("blue")).scale(10), "fg = blue")

# test angles
arrows.test(Arrowhead(angle=0).scale(10), "angle=0")  # should point north
arrows.test(Arrowhead(angle=90).scale(10), "angle=90") # should point east
arrows.test(Arrowhead(angle=180).scale(10), "angle=180") # should point south
arrows.test(Arrowhead(angle=270).scale(10), "angle=270") # should point west
arrows.test(Arrowhead(angle=-90).scale(10), "angle=-90") # should also point west
# make sure can handle floats
arrows.test(Arrowhead(angle=83.71).scale(10), "angle=83.71") 

# test the tip position
arrows.test(Arrowhead(tip=P(0,0)).scale(10), "tip=P(0,0) default") # the default
# won't look much different on its own
arrows.test(Arrowhead(tip=P(1.5,6.2)).scale(10), "tip=P(1.5,6.2)") 

# test the other arrowheads
arrows.test(Arrowhead1().scale(10), "Arrowhead1")
arrows.test(Arrowhead2().scale(10), "Arrowhead2")
arrows.test(Arrowhead3().scale(10), "Arrowhead2")
arrows.test(Arrowhead4().scale(10), "Arrowhead4")

# render them
render(arrows, file="test_arrow.eps")

# vim: expandtab shiftwidth=4:
