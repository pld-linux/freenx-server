Summary:	A free (GPL) implementation of the NX server
Summary(pl):	Darmowa (GPL) imlementacja serwera NX
Name:		freenx
Version:	0.2.8
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://debian.tu-bs.de/knoppix/nx/%{name}-%{version}.tar.gz
# Source0-md5:	db4c4a9f91619f4d9ac30fdea10925e8
URL:		http://debian.tu-bs.de/knoppix/nx/
BuildRequires:	sed >= 4.0
Requires:	expect
Requires:	nc
Requires:	nx-X11
Requires:	openssh-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 56k modem
dialup links or anything better.

This package contains a free (GPL) implementation of the nxserver
component.

%description -l pl
NoMachine NX to schemat kompresji dla X nowej generacji. Dzia³a na
zdalnych sesjach X11 nawet przy prêdko¶ci 56k albo szybszej.

Ten pakiet zawiera darmow± (GPL) implementacjê komponentu nxserwer.

%prep
%setup -q

%build
sed -i -e 's#useradd -d $NX_HOME_DIR -s $(which nxserver) nx#useradd -d $NX_HOME_DIR -u 138 -s $(which nxserver) nx#g' nxsetup
sed -i -e 's#NX_HOME_DIR=/home/.nx/#NX_HOME_DIR=%{_sysconfdir}/nxserver/#g' nxserver
sed -i -e 's#netcat#nc#g' nxserver
sed -i -e 's#export PATH#export LD_LIBRARY_PATH=%{_libdir}/NX/lib\nexport PATH#g' nxnode

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/nxserver

install nx* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/nxsetup

%postun
if [ "$1" = "0" ]; then
    %userremove nx
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIB ChangeLog
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/nxserver
