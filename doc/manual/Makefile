
MAIN = pyscript
FIGS = 

all: $(FIGS) $(MAIN).pdf $(MAIN).dvi

view: $(FIGS) $(MAIN).pdf
	gv $(MAIN).pdf

acro: $(FIGS) $(MAIN).pdf
	acroread $(MAIN).pdf

$(FIGS) : %.pdf : %.py
	./$<
	epstopdf $*.eps

%.pdf:  %.tex $(FIGS) pyscript_defs.tex libpresent.tex libpresentation.tex libqi.tex pyscriptElectronics.tex pyscriptOptics.tex pyscript.bib
	pdflatex $<
	-bibtex $*
	pdflatex $<
	pdflatex $<

%.dvi:  %.tex $(FIGS) pyscript_defs.tex libpresent.tex libpresentation.tex libqi.tex pyscriptElectronics.tex pyscriptOptics.tex pyscript.bib
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
	-rm -f *~ *.mpx *.log *.aux *.blg

reallyclean: clean
	-rm -f figs.[0-9]*.eps *.pdf *.dvi $(FIGS) *.bbl
