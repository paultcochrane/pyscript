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

"""
A class to hold default settings
"""

from base import UNITS,Color

class defaults:

    tex_head=r"""\documentclass{article}
    \pagestyle{empty}
    \begin{document}
    """
    tex_tail=r"\end{document}"
    tex_command="latex -interaction=batchmode %s"

    dvips_options="-Ppdf"
  
    units=UNITS['cm']

    linewidth=0.5
    linecap=1  #0=butt, 1=round, 2=square
    linejoin=0 #0=miter, 1=round, 2=bevel

    # miterlimit:
    # 1.414 cuts off miters at angles less than 90 degrees.
    # 2.0 cuts off miters at angles less than 60 degrees.
    # 10.0 cuts off miters at angles less than 11 degrees.
    # 1.0 cuts off miters at all angles, so that bevels are always produced
    miterlimit=10  

    # [ ] 0 setdash % Solid, unbroken lines
    # [ 3] 0 setdash % 3 units on, 3 units off,
    # [ 2] 1 setdash % 1 on, 2 off, 2 on, 2 off,
    # [ 2 1] 0 setdash % 2 on, 1 off, 2 on, 1 off,
    # [ 3 5] 6 setdash % 2 off, 3 on, 5 off, 3 on, 5 off,
    # [ 2 3 ] 11 setdash % 1 on, 3 off, 2 on, 3 off, 2 on
    dash="[ ] 0"

    # a 'color' of None is transparent 
    #fg=Color(0)
    #bg=None

