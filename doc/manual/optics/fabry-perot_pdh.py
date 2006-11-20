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

# a Fabry-Perot cavity in a Pound-Drever-Hall setup

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

# the EOM
eom = Modulator()
eom.w = laser.e + P(1,0)
beam.append(Path(laser.e, eom.w))

# the "west" mirror
mirror_w = Mirror()
mirror_w.w = eom.e + P(1,0)
beam.append(Path(eom.e, mirror_w.w))

# some free space
fs = FreeSpace()
fs.w = mirror_w.e + P(1,0)
beam.append(Path(mirror_w.e, fs.w))

# the "east" mirror
mirror_e = Mirror()
mirror_e.w = fs.e + P(1,0)
beam.append(Path(fs.e, mirror_e.w))

# set the colour of the beam
beam.apply(fg=Color("red"))

# collect all the objects together
fig = Group(
        beam,
        laser,
        eom,
        mirror_e, mirror_w,
        fs,
        )

# render the figure
render(fig, 
        file="fabry-perot_pdh.eps")

# vim: expandtab shiftwidth=4:
