.PHONY: clean realclean

FIGS = \
	BS.pdf \
	BSBox.pdf \
	BSLine.pdf \
	Detector.pdf \
	FreeSpace.pdf \
	LambdaPlate.pdf \
	Laser.pdf \
	Lens.pdf \
	Mirror.pdf \
	Modulator.pdf \
	PBS.pdf \
	PhaseShifter.pdf \
	fabry-perot_pdh.pdf \
	mach-zehnder.pdf \
	michelson-morely.pdf \
	sagnac.pdf

all: $(FIGS)

%.pdf: %.py
	pyscript $<
	epstopdf $*.eps

clean:
	rm -f *.eps *.pdf

realclean:
	rm -r *~
