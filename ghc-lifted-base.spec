#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	lifted-base
Summary:	Lifted IO operations from the base library
Summary(pl.UTF-8):	Operacje IO podniesione z biblioteki base
Name:		ghc-%{pkgname}
Version:	0.2.3.12
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/lifted-base
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	fc74e75a2d8ab5171f801ba80c86ab82
URL:		http://hackage.haskell.org/package/lifted-base
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-base-unicode-symbols >= 0.1.1
BuildRequires:	ghc-monad-control >= 0.3
BuildRequires:	ghc-transformers-base >= 0.4
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-base-unicode-symbols-prof >= 0.1.1
BuildRequires:	ghc-monad-control-prof >= 0.3
BuildRequires:	ghc-transformers-base-prof >= 0.4
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-base-unicode-symbols >= 0.1.1
Requires:	ghc-monad-control >= 0.3
Requires:	ghc-transformers-base >= 0.4
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
Requires:	ghc-base-unicode-symbols-prof >= 0.1.1
Requires:	ghc-monad-control-prof >= 0.3
Requires:	ghc-transformers-base-prof >= 0.4

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
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSlifted-base-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSlifted-base-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSlifted-base-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/Chan
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/Chan/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/Chan/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/MVar
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/MVar/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/MVar/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/QSem
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/QSem/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/QSem/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/QSemN
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/QSemN/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/QSemN/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Marshal
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Marshal/Utils
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Marshal/Utils/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Marshal/Utils/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Timeout
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Timeout/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Timeout/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSlifted-base-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/Chan/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/MVar/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/QSem/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Concurrent/QSemN/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Exception/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/IORef/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Marshal/Utils/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Timeout/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
