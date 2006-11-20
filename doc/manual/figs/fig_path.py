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

p0=P(2,1)
p1=P(4,2)
c1=R(4,2)
c2=R(-4,-2)/2.
p2=P(4,4)
p3=P(6,5)

path=Path(p0,p1,C(c1,c2),p2,p3,fg=Color('red'),linewidth=.8)

d=R(0,.1)
g=Group()
for p in [p0,p1,p2,p3,p1+c1,p2+c2]:
    g.append(Dot(p))

render(
    path,
    Path(p1,p1+c1,dash="[3] 0 "),
    Path(p2,p2+c2,dash="[3] 0 "),
    g,
    Text("p0",n=p0-d),
    Text("p1",n=p1-d),
    Text("c1",n=p1+c1-d),
    Text("p2",s=p2+d),
    Text("p3",s=p3+d),
    Text("c2",s=p2+c2+d),
    file="fig_path.eps"
    )

# vim: expandtab shiftwidth=4:
