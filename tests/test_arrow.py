#!/usr/bin/env pyscript

import sys
sys.path.insert(0,"../")

from pyscript import *

render(
	Arrow(P(-1,-1),P(2,1),heads=[ArrowHead(0,reverse=1),ArrowHead(1)]),
	DoubleArrow(P(0,0),P(1,-1)),
	Arrow(P(0,0),C(0,0),P(1,1),dash=Dash(2,2),fg=Color('red')),
	
    file='test_arrow.eps',
	
    )

