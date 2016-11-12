# $Id$

MAIN = test_arrow.eps\
       test_arrowhead.eps\
       test_circle.eps\
       test_dot.eps\
       test_epsf.eps\
       test_rectangle.eps\
       test_tex.eps\
       test_text.eps

#view: $(MAIN).ps
#	gv $(MAIN).ps

all: $(MAIN)

# standard TeX stuff
%.eps:  %.py
	./$<

clean:
	rm -f $(MAIN)

# vim: shiftwidth=4:
