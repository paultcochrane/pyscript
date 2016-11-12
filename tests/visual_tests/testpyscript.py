#!/usr/bin/env python

from pyscript import HAlign, Epsf, render
import glob
import os
import commands


def printit(test, message):
    print(test.ljust(70), message)

# clean up previous tests
os.system('rm test_*.eps')

tests = glob.glob('test_*.py')
for test in tests:
    # this should generate a test_foo.eps for visual tests
    # otherwise test something silently, but raise exception
    # if it doesn't pass
    commands.getoutput('pyscript %s' % test)

    # for the moment assume all tests are visual and that there is
    # one eps file produced for each test with the same basename
    sample, ext = os.path.splitext(os.path.basename(test))
    sample = sample+".eps"
    if not os.path.exists(sample):
        printit(test, "no test file: %s" % sample)
        continue

    expect = os.path.join('expected', sample)

    # check expected/test_foo.eps exists otherwise nothing to compare to
    if not os.path.exists(expect):
        printit(test, "no expected file: %s" % expect)
        continue

    # there will be trivial changes to the EPS files
    # such as date stamp and pyscript version
    output = commands.getoutput(
        "diff -I '^%%%%CreationDate' %s %s " % (sample, expect))
    if len(output) == 0:
        printit(test, "OK")
        continue

    # put them side by side and display
    # XXX need a verbose switch on output
    render(
        HAlign(Epsf(sample), Epsf(expect)),
        file='comparison.eps'
        )

    os.system('evince comparison.eps')

# vim: expandtab shiftwidth=4 softtabstop=4
