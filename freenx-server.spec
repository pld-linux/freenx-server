Summary:	A free (GPL) implementation of the NX server
Summary(pl):	Darmowa (GPL) imlementacja serwera NX
Name:		freenx
Version:	0.5.0
%define cvs 2006-03-08-5
Release:	0.%(echo %{cvs} | tr '-' '.').1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://debian.tu-bs.de/knoppix/nx/snapshots/freenx-%{version}-test-%{cvs}.tar.gz
# Source0-md5:	db02370347fc31dd190db047f4481022
URL:		http://debian.tu-bs.de/knoppix/nx/
BuildRequires:	sed >= 4.0
Requires:	expect
Requires:	nc
Requires:	nx-X11
Requires:	xorg-app-xmessage
Requires:	xinitrc-ng
Requires:	openssh-server
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Provides:	user(nx)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 56k modem
dialup links or anything better.

This package contains a free (GPL) implementation of the nxserver
component.

%description -l pl
NoMachine NX to schemat kompresji dla X nowej generacji. Dzia³a na
zdalnych sesjach X11 nawet przy prêdko¶ci 56k i na ka¿dej szybszej.

Ten pakiet zawiera darmow± (GPL) implementacjê komponentu nxserwer.

%prep
%setup -q -n %{name}-%{version}-test-%{cvs}

#%build
# THIS ALL IS BROKEN. create .patch next time.
#sed -i -e 's#useradd -d $NX_HOME_DIR -s $(which nxserver) nx#useradd -d $NX_HOME_DIR -u 138 -s $(which nxserver) nx#g' nxsetup
#sed -i -e 's#NX_HOME_DIR=/home/.nx/#NX_HOME_DIR=%{_sysconfdir}/nxserver/#g' nxserver
#sed -i -e 's#netcat#nc#g' nxserver
#sed -i -e 's#export PATH#export LD_LIBRARY_PATH=%{_libdir}/NX/lib\nexport PATH#g' nxnode

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/nxserver
install node.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/nxserver/node.conf

install nx* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# FIXME: what group it should have?
%useradd -u 160 -d %{_sysconfdir}/nxserver -s %{_bindir}/nxserver -g users -c "FreeNX User" nx

%post
# FIXME: this displays usage. what it should do?
#%{_bindir}/nxsetup

%postun
if [ "$1" = "0" ]; then
    %userremove nx
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIB ChangeLog
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/nxserver
%config(noreplace) %{_sysconfdir}/nxserver/node.conf
