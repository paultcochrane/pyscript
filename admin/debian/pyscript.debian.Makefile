#!/usr/bin/make

.PHONY: build install
	
install:
	python setup.py install --prefix=$(DESTDIR)/usr
	install -d $(DESTDIR)/usr/share/doc/pyscript/
	cp -a doc/manual/pyscript.pdf $(DESTDIR)/usr/share/doc/pyscript
	cp -a README $(DESTDIR)/usr/share/doc/pyscript
	cp -a CHANGES $(DESTDIR)/usr/share/doc/pyscript
	cp -a TODO $(DESTDIR)/usr/share/doc/pyscript
	cp -a BUGS $(DESTDIR)/usr/share/doc/pyscript
