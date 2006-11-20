.PHONY: clean realclean

FIGS = \
	AndGate.pdf \
	Capacitor.pdf \
	NandGate.pdf \
	NorGate.pdf \
	NotGate.pdf \
	NxorGate.pdf \
	OrGate.pdf \
	Resistor.pdf \
	XorGate.pdf

all: $(FIGS)

%.pdf: %.py
	pyscript $<
	epstopdf $*.eps

clean:
	rm -f *.eps *.pdf

realclean: clean
	rm -r *~

