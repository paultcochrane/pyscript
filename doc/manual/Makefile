
MAIN = pyscript
FIGS = 

all: $(FIGS) $(MAIN).pdf

view: $(FIGS) $(MAIN).pdf
	gv $(MAIN).pdf

acro: $(FIGS) $(MAIN).pdf
	acroread $(MAIN).pdf

$(FIGS) : %.pdf : %.py
	./$<
	epstopdf $*.eps

%.pdf:  %.tex $(FIGS) pyscript_defs.tex pyscriptPlot.tex pyscriptElectronics.tex pyscriptOptics.tex
	pdflatex $<
	-bibtex $*
	pdflatex $<
	pdflatex $<

%.dvi:  %.tex $(FIGS) pyscript_defs.tex
	latex $<
	-bibtex $*
	latex $<
	latex $<

# standard TeX stuff
#%.dvi:  %.tex $(FIGS)
#	latex $<
#	-bibtex $*
#	latex $<
#	latex $<

#%.ps: %.dvi
#	dvips -o $*.ps $*.dvi

#%.pdf: %.tex
#	ps2pdf $*.ps $*.pdf

#dvi: $(MAIN).dvi
#ps: $(MAIN).ps
#pdf: $(MAIN).pdf
figs: $(FIGS)

clean:
	-rm *~ *.mpx *.log *.aux *.blg

reallyclean: clean
	-rm figs.[0-9]*.eps *.pdf *.dvi $(FIGS) *.bbl
