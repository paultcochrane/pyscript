#!/usr/bin/env python

from pyscript import HAlign,Epsf,render
import glob,os

tests=glob.glob('test_*.py')
for test in tests:
	basefile=os.path.splitext(test)[0]
	expectfile=basefile+'_expect.eps'
	if not os.path.exists(expectfile):
		raise "%s doesn't exist"%expectfile

	os.system('pyscript %s'%test)

	render(
		HAlign(Epsf(basefile+".eps"),Epsf(expectfile)),
		file='comparison.eps'
		)
	
	os.system('gv comparison.eps')




