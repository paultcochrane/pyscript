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
	
	funcs = [ 'AndGate()',
          	'NandGate()',
          	'OrGate()',
          	'NorGate()',
          	'XorGate()',
          	'NxorGate()' ]
	
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
	
