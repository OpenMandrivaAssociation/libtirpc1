%define major	1
%define libname	%mklibname tirpc %{major}
%define devname	%mklibname tirpc -d
%define static	%mklibname -d -s tirpc

%bcond_without	gss

Summary:	Old version of the Transport Independent RPC Library
Name:		libtirpc1
Version:	0.3.2
Release:	8
License:	SISSL and BSD
Group:		System/Libraries
Url:		http://sourceforge.net/projects/libtirpc
Source0:	http://downloads.sourceforge.net/libtirpc/libtirpc-%{version}.tar.bz2
# Related headers that were removed from glibc
Source10:	nis.h
Source11:	nis_tags.h
Source12:	nislib.h
Source13:	yp_prot.h
Source14:	ypclnt.h
Source15:	key_prot.h
Source16:	rpc_des.h
Patch1:		libtirpc-0.3.2-fix-undefined-symbol-__rpc_get_default_domain.patch
Patch2:		libtirpc-0.2.3-types.h.patch
Patch5:		libtirpc-0008-Add-rpcgen-program-from-nfs-utils-sources.patch
Patch6:		libtirpc-0.2.3-update-rpcgen-from-glibc.patch
Patch7:		rpcgen-compile.patch
Patch8:		libtirpc-0.3.0-sizeof.patch
# disabled as it breaks nfs etc.
#Patch8:	tirpc-xdr-update-from-glibc.patch
Patch10:	libtirpc-0002-uClibc-without-RPC-support-does-not-install-rpcent.h.patch
Patch12:	libtirpc-0010-Add-more-XDR-files-needed-to-build-rpcbind-on-top-of.patch
Patch13:	libtirpc-0.3.2-des_crypt.patch

BuildRequires:	libtool
%if %{with gss}
BuildRequires:	krb5-devel
%else
BuildConflicts:	krb5-devel
%endif
BuildRequires:	pkgconfig
BuildRequires:	autoconf
BuildRequires:	automake

%description
This package contains SunLib's implementation of transport-independent
RPC (TI-RPC) documentation.  This library forms a piece of the base of 
Open Network Computing (ONC), and is derived directly from the 
Solaris 2.3 source.

TI-RPC is an enhanced version of TS-RPC that requires the UNIX System V 
Transport Layer Interface (TLI) or an equivalent X/Open Transport Interface 
(XTI).  TI-RPC is on-the-wire compatible with the TS-RPC, which is supported 
by almost 70 vendors on all major operating systems.  TS-RPC source code 
(RPCSRC 4.0) remains available from several internet sites.

%package -n %{libname}
Summary:	Old version of the Transport Independent RPC Library
Group:		System/Libraries

%description -n	%{libname}
This package contains an old version of the shared library for %{name}.

It is for compatibility with legacy applications only and will be removed
in a future release.

%prep
%setup -qn libtirpc-%{version}
%apply_patches
autoreconf -fiv

install -m644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} tirpc/rpcsvc/
install -m644 %{SOURCE15} %{SOURCE16} tirpc/rpc/

%build
export CFLAGS="%{optflags} -fPIC"

%configure \
	--libdir=/%{_lib} \
	--enable-shared \
	--enable-static \
%if %{with gss}
	--enable-gssapi
%else
	--disable-gssapi
%endif

%make all

%install
%makeinstall_std
install -m 755 -d %{buildroot}%{_sysconfdir}
install -m 644 doc/netconfig %{buildroot}%{_sysconfdir}/netconfig
install -m644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{buildroot}%{_includedir}/tirpc/rpcsvc/
install -m644 %{SOURCE15} %{SOURCE16} %{buildroot}%{_includedir}/tirpc/rpc/

install -d %{buildroot}%{_includedir}/{rpc,rpcsvc}/
cd %{buildroot}%{_includedir}/tirpc/rpc
for i in *.h; do
	ln -sf ../tirpc/rpc/$i %{buildroot}%{_includedir}/rpc/$i
done
cd ../rpcsvc
for i in *.h; do
	ln -sf ../tirpc/rpcsvc/$i %{buildroot}%{_includedir}/rpcsvc/$i
done
cd %{buildroot}%{_includedir}
ln -s tirpc/netconfig.h .

install -d %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/libtirpc.a %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}
rm %{buildroot}/%{_lib}/libtirpc.so
ln -srf %{buildroot}/%{_lib}/libtirpc.so.%{major}.* %{buildroot}%{_libdir}/libtirpc.so

# Remove -devel files and anything else not needed in a compat package
rm -rf %{buildroot}%{_lib} \
	%{buildroot}%{_bindir} \
	%{buildroot}%{_libdir}/*.{a,so} \
	%{buildroot}%{_libdir}/pkgconfig \
	%{buildroot}%{_mandir} \
	%{buildroot}%{_includedir}

%files
%config(noreplace) %{_sysconfdir}/netconfig

%files -n %{libname}
/%{_lib}/libtirpc.so.%{major}*
