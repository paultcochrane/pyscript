.PHONY: clean realclean

FIGS = \
	fig_area.pdf \
	fig_circle.pdf \
	fig_circle_eg1.pdf \
	fig_circle_eg2.pdf \
	fig_colorchart.pdf \
	fig_path.pdf \
	fig_path_eg.pdf \
	fig_position_eg1.pdf \
	fig_position_eg2.pdf \
	fig_rectangle.pdf \
	fig_tex_eg.pdf \
	fig_text_kerning.pdf \
	logo.pdf \
	tutorial.pdf

all: $(FIGS)

%.pdf: %.py
	pyscript $<
	epstopdf $*.eps

clean:
	rm -f *.eps *.pdf

realclean: clean
	rm -f *~
