#!/usr/bin/env pyscript

# $Id$

"""
Example showing the different kinds of arrowheads defined in pyscript.
"""

from pyscript import *

p=Path(P(0,0),C(20,200),P(4,4),
	heads=[Arrowhead(1), Arrowhead2(.8), Arrowhead3(.6), Arrowhead4(.4)])

render(
    p,
    file='arrow.eps',
    )

# vim: expandtab shiftwidth=4:
