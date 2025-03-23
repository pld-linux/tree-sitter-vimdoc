Summary:	Tree-sitter parser for Vim help files
Name:		tree-sitter-vimdoc
Version:	3.0.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/neovim/tree-sitter-vimdoc/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	043ae1473a6790b92d6d7b56da0fa511
URL:		https://github.com/neovim/tree-sitter-vimdoc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ts_vimdoc_soname	libtree-sitter-vimdoc.so.3

%description
Tree-sitter parser for Vim help files.

%package devel
Summary:	Header files for tree-sitter-vimdoc
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-vimdoc.

%package static
Summary:	Static tree-sitter-vimdoc library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-vimdoc library.

%package -n neovim-parser-vimdoc
Summary:	Vim help files parser for Neovim
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-vimdoc
Vim help files parser for Neovim.

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

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/nvim/parser

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} %{_libdir}/%{ts_vimdoc_soname} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/vimdoc.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libtree-sitter-vimdoc.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{ts_vimdoc_soname}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtree-sitter-vimdoc.so
%{_includedir}/tree_sitter/tree-sitter-vimdoc.h
%{_pkgconfigdir}/tree-sitter-vimdoc.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-vimdoc.a

%files -n neovim-parser-vimdoc
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/vimdoc.so
