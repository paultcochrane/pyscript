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

    """
    # need to implement the angle
    beamSplitter = Path(sw, sw+P(0,h), sw+P(h,h), sw+P(h,0), sw, sw+P(h,h),
             fg=Color("black"), bg=Color("white"))
    if label is not None:
        label['w'] = sw+P(h,0)+P(-h/4,h/2)
        return Group(beamSplitter, label)
    else:
        return Group(beamSplitter)

# line beam splitter
def BSLine(sw=P(0,0), label=None, w=1.0, h=0.1, angle=0):
    """

    """
    # need to implement the angle
    beamSplitter = Path(sw, sw+P(0,h), sw+P(w,h), sw+P(w,0), sw,
             fg=Color("black"), bg=Color("black"))
    if label is not None:
        label['w'] = sw+P(h,0)+P(-h/4,h/2)
        return Group(beamSplitter, label)
    else:
        return Group(beamSplitter)

# phase shifter
def PhaseShifter(sw=P(0,0), label=None, w=0.5, h=0.7, angle=0):
    """

    """
    # need to implement the angle
    # call PhaseShift??
    phaseShifter = Path(sw, sw+P(w/2,h), sw+P(w,0), sw,
                        fg=Color("white"), bg=Color("white"))
    if label is not None:
        label['s'] = sw+P(w/2,-h)
        return Group(phaseShifter, label)
    else:
        return Group(phaseShifter)


