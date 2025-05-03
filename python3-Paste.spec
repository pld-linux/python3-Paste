#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Tools for using a Web Server Gateway Interface stack
Summary(pl.UTF-8):	Narzędzia do używania stosu Web Server Gateway Interface
Name:		python3-Paste
Version:	3.10.1
Release:	1
Group:		Libraries/Python
License:	MIT
#Source0Download: https://pypi.org/simple/paste/
Source0:	https://files.pythonhosted.org/packages/source/P/Paste/paste-%{version}.tar.gz
# Source0-md5:	7d59952c9e108d8d381944b40e90e47a
URL:		https://pypi.org/project/Paste/
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools >= 0.6-0.a9.1
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-six >= 1.4.0
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Paste provides several pieces of "middleware" (or filters) that can be
nested to build web applications. Each piece of middleware uses the
WSGI (PEP 333) interface, and should be compatible with other
middleware based on those interfaces.

%description -l pl.UTF-8
Pakiet Paste dostarcza kilka części warstwy pośredniej (lub filtrów),
które można osadzać w celu zbudowania aplikacji WWW. Każda część
warstwy pośredniej używa interfejsu WSGI (PEP 333) i powinna być
kompatybilna z inną warstwą pośrednią opartą na tych interfejsach.

%package apidocs
Summary:	API documentation for Python Paste module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona Paste
Group:		Documentation

%description apidocs
API documentation for Python Paste module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona Paste.

%prep
%setup -q -n paste-%{version}

# online test + requires outdated pythonpaste.org website content
%{__rm} tests/test_proxy.py

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst docs/{license,news}.txt
# paste is also top dir for other python3-Paste* packages
%dir %{py3_sitescriptdir}/paste
%{py3_sitescriptdir}/paste/auth
%{py3_sitescriptdir}/paste/cowbell
%{py3_sitescriptdir}/paste/debug
%{py3_sitescriptdir}/paste/evalexception
%{py3_sitescriptdir}/paste/exceptions
%{py3_sitescriptdir}/paste/util
%{py3_sitescriptdir}/paste/*.py
%{py3_sitescriptdir}/paste/__pycache__
%{py3_sitescriptdir}/Paste-%{version}-py*.egg-info
%{py3_sitescriptdir}/Paste-%{version}-py*-nspkg.pth

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,community,download,include,modules,*.html,*.js}
%endif
