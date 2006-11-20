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

# Michelson-Morely interferometer

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
mirror_n = Mirror(angle=90)
mirror_n.s = bs.n + P(0,3)
beam.append(Path(bs.n, mirror_n.s))

# the "east" mirror
mirror_e = Mirror()
mirror_e.w = bs.e + P(3,0)
beam.append(Path(bs.e, mirror_e.w))

# the detector
det = Detector(angle=90)
det.n = bs.s + P(0,-1)
beam.append(Path(bs.s, det.n))

# make the beam red
beam.apply(fg=Color("red"))

# collect all the objects together
fig = Group(
        laser,
        bs,
        mirror_n, mirror_e,
        det,
        beam,
        )

# render the figure
render(fig, 
        file="michelson-morely.eps")

# vim: expandtab shiftwidth=4:
