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

r=Rectangle(width=2,height=2)
g=Group()

for a in [0,20,40]:
    p=P(a/7.,0)
    r2=r.copy(c=p).rotate(a,p)
    g.append(r2,Dot(r2.bbox().nw))

render(
    g,
    file="fig_position_eg2.eps",
    )

# vim: expandtab shiftwidth=4:
