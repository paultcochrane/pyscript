#!/usr/bin/env pyscript
# $Id$

# test script to test what the Circle class should be able to do

__revision__ = '$Revision$'

from pyscript import *
import sys
sys.path.append('../../../pyscript/tests/')
from pyscriptTest import PyScriptTest

defaults.units=UNITS['cm']

# make a wee file to test
render(VAlign(
    Rectangle(),
    Circle()
    ), file="epsf.eps")

epsfs = PyScriptTest()

# test init with file
epsfs.test( Epsf(fname="epsf.eps"), "init with filename" ) 

# test init without file
epsfs.test( Epsf("epsf.eps"), "init without filename" )

# render them
render(epsfs, file="test_epsf.eps")

# vim: expandtab shiftwidth=4:
