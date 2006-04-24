# Copyright 1999-2004 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header$

inherit distutils

DESCRIPTION="Python module for producing high quality postscript graphics"
SRC_URI="http://dl.sourceforge.net/sourceforge/pyscript/pyscript-${PV}.tar.gz"
HOMEPAGE="http://pyscript.sourceforge.net/"
LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~x86 ~ppc ~ppcmacos"
IUSE="doc"
DEPEND="virtual/python
	virtual/tetex"

DOCS="AUTHORS CHANGES README BUGS LICENSE"

src_unpack() {
	unpack ${A}
	cd ${S}
}

src_compile() {
	distutils_src_compile
}

src_install() {
	distutils_src_install

	if use doc; then
		insinto /usr/share/doc/${P}/
		doins doc/manual/pyscript.pdf
	fi
}
