from pyscript import *
from pyscript.lib.electronics import *

def fig_and():
	obj = AndGate()
	render(obj,file="fig_and.eps")

def fig_nand():
	obj = NandGate()
	render(obj,file="fig_nand.eps")

def fig_or():
	obj = OrGate()
	render(obj,file="fig_or.eps")

def fig_nor():
	obj = NorGate()
	render(obj,file="fig_nor.eps")

def fig_xor():
	obj = XorGate()
	render(obj,file="fig_xor.eps")

def fig_nxor():
	obj = NxorGate()
	render(obj,file="fig_nxor.eps")

def fig_not():
	obj = NotGate()
	render(obj,file="fig_not.eps")

def fig_resistor():
	obj = Resistor()
	render(obj,file="fig_res.eps")

def fig_capacitor():
	obj = Capacitor()
	render(obj,file="fig_cap.eps")

fig_and()
fig_nand()
fig_or()
fig_nor()
fig_xor()
fig_nxor()
fig_not()
fig_resistor()
fig_capacitor()
