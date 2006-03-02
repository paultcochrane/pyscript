#!/usr/bin/env pyscript

from pyscript import *
from pyscript.lib.optics import *
from pyscript.tests.test import test_run

lib = "optics"

# test the line beam splitter
test_run(BS(), lib)

# test the BSBox object
test_run(BSBox(), lib)

# test the PBS object
test_run(PBS(), lib)

# test the BSLine object
test_run(BSLine(), lib)

# test the PhaseShifter object
test_run(PhaseShifter(), lib)

# test the Mirror object
test_run(Mirror(), lib)

# test the Detector object
test_run(Detector(), lib)

# test the Laser object
test_run(Laser(), lib)

# test the Modulator object
test_run(Modulator(), lib)

# test the FreeSpace object
test_run(FreeSpace(), lib)

# test the Lens object
test_run(Lens(), lib)

# test the LambdaPlate object
test_run(LambdaPlate(), lib)

# vim: expandtab shiftwidth=4:
