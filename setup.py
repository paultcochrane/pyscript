#!/usr/bin/env python

from distutils.core import setup

a=setup(name="pyscript",
      version="0.6",
      description="Postscript Graphics with Python",
      author="Alexei Gilchrist and Paul Cochrane",
      author_email="aalexei@sourceforge.net",
      url="http://pyscript.sourceforge.net",
      packages=['pyscript','pyscript.lib','pyscript.fonts'],
      scripts=['bin/pyscript'],
)


