#!/usr/bin/env pyscript
# $Id$

# test script to test what the Circle class should be able to do

__revision__ = '$Revision$'

from pyscript import *
import sys
sys.path.append('../../../pyscript/tests/')
from pyscriptTest import PyScriptTest

defaults.units=UNITS['cm']

texts = PyScriptTest()
textStr = "text string"

# test init
texts.test( Text(textStr) ) 

# test colour
texts.test( Text(textStr, fg=Color("red")), "fg = red" )

# test size
texts.test( Text(textStr, size=5), "size=5" )
texts.test( Text(textStr, size=9), "size=9" )
texts.test( Text(textStr, size=10), "size=10" )
texts.test( Text(textStr, size=11), "size=11" )
texts.test( Text(textStr, size=12), "size=12" )
texts.test( Text(textStr, size=20), "size=20" )

# test font
## courier
texts.test( Text(textStr, font="courier"), "font = courier" )
texts.test( Text(textStr, font="courier_bold"), "font = courier_bold" )
texts.test( Text(textStr, font="courier_boldoblique"), 
        "font = courier_boldoblique" )
texts.test( Text(textStr, font="courier_oblique"), "font = courier_oblique" )
## helvetica
texts.test( Text(textStr, font="helvetica"), "font = helvetica" )
texts.test( Text(textStr, font="helvetica_bold"), "font = helvetica_bold" )
texts.test( Text(textStr, font="helvetica_boldoblique"), 
        "font = helvetica_boldoblique" )
texts.test( Text(textStr, font="helvetica_oblique"), 
        "font = helvetica_oblique" )
## symbol
texts.test( Text(textStr, font="symbol"), "font = symbol" )
## times
texts.test( Text(textStr, font="times_bold"), "font = times_bold" )
texts.test( Text(textStr, font="times_bolditalic"), 
        "font = times_bolditalic" )
texts.test( Text(textStr, font="times_italic"), "font = times_italic" )
texts.test( Text(textStr, font="times_roman"), "font = times_roman" )
## zapfdingbats
texts.test( Text(textStr, font="zapfdingbats"), "font = zapfdingbats" )

# test kerning
texts.test( Text("AWAV", kerning=1), "kerning=1" )
texts.test( Text("AWAV", kerning=0), "kerning=0" )


# render them
render(texts, file="test_text.eps")

# vim: expandtab shiftwidth=4:
