#!/usr/bin/env python

# a python in script

from pyscript import *

#----------------------------------------------------------------------------------------------
defaults.units=UNITS['cm']

defaults.tex_head=r"""
\documentclass{article}
\pagestyle{empty}
\begin{document}
"""

thick = 0.3
lp = (P(0,0),P(1,0.5),P(2,0),P(3,-0.5),P(4-0.1,0-0.1))
rp = (P(0,0-thick),P(1,0.5-thick),P(2,0-thick),P(3,-0.5-thick),P(4,0-thick))

tail = P(-0.5,-0.4)

body= Path(tail,
	lp[0],C(lp[1]),lp[2],C(lp[3]),lp[4],
	C(lp[4]+P(0.1,0.25)),lp[4]+P(0.55,0.2),
         rp[4]+P(0.5,0.3),C(rp[4]+P(0.3,-0.1)),
         rp[4],  C(rp[3]),rp[2],C(rp[1]),rp[0],tail,
           bg=Color(.91,.82,.63))
         

tpoint = (lp[4]+P(0.55,0.2)+rp[4]+P(0.5,0.3))/2.0
tongue = Group(
	Path(tpoint,C(tpoint+P(0.1,0.1)),tpoint+P(0.1,0.2),fg=Color('cyan')),
	Path(tpoint,C(tpoint+P(0.1,0.1)),tpoint+P(0.2,0.05),fg=Color('cyan')),
)

el1 = lp[4]+P(0.19,0.03)
el2 = el1+P(0.05,0.05)
er1 = rp[4]+P(0.19,0.13)
er2 = er1+P(0.05,0.05)
eyes = Group(
	Path(el1,el2,fg=Color('magenta')),
	Path(er1,er2,fg=Color('magenta')),
)

cpoints = (
	lp[0],
	(rp[1]+rp[0])/2.0,
	lp[1]-P(0,thick/3.0),
	(rp[2]+rp[1])/2.0,
	lp[2],
	(rp[3]+rp[2])/2.0,
	lp[3]+P(0,thick/3.0),
	(rp[4]+rp[3])/2.0,
)

squiggle = Path(tail+P(0.25,0.05),
	C(cpoints[0]),
	(cpoints[0]+cpoints[1])/2.0,
	C(cpoints[1]),
	(cpoints[1]+cpoints[2])/2.0,
	C(cpoints[2]),
	(cpoints[2]+cpoints[3])/2.0,
	C(cpoints[3]),
	(cpoints[3]+cpoints[4])/2.0,
	C(cpoints[4]),
	(cpoints[4]+cpoints[5])/2.0,
	C(cpoints[5]),
	(cpoints[5]+cpoints[6])/2.0,
	C(cpoints[6]),
	(cpoints[6]+cpoints[7])/2.0,
	C(cpoints[7]),
	lp[4],
)
squiggle.fg = Color('red')

dotR = 0.02
dotpoints = (
	P(lp[0][0],rp[0][1]+thick/2.0),
	rp[1],
	P(lp[2][0],rp[2][1]+thick/2.0),
	lp[3],
)
dotfg = Color('yellow')
dots = Group(
	Dot(dotpoints[0],r=dotR,fg=dotfg),
	Dot((dotpoints[0]+dotpoints[1])/2.0+P(-0.03,0.03),r=dotR,fg=dotfg),
	Dot(dotpoints[1],r=dotR,fg=dotfg),
	Dot((dotpoints[1]+dotpoints[2])/2.0+P(0.03,0.03),r=dotR,fg=dotfg),
	Dot(dotpoints[2],r=dotR,fg=dotfg),
	Dot((dotpoints[2]+dotpoints[3])/2.0-P(0.03,0.03),r=dotR,fg=dotfg),
	Dot(dotpoints[3],r=dotR,fg=dotfg),
	)

py=Text("Py",size=40,font="Times-BoldItalic")
script=Text("Script",size=40,font="Times-BoldItalic")
py.e=squiggle.c-P(.5,0)
script.w=py.e

schlange = Group(script,body,eyes,squiggle,dots,tongue,py)


# draw it!
render(schlange,file="logo.eps")


