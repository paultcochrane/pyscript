# Copyright (C) 2002-2006  Alexei Gilchrist and Paul Cochrane
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# $Id$

.PHONY: clean realclean figs optics

MAIN = pyscript
TEXFILES = $(MAIN).tex \
	   pyscript_defs.tex \
	   libpresent.tex \
	   libpresentation.tex \
	   libqi.tex \
	   pyscriptElectronics.tex \
	   pyscriptOptics.tex \
	   pyscript.bib

all: figs optics pdf

figs:
	$(MAKE) --directory=$@

optics:
	$(MAKE) --directory=$@

view: all
	gv $(MAIN).pdf

acro: all
	acroread $(MAIN).pdf

pdf: $(MAIN).pdf

$(MAIN).pdf: $(TEXFILES)
	pdflatex $<
	-bibtex $*
	pdflatex $<
	pdflatex $<

clean:
	-rm -f *.mpx *.log *.aux *.blg *.toc *.out *.bbl *.dvi $(MAIN).pdf

realclean: clean
	for d in figs optics;                \
	do                                   \
	     $(MAKE) --directory=$$d clean;  \
	done

# vim: shiftwidth=4:
