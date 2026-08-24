%global libname %mklibname b2
%global oldlibname %mklibname b2 1
%global devname %mklibname -d b2

Summary:	C library providing BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp
Name:		libb2
Version:	0.98.1
Release:	7
License:	CC0
Group:		Development/C
Url:		https://blake2.net/
Source0:	https://github.com/BLAKE2/libb2/releases/download/v%{version}/libb2-%{version}.tar.gz

BuildSystem:	autotools
# Default --enable-native adds -march=native (wrong for a distro package)
# and is also the only path that selects the SSE sources. Use fat dispatch
# on x86_64 instead; other arches stay on the portable reference C.
BuildOption:	--disable-native
%ifarch %{x86_64}
BuildOption:	--enable-fat
%endif
BuildRequires:	automake
BuildRequires:	autoconf-archive

%description
BLAKE2 is a cryptographic hash function faster than MD5, SHA-1, SHA-2, and
SHA-3, yet is at least as secure as the latest standard SHA-3.

%package -n %{libname}
Summary:	C library providing BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
BLAKE2 is a cryptographic hash function faster than MD5, SHA-1, SHA-2, and
SHA-3, yet is at least as secure as the latest standard SHA-3.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	blake2-devel = %{EVRD}

%description -n %{devname}
Development files and headers for BLAKE2.

%prep -a
# configure.ac does CFLAGS=-O3, which drops distro (and PGO) flags
sed -i -e '/AX_CHECK_COMPILE_FLAG(\[-O3\], \[CFLAGS=-O3\])/d' configure.ac

%pgo
%make_build -C _OMV_rpm_build check LIBTOOL=slibtool-shared

%if ! %{cross_compiling}
%check
%make_build -C _OMV_rpm_build check LIBTOOL=slibtool-shared
%endif

%files -n %{libname}
%{_libdir}/libb2.so.*

%files -n %{devname}
%license COPYING
%{_includedir}/blake2.h
%{_libdir}/libb2.so
%{_libdir}/pkgconfig/libb2.pc
