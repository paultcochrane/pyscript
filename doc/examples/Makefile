
MAIN = align.eps\
       align2.eps\
       atom.eps\
       detector.eps\
       distribute.eps\
       div_con.eps\
       flower_algorithm.eps\
       qcirc.eps\
       sarah.eps\
       sphere.eps\
       stateSwap.eps\
       tex.eps

#view: $(MAIN).ps
#	gv $(MAIN).ps

all: $(MAIN)

# standard TeX stuff
%.eps:  %.py
	./$<

clean:
	rm -f $(MAIN)

# vim: shiftwidth=4:
