#!/usr/bin/env pyscript
# $Id$

# test script to test what the Circle class should be able to do

__revision__ = '$Revision$'

from pyscript import *
import sys
sys.path.append('../../../pyscript/tests/')
from pyscriptTest import PyScriptTest

defaults.units=UNITS['cm']

texs = PyScriptTest()
texStr = r"\TeX{} object test, $\pi r^2$, \textit{moo}, \textbf{baa}"

# test init
texs.test( TeX(texStr) ) 

# test colour
texs.test( TeX(texStr, fg=Color("red")), "fg = red" )

# test iscale
texs.test( TeX(texStr, iscale=1.0), "iscale=1.0" ) # default
texs.test( TeX(texStr, iscale=2.0), "iscale=2.0" ) 
texs.test( TeX(texStr, iscale=0.5), "iscale=0.5" )

# render them
render(texs, file="test_tex.eps")

# vim: expandtab shiftwidth=4:
