#!/usr/bin/env pyscript

from pyscript import *

p=Path(P(0,0),P(1,1))

g=Group(p,
    Arrowhead1(tip=p.P( 1),angle=45),
    Arrowhead2(tip=p.P(.8),angle=45),
    Arrowhead3(tip=p.P(.6),angle=45),
    Arrowhead4(tip=p.P(.4),angle=45)
    ).scale(5)

render(
    g,
    file='arrow.eps',
    )

