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

"""
Pyscript test utility functions
"""

__revision__ = "$Revision$"

from pyscript import *
import os

def test_run(obj, lib):
    """
    Render the given object of the given library in pyscript and view 
    with ghostview

    @param obj: the object to render
    @type obj: pyscript object

    @param lib: the library that the object belongs to
    @type lib: string
    """

    render(obj, file="test_%s_%s.eps" % (lib, obj.__class__.__name__))
    os.system("gv -scale 10 test_%s_%s.eps" % (lib, obj.__class__.__name__))
    return

# vim: expandtab shiftwidth=4:
