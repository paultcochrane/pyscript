#!/usr/bin/env python

import sys
sys.path.insert(0,'../../')
sys.path.insert(0,'../../pyscript')
sys.path.insert(0,'../../pyscript/lib')

from pyscript import *

#----------------------------------------------------------------------------------------------
defaults.units=UNITS['cm']

defaults.tex_head=r"""
\documentclass{article}
\pagestyle{empty}

\newcommand{\ket}[2]{\mbox{$|#1\rangle_{#2}$}}
\newcommand{\bra}[1]{\mbox{$\langle #1|$}}
\newcommand{\braket}[2]{\mbox{$\langle #1|#2\rangle$}}
\newcommand{\op}[1]{\mbox{\boldmath $\hat{#1}$}}
\begin{document}
"""

def ArrowHead(tip=P(0,0),width=0.2,height=0.2,dir="e",fg=Color("black"),bg=Color("black"),angle=0,dent=0.2):
    """
    ArrowHead object
    """
    # need to chuck some bezier spline stuff in here to make nicer arrowheads
#      ah = Path(e,C(?,?,?,?),
#                e+P(-h,w/2.0),e+P(-h*(1-dent),0),e+P(-h,-w/2.0),
#                C(?,?,?,?),e,fg=fg,bg=bg)

    if dir == "e":
        ah = Path(tip,
                  tip+P(-height,width/2.0),tip+P(-height*(1-dent),0),tip+P(-height,-width/2.0),
                  tip,fg=fg,bg=bg)
    elif dir == "n":
        ah = Path(tip,
                  tip+P(width/2.0,-height),tip+P(0,-height*(1-dent)),tip+P(-width/2.0,-height),
                  tip,fg=fg,bg=bg)
    elif dir == "w":
        ah = Path(tip,
                  tip-P(-height,width/2.0),tip-P(-height*(1-dent),0),tip-P(-height,-width/2.0),
                  tip,fg=fg,bg=bg)
    elif dir == "s":
        ah = Path(tip,
                  tip-P(width/2.0,-height),tip-P(0,-height*(1-dent)),tip-P(-width/2.0,-height),
                  tip,fg=fg,bg=bg)

    ah.rotate(angle)

    return ah


circ1 = Circle(c=P(0,0), start=0,end=360)

circ2front = Circle(c=P(0,0), start=90,end=270)
circ2back = Circle(c=P(0,0), start=270,end=90,dash="[ 3 ] 0")
circ2 = Group(circ2front,circ2back)
circ2.scale(1,0.3)

circ3front = Circle(c=P(0,0), start=90,end=270)
circ3back = Circle(c=P(0,0), start=270,end=90,dash="[ 3 ] 0")
circ3 = Group(circ3front,circ3back)
x2 = 0.78
circ3.scale(x2,0.3*x2)
circ3.c = P(0,-0.6)

zaxis = Path(P(0,-1.2),P(0,1.2),linewidth=0.3)
xaxis = Path(P(-1.2,0),P(1.2,0),linewidth=0.3)
yaxis = Path(P(-0.7,0),P(0.7,0),linewidth=0.3)
yaxis.rotate(p=yaxis.c,angle=-30)

xArrow = ArrowHead(tip=xaxis.e+P(0,0),width=0.07,height=0.07)
yArrow = ArrowHead(tip=yaxis.bbox().ne+P(0.09,0),angle=-30,width=0.07,height=0.07)
zArrow = ArrowHead(tip=zaxis.n,dir="n",width=0.07,height=0.07)

xLabel = TeX(sw=xaxis.ne,text="$\mathbf{J}_x$").scale(0.5,0.5)
yLabel = TeX(sw=yaxis.ne,text="$\mathbf{J}_y$").scale(0.5,0.5)
zLabel = TeX(sw=zaxis.ne,text="$\mathbf{J}_z$").scale(0.5,0.5)

rad = Path(P(0,-0.59),P(0.5,-0.59))
rad.rotate(p=rad.w,angle=20)
radArrow = ArrowHead(tip=rad.e+P(0.01,0.02),dir="e",width=0.06,height=0.06,angle=20)
radThing = Group(rad,radArrow)
radLabel = TeX(sw=rad.c,text="$\mathcal{R}$").scale(0.5,0.5)

fig = Group(circ1,circ2,circ3,
	    zaxis,xaxis,yaxis,
	    xArrow,yArrow,zArrow,
	    xLabel,yLabel,zLabel,
	    radThing,radLabel)

render(fig,file="sphere.eps")
