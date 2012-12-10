Summary: 	Line Control Server
Name: 		linesrv
Version: 	2.1.21
Release: 	%mkrel 10
# debian/copyright in the source suggests GPLv2 specifically applies
License: 	GPLv2
Group: 		Networking/Other
URL: 		http://linecontrol.sourceforge.net
Source: 	%{name}-%{version}.src.tar.bz2
Source1:	linesrv.init.bz2
Source2:	linesrv.conf.bz2
Source3:	linesrv-scripts.tar.bz2
Source4:	linesrv.conf.documentation.bz2
Patch0:		linesrv-2.1.21-debian-syslog_header.patch
Patch1:		linesrv-2.1.21-str-fmt.patch
Requires(pre): 	rpm-helper
BuildRoot: 	%{_tmppath}/%{name}-%{version}
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

%package web
Requires:	webserver
Requires:	linesrv
Group:		Networking/Other
Summary:	Line Control Server - Web Status

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
%patch0 -p1 -b .header
%patch1 -p0 -b .str
cp %{SOURCE4} .
bunzip2 `basename %{SOURCE4}`

%build

%configure2_5x
%make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}/{%{_sbindir},%{_bindir}}
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_mandir}/{man5,man8}
mkdir -p %{buildroot}/%{_sysconfdir}/pam.d
mkdir -p %{buildroot}/%{_libdir}/%{name}
mkdir -p %{buildroot}/%{_localstatedir}/www/cgi-bin/
install -m 755 -s server/%{name} %{buildroot}%{_sbindir}/
install -m 755 -s lclog/lclog %{buildroot}/%{_localstatedir}/www/cgi-bin/
install -m 4755 -s htmlstatus/htmlstatus %{buildroot}/%{_localstatedir}/www/cgi-bin/
bzcat %{SOURCE1} > %{buildroot}/%{_initrddir}/%{name}
chmod 755 %{buildroot}/%{_initrddir}/%{name}
install -m664 server/config/pam.d/l*  %{buildroot}/%{_sysconfdir}/pam.d/

bzcat %{SOURCE2} > %{buildroot}/%{_sysconfdir}/%{name}.conf
install -d -m755 %{buildroot}/%{_sysconfdir}/%{name}
install -m644 server/config/complete_syntax/addr_book %{buildroot}/%{_sysconfdir}/%{name}
install -m644 server/config/complete_syntax/tarif.conf %{buildroot}/%{_sysconfdir}/%{name}

# scripts
install -m755 scripts/*  %{buildroot}/%{_libdir}/%{name}

#web stuff
install -d %{buildroot}/%{_localstatedir}/www/html/lclog
install lclog/html/* %{buildroot}/%{_localstatedir}/www/html/lclog/
install -d %{buildroot}/%{_localstatedir}/lib/%{name}
mknod %{buildroot}/%{_localstatedir}/lib/%{name}/htmlstatus p

#logs:
install -d %{buildroot}/%{_localstatedir}/log/%{name}

#fix docs:
cp htmlstatus/README README.htmlstatus 
cp lclog/INSTALL INSTALL.lclog

%clean
rm -rf %{buildroot}

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
%{_localstatedir}/log/%{name}
%doc AUTHORS server/INSTALL server/COPYING server/NEWS server/README
%doc server/LICENSE INSTALL.lclog linesrv.conf.documentation

%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}

%files web
%defattr(-,root,root)
%{_localstatedir}/www/html/lclog/
%attr(4750,root,apache) %{_localstatedir}/www/cgi-bin/*
%dir %{_localstatedir}/lib/%{name}
%attr(640,root,apache) %{_localstatedir}/lib/%{name}/htmlstatus
%doc htmlstatus/README



%changelog
* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.21-10mdv2011.0
+ Revision: 645813
- relink against libmysqlclient.so.18

* Sun Jan 02 2011 Funda Wang <fwang@mandriva.org> 2.1.21-9mdv2011.0
+ Revision: 627616
- fix str fmt

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against mysql-5.5.8 libs, again
    - rebuilt against mysql-5.5.8 libs

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.21-5mdv2009.1
+ Revision: 311338
- rebuilt against mysql-5.1.30 libs

* Fri Sep 05 2008 Adam Williamson <awilliamson@mandriva.org> 2.1.21-4mdv2009.0
+ Revision: 281027
- don't use a silly name for the patch backup file...
- s,%%{_var},%%{_localstatedir}
- s,$RPM_BUILD_ROOT,%%{buildroot}
- restore the mysql build (seems to work...)
- add debian-syslog_header.patch from Debian: fixes a build error
- new license policy
- drop unnecessary defines

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix spacing at top of description
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Wed Sep 14 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.21-1mdk
- New release 2.1.21
- drop patch, fix conflict

* Thu Aug 21 2003 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.17-2mdk
- gcc3.3 fixes (Steffen)

* Fri Jul 25 2003 Steffen Barszus <st_barszus@gmx.de> 2.1.17-1mdk
- new version
- small fix for config 
- This is a temporary RPM for convinience for 9.1 users

* Mon May 26 2003 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.16-2mdk
- Make distriblint happy
- Fix permissions of scripts

* Mon Mar 03 2003 Buchan Milne <bgmilne@linux-mandrake.com> 2.1.16-1mdk
- Initial Mandrake RPM based on mserver
- Lots of work from Steffen Barzus on configs and scripts

