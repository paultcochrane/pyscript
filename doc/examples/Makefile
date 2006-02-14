# $Id$

MAIN = align.eps\
       align2.eps\
       atom.eps\
       bifurcate.eps\
       detector.eps\
       distribute.eps\
       div_con.eps\
       flower_algorithm.eps\
       qcirc.eps\
       sphere.eps\
       stateSwap.eps\
       teleport.eps\
       tex.eps\
       tutorial.eps

#view: $(MAIN).ps
#	gv $(MAIN).ps

all: $(MAIN)

# standard TeX stuff
%.eps:  %.py
	pyscript $<

clean:
	rm -f $(MAIN)

# vim: shiftwidth=4:
