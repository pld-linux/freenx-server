# TODO
# - nxserver-helper ?
Summary:	A free (GPL) implementation of the NX server
Summary(pl.UTF-8):	Darmowa (GPL) imlementacja serwera NX
Name:		freenx-server
Version:	0.7.2
Release:	1.3
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://download.berlios.de/freenx/%{name}-%{version}.tar.gz
# Source0-md5:	961913bb82ee6e60d8df6f10e647bda9
Source1:	%{name}.init
Patch0:		freenx-node-conf.patch
Patch1:		%{name}-nx-3.2.0.patch
URL:		http://freenx.berlios.de/
BuildRequires:	sed >= 4.0
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	bc
Requires:	binutils
Requires:	expect
Requires:	nc
Requires:	nx-X11
Requires:	openssh-clients
Requires:	openssh-server
Requires:	openssl-tools
Requires:	xinitrc-ng
Requires:	xorg-app-sessreg
Requires:	xorg-app-xauth
Requires:	xorg-app-xmessage
Requires:	xorg-lib-libXcomposite
Suggests:	cups-backend-smb
Suggests:	gnome-session
Suggests:	kdebase-desktop
Suggests:	openssl-tools
Suggests:	rdesktop
Suggests:	samba-clients
Suggests:	xorg-app-sessreg
Suggests:	xterm
Provides:	user(nx)
Obsoletes:	freenx
Conflicts:	freenx
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
%patch1 -p1

%if "%{_lib}" == "lib64"
%{__sed} -i -e 's/PATH_LIB=$NX_DIR\/lib/PATH_LIB=$NX_DIR\/lib64/' nxloadconfig
%endif

%build
%{__make}

# THIS ALL IS BROKEN. create .patch next time.
#sed -i -e 's#useradd -d $NX_HOME_DIR -s $(which nxserver) nx#useradd -d $NX_HOME_DIR -u 138 -s $(which nxserver) nx#g' nxsetup
#sed -i -e 's#NX_HOME_DIR=/home/.nx/#NX_HOME_DIR=%{_sysconfdir}/nxserver/#g' nxserver
#sed -i -e 's#netcat#nc#g' nxserver
#sed -i -e 's#export PATH#export LD_LIBRARY_PATH=%{_libdir}/NX/lib\nexport PATH#g' nxnode

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/nxserver
install node.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/nxserver/node.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/freenx

install nxcheckload.sample $RPM_BUILD_ROOT%{_bindir}/nxcheckload
install nxcups-gethost nxdesktop_helper nxdialog nxkeygen nxloadconfig nxnode nxnode-login nxprint nxserver nxserver-helper/nxserver-helper nxsetup nxviewer_helper nxviewer-passwd/nxpasswd/nxpasswd $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 160 -d %{_sysconfdir}/nxserver -s %{_bindir}/nxserver -g users -c "FreeNX User" nx

%post
/sbin/chkconfig --add freenx
%service freenx restart

%preun
if [ "$1" = "0" ]; then
%service freenx stop
/sbin/chkconfig --del freenx
fi

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
%attr(754,root,root) /etc/rc.d/init.d/freenx
