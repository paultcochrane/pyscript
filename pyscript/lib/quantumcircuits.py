# Quantum Information Theory objects library

from pyscript import *

# Rail
def Rail(w=P(0,0), length=1.0, labelIn=None, labelOut=None, buff=0.05):

    if labelIn is not None and labelOut is not None:
        return Group(
            Path(w+P(0,0),w+P(length,0)),
            TeX(labelIn,e=w-P(buff,0)),
            TeX(labelOut,w=w+P(buff+length,0))
            )
    elif labelIn is not None and labelOut is None:
        return Group(
            Path(w+P(0,0),w+P(length,0)),
            TeX(labelIn,e=w-P(buff,0))
            )
    elif labelIn is None and labelOut is not None:
        return Group(
            Path(w+P(0,0),w+P(length,0)),
            TeX(labelOut,w=w+P(buff+length,0))
            )
    else:
        return Group(
            Path(w+P(0,0),w+P(length,0))
            )
            
# CNOT (controlled not)
def Cnot(c=P(0,0), targetDist=1.0, direction="up"):

    if direction is "up":
        return Group(
            Circle(radius=0.06, bg=Color("black"), c=c),
            Circle(radius=0.2, c=c+P(0,targetDist)),
            Path(c,c+P(0,targetDist+0.2))
            )
    elif direction is "down":
        return Group(
            Circle(radius=0.06, bg=Color("black"), c=c),
            Circle(radius=0.2, c=c+P(0,-targetDist)),
            Path(c,c+P(0,-targetDist-0.2))
            )

# vacuum
def Vacuum():
    return

# Hadamard gate
def HGate(c=P(0,0), side=0.5):
    return Group(
        Box(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'H',c=c)
        )

# Phase gate
def PGate(c=P(0,0), side=0.5):
    return Group(
        Box(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'P',c=c)
        )

# Controlled phase gate
def CPGate(c=P(0,0), controlDist=1.0, direction="up", side=0.5):
    
    if direction is "up":
        return Group(
            Circle(c=c+P(0,controlDist), radius=0.065, bg=Color("black")),
            Path(c+P(0,side/2.),c+P(0,controlDist)),
            Box(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'P',c=c)
            )
    elif direction is "down":
        return Group(
            Circle(c=c-P(0,controlDist), radius=0.65, bg=Color("black")),
            Path(c-P(0,side/2.),c-P(0,controlDist)),
            Box(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'P',c=c)
            )

def Detector(e=P(0,0), height=1.0, label=None):
    if label is not None:
        return Group(Path(e-P(0,height/2.),e+P(0,height/2.)),Arc(c=e, radius=height/2., angle1=-90, angle2=90),label)
    else:
        return Group(Path(e-P(0,height/2.),e+P(0,height/2.)),Arc(c=e, radius=height/2., angle1=-90, angle2=90))

# X gate
def XGate(c=P(0,0), side=0.5):
    return Group(
        Box(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'X',c=c)
        )

# Y gate
def YGate(c=P(0,0), side=0.5):
    return Group(
        Box(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'Y',c=c)
        )

# Z gate
def ZGate(c=P(0,0), side=0.5):
    return Group(
        Box(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'Z',c=c)
        )

# Controlled X gate
def CXGate(c=P(0,0), controlDist=1.0, direction="up", side=0.5):
    
    if direction is "up":
        return Group(
            Circle(c=c+P(0,controlDist), radius=0.065, bg=Color("black")),
            Path(c+P(0,side/2.),c+P(0,controlDist)),
            Box(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'X',c=c)
            )
    elif direction is "down":
        return Group(
            Circle(c=c-P(0,controlDist), radius=0.65, bg=Color("black")),
            Path(c-P(0,side/2.),c-P(0,controlDist)),
            Box(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'X',c=c)
            )

# Controlled Y gate
def CYGate(c=P(0,0), controlDist=1.0, direction="up", side=0.5):
    
    if direction is "up":
        return Group(
            Circle(c=c+P(0,controlDist), radius=0.065, bg=Color("black")),
            Path(c+P(0,side/2.),c+P(0,controlDist)),
            Box(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'Y',c=c)
            )
    elif direction is "down":
        return Group(
            Circle(c=c-P(0,controlDist), radius=0.65, bg=Color("black")),
            Path(c-P(0,side/2.),c-P(0,controlDist)),
            Box(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'Y',c=c)
            )

# Controlled Z gate
def CZGate(c=P(0,0), controlDist=1.0, direction="up", side=0.5):
    
    if direction is "up":
        return Group(
            Circle(c=c+P(0,controlDist), radius=0.065, bg=Color("black")),
            Path(c+P(0,side/2.),c+P(0,controlDist)),
            Box(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'Z',c=c)
            )
    elif direction is "down":
        return Group(
            Circle(c=c-P(0,controlDist), radius=0.65, bg=Color("black")),
            Path(c-P(0,side/2.),c-P(0,controlDist)),
            Box(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'Z',c=c)
            )

