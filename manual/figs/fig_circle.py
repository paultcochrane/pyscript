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

from pyscript import *

# define our own dot
def dot(c):
    return Circle(r=.1,bg=Color('red'),c=c)

def s(angle):
    return U(angle)*.2

acol=Color('blue')
axis=Group(
    Path(P(-1,0),P(4,0),fg=acol),
    Path(P(0,-1),P(0,4),fg=acol),
    Text('(0,0)',ne=s(-135),fg=acol)
    )

# -----------------------------------------------------

r=Circle(r=3,linewidth=2)

dots=Group()
for ii in ['n','ne','e','se','s','sw','w','nw','c']:
    p=getattr(r,ii)
    dots.append(dot(p))
    dots.append(Text(str(ii),c=p-p/8.))

rad=Arrow(P(0,0),P(0,3)).rotate(60)
radt=Text('r')
    
render(
    axis,
    r,
    dots,
    rad,
    radt.rotate(-30)(s=rad.P(.5)+U(-30,.2)),
    file="fig_circle.eps",
    )

# vim: expandtab shiftwidth=4:
