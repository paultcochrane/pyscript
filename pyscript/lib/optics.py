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

# $Id$

__revision__ = '$Revision$'

'''
pyscript Optics objects library
'''

from pyscript import *
import types

# beam splitter
def BS(sw=P(0,0),label=None,h=1.0):
    """
    Beam splitter; displayed as a line
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
class BSBox(Group):
    """
    Beam splitter as a box as opposed to a line

    @param label: 
    @param height:
    @param angle:
    @param fg:
    @param bg:
    """

    label = None
    height = 1.0
    angle = 0.0  # not going to be used much (maybe for a Ralph-splitter ;-))
    fg = Color(0)
    bg = Color(1)

    def __init__(self, **options):
        # inherit from the base class
        Group.__init__(self, **options)

        # process the options if any
        self.fg = options.get("fg", self.fg)
        self.bg = options.get("bg", self.bg)
        self.height = options.get("height", self.height)
        self.angle = options.get("angle", self.angle)
        self.label = options.get("label", self.label)

        # make the beam splitter
        bs = Group()
        bs.append(Path(P(0,0),
                  P(0,self.height),
                  P(self.height,self.height),
                  P(self.height,0),
                  P(0,0),
                  P(self.height, self.height),
                  fg=self.fg, bg=self.bg)
                  )

        # rotate if necessary
        bs.rotate(self.angle, p=bs.bbox().c)

        # put a label on if required
        if self.label is not None:
            # if the label is just a string, wrap it in a Text object
            if type(self.label) is types.StringType:
                self.label = Text(self.label)

            # test to see if the label isn't a Text or a TeX object
            if not isinstance(self.label, TeX) and \
                    not isinstance(self.label, Text):
                raise ValueError, \
                        "label is not a string or Text or TeX object"

            self.label.w = P(3.0*self.height/4.0,self.height/2.0)
            bs.append(self.label)

        self.append(bs)

# polarising beam splitter
PBS = BSBox

#def PBS(c=P(0,0), h=1.0, angle=0):
    #"""
    #Polarising beam splitter (box)
    #"""
    #sw=c-P(h/2.0,h/2.0)
    #beamSplitter = Path(sw, sw+P(0,h), sw+P(h,h), sw+P(h,0), sw, sw+P(h,h),
             #fg=Color("black"), bg=Color("white"))
    #beamSplitter.rotate(angle,p=sw+P(h/2.0,h/2.0))
    #return Group(beamSplitter)

# line beam splitter
def BSLine(c=P(0,0), label=None, w=1.0, h=0.1, angle=0, anchor=None, fg=Color(0), bg=Color(0)):
    """
    Line beam splitter
    """
    sw = c-P(w/2.0,h/2.0)
    beamSplitter = Path(sw, sw+P(0,h), sw+P(w,h), sw+P(w,0), sw,
             fg=fg, bg=bg)
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
class Mirror(Group):
    """
    Mirror
    """

    label = None
    length = 1.0
    thickness = 0.1
    angle = 0.0
    fg = Color(0)
    bg = Color(0)
    flicks = False

    def __init__(self, **options):
        # inherit from the base class
        Group.__init__(self, **options)

        # process the options if any
        self.fg = options.get("fg", self.fg)
        self.bg = options.get("bg", self.bg)
        self.length = options.get("length", self.length)
        self.thickness = options.get("thickness", self.thickness)
        self.angle = options.get("angle", self.thickness)
        self.label = options.get("label", self.label)
        self.flicks = options.get("flicks", self.flicks)

        # make the mirror itself
        mirror = Group()
        mirror.append(
                      Path(P(0,0), 
                      P(0,self.thickness),
                      P(self.length,self.thickness), 
                      P(self.length,0), 
                      fg=self.fg, bg=self.bg, closed=1)
                      )

        if self.flicks:
            # make the flicks on the back of the mirror
            flickLen = 0.15
            flicksObj = Group()
            for i in range(10):
                flicksObj.append(
                        Path(P((i+1.0)*self.length/10.0, self.thickness),
                             P(i*self.length/10.0, self.thickness+flickLen),
                             fg=self.fg, bg=self.bg))

            mirror.append(flicksObj)

        # rotate the mirror if necessary
        mirror.rotate(self.angle, p=mirror.bbox().c)

        # make the mirror the current object
        self.append(mirror)

        # put a label on if required
        if self.label is not None:
            # if the label is just a string, wrap it in a Text object
            if type(self.label) is types.StringType:
                self.label = Text(self.label)

            # test to see if the label isn't a Text or a TeX object
            if not isinstance(self.label, TeX) and \
                    not isinstance(self.label, Text):
                raise ValueError, \
                        "label is not a string or Text or TeX object"

            self.label.c = self.bbox().c
            self.append(self.label)

# detector
class Detector(Group):
    """
    A D-shaped detector
    """

    height = 0.8
    width = height/2.0
    bg = Color(1)
    fg = Color(0)
    pad = 0.1
    angle = 0.0
    label = None

    def __init__(self, **options):
        Group.__init__(self, **options)
        p = Group()

        self.fg = options.get("fg", self.fg)
        self.bg = options.get("bg", self.bg)
        if self.width > self.height:
            p.append(Path(
                P(0, 0), P(0, self.height),
                P(self.width-self.height/2.0, self.height), C(90, 0),
                P(self.width, self.height/2.0), C(180, 90),
                P(self.width-self.height/2.0, 0),
                fg=self.fg, bg=self.bg,
                closed=1)
                )
        else:
            p.append(Path(
                P(0, 0), P(0, self.height),  C(90, 0),
                P(self.width, self.height/2.0), C(180, 90),
                closed=1)
                )

        # rotate if necessary
        self.angle = options.get("angle", self.angle)
        p.rotate(self.angle, p=p.bbox().c)

        # put a label on if required
        self.label = options.get("label", self.label)
        if self.label is not None:
            # if the label is just a string, wrap it in a Text object
            if type(self.label) is types.StringType:
                self.label = Text(self.label)

            # test to see if the label isn't a Text or a TeX object
            if not isinstance(self.label, TeX) and \
                    not isinstance(self.label, Text):
                raise ValueError, \
                        "label is not a string or Text or TeX object"

            # the location given here not tested!!!
            self.label.w = P(3.0*self.height/4.0,self.height/2.0)
            p.append(self.label)

        self.append(p)

# laser (this is just a container, in case we want to make this fancier later)
class Laser(Group):
    """
    Laser
    """

    label = None
    height = 1.0
    width = 3.0
    angle = 0.0
    fg = Color(0)
    bg = Color(1)

    def __init__(self, **options):
        # inherit from the base class
        Group.__init__(self, **options)

        # process the options if any
        self.fg = options.get("fg", self.fg)
        self.bg = options.get("bg", self.bg)
        self.height = options.get("height", self.height)
        self.width = options.get("width", self.width)
        self.angle = options.get("angle", self.angle)
        self.label = options.get("label", self.label)

        # make the laser
        laser = Group()
        laser.append(Path(P(0,0),
                  P(0,self.height),
                  P(self.width,self.height),
                  P(self.width,0),
                  closed=1,
                  fg=self.fg, bg=self.bg)
                  )

        # rotate if necessary
        laser.rotate(self.angle, p=laser.bbox().c)

        # put a label on if required
        if self.label is not None:
            # if the label is just a string, wrap it in a Text object
            if type(self.label) is types.StringType:
                self.label = Text(self.label)

            # test to see if the label isn't a Text or a TeX object
            if not isinstance(self.label, TeX) and \
                    not isinstance(self.label, Text):
                raise ValueError, \
                        "label is not a string or Text or TeX object"

            # put the label in an appropriate location
            self.label.c = laser.bbox().c
            laser.append(self.label)

        self.append(laser)

# modulator 
# (this is just a container, in case we want to make this fancier later)
class Modulator(Group):
    """
    Modulator (EOM, AOM etc.)
    """

    label = None
    height = 1.0
    width = 0.5 
    angle = 0.0
    fg = Color(0)
    bg = Color(1)

    def __init__(self, **options):
        # inherit from the base class
        Group.__init__(self, **options)

        # process the options if any
        self.fg = options.get("fg", self.fg)
        self.bg = options.get("bg", self.bg)
        self.height = options.get("height", self.height)
        self.width = options.get("width", self.width)
        self.angle = options.get("angle", self.angle)
        self.label = options.get("label", self.label)

        # make the laser
        modulator = Group()
        modulator.append(Path(P(0,0),
                  P(0,self.height),
                  P(self.width,self.height),
                  P(self.width,0),
                  closed=1,
                  fg=self.fg, bg=self.bg)
                  )

        # rotate if necessary
        modulator.rotate(self.angle, p=modulator.bbox().c)

        # put a label on if required
        if self.label is not None:
            # if the label is just a string, wrap it in a Text object
            if type(self.label) is types.StringType:
                self.label = Text(self.label)

            # test to see if the label isn't a Text or a TeX object
            if not isinstance(self.label, TeX) and \
                    not isinstance(self.label, Text):
                raise ValueError, \
                        "label is not a string or Text or TeX object"

            # put in appropriate location
            self.label.c = modulator.bbox().c
            modulator.append(self.label)

        self.append(modulator)

# free space 
class FreeSpace(Group):
    """
    A patch of free space (for example, in an interferometer)
    """

    label = None
    height = 1.0
    width = 3.0
    angle = 0.0
    fg = Color(0)
    bg = Color(1)

    def __init__(self, **options):
        # inherit from the base class
        Group.__init__(self, **options)

        # process the options if any
        self.fg = options.get("fg", self.fg)
        self.bg = options.get("bg", self.bg)
        self.height = options.get("height", self.height)
        self.width = options.get("width", self.width)
        self.angle = options.get("angle", self.angle)
        self.label = options.get("label", self.label)

        # make the laser
        fs = Group()
        fs.append(Path(P(0,0),
                  P(0,self.height),
                  P(self.width,self.height),
                  P(self.width,0),
                  closed=1,
                  fg=self.fg, bg=self.bg,
                  dash=Dash())
                  )

        # rotate if necessary
        fs.rotate(self.angle, p=fs.bbox().c)

        # put a label on if required
        if self.label is not None:
            # if the label is just a string, wrap it in a Text object
            if type(self.label) is types.StringType:
                self.label = Text(self.label)

            # test to see if the label isn't a Text or a TeX object
            if not isinstance(self.label, TeX) and \
                    not isinstance(self.label, Text):
                raise ValueError, \
                        "label is not a string or Text or TeX object"

            # put the label in appropriate location
            self.label.c = fs.bbox().c
            fs.append(self.label)

        self.append(fs)

# vim: expandtab shiftwidth=4:
