#!/usr/bin/env pyscript

from pyscript import *
from pyscript.lib.optics import *

import os

# test the line beam splitter
obj = BS()
render(obj, file="test_optics_BS.eps")
#os.system("gv -scale 10 test_optics_BS.eps")

# test the BSBox object
obj = BSBox()
render(obj, file="test_optics_BSBox.eps")
#os.system("gv -scale 10 test_optics_BSBox.eps")

# test the PBS object
obj = PBS()
render(obj, file="test_optics_PBS.eps")
#os.system("gv -scale 10 test_optics_PBS.eps")

# test the BSLine object
obj = BSLine()
render(obj, file="test_optics_BSLine.eps")
#os.system("gv -scale 10 test_optics_BSLine.eps")

# test the PhaseShifter object
obj = PhaseShifter()
render(obj, file="test_optics_PhaseShifter.eps")
#os.system("gv -scale 10 test_optics_PhaseShifter.eps")

# test the Mirror object
obj = Mirror()
render(obj, file="test_optics_Mirror.eps")
#os.system("gv -scale 10 test_optics_Mirror.eps")

# test the Detector object
obj = Detector()
render(obj, file="test_optics_Detector.eps")
#os.system("gv -scale 10 test_optics_Detector.eps")

# test the Laser object
obj = Laser()
render(obj, file="test_optics_Laser.eps")
#os.system("gv -scale 10 test_optics_Laser.eps")

# test the Modulator object
obj = Modulator()
render(obj, file="test_optics_Modulator.eps")
#os.system("gv -scale 10 test_optics_Modulator.eps")

# test the FreeSpace object
obj = FreeSpace()
render(obj, file="test_optics_FreeSpace.eps")
#os.system("gv -scale 10 test_optics_FreeSpace.eps")

# test the Lens object
obj = Lens()
render(obj, file="test_optics_Lens.eps")
os.system("gv -scale 10 test_optics_Lens.eps")

# test the LambdaPlate object
obj = LambdaPlate()
render(obj, file="test_optics_LambdaPlate.eps")
os.system("gv -scale 10 test_optics_LambdaPlate.eps")

# vim: expandtab shiftwidth=4:
