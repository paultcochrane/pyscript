#!/usr/bin/env python

from distutils.core import setup

a=setup(name="pyscript",
      version="0.1",
      description="Python Postscript Scripting",
      author="Alexei Gilchrist and Paul Cochrane",
      author_email="aalexei@sourceforge.net",
      url="http://pyscript.sourceforge.net",
      packages=['pyscript','pyscript.lib','pyscript.fonts'],
)


