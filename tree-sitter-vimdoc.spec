#
# Conditional build:
%bcond_without	python3	# Python 3.x binding

Summary:	Tree-sitter parser for Vim help files
Summary(pl.UTF-8):	Analizator składniowy tree-parsera dla plików pomocy Vima
Name:		tree-sitter-vimdoc
Version:	4.1.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/neovim/tree-sitter-vimdoc/releases
Source0:	https://github.com/neovim/tree-sitter-vimdoc/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ae7a33135da79891cca389dd86711ccb
URL:		https://github.com/neovim/tree-sitter-vimdoc
# c11
BuildRequires:	gcc >= 6:4.7
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-setuptools >= 1:62.4.0
BuildRequires:	python3-wheel
BuildRequires:	rpmbuild(macros) >= 1.714
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		soname_ver	4

%description
Tree-sitter parser for Vim help files.

%description -l pl.UTF-8
Analizator składniowy tree-parsera dla plików pomocy Vima.

%package devel
Summary:	Header files for tree-sitter-vimdoc
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tree-sitter-vimdoc
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-vimdoc.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tree-sitter-vimdoc.

%package static
Summary:	Static tree-sitter-vimdoc library
Summary(pl.UTF-8):	Biblioteka statyczna tree-sitter-vimdoc
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-vimdoc library.

%description static -l pl.UTF-8
Biblioteka statyczna tree-sitter-vimdoc.

%package -n neovim-parser-vimdoc
Summary:	Vim help files parser for Neovim
Summary(pl.UTF-8):	Analizator składni plików pomocy Vima dla Neovima
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-vimdoc
Vim help files parser for Neovim.

%description -n neovim-parser-vimdoc -l pl.UTF-8
Analizator składni plików pomocy Vima dla Neovima.

%package -n python3-tree-sitter-vimdoc
Summary:	Vim help files parser for Python
Summary(pl.UTF-8):	Analizator składni plików pomocy Vima dla Pythona
Group:		Libraries/Python
Requires:	python3-tree-sitter >= 0.24

%description -n python3-tree-sitter-vimdoc
Vim help files parser for Python.

%description -n python3-tree-sitter-vimdoc -l pl.UTF-8
Analizator składni plików pomocy Vima dla Pythona.

%prep
%setup -q

%build
%{__make} \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/nvim/parser

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} ../../libtree-sitter-vimdoc.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/vimdoc.so

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/tree_sitter_vimdoc/*.c
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libtree-sitter-vimdoc.so.*.*
%ghost %{_libdir}/libtree-sitter-vimdoc.so.%{soname_ver}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-vimdoc.so
%{_includedir}/tree_sitter/tree-sitter-vimdoc.h
%{_pkgconfigdir}/tree-sitter-vimdoc.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-vimdoc.a

%files -n neovim-parser-vimdoc
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/vimdoc.so

%if %{with python3}
%files -n python3-tree-sitter-vimdoc
%defattr(644,root,root,755)
%dir %{py3_sitedir}/tree_sitter_vimdoc
%{py3_sitedir}/tree_sitter_vimdoc/_binding.abi3.so
%{py3_sitedir}/tree_sitter_vimdoc/__init__.py
%{py3_sitedir}/tree_sitter_vimdoc/__init__.pyi
%{py3_sitedir}/tree_sitter_vimdoc/py.typed
%{py3_sitedir}/tree_sitter_vimdoc/__pycache__
%{py3_sitedir}/tree_sitter_vimdoc/queries
%{py3_sitedir}/tree_sitter_vimdoc-%{version}-py*.egg-info
%endif
