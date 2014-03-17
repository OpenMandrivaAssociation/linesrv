Summary:	Line Control Server
Name:		linesrv
Version:	2.1.21
Release:	11
# debian/copyright in the source suggests GPLv2 specifically applies
License:	GPLv2+
Group:		Networking/Other
Url:		http://linecontrol.sourceforge.net
Source0:	%{name}-%{version}.src.tar.bz2
Source1:	linesrv.init.bz2
Source2:	linesrv.conf.bz2
Source3:	linesrv-scripts.tar.bz2
Source4:	linesrv.conf.documentation.bz2
Patch0:		linesrv-2.1.21-debian-syslog_header.patch
Patch1:		linesrv-2.1.21-str-fmt.patch
Requires(pre):	rpm-helper
BuildRequires:	pam-devel
BuildRequires:	mysql-devel

%description
The line control system will allow authorized LAN users to manipulate
the network interface (usually a modem) that gives the Internet
access on a Linux box without having to use telnet. It's based on
a client/server approach so any TCP/IP enabled system should be able
to take advantage of this server, if a client is written for it.
Currently; Linux, Windows, NetBSD, and any system with a Java
implementation or Web Browser have clients.

Note: Please make changes to /etc/lineserv.conf.

%files
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_initrddir}/%{name}
%{_sbindir}/%{name}
%{_libdir}/%{name}
%{_localstatedir}/log/%{name}
%doc AUTHORS server/INSTALL server/COPYING server/NEWS server/README
%doc server/LICENSE INSTALL.lclog linesrv.conf.documentation
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

#----------------------------------------------------------------------------

%package web
Summary:	Line Control Server - Web Status
Group:		Networking/Other
Requires:	webserver
Requires:	linesrv

%description web
The line control system will allow authorized LAN users to manipulate
the network interface (usually a modem) that gives the Internet
access on a Linux box without having to use telnet. It's based on
a client/server approach so any TCP/IP enabled system should be able
to take advantage of this server, if a client is written for it.
Currently; Linux, Windows, NetBSD, and any system with a Java
implementation or Web Browser have clients.

This package provides web-based status report of the line.

%files web
%{_localstatedir}/www/html/lclog/
%attr(4750,root,apache) %{_localstatedir}/www/cgi-bin/*
%dir %{_localstatedir}/lib/%{name}
%attr(640,root,apache) %{_localstatedir}/lib/%{name}/htmlstatus
%doc htmlstatus/README

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%(echo %{version}|cut -f1-2 -d.) -a3
%patch0 -p1 -b .header
%patch1 -p0 -b .str
cp %{SOURCE4} .
bunzip2 `basename %{SOURCE4}`

%build
%configure2_5x
%make

%install
mkdir -p %{buildroot}{%{_sbindir},%{_bindir}}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_mandir}/{man5,man8}
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/www/cgi-bin/
install -m 755 server/%{name} %{buildroot}%{_sbindir}/
install -m 755 lclog/lclog %{buildroot}%{_localstatedir}/www/cgi-bin/
install -m 4755 htmlstatus/htmlstatus %{buildroot}%{_localstatedir}/www/cgi-bin/
bzcat %{SOURCE1} > %{buildroot}%{_initrddir}/%{name}
chmod 755 %{buildroot}/%{_initrddir}/%{name}
install -m664 server/config/pam.d/l*  %{buildroot}/%{_sysconfdir}/pam.d/

bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/%{name}.conf
install -d -m755 %{buildroot}%{_sysconfdir}/%{name}
install -m644 server/config/complete_syntax/addr_book %{buildroot}%{_sysconfdir}/%{name}
install -m644 server/config/complete_syntax/tarif.conf %{buildroot}%{_sysconfdir}/%{name}

# scripts
install -m755 scripts/*  %{buildroot}%{_libdir}/%{name}

#web stuff
install -d %{buildroot}%{_localstatedir}/www/html/lclog
install lclog/html/* %{buildroot}%{_localstatedir}/www/html/lclog/
install -d %{buildroot}%{_localstatedir}/lib/%{name}
mknod %{buildroot}%{_localstatedir}/lib/%{name}/htmlstatus p

#logs:
install -d %{buildroot}%{_localstatedir}/log/%{name}

#fix docs:
cp htmlstatus/README README.htmlstatus 
cp lclog/INSTALL INSTALL.lclog

