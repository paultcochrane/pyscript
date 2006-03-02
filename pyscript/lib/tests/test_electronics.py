#!/usr/bin/env pyscript

from pyscript import *
from pyscript.lib.electronics import *

import os

def test(obj):
    """
    Render the given object in pyscript and view with ghostview
    """

    render(obj, file="test_optics_%s.eps" % obj.__class__.__name__)
    os.system("gv -scale 10 test_optics_%s.eps" % obj.__class__.__name__)
    return

# test the AND gate
test(AndGate())

# test the NAND gate
test(NandGate())

# test the OR gate
test(OrGate())

# test the NOR gate
test(NorGate())

# test the XOR gate
test(XorGate())

# test the NXOR gate
test(NxorGate())

# test the NOT gate
test(NotGate())

# test the Resistor
test(Resistor())

# test the Capacitor
test(Capacitor())

# vim: expandtab shiftwidth=4:
