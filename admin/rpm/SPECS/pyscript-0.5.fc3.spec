Summary:   PyScript - Postscript graphics with Python
Name:      pyscript
Version:   0.5
Release:   1%{?dist}
URL:       http://pyscript.sourceforge.net
Source:    http://dl.sourceforge.net/sourceforge/pyscript/pyscript-0.5.tar.gz
License:   GPL
Group:     Applications/Publishing
Requires:  python, tetex
Patch:     qi.patch
BuildRoot: /tmp/%{name}-%{version}-buildroot
Prefix:    /usr

%description
PyScript is a Python module for producing high quality postscript graphics.
Rather than use a GUI to draw a picture, the picture is programmed using
Python and the PyScript objects.

%prep
cp -f ../SOURCES/%{name}-%{version}.tar.gz .
rm -rf %{name}-%{version}
tar -xvzf %{name}-%{version}.tar.gz
cp ../SOURCES/qi.patch %{name}-%{version}/pyscript/lib
cd %{name}-%{version}/pyscript/lib
patch -p1 qi.py qi.patch

%build
cd %{name}-%{version}
python setup.py build

%install
cd %{name}-%{version}
python setup.py install --prefix=$RPM_BUILD_ROOT/usr

%clean
rm -f %{name}-%{version}.tar.gz
rm -rf %{name}-%{version}
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc %{name}-%{version}/README %{name}-%{version}/LICENSE %{name}-%{version}/BUGS %{name}-%{version}/CHANGES %{name}-%{version}/TODO %{name}-%{version}/doc/manual/pyscript.pdf
%{prefix}/bin/pyscript
%{prefix}/lib/python2.3/site-packages/pyscript/__init__.py
%{prefix}/lib/python2.3/site-packages/pyscript/__init__.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/afm.py
%{prefix}/lib/python2.3/site-packages/pyscript/afm.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/base.py
%{prefix}/lib/python2.3/site-packages/pyscript/base.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/defaults.py
%{prefix}/lib/python2.3/site-packages/pyscript/defaults.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/groups.py
%{prefix}/lib/python2.3/site-packages/pyscript/groups.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/objects.py
%{prefix}/lib/python2.3/site-packages/pyscript/objects.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/path.py
%{prefix}/lib/python2.3/site-packages/pyscript/path.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/render.py
%{prefix}/lib/python2.3/site-packages/pyscript/render.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/vectors.py
%{prefix}/lib/python2.3/site-packages/pyscript/vectors.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/version.py
%{prefix}/lib/python2.3/site-packages/pyscript/version.pyc

# add pyscript font files
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/__init__.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/__init__.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/courier_boldoblique.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/courier_boldoblique.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/courier_bold.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/courier_bold.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/courier_oblique.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/courier_oblique.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/courier.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/courier.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/helvetica_boldoblique.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/helvetica_boldoblique.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/helvetica_bold.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/helvetica_bold.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/helvetica_oblique.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/helvetica_oblique.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/helvetica.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/helvetica.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/symbol.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/symbol.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/times_bolditalic.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/times_bolditalic.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/times_bold.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/times_bold.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/times_italic.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/times_italic.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/times_roman.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/times_roman.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/zapfdingbats.py
%{prefix}/lib/python2.3/site-packages/pyscript/fonts/zapfdingbats.pyc

# add pyscript library files
%{prefix}/lib/python2.3/site-packages/pyscript/lib/__init__.py
%{prefix}/lib/python2.3/site-packages/pyscript/lib/__init__.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/lib/electronics.py
%{prefix}/lib/python2.3/site-packages/pyscript/lib/electronics.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/lib/misc.py
%{prefix}/lib/python2.3/site-packages/pyscript/lib/misc.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/lib/optics.py
%{prefix}/lib/python2.3/site-packages/pyscript/lib/optics.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/lib/plot.py
%{prefix}/lib/python2.3/site-packages/pyscript/lib/plot.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/lib/presentation.py
%{prefix}/lib/python2.3/site-packages/pyscript/lib/presentation.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/lib/qi.py
%{prefix}/lib/python2.3/site-packages/pyscript/lib/qi.pyc
%{prefix}/lib/python2.3/site-packages/pyscript/lib/quantumcircuits.py
%{prefix}/lib/python2.3/site-packages/pyscript/lib/quantumcircuits.pyc

%changelog
* Fri Apr 7 2006 Paul Cochrane <paultcochrane@gmail.com>
- Corrected Group tag, added dist to the Release tag, and changed the
  Copyright tag to License as it now is (and corrected the tag value).

* Fri Mar 30 2006 Paul Cochrane <paultcochrane@gmail.com>
- Finally got building to work properly

* Fri Mar 3 2006 Paul Cochrane <paultcochrane@gmail.com>
- New spec file made for pyscript-0.5
