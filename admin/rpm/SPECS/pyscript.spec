Name:      pyscript
Version:   0.6
Release:   3%{?dist}
Summary:   PyScript - Postscript graphics with Python

Group:     Applications/Publishing
License:   GPL
URL:       http://pyscript.sourceforge.net
Source0:   http://dl.sourceforge.net/sourceforge/pyscript/pyscript-0.6.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python
Requires:  python, tetex

# define python_sitelib
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%description
PyScript is a Python module for producing high quality postscript graphics.
Rather than use a GUI to draw a picture, the picture is programmed using
Python and the PyScript objects.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README LICENSE BUGS CHANGES TODO doc/manual/pyscript.pdf
%{_bindir}/pyscript
%dir %{python_sitelib}/pyscript

# add pyscript base files
%{python_sitelib}/pyscript/*.py
%{python_sitelib}/pyscript/*.pyc
%ghost %{python_sitelib}/pyscript/*.pyo

# add pyscript font files
%{python_sitelib}/pyscript/fonts/*.py
%{python_sitelib}/pyscript/fonts/*.pyc
%ghost %{python_sitelib}/pyscript/fonts/*.pyo

# add pyscript library files
%{python_sitelib}/pyscript/lib/__init__.py
%{python_sitelib}/pyscript/lib/__init__.pyc
%{python_sitelib}/pyscript/lib/electronics.py
%{python_sitelib}/pyscript/lib/electronics.pyc
%{python_sitelib}/pyscript/lib/optics.py
%{python_sitelib}/pyscript/lib/optics.pyc
%{python_sitelib}/pyscript/lib/present.py
%{python_sitelib}/pyscript/lib/present.pyc
%{python_sitelib}/pyscript/lib/presentation.py
%{python_sitelib}/pyscript/lib/presentation.pyc
%{python_sitelib}/pyscript/lib/qi.py
%{python_sitelib}/pyscript/lib/qi.pyc
%{python_sitelib}/pyscript/lib/quantumcircuits.py
%{python_sitelib}/pyscript/lib/quantumcircuits.pyc
# ghost of optimised python files
%ghost %{python_sitelib}/pyscript/lib/__init__.pyo
%ghost %{python_sitelib}/pyscript/lib/electronics.pyo
%ghost %{python_sitelib}/pyscript/lib/optics.pyo
%ghost %{python_sitelib}/pyscript/lib/present.pyo
%ghost %{python_sitelib}/pyscript/lib/presentation.pyo
%ghost %{python_sitelib}/pyscript/lib/qi.pyo
%ghost %{python_sitelib}/pyscript/lib/quantumcircuits.pyo

%changelog
* Mon May 15 2006 Paul Cochrane <paultcochrane@gmail.com>
- On further advice from <tjikkun@xs4all.nl>; Bugzilla ref: #191218
  And from the python packaging guidelines the following changes have been
  made:
- %{python_sitelib} variable introduced.
- %{ghost}ing of optimised python files so that they are uninstalled were
  someone to create them at some later stage.
- Simplification of prep, build and install sections.
- Use of wildcards where possible (not possible for library files as wish to
  exclude some from the distribution).
- Use of the %{__python} macro, and an improved version of the install
  command.

* Fri May 12 2006 Paul Cochrane <paultcochrane@gmail.com>
- On advice from: <tjikkun@xs4all.nl>; Bugzilla ref: #191218
- Removed Prefix, and made non-relocatable
- Corrected BuildRoot
- Corrected spec file filename
- Cleaning BuildRoot at beginning of install
- Corrected defattr and Source0 values from fedora-newrpmspec
- Changed ordering of attribute values to agree with the standard spec file
  format from fedora-newrpmspec
- Increased release number
- Added %{_libdir} and %{_bindir} macros in relevant locations

* Mon Apr 24 2006 Paul Cochrane <paultcochrane@gmail.com>
- Updated for PyScript version 0.6
- Removed patch commands as not required for version 0.6

* Fri Apr 7 2006 Paul Cochrane <paultcochrane@gmail.com>
- Corrected Group tag, added dist to the Release tag, and changed the
  Copyright tag to License as it now is (and corrected the tag value).

* Fri Mar 30 2006 Paul Cochrane <paultcochrane@gmail.com>
- Finally got building to work properly

* Fri Mar 3 2006 Paul Cochrane <paultcochrane@gmail.com>
- New spec file made for pyscript-0.5
