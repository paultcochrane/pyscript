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
arrows.test( Arrow(P(0,0), P(0,1)) ) 

arrows.test( DoubleArrow(P(0,0), P(0,1)) )

# render them
render(arrows, file="test_arrow.eps")

# vim: expandtab shiftwidth=4:
