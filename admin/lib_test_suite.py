#!/usr/bin/env python

import sys

if sys.argv[1] is not None:
	testLib = str(sys.argv[1])
else:
	testLib = 'all'

from pyscript import *

defaults.units=UNITS['cm']

defaults.tex_head=r"""
\documentclass{article}
\pagestyle{empty}
\begin{document}
"""

if testLib == 'optics' or testLib == 'all':

	# optics library
	library = 'optics'
	from pyscript.lib.optics import *
	print "Testing %s library routines" % library
	
	funcs = [ 'BS()', 
	  	'BSBox()', 
	  	'PBS()', 
	  	'BSLine()', 
	  	'PhaseShifter()', 
	  	'Mirror()' ]
	
	for i in range(len(funcs)):
		try:
        		obj = eval(funcs[i])
		except Exception, e:
			print "\tEeek!  Couldn't assign %s" % funcs[i]
			print "Error output:\n %s" % e
		
		try: 
			fname = funcs[i] + '.eps'
                	render(obj,file=fname)
		except:
			print "\tEeek!  Couldn't render %s" % funcs[i]
		else:
			print "\tOk, %s seems to work" % funcs[i]
	
	print "done %s library\n" % library

if testLib == 'electronics' or testLib == 'all':

	# electronics library
	library = 'electronics'
	from pyscript.lib.electronics import *
	print "Testing %s library routines" % library
	
	funcs = [ 
		r"AndGate()",
		r"AndGate(direction='e')",
		r"AndGate(direction='w')",
		r"AndGate(direction='s')",
		r"AndGate(direction='n')",
		r"AndGate(direction='moo')",
          	r"NandGate()",
          	r"NandGate(direction='e')",
          	r"NandGate(direction='w')",
          	r"NandGate(direction='s')",
          	r"NandGate(direction='n')",
          	r"NandGate(direction='moo')",
          	r"OrGate()",
          	r"OrGate(direction='e')",
          	r"OrGate(direction='w')",
          	r"OrGate(direction='s')",
          	r"OrGate(direction='n')",
          	r"OrGate(direction='moo')",
          	r"NorGate()",
          	r"NorGate(direction='e')",
          	r"NorGate(direction='w')",
          	r"NorGate(direction='s')",
          	r"NorGate(direction='n')",
          	r"NorGate(direction='moo')",
          	r"XorGate()",
          	r"XorGate(direction='e')",
          	r"XorGate(direction='w')",
          	r"XorGate(direction='s')",
          	r"XorGate(direction='n')",
          	r"XorGate(direction='moo')",
          	r"NxorGate()",
          	r"NxorGate(direction='e')",
          	r"NxorGate(direction='w')",
          	r"NxorGate(direction='s')",
          	r"NxorGate(direction='n')",
          	r"NxorGate(direction='moo')",
          	r"NotGate()",
          	r"NotGate(direction='e')",
          	r"NotGate(direction='w')",
          	r"NotGate(direction='s')",
          	r"NotGate(direction='n')",
          	r"NotGate(direction='moo')",
		r"Resistor()",
		r"Resistor(direction='ew')",
		r"Resistor(direction='ns')",
		r"Resistor(direction='moo')",
		r"Capacitor()",
		r"Capacitor(direction='ew')",
		r"Capacitor(direction='ns')",
		r"Capacitor(direction='moo')",
		 ]
	
	electronicsObjs = Group()
	for i in range(len(funcs)):
		print "\tTesting %s" % funcs[i]
		try:
        		obj = eval(funcs[i])
		except Exception, e:
			print "\tEeek!  Couldn't assign %s" % funcs[i]
			print "Error output:\n %s" % e
	
        	try:
			fname = funcs[i] + '.eps'
                	render(obj,file=fname)
			obj.move(0,3.2*i)
			electronicsObjs.append(obj)
			electronicsObjs.append(Text(nw=obj.sw-P(0,0.2),text=funcs[i]))
        	except:
                	print "\tEeek!  Couldn't render %s" % funcs[i]
        	else:
                	print "\tOk, %s seems to work" % funcs[i]

	render(electronicsObjs,file="electronicsLib.eps")
	
	print "done %s library\n" % library

if testLib == 'quantumcircuits' or testLib == 'all':
	
	# quantum circuits library
	library = 'quantumcircuits'
	from pyscript.lib.quantumcircuits import *
	print "Testing %s library routines" % library
	
	funcs = [ 'Rail()',
          	'Cnot()',
          	'HGate()',
          	'PGate()',
          	'CPGate()',
          	'Detector()',
          	'XGate()',
          	'YGate()',
          	'ZGate()',
          	'CXGate()',
          	'CYGate()',
          	'CZGate()',
	 	]
	
	for i in range(len(funcs)):
        	try:
                	obj = eval(funcs[i])
        	except Exception, e:
                	print "\tEeek!  Couldn't assign %s" % funcs[i]
                	print "Error output:\n %s" % e
	
        	try:
			fname = funcs[i] + '.eps'
                	render(obj,file=fname)
        	except:
                	print "\tEeek!  Couldn't render %s" % funcs[i]
        	else:
                	print "\tOk, %s seems to work" % funcs[i]
	
	print "done %s library\n" % library
	
