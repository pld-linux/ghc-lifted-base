#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	lifted-base
Summary:	Lifted IO operations from the base library
Summary(pl.UTF-8):	Operacje IO podniesione z biblioteki base
Name:		ghc-%{pkgname}
Version:	0.2.1.1
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/lifted-base
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	8fc0e62111c97a051b51bbf5e3484244
URL:		http://hackage.haskell.org/package/lifted-base
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-base-unicode-symbols >= 0.1.1
BuildRequires:	ghc-base-unicode-symbols < 0.3
BuildRequires:	ghc-monad-control >= 0.3
BuildRequires:	ghc-monad-control < 0.4
BuildRequires:	ghc-transformers-base >= 0.4
BuildRequires:	ghc-transformers-base < 0.5
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-base-unicode-symbols-prof >= 0.1.1
BuildRequires:	ghc-base-unicode-symbols-prof < 0.3
BuildRequires:	ghc-monad-control-prof >= 0.3
BuildRequires:	ghc-monad-control-prof < 0.4
BuildRequires:	ghc-transformers-base-prof >= 0.4
BuildRequires:	ghc-transformers-base-prof < 0.5
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-base < 5
Requires:	ghc-base-unicode-symbols >= 0.1.1
Requires:	ghc-base-unicode-symbols < 0.3
Requires:	ghc-monad-control >= 0.3
Requires:	ghc-monad-control < 0.4
Requires:	ghc-transformers-base >= 0.4
Requires:	ghc-transformers-base < 0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
lifted-base exports IO operations from the base library lifted to any
instance of MonadBase or MonadBaseControl.

%description -l pl.UTF-8
lifted-base eksportuje operacje IO z biblioteki base podniesione do
dowolnej instancji MonadBase lub MonadBaseControl.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-base-prof < 5
Requires:	ghc-base-unicode-symbols-prof >= 0.1.1
Requires:	ghc-base-unicode-symbols-prof < 0.3
Requires:	ghc-monad-control-prof >= 0.3
Requires:	ghc-monad-control-prof < 0.4
Requires:	ghc-transformers-base-prof >= 0.4
Requires:	ghc-transformers-base-prof < 0.5

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE README.markdown
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSlifted-base-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSlifted-base-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/Lifted.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/Chan
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/Chan/Lifted.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/MVar
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/MVar/Lifted.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception/Lifted.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef/Lifted.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Timeout
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Timeout/Lifted.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSlifted-base-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/Lifted.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/Chan/Lifted.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/MVar/Lifted.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception/Lifted.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef/Lifted.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Timeout/Lifted.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
