# Copyright (C) 2002-2005  Alexei Gilchrist and Paul Cochrane
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

'''
Quantum circuits objects library
'''

from pyscript import *

class Boxed(Group,Area):
    '''
    Draws a box around an object,
    the box can be placed acording to standard Area tags
    '''
        
    def __init__(self,obj,**dict):
        
        bbox=obj.bbox()

        pad=.1
        w=bbox.width+2*pad
        h=bbox.height+2*pad

        self.width=w
        self.height=h
        self.bg=dict.get('bg',Color(1))
        if dict.has_key('bg'):
            del dict['bg']

        apply(Group.__init__, (self,), dict)
        apply(Area.__init__, (self,), dict)

        obj.c=P(w/2.,h/2.)

        self.append(
            Rectangle(width=w,height=h,bg=self.bg),
            obj,
            )

class Circled(Group,Area):
        
    def __init__(self,obj,**dict):
        
        bbox=obj.bbox()

        pad=.1
        r=max( bbox.width+2*pad , bbox.height+2*pad )/2.0

        self.width=2*r
        self.height=2*r

        
        self.bg=dict.get('bg',Color(1))
        if dict.has_key('bg'):
            del dict['bg']

        apply(Group.__init__, (self,), dict)
        apply(Area.__init__, (self,), dict)

        obj.c=P(r,r)

        self.append(
            Circle(r=r,bg=self.bg,c=P(r,r)),
            obj,
            )


def cbox(obj,x,yt,yc):
    '''
    @return: a controlled box
    @param obj: the object to put a box around
    @param x: x position of line and center of box
    @param yt: y position of target
    @param yc: y position of control
    '''
    g=Group(
        Path(P(x,yt),P(x,yc)),
        Boxed(obj,c=P(x,yt),bg=Color(1)),
        Dot(P(x,yc)),
        )
    return g

def detector(**dict):
    '''
    @return: a D shaped detector
    '''
    r=0.3
    c=0.65*r
    path=[P(0,-r),P(0,r),C(P(c,r),P(r,c)),P(r,0),C(P(r,-c),P(c,-r)),P(0,-r)]
    dict['bg']=dict.get('bg',Color(.8))
    dict['closed']=1
    p=apply(Path,path,dict)
    a=Area(width=r,height=2*r,e=P(0,0))
    
    return Group(a,p)
    
def classicalpath(*paths):
    '''
    @return: classical path
    @param paths: 1 or more Path() objects
    '''
    g=Group()

    for path in paths:
        g.append(path.copy(linewidth=2,fg=Color(0)))

    # reuse these paths
    for path in paths:
        g.append(path(linewidth=1,fg=Color(1)))

    return g

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
            Circle(r=0.06, bg=Color("black"), c=c),
            Circle(r=0.2, c=c+P(0,targetDist)),
            Path(c,c+P(0,targetDist+0.2))
            )
    elif direction is "down":
        return Group(
            Circle(r=0.06, bg=Color("black"), c=c),
            Circle(r=0.2, c=c+P(0,-targetDist)),
            Path(c,c+P(0,-targetDist-0.2))
            )

# Hadamard gate
def HGate(c=P(0,0), side=0.5):
    return Group(
        Rectangle(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'H',c=c)
        )

# Phase gate
def PGate(c=P(0,0), side=0.5):
    return Group(
        Rectangle(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'P',c=c)
        )

# Controlled phase gate
def CPGate(c=P(0,0), controlDist=1.0, direction="up", side=0.5):
    
    if direction is "up":
        return Group(
            Circle(c=c+P(0,controlDist), r=0.065, bg=Color("black")),
            Path(c+P(0,side/2.),c+P(0,controlDist)),
            Rectangle(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'P',c=c)
            )
    elif direction is "down":
        return Group(
            Circle(c=c-P(0,controlDist), r=0.65, bg=Color("black")),
            Path(c-P(0,side/2.),c-P(0,controlDist)),
            Rectangle(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'P',c=c)
            )

def Detector(e=P(0,0), height=1.0, label=None):
    if label is not None:
        return Group(Path(e-P(0,height/2.),e+P(0,height/2.)),
		Circle(c=e, r=height/2., start=0, end=180),label)
    else:
        return Group(Path(e-P(0,height/2.),e+P(0,height/2.)),
		Circle(c=e, r=height/2., start=0, end=180))

# X gate
def XGate(c=P(0,0), side=0.5):
    return Group(
        Rectangle(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'X',c=c)
        )

# Y gate
def YGate(c=P(0,0), side=0.5):
    return Group(
        Rectangle(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'Y',c=c)
        )

# Z gate
def ZGate(c=P(0,0), side=0.5):
    return Group(
        Rectangle(width=side, height=side, c=c, bg=Color("white")),
        TeX(r'Z',c=c)
        )

# Controlled X gate
def CXGate(c=P(0,0), controlDist=1.0, direction="up", side=0.5):
    
    if direction is "up":
        return Group(
            Circle(c=c+P(0,controlDist), r=0.065, bg=Color("black")),
            Path(c+P(0,side/2.),c+P(0,controlDist)),
            Rectangle(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'X',c=c)
            )
    elif direction is "down":
        return Group(
            Circle(c=c-P(0,controlDist), r=0.65, bg=Color("black")),
            Path(c-P(0,side/2.),c-P(0,controlDist)),
            Rectangle(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'X',c=c)
            )

# Controlled Y gate
def CYGate(c=P(0,0), controlDist=1.0, direction="up", side=0.5):
    
    if direction is "up":
        return Group(
            Circle(c=c+P(0,controlDist), r=0.065, bg=Color("black")),
            Path(c+P(0,side/2.),c+P(0,controlDist)),
            Rectangle(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'Y',c=c)
            )
    elif direction is "down":
        return Group(
            Circle(c=c-P(0,controlDist), r=0.65, bg=Color("black")),
            Path(c-P(0,side/2.),c-P(0,controlDist)),
            Rectangle(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'Y',c=c)
            )

# Controlled Z gate
def CZGate(c=P(0,0), controlDist=1.0, direction="up", side=0.5):
    
    if direction is "up":
        return Group(
            Circle(c=c+P(0,controlDist), r=0.065, bg=Color("black")),
            Path(c+P(0,side/2.),c+P(0,controlDist)),
            Rectangle(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'Z',c=c)
            )
    elif direction is "down":
        return Group(
            Circle(c=c-P(0,controlDist), r=0.65, bg=Color("black")),
            Path(c-P(0,side/2.),c-P(0,controlDist)),
            Rectangle(width=side, height=side, c=c, bg=Color("white")),
            TeX(r'Z',c=c)
            )

# vim: expandtab shiftwidth=4:

