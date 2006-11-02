#!/usr/bin/env pyscript

from pyscript import *
from pyscript.lib.electronics import *
from pyscript.tests import test_run

lib = "electronics"

# test the AND gate
test_run(AndGate(), lib)

# test the NAND gate
test_run(NandGate(), lib)

# test the OR gate
test_run(OrGate(), lib)

# test the NOR gate
test_run(NorGate(), lib)

# test the XOR gate
test_run(XorGate(), lib)

# test the NXOR gate
test_run(NxorGate(), lib)

# test the NOT gate
test_run(NotGate(), lib)

# test the Resistor
test_run(Resistor(), lib)

# test the Capacitor
test_run(Capacitor(), lib)

# vim: expandtab shiftwidth=4:
