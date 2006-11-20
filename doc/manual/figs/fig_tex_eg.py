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

tex=TeX(r'$|\psi_t\rangle=e^{-iHt/\hbar}|\psi_0\rangle$',w=P(.5,0))

g=Group()
for ii in range(0,360,60):
    g.append(tex.copy().rotate(ii,P(0,0)))

render(g,file="fig_tex_eg.eps")

# vim: expandtab shiftwidth=4:
