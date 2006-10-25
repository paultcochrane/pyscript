# $Id$

MAIN = align.eps\
       align2.eps\
       arrow.eps\
       atom.eps\
       bifurcate.eps\
       cryptClonerDiag.eps\
       detector.eps\
       distribute.eps\
       div_con.eps\
       fabry-perot_pdh.eps\
       flower_algorithm.eps\
       mach-zehnder.eps\
       michelson-morely.eps\
       qcirc.eps\
       sagnac.eps\
       sphere.eps\
       stateSwap.eps\
       teleport.eps\
       tex.eps\
       tutorial.eps\
       twoqubitQST.eps\
       xmdsFunctionality.eps\
       xmdsProcess.eps

all: $(MAIN) Makefile

view: $(MAIN)
	$(foreach i, $(MAIN), $(shell gv $i))

# standard TeX stuff
%.eps:  %.py
	pyscript $<

clean:
	rm -f $(MAIN)

# vim: shiftwidth=4:
