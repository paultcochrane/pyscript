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

from pyscript import *

p0=P(2,1)
p1=P(4,2)
c1=R(4,2)
c2=R(-4,-2)/2.
#c2=R(-1,-.5)
p2=P(4,4)
p3=P(6,5)

path=Path(p0,p1,C(c1,c2),p2,p3,fg=Color('red'),linewidth=.8)

g=Group()
delta=1/20.
for p in range(21):
    g.append(Dot(path.P(p*delta)))

render(
    path,
    g,
    file="fig_path_eg.eps"
    )

# vim: expandtab shiftwidth=4:
