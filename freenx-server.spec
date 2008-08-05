# TODO
# - nxserver-helper ?
Summary:	A free (GPL) implementation of the NX server
Summary(pl.UTF-8):	Darmowa (GPL) imlementacja serwera NX
Name:		freenx
Version:	0.7.1
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://download.berlios.de/freenx/%{name}-%{version}.tar.gz
# Source0-md5:	80e7a57f787daabd0f80dfe8f58e67d3
Patch0:		%{name}-node-conf.patch
URL:		http://freenx.berlios.de/
BuildRequires:	sed >= 4.0
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	bc
Requires:	expect
Requires:	nc
Requires:	nx-X11
Requires:	openssh-clients
Requires:	openssh-server
Requires:	xinitrc-ng
Requires:	xorg-app-xauth
Requires:	xorg-app-xmessage
Requires:	xorg-lib-libXcomposite
Provides:	user(nx)
Suggests:	rdesktop
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 56k modem
dialup links or anything better.

This package contains a free (GPL) implementation of the nxserver
component.

%description -l pl.UTF-8
NoMachine NX to schemat kompresji dla X nowej generacji. Działa na
zdalnych sesjach X11 nawet przy prędkości 56k i na każdej szybszej.

Ten pakiet zawiera darmową (GPL) implementację komponentu nxserwer.

%prep
%setup -q
%patch0 -p1

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

install nxcheckload.sample $RPM_BUILD_ROOT%{_bindir}/nxcheckload
install nxcups-gethost nxdesktop_helper nxdialog nxkeygen nxloadconfig nxnode nxnode-login nxprint nxserver nxsetup $RPM_BUILD_ROOT%{_bindir}

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nxserver/node.conf
