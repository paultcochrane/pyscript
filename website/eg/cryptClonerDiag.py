#!/usr/bin/env python

# state sniffing in a cryptography scheme with a quantum cloner diagram

import sys
sys.path.append('../../')
sys.path.append('../../pyscript')
sys.path.append('../../pyscript/lib')

from pyscript import *
from optics import *

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

def Line(start=P(0,0), length=1.0, angle=0, dash="[]"):
    """
    A dodgy line object
    """

    xDist = length*cos(angle*pi/180)
    yDist = length*sin(angle*pi/180)
    line = Path(start,start+P(xDist,yDist),dash=dash)

    return line

anchorPoint = P(0.0,0.0)

### input mode
inputTail = anchorPoint
inputHead = anchorPoint+P(2.0,0.0)
inputLine = Path(inputTail,inputHead)
inputArrow = ArrowHead(tip=inputHead,dir="e")
inputText = TeX(sw=inputTail+P(0.2,0.1),text=r"$\hat{a}_\mathrm{in}$")
mainInput = Group(inputLine,inputArrow,inputText)

### first PBS
pbsHeight = 0.7
pbsBox = PBS(c=inputHead+P(0.2+pbsHeight/2.0,0.0),h=pbsHeight,angle=90)
pbs = Group(pbsBox)

### line to input of bottom cloner
pbsCentre = inputHead+P(0.2+pbsHeight/2.0,0.0)
pbsOutTail = pbsCentre-P(0.0,0.2+pbsHeight/2.0)
pbsOutHead = pbsOutTail-P(0.0,2.8-pbsHeight/2.0)
pbsOutLine = Path(pbsOutTail,pbsOutHead)
pbsOutArrow = ArrowHead(tip=pbsOutHead, dir="s")
pbsOutput = Group(pbsOutLine)

### mirror
mirrorPbs = Mirror(c=pbsCentre-P(0.0,3.0),angle=-135)

### the cloners

clonersDiff = 3.0
clonersAnchor = inputHead+P(pbsHeight+0.4,0.0)
### cloner 1

# input mode
inTailPoint = clonersAnchor
inHeadPoint = inTailPoint+P(2.0-pbsHeight/2.0,0)
inMode = Path(inTailPoint,inHeadPoint)
inModeText = TeX(sw=inTailPoint+P(0.2,0.1),text=r"$\hat{a}_\mathrm{in}$")
arrow = ArrowHead(tip=inHeadPoint)
input = Group(inMode,arrow)

# amplifier
ampBox = Rectangle(w=inHeadPoint+P(0.2,0),height=1.0,width=1.0,bg=Color("white"))
ampText = TeX(c=ampBox.c,text=r"\large $G$")
amp = Group(ampBox,ampText)

# vac 1
vac1 = Group()
vac1.append(Line(start=ampBox.c+P(-0.7,0.4),length=1.0,angle=150,dash="[ 3] 0"))
vac1.append(Line(start=ampBox.c+P(0.7,-0.4),length=1.0,angle=-30,dash="[ 3] 0"))
vac1Text = TeX(se=ampBox.c+P(-1.1,0.9),text=r"$\hat{v}_1$")
vac1.append(vac1Text)
tipPoint = ampBox.c+P(0.7+sqrt(3.0)/2.0,-0.8)
vac1Arrow = ArrowHead(tip=tipPoint,dir="e")
vac1Arrow.rotate(30,p=vac1Arrow.bbox().sw)
vac1.append(vac1Arrow)

# output mode from amp
outAmpTail = inHeadPoint+P(1.4,0)
outAmpHead = outAmpTail+P(2.0,0)
outAmpMode = Path(outAmpTail,outAmpHead)
outAmpText = TeX(sw=outAmpTail+P(0.2,0.1),text=r"$\hat{a}_\mathrm{out}$")
outAmpArrow = ArrowHead(tip=outAmpHead)
outAmp = Group(outAmpMode,outAmpText,outAmpArrow)

# beam splitter
bsDist = 0.5*sqrt(1.0/2.0)
beamSplitter = BSLine(c=outAmpHead+P(bsDist/2.0,0), angle=-45)

# vac 2
vac2Head = outAmpHead+P(bsDist/2.0,-0.3)
vac2Tail = vac2Head+P(0,-1.0)
vac2Mode = Path(vac2Tail,vac2Head,dash="[ 3] 0")
vac2Arrow = ArrowHead(tip=vac2Head,dir="n")
vac2Text = TeX(sw=vac2Tail+P(0.2,0),text=r"$\hat{v}_2$")
vac2 = Group(vac2Mode,vac2Text,vac2Arrow)

# b1
b1upTail = outAmpHead+P(bsDist/2.0,0.3)
b1upHead = b1upTail+P(0,1.0)
b1upMode = Path(b1upTail,b1upHead)
b1upArrow = ArrowHead(tip=b1upHead,dir="n")
b1up = Group(b1upMode)

# b2
b2Tail = outAmpHead+P(0.5,0)
b2Head = b2Tail+P(1.7+pbsHeight/2.0,0)
b2DownHead = b2Head-P(0.0,2.8-pbsHeight/2.0)
b2Mode = Path(b2Tail,b2Head,b2DownHead)
b2Text = TeX(sw=b2Tail+P(0.3,0.1),text=r"$\hat{b}_2$")
b2Arrow = ArrowHead(tip=b2DownHead,dir="s")
b2 = Group(b2Mode,b2Arrow,b2Text)

# mirror
mirror = Mirror(c=b1upHead+P(0.0,bsDist/2.0),angle=-45)

# b1 (across bit)
b1Tail = b1upHead
b1Head = b1Tail+P(2.6+pbsHeight+pbsHeight/2.0,0)
b1DownHead = b1Head-P(0.0,5.4-pbsHeight/2.0)
b1Mode = Path(b1Tail,b1Head,b1DownHead)
b1Arrow = ArrowHead(tip=b1DownHead,dir="s")
b1Text = TeX(sw=b1Tail+P(0.2,0.1),text=r"$\hat{b}_1$")
b1 = Group(b1Mode,b1Arrow,b1Text)

# X1plus and minus
X1plus = TeX(sw=b1Head+P(0.1,0.2),text=r"$\hat{X}_1^+$")
X1minus = TeX(nw=b1Head+P(0.1,-0.2),text=r"$\hat{X}_1^-$")
X1 = Group(X1plus,X1minus)

# X2plus and minus
X2plus = TeX(sw=b2Head+P(0.1,0.2),text=r"$\hat{X}_2^+$")
X2minus = TeX(nw=b2Head+P(0.1,-0.2),text=r"$\hat{X}_2^-$")
X2 = Group(X2plus,X2minus)

cloner1 = Group(input,
                amp,
                vac1,
                outAmp,
                beamSplitter,
                vac2,
                b1up,
                b2,
                b1,
                )

### cloner 2

# input mode
inTailPoint = pbsOutHead
inHeadPoint = inTailPoint+P(2.2,0.0)
inMode = Path(inTailPoint,inHeadPoint)
inModeText = TeX(sw=inTailPoint+P(0.2,0.1),text=r"$\hat{a}_\mathrm{in}$")
arrow = ArrowHead(tip=inHeadPoint)
input = Group(inMode,arrow)

# amplifier
ampBox = Rectangle(w=inHeadPoint+P(0.2,0),height=1.0,width=1.0,bg=Color("white"))
ampText = TeX(c=ampBox.c,text=r"\large $G$")
amp = Group(ampBox,ampText)

# vac 1
vac1 = Group()
vac1.append(Line(start=ampBox.c+P(-0.7,0.4),length=1.0,angle=150,dash="[ 3] 0"))
vac1.append(Line(start=ampBox.c+P(0.7,-0.4),length=1.0,angle=-30,dash="[ 3] 0"))
vac1Text = TeX(se=ampBox.c+P(-1.1,0.9),text=r"$\hat{v}_1$")
vac1.append(vac1Text)
tipPoint = ampBox.c+P(0.7+sqrt(3.0)/2.0,-0.8)
vac1Arrow = ArrowHead(tip=tipPoint,dir="e")
vac1Arrow.rotate(30,p=vac1Arrow.bbox().sw)
vac1.append(vac1Arrow)

# output mode from amp
outAmpTail = inHeadPoint+P(1.4,0)
outAmpHead = outAmpTail+P(2.0,0)
outAmpMode = Path(outAmpTail,outAmpHead)
outAmpText = TeX(sw=outAmpTail+P(0.2,0.1),text=r"$\hat{a}_\mathrm{out}$")
outAmpArrow = ArrowHead(tip=outAmpHead)
outAmp = Group(outAmpMode,outAmpText,outAmpArrow)

# beam splitter
bsDist = 0.5*sqrt(1.0/2.0)
beamSplitter = BSLine(c=outAmpHead+P(bsDist/2.0,0.0), angle=45)

# vac 2
vac2Head = outAmpHead+P(bsDist/2.0,0.3)
vac2Tail = vac2Head+P(0,1.0)
vac2Mode = Path(vac2Tail,vac2Head,dash="[ 3] 0")
vac2Arrow = ArrowHead(tip=vac2Head,dir="s")
vac2Text = TeX(nw=vac2Tail+P(0.2,0),text=r"$\hat{v}_2$")
vac2 = Group(vac2Mode,vac2Text,vac2Arrow)

# b1
b1upTail = outAmpHead+P(bsDist/2.0,-0.3)
b1upHead = b1upTail+P(0,-1.0)
b1upMode = Path(b1upTail,b1upHead)
b1upArrow = ArrowHead(tip=b1upHead,dir="s")
b1up = Group(b1upMode)

# b2
b2Tail = outAmpHead+P(0.5,0)
b2Head = b2Tail+P(1.5,0)
b2Mode = Path(b2Tail,b2Head)
b2Text = TeX(sw=b2Tail+P(0.2,0.1),text=r"$\hat{b}_2$")
b2Arrow = ArrowHead(tip=b2Head)
b2 = Group(b2Mode,b2Arrow,b2Text)

# mirror
mirror = Mirror(c=b1upHead-P(0.0,bsDist/2.0),angle=-135)

# b1 (across bit)
b1Tail = b1upHead
b1Head = b1Tail+P(2.4+pbsHeight,0)
b1Mode = Path(b1Tail,b1Head)
b1Arrow = ArrowHead(tip=b1Head,dir="e")
b1Text = TeX(sw=b1Tail+P(0.2,0.1),text=r"$\hat{b}_1$")
b1 = Group(b1Mode,b1Arrow,b1Text)

# X1plus and minus
X1plus = TeX(sw=b1Head+P(0.1,0.2),text=r"$\hat{X}_1^+$")
X1minus = TeX(nw=b1Head+P(0.1,-0.2),text=r"$\hat{X}_1^-$")
X1 = Group(X1plus,X1minus)

# X2plus and minus
X2plus = TeX(sw=b2Head+P(0.1,0.2),text=r"$\hat{X}_2^+$")
X2minus = TeX(nw=b2Head+P(0.1,-0.2),text=r"$\hat{X}_2^-$")
X2 = Group(X2plus,X2minus)


cloner2 = Group(input,
                amp,
                vac1,
                outAmp,
                beamSplitter,
                vac2,
                b1up,
                b2,
                b1
                )

rightExtent = b2Head+P(2.4+pbsHeight,0.0)
### top output pbs

pbsBox = PBS(c=b2Head+P(0.2+pbsHeight/2.0,0.0),h=pbsHeight,angle=90)
pbsLineTail = b2Head+P(0.4+pbsHeight,0.0)
pbsLineHead = rightExtent
pbsArrow = ArrowHead(tip=pbsLineHead, dir="e")
pbsLine = Path(pbsLineTail,pbsLineHead)
pbsOutTop = Group(pbsBox,pbsLine,pbsArrow)

### bottom output pbs

pbsBox = PBS(c=b1Head+P(0.2+pbsHeight/2.0,0.0),h=pbsHeight,angle=90)
pbsLineTail = b1Head+P(0.4+pbsHeight,0.0)
pbsLineHead = rightExtent-P(0.0,1.3)
pbsArrow = ArrowHead(tip=pbsLineHead, dir="e")
pbsLine = Path(pbsLineTail,pbsLineHead)
pbsOutBot = Group(pbsBox,pbsLine,pbsArrow)

### put a "hop" on the downward big b1 mode line
hopBoxHeight = 0.3
hopBox = Rectangle(c=b1Head+P(0.2+pbsHeight/2.0,1.3), height=hopBoxHeight, width=hopBoxHeight, bg=Color("white"), fg=Color("white"))
hopCurve = Path(hopBox.n,
               C(hopBox.n,hopBox.e), #hopBox.se,hopBox.s),
               hopBox.s)
hop = Group(hopBox,hopCurve)

### background shading
backBoxTop = Rectangle(w=inputHead+P(0.8+pbsHeight,0.0),
                       width=6.1, height=2.8,
                       fg=Color(0,0,0,0.2), bg=Color(0,0,0,0.2))

backBoxBot = Rectangle(w=inputHead+P(0.8+pbsHeight,-clonersDiff),
                       width=6.1, height=2.8,
                       fg=Color(0,0,0,0.2), bg=Color(0,0,0,0.2))

# draw it!
render(backBoxTop,
       backBoxBot,
       mainInput,
       pbs,
       pbsOutput,
       cloner1,
       cloner2,
       pbsOutTop,
       pbsOutBot,
       hop,
       file="cryptClonerDiag.eps")

