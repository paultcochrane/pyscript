#!/usr/bin/env pyscript

# Copyright (C) 2002-2006  Alexei Gilchrist and Paul Cochrane
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

# Sagnac interferometer

# import the pyscript objects
from pyscript import *
# import the optics library
from pyscript.lib.optics import *

# set up some handy defaults
defaults.units=UNITS['cm']

# initialise a laser beam
beam = Group()

# the laser
laser = Laser(c=P(0,0))

# the beam splitter
bs = BSBox(height=0.7)
bs.w = laser.e + P(1,0)
beam.append(Path(laser.e, bs.w))

# the "north" mirror
mirror_n = Mirror(angle=45)
mirror_n.s = bs.n + P(0,2)
beam.append(Path(bs.n, mirror_n.c))

# the "east" mirror
mirror_e = Mirror(angle=45)
mirror_e.w = bs.e + P(3,0)
beam.append(Path(bs.e, mirror_e.c))

# the "north-east" mirror
mirror_ne = Mirror(angle=135)
mirror_ne.c = P(mirror_e.c.x, mirror_n.c.y)
beam.append(Path(mirror_n.c, mirror_ne.c))
beam.append(Path(mirror_e.c, mirror_ne.c))

# the detector
det = Detector(angle=90)
det.n = bs.s + P(0,-1)
beam.append(Path(bs.s, det.n))

# set the colour of the beam
beam.apply(fg=Color("red"))

# collect all the objects together
fig = Group(
        beam,
        laser,
        bs,
        mirror_n, mirror_e, mirror_ne,
        det,
        )

# render the figure
render(fig, 
        file="sagnac.eps")

# vim: expandtab shiftwidth=4:
