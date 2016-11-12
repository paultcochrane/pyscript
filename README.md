# Pyscript

## Summary

Pyscript is a set of modules and scripts for python that facilitate
the creation of high-quality postscript diagrams. The diagrams are
scripted rather than drawn.

See http://pyscript.sourceforge.net


## Installation

Pyscript is just a python module ... treat it as any other module

 * Global Installation:

   As root use

   > python setup.py install

   This will install the files, in the appropriate place for
   your python distribution. This will be something like
   e.g. /usr/lib/python2.2/site-packages/

 * Local installation:

   You can supply the base directory using

    > python setup.py install --home=<dir>

   which will install the files in

    <dir>/lib/python/

   for more help and options use

    > python setup.py install --help

   also see http://www.python.org/doc/current/inst/ for more details on
   using the distutils package

 * By hand:

   copy all the files in the pyscript directory to somewhere in your
   python path, e.g.

    cp -r pyscript ~/lib/python/

 * RPM package:

   Install using your favourite rpm installation tool, or from root issue a
   command like:

    > rpm -i pyscript-<version>.rpm

   (where `<version>` is the version string of the rpm file).

 * DEB package:

   Check to make sure that the tetex-base and python packages are installed
   (just in case), and then use dpkg in the usual manner, e.g.

    > dpkg -i pyscript_<version>.deb

   (where `<version>` is the verstion string of the .deb package).
