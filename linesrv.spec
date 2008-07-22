%define version 2.1.21
%define rel %mkrel 3

Summary: 	Line Control Server
Name: 		linesrv
Version: 	%version
Release: 	%rel
License: 	GPL
Group: 		Networking/Other
URL: 		http://linecontrol.sourceforge.net
Source: 	%{name}-%{version}.src.tar.bz2
Source1:	linesrv.init.bz2
Source2:	linesrv.conf.bz2
Source3:	linesrv-scripts.tar.bz2
Source4:	linesrv.conf.documentation.bz2
Requires(pre): 	rpm-helper
BuildRoot: 	%{_tmppath}/%{name}-%{version}
BuildRequires:	pam-devel 
#BuildRequires:	mysql-devel

%description
The line control system will allow authorized LAN users to manipulate
the network interface (usually a modem) that gives the Internet
access on a Linux box without having to use telnet. It's based on
a client/server approach so any TCP/IP enabled system should be able
to take advantage of this server, if a client is written for it.
Currently; Linux, Windows, NetBSD, and any system with a Java
implementation or Web Browser have clients.

Note: Please make changes to /etc/lineserv.conf.

%package web
Requires:	webserver linesrv
Group:          Networking/Other
Summary:        Line Control Server - Web Status

%description web
The line control system will allow authorized LAN users to manipulate
the network interface (usually a modem) that gives the Internet
access on a Linux box without having to use telnet. It's based on
a client/server approach so any TCP/IP enabled system should be able
to take advantage of this server, if a client is written for it.
Currently; Linux, Windows, NetBSD, and any system with a Java
implementation or Web Browser have clients.

This package provides web-based status report of the line.

%prep
%setup -q -n %{name}-%(echo %{version}|cut -f1-2 -d.) -a3
cp %{SOURCE4} .
bunzip2 `basename %{SOURCE4}`

%build

%configure --disable-mysql
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_sbindir},%{_bindir}}
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/{man5,man8}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/%{name}
mkdir -p %{buildroot}/%{_var}/www/cgi-bin/
install -m 755 -s server/%{name} $RPM_BUILD_ROOT%{_sbindir}/
install -m 755 -s lclog/lclog $RPM_BUILD_ROOT/%{_var}/www/cgi-bin/
install -m 4755 -s htmlstatus/htmlstatus %{buildroot}/%{_var}/www/cgi-bin/
bzcat %{SOURCE1} > $RPM_BUILD_ROOT/%{_initrddir}/%{name}
chmod 755 $RPM_BUILD_ROOT/%{_initrddir}/%{name}
install -m664 server/config/pam.d/l*  $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/

bzcat %{SOURCE2} > %{buildroot}/%{_sysconfdir}/%{name}.conf
install -d -m755 %{buildroot}/%{_sysconfdir}/%{name}
install -m644 server/config/complete_syntax/addr_book %{buildroot}/%{_sysconfdir}/%{name}
install -m644 server/config/complete_syntax/tarif.conf %{buildroot}/%{_sysconfdir}/%{name}

# scripts
install -m755 scripts/*  %{buildroot}/%{_libdir}/%{name}

#web stuff
install -d %{buildroot}/%{_var}/www/html/lclog
install lclog/html/* %{buildroot}/%{_var}/www/html/lclog/
install -d %{buildroot}/%{_localstatedir}/lib/%{name}
mknod %{buildroot}/%{_localstatedir}/lib/%{name}/htmlstatus p

#logs:
install -d %{buildroot}/%{_var}/log/%{name}

#fix docs:
cp htmlstatus/README README.htmlstatus 
cp lclog/INSTALL INSTALL.lclog

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_initrddir}/%{name}
%{_sbindir}/%{name}
%{_libdir}/%{name}
%{_var}/log/%{name}
%doc AUTHORS server/INSTALL server/COPYING server/NEWS server/README
%doc server/LICENSE INSTALL.lclog linesrv.conf.documentation

%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}

%files web
%defattr(-,root,root)
%{_var}/www/html/lclog/
%attr(4750,root,apache) %{_var}/www/cgi-bin/*
%dir %{_localstatedir}/lib/%{name}
%attr(640,root,apache) %{_localstatedir}/lib/%{name}/htmlstatus
%doc htmlstatus/README

