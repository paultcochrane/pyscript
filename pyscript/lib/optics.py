# Copyright (C) 2002  Alexei Gilchrist and Paul Cochrane
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
pyscript Optics objects library
'''

from pyscript import *
# beam splitter
def BS(sw=P(0,0),label=None,h=1.0):
    """

    """
    buff=P(0,0.1)
    b=Path(sw-buff,sw+P(0,h)+buff,sw+P(h,h)+buff,
           sw+P(h,0)-buff,sw-buff,fg=None,bg=Color("white"))
    p1=Path(sw,sw+P(h,h))
    p2=Path(sw+P(0,h),sw+P(h,0))
    p3=Path(sw+P(h/4,h/2),sw+P(h,0)+P(-h/4,h/2),linewidth=1)
    if label is not None:
        label['w']=sw+P(h,0)+P(-h/4,h/2)
        return Group(b,p1,p2,p3,label)
    else:
        return Group(b,p1,p2,p3)

# box beam splitter (aka polarising beam splitter)
def BSBox(sw=P(0,0), label=None, h=1.0, angle=0):
    """
    Beam splitter as a box as opposed to a line
    """
    beamSplitter = Path(sw, sw+P(0,h), sw+P(h,h), sw+P(h,0), sw, sw+P(h,h),
             fg=Color("black"), bg=Color("white"))
    beamSplitter.rotate(angle,p=sw+P(h/2.0,h/2.0))
    if label is not None:
        label.w = sw+P(h,0)+P(-h/4,h/2)
        return Group(beamSplitter, label)
    else:
        return Group(beamSplitter)

# polarising beam splitter
def PBS(c=P(0,0), h=1.0, angle=0):
    """
    Polarising beam splitter (box)
    """
    sw=c-P(h/2.0,h/2.0)
    beamSplitter = Path(sw, sw+P(0,h), sw+P(h,h), sw+P(h,0), sw, sw+P(h,h),
             fg=Color("black"), bg=Color("white"))
    beamSplitter.rotate(angle,p=sw+P(h/2.0,h/2.0))
    return Group(beamSplitter)


# line beam splitter
def BSLine(c=P(0,0), label=None, w=1.0, h=0.1, angle=0, anchor=None):
    """
    Line beam splitter
    """
    sw = c-P(w/2.0,h/2.0)
    beamSplitter = Path(sw, sw+P(0,h), sw+P(w,h), sw+P(w,0), sw,
             fg=Color("black"), bg=Color("black"))
    beamSplitter.rotate(angle,p=c)
    if label is not None:
        label.w = sw+P(h,0)+P(-h/4,h/2)
        return Group(beamSplitter, label)
    else:
        return Group(beamSplitter)

# phase shifter
def PhaseShifter(sw=P(0,0), label=None, w=0.5, h=0.7, angle=0):
    """
    Phase shifter
    """
    # need to implement the angle
    # call PhaseShift??
    phaseShifter = Path(sw, sw+P(w/2,h), sw+P(w,0), sw)
    phaseShifter.rotate(angle,p=phaseShifter.c)
    if label is not None:
        label.s = sw+P(w/2,-h)
        return Group(phaseShifter, label)
    else:
        return Group(phaseShifter)


# mirror
def Mirror(c=P(0,0), label=None, length=1.0, thickness=0.1, angle=0, anchor=None):
    """
    Mirror
    """
    
    # different kinds of mirrors??
    sw = c-P(length/2.0,thickness/2.0)
    mirror = Group()
    mirror.append(Path(sw, sw+P(0,thickness),
                  sw+P(length,thickness), sw+P(length,0), sw,
                  fg=Color("black"), bg=Color("black")))
    flickLen = 0.15
    flicks = Group()
    for i in range(10):
        flicks.append(Path(sw+P((i+1.0)*length/10.0,thickness),
                           sw+P(i*length/10.0,thickness+flickLen)))

    mirror.append(flicks)
    mirror.rotate(angle, p=c)
    if label is not None:
        label.w = sw+P(thickness,0)+P(-thickness/4,thickness/2)
        return mirror.append(label)
    else:
        return mirror

