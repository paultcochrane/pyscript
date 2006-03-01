#!/usr/bin/env pyscript

# $Id$

from pyscript import *
from pyscript.lib.optics import *

import os

# line beam splitter
obj = BS()
render(obj, file="BS.eps")

# BSBox object
obj = BSBox()
render(obj, file="BSBox.eps")

# PBS object
obj = PBS()
render(obj, file="PBS.eps")

# BSLine object
obj = BSLine()
render(obj, file="BSLine.eps")

# PhaseShifter object
obj = PhaseShifter()
render(obj, file="PhaseShifter.eps")

# Mirror object
obj = Mirror()
render(obj, file="Mirror.eps")

# Detector object
obj = Detector()
render(obj, file="Detector.eps")

# Laser object
obj = Laser()
render(obj, file="Laser.eps")

# Modulator object
obj = Modulator()
render(obj, file="Modulator.eps")

# FreeSpace object
obj = FreeSpace()
render(obj, file="FreeSpace.eps")

# Lens object
obj = Lens()
render(obj, file="Lens.eps")

# LambdaPlate object
obj = LambdaPlate()
render(obj, file="LambdaPlate.eps")

# vim: expandtab shiftwidth=4:
