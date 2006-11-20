#!/usr/bin/env pyscript

# $Id: /pyscript/local/trunk/doc/manual/optics/make_objects.py 4334 2006-03-01T16:23:44.000000Z paultcochrane  $

from pyscript import *
from pyscript.lib.optics import *

# line beam splitter
obj = BS()
render(obj, file="BS.eps")

# vim: expandtab shiftwidth=4:
