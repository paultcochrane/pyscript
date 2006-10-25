#!/usr/bin/env pyscript

# $Id$

"""
Example showing the different kinds of arrowheads defined in pyscript.
"""

from pyscript import *

p=Path(P(0,0),C(20,200),P(4,4),
	heads=[ArrowHead(1), ArrowHead2(.8), ArrowHead3(.6), ArrowHead4(.4)])

render(
    p,
    file='arrow.eps',
    )

# vim: expandtab shiftwidth=4:
