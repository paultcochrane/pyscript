#!/usr/bin/env python

from pyscript import HAlign,Epsf,render
import glob,os

# clean up previous tests
os.system('rm test_*.eps')

tests=glob.glob('test_*.py')
for test in tests:
	# this should generate a test_foo.eps for visual tests
	# otherwise test something silently, but raise exception
	# if it doesn't pass
	os.system('pyscript %s'%test)

# compare visual outputs
samples=glob.glob('test_*.eps')
for sample in samples:
	expect=os.path.join('expected',sample)

	# check expected/test_foo.eps exists otherwise nothing to compare to
	if not os.path.exists(expect):
		raise "%s doesn't exist"%expect

	# put them side by side and display
	render(
		HAlign(Epsf(sample),Epsf(expect)),
		file='comparison.eps'
		)
	
	os.system('gv comparison.eps')




