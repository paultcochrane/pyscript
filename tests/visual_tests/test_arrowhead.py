import sys
sys.path.insert(0,"../")

from pyscript import *

g=Group(
	ArrowHead1(tip=P( 1,0),angle=10),
	ArrowHead2(tip=P(.8,0),angle=30,bg=Color('yellow')),
	ArrowHead3(tip=P(.6,0),angle=60,fg=Color('red')),
	ArrowHead4(tip=P(.4,0),angle=90)
	).scale(3)

g2=HAlign(ArrowHead(),ArrowHead(scalew=2),ArrowHead(scaleh=2),space=.2).scale(2)
g2.move(0,-1)

p=Path(P(0,0),C(90,-90),P(2,2),
	heads=[ArrowHead(1),ArrowHead2(.8),ArrowHead3(.6),ArrowHead4(.4,reverse=1)]).scale(1.5)
	
render(
	g,
	g2,
	p,
	
    file='test_arrowhead.eps',
	
    )

