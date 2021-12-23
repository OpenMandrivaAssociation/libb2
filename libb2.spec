%global major 1
%global libname %mklibname b 2 %{major}
%global devname %mklibname b 2 -d

%global optflags %{optflags} -O3

# (tpg) enable PGO build
%bcond_without pgo

Summary:	C library providing BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp
Name:		libb2
Version:	0.98.1
Release:	4
License:	CC0
Group:		Development/C
Url:		https://blake2.net/
Source0:	https://github.com/BLAKE2/libb2/releases/download/v%{version}/libb2-%{version}.tar.gz
BuildRequires:	autoconf-archive

%description
BLAKE2 is a cryptographic hash function faster than MD5, SHA-1, SHA-2, and
SHA-3, yet is at least as secure as the latest standard SHA-3.

%package -n %{libname}
Summary:	C library providing BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp
Group:		System/Libraries

%description -n %{libname}
BLAKE2 is a cryptographic hash function faster than MD5, SHA-1, SHA-2, and
SHA-3, yet is at least as secure as the latest standard SHA-3.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	blake2-devel = %{version}-%{release}

%description -n %{devname}
Development files and headers for BLAKE2.

%prep
%autosetup -p1

sed -e 's|CFLAGS=-O3|CFLAGS="%{optflags}"|g' -i configure.ac
autoreconf -vfi

%build

%if %{with pgo}
export LD_LIBRARY_PATH="$(pwd)"

CFLAGS="%{optflags} -fprofile-generate" \
CXXFLAGS="%{optflags} -fprofile-generate" \
LDFLAGS="%{build_ldflags} -fprofile-generate" \
%configure \
	--disable-static \
	--disable-native

%make_build

make check

unset LD_LIBRARY_PATH
llvm-profdata merge --output=%{name}-llvm.profdata $(find . -name "*.profraw" -type f)
PROFDATA="$(realpath %{name}-llvm.profdata)"
rm -f *.profraw
make clean

CFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
CXXFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
LDFLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
%endif
%configure \
	--disable-static \
	--disable-native

%make_build

%install
%make_install

# we don't want these
find %{buildroot} -name "*.la" -delete

%check
%make_build check

%files -n %{libname}
%{_libdir}/libb2.so.%{major}{,.*}

%files -n %{devname}
%license COPYING
%{_includedir}/blake2.h
%{_libdir}/libb2.so
%{_libdir}/pkgconfig/libb2.pc
