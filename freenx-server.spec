Summary:	A free (GPL) implementation of the NX server.
Summary(pl):	Darmowa (GPL) imlementacja serwera NX.
Name:		freenx
Version:	0.2.6
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://debian.tu-bs.de/knoppix/nx/%{name}-%{version}.tar.gz
# Source0-md5:	c2f976a4940496353f63e5739f30dda4
URL:		http://debian.tu-bs.de/knoppix/nx/
Requires:	nx-X11
Requires:	expect
Requires:	nc
Requires:	openssh-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 56k modem
dialup links or anything better.

This package contains a free (GPL) implementation of the nxserver
component.

%description -l pl
NoMachine NX to schemat kompresji dla X nowej generacji. Dziala na
zdalnych sesjach X11 nawet przy predkosci 56k albo szybszej.

Ten pakiet zawiera darmowa (GPL) implementacje komponentu nxserwer.

%prep
%setup -q -n %{name}-%{version}

%build
sed -i -e 's#useradd -d $NX_HOME_DIR -s $(which nxserver) nx#useradd -d $NX_HOME_DIR -u 138 -s $(which nxserver) nx#g' nxsetup
sed -i -e 's#NX_HOME_DIR=/home/.nx/#NX_HOME_DIR=/home/services/nx/#g' nxserver
sed -i -e 's#netcat#nc#g' nxserver
sed -i -e 's#export PATH#export LD_LIBRARY_PATH=%{_libdir}/NX/lib\nexport PATH#g' nxnode

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_bindir}
cp nx* $RPM_BUILD_ROOT/%{_bindir}
chmod 755 $RPM_BUILD_ROOT/%{_bindir}/nxclient \
    $RPM_BUILD_ROOT/%{_bindir}/nxnode \
    $RPM_BUILD_ROOT/%{_bindir}/nxserver \
    $RPM_BUILD_ROOT/%{_bindir}/nxkeygen \
    $RPM_BUILD_ROOT/%{_bindir}/nxnode-login \
    $RPM_BUILD_ROOT/%{_bindir}/nxsetup

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
%doc AUTHORS COPYING ChangeLog
%attr(755,root,root) %{_bindir}/*
