# Version of ssh-askpass
%define aversion 1.2.4.1

# Do we want to disable building of x11-askpass? (1=yes 0=no)
%define no_x11_askpass 1

# Do we want to disable building of gnome-askpass? (1=yes 0=no)
%define no_gnome_askpass 1

# Do we want to link against a static libcrypto? (1=yes 0=no)
%define static_libcrypto 0

# Do we want smartcard support (1=yes 0=no)
%define scard 0

# Is this build for RHL 6.x?
%define build6x 0

# Disable IPv6 (avoids DNS hangs on some glibc versions)
%define noip6 0

# Reserve options to override askpass settings with:
# rpm -ba|--rebuild --define 'skip_xxx 1'
%{?skip_x11_askpass:%define no_x11_askpass 1}
%{?skip_gnome_askpass:%define no_gnome_askpass 1}

# Is this a build for RHL 6.x or earlier?
%{?build_6x:%define build6x 1}

# If this is RHL 6.x, the default configuration has sysconfdir in /usr/etc.
%if %{build6x}
%define _sysconfdir /etc
%define noip6 1
%endif

# Options for static OpenSSL link:
# rpm -ba|--rebuild --define "static_openssl 1"
%{?static_openssl:%define static_libcrypto 1}

# Options for Smartcard support: (needs libsectok and openssl-engine)
# rpm -ba|--rebuild --define "smartcard 1"
%{?smartcard:%define scard 1}

# Option to disable ipv6
# rpm -ba|--rebuild --define "noipv6 1"
%{?noipv6:%define noip6 1}

# Is this a build for the rescue CD (without PAM, with MD5)? (1=yes 0=no)
%define rescue 0
%{?build_rescue:%define rescue 1}

Summary: The OpenSSH implementation of SSH.
Name: openssh
Version: 3.4p1
%if %{rescue}
Release: 1rescue
%else
Release: 1
%endif
URL: http://www.openssh.com/portable.html
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1: http://www.pobox.com/~jmknoble/software/x11-ssh-askpass/x11-ssh-askpass-%{aversion}.tar.gz
Source2: openssh.init
Source3: gnome-ssh-askpass.sh
Source4: gnome-ssh-askpass.csh
Source5: openssh-closing.txt
Patch0: openssh-SNAP-20020220-redhat.patch
Patch1: openssh-2.3.0p1-path.patch
Patch2: openssh-2.9p1-groups.patch
Patch3: openssh-3.1p1-defaultkeys.patch
Patch4: openssh-adv.iss.patch
Patch11: http://www.sxw.org.uk/computing/patches/openssh-mit-krb5-20020326.diff
Patch12: http://www.sxw.org.uk/computing/patches/openssh-3.1p1-gssapi-20020325.diff
Patch13: http://bugzilla.mindrot.org/showattachment.cgi?attach_id=37
License: BSD
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Obsoletes: ssh
%if %{build6x}
PreReq: initscripts >= 5.00
%else
PreReq: initscripts >= 5.20
%endif
BuildPreReq: perl, openssl-devel, sharutils, tcp_wrappers
BuildPreReq: /bin/login
%if %{build6x}
BuildPreReq: glibc-devel, pam
%else
BuildPreReq: /usr/include/security/pam_appl.h
%endif
BuildPrereq: autoconf
%if ! %{no_x11_askpass}
BuildPreReq: XFree86-devel
%endif
%if ! %{no_gnome_askpass}
BuildPreReq: gnome-libs-devel, db1-devel
%endif

%package clients
Summary: OpenSSH clients.
Requires: openssh = %{version}-%{release}
Group: Applications/Internet
Obsoletes: ssh-clients

%package server
Summary: The OpenSSH server daemon.
Group: System Environment/Daemons
Obsoletes: ssh-server
PreReq: openssh = %{version}-%{release}, chkconfig >= 0.9
%if ! %{build6x}
Requires: /etc/pam.d/system-auth
%endif

%package askpass
Summary: A passphrase dialog for OpenSSH and X.
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: ssh-extras

%package askpass-gnome
Summary: A passphrase dialog for OpenSSH, X, and GNOME.
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: ssh-extras

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features, as well as removing
all patented algorithms to separate libraries.

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.
You'll also need to install the openssh package on OpenSSH clients.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server. You also need to have the openssh
package installed.

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%description askpass-gnome
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH and the GNOME GUI desktop
environment.

%prep

%if ! %{no_x11_askpass}
%setup -q -a 1
%else
%setup -q
%endif
%patch0 -p1 -b .redhat
#%patch1 -p1 -b .path
%patch2 -p1 -b .groups
#%patch3 -p0 -b .defaultkeys
#%patch4 -p0 -b .adv.iss

%if %{build6x}
%patch13 -p0 -b .openssl095a
%endif

# Apply gss-specific patches only if the release tag includes "gss".  (Not
# to be used for actual releases until it's in the mainline.)
if echo "%{release}" | grep -q gss; then
%patch11 -p0 -b .krb5
%patch12 -p1 -b .gssapi
autoreconf-2.53
fi

%build
%if %{rescue}
CFLAGS="$RPM_OPT_FLAGS -Os"; export CFLAGS
%endif

# Only enable Kerberos support if we applied a patch for GSSAPI support.
moreflags=
if echo "%{release}" | grep -q gss; then
moreflags=--with-kerberos5=/usr/kerberos
fi

%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
	--with-tcp-wrappers \
	--with-rsh=%{_bindir}/rsh \
%if %{scard}
	--with-smartcard \
%endif
%if %{noip6}
	--with-ipv4-default \
%endif
%if %{build6x}
	--with-ipv4-default \
%endif
%if %{rescue}
	--without-pam --with-md5-passwords $moreflags
%else
	--with-pam $moreflags
%endif

%if %{static_libcrypto}
perl -pi -e "s|-lcrypto|%{_libdir}/libcrypto.a|g" Makefile
%endif

make

%if ! %{no_x11_askpass}
pushd x11-ssh-askpass-%{aversion}
# This configure can't handle platform strings.
./configure --prefix=%{_prefix} --libexecdir=%{_libexecdir}/openssh
xmkmf -a
make
popd
%endif

%if ! %{no_gnome_askpass}
pushd contrib
gcc $RPM_OPT_FLAGS `gnome-config --cflags gnome gnomeui` \
        gnome-ssh-askpass.c -o gnome-ssh-askpass \
        `gnome-config --libs gnome gnomeui`
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
%if ! %{build6x}
install -m644 contrib/redhat/sshd.pam $RPM_BUILD_ROOT/etc/pam.d/sshd
%else
install -m644 contrib/redhat/sshd.pam     $RPM_BUILD_ROOT/etc/pam.d/sshd
%endif
install -m755 $RPM_SOURCE_DIR/openssh.init $RPM_BUILD_ROOT/etc/rc.d/init.d/sshd

%if ! %{no_x11_askpass}
install -s x11-ssh-askpass-%{aversion}/x11-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/x11-ssh-askpass
ln -s x11-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/ssh-askpass
%endif

%if ! %{no_gnome_askpass}
install -s contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass
%endif

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

%clean
rm -rf $RPM_BUILD_ROOT

%triggerun server -- ssh-server
if [ "$1" != 0 -a -r /var/run/sshd.pid ] ; then
	touch /var/run/sshd.restart
fi

%triggerun server -- openssh-server < 2.5.0p1
# Count the number of HostKey and HostDsaKey statements we have.
gawk	'BEGIN {IGNORECASE=1}
	 /^hostkey/ || /^hostdsakey/ {sawhostkey = sawhostkey + 1}
	 END {exit sawhostkey}' /etc/ssh/sshd_config
# And if we only found one, we know the client was relying on the old default
# behavior, which loaded the the SSH2 DSA host key when HostDsaKey wasn't
# specified.  Now that HostKey is used for both SSH1 and SSH2 keys, specifying
# one nullifies the default, which would have loaded both.
if [ $? -eq 1 ] ; then
	echo HostKey /etc/ssh/ssh_host_rsa_key >> /etc/ssh/sshd_config
	echo HostKey /etc/ssh/ssh_host_dsa_key >> /etc/ssh/sshd_config
fi

%triggerpostun server -- ssh-server
if [ "$1" != 0 ] ; then
	/sbin/chkconfig --add sshd
	if test -f /var/run/sshd.restart ; then
		rm -f /var/run/sshd.restart
		/sbin/service sshd start > /dev/null 2>&1 || :
	fi
fi

%pre server
grep "^sshd:" %{_sysconfdir}/group >/dev/null || groupadd -g 94 sshd
grep "^sshd:" %{_sysconfdir}/passwd >/dev/null || useradd -u 94 -g 94 -s /bin/true -M -r sshd
mkdir /var/empty

%post server
/sbin/chkconfig --add sshd

%postun server
/sbin/service sshd condrestart > /dev/null 2>&1 || :

%preun server
if [ "$1" = 0 ]
then
	/sbin/service sshd stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del sshd
fi

%files
%defattr(-,root,root)
%doc CREDITS ChangeLog INSTALL LICENCE OVERVIEW README* RFC* TODO WARNING*
%attr(0755,root,root) %{_bindir}/scp
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%endif
%if %{scard}
%attr(0755,root,root) %dir %{_datadir}/openssh
%attr(0644,root,root) %{_datadir}/openssh/Ssh.bin
%endif

%files clients
%defattr(-,root,root)
%attr(4755,root,root) %{_bindir}/ssh
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(-,root,root) %{_bindir}/slogin
%attr(-,root,root) %{_mandir}/man1/slogin.1*
%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%endif

%if ! %{rescue}
%files server
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0600,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0755,root,root) %config /etc/rc.d/init.d/sshd
%endif

%if ! %{no_x11_askpass}
%files askpass
%defattr(-,root,root)
%doc x11-ssh-askpass-%{aversion}/README
%doc x11-ssh-askpass-%{aversion}/ChangeLog
%doc x11-ssh-askpass-%{aversion}/SshAskpass*.ad
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-askpass
%attr(0755,root,root) %{_libexecdir}/openssh/x11-ssh-askpass
%endif

%if ! %{no_gnome_askpass}
%files askpass-gnome
%defattr(-,root,root)
%attr(0755,root,root) %config %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%endif

%changelog

* Mon Jul 1 2002 Kurt Seifried <kurt@seifried.org> 3.4p1
- creates sshd user and group, creates /var/empty directory
- imported openssh-3.4p1 portable source, removed various conflicting patches
- turned off askpass, gnome stuff, this rpm is aimed at servers
- USE AT YOUR OWN RISK

* Wed Jun 26 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-6
- rebuild

* Wed Jun 26 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-5
- include patch from Markus's ISS advisory for missing bounds checks
- re-require db1-devel
- re-require pam-devel by package file
- re-require autoconf instead of autoconf253
- make sure Kerberos is disabled unless the not-enabled gssapi patch was applied

* Wed May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-4
- drop buildreq on db1-devel
- require pam-devel by package name
- require autoconf instead of autoconf253 again

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-3
- pull patch from CVS to avoid printing error messages when some of the
  default keys aren't available when running ssh-add
- refresh to current revisions of Simon's patches
 
* Thu Mar 21 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-2gss
- reintroduce Simon's gssapi patches
- add buildprereq for autoconf253, which is needed to regenerate configure
  after applying the gssapi patches
- refresh to the latest version of Markus's patch to build properly with
  older versions of OpenSSL

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-2
- bump and grind (through the build system)

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-1
- require sharutils for building (mindrot #137)
- require db1-devel only when building for 6.x (#55105), which probably won't
  work anyway (3.1 requires OpenSSL 0.9.6 to build), but what the heck
- require pam-devel by file (not by package name) again
- add Markus's patch to compile with OpenSSL 0.9.5a (from
  http://bugzilla.mindrot.org/show_bug.cgi?id=141) and apply it if we're
  building for 6.x

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-0
- update to 3.1p1

* Tue Mar  5 2002 Nalin Dahyabhai <nalin@redhat.com> SNAP-20020305
- update to SNAP-20020305
- drop debug patch, fixed upstream

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> SNAP-20020220
- update to SNAP-20020220 for testing purposes (you've been warned, if there's
  anything to be warned about, gss patches won't apply, I don't mind)

* Wed Feb 13 2002 Nalin Dahyabhai <nalin@redhat.com> 3.0.2p1-3
- add patches from Simon Wilkinson and Nicolas Williams for GSSAPI key
  exchange, authentication, and named key support

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 3.0.2p1-2
- remove dependency on db1-devel, which has just been swallowed up whole
  by gnome-libs-devel

* Sun Dec 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- adjust build dependencies so that build6x actually works right (fix
  from Hugo van der Kooij)

* Tue Dec  4 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0.2p1-1
- update to 3.0.2p1

* Fri Nov 16 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0.1p1-1
- update to 3.0.1p1

* Tue Nov 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to current CVS (not for use in distribution)

* Thu Nov  8 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0p1-1
- merge some of Damien Miller <djm@mindrot.org> changes from the upstream
  3.0p1 spec file and init script

* Wed Nov  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.0p1
- update to x11-ssh-askpass 1.2.4.1
- change build dependency on a file from pam-devel to the pam-devel package
- replace primes with moduli

* Thu Sep 27 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9p2-9
- incorporate fix from Markus Friedl's advisory for IP-based authorization bugs

* Thu Sep 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.9p2-8
- Merge changes to rescue build from current sysadmin survival cd

* Thu Sep  6 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9p2-7
- fix scp's server's reporting of file sizes, and build with the proper
  preprocessor define to get large-file capable open(), stat(), etc.
  (sftp has been doing this correctly all along) (#51827)
- configure without --with-ipv4-default on RHL 7.x and newer (#45987,#52247)
- pull cvs patch to fix support for /etc/nologin for non-PAM logins (#47298)
- mark profile.d scriptlets as config files (#42337)
- refer to Jason Stone's mail for zsh workaround for exit-hanging quasi-bug
- change a couple of log() statements to debug() statements (#50751)
- pull cvs patch to add -t flag to sshd (#28611)
- clear fd_sets correctly (one bit per FD, not one byte per FD) (#43221)

* Mon Aug 20 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9p2-6
- add db1-devel as a BuildPrerequisite (noted by Hans Ecke)

* Thu Aug 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- pull cvs patch to fix remote port forwarding with protocol 2

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- pull cvs patch to add session initialization to no-pty sessions
- pull cvs patch to not cut off challengeresponse auth needlessly
- refuse to do X11 forwarding if xauth isn't there, handy if you enable
  it by default on a system that doesn't have X installed (#49263)

* Wed Aug  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't apply patches to code we don't intend to build (spotted by Matt Galgoci)

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- pass OPTIONS correctly to initlog (#50151)

* Wed Jul 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- switch to x11-ssh-askpass 1.2.2

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- disable the gssapi patch

* Mon Jun 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.9p2
- refresh to a new version of the gssapi patch

* Thu Jun  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- change Copyright: BSD to License: BSD
- add Markus Friedl's unverified patch for the cookie file deletion problem
  so that we can verify it
- drop patch to check if xauth is present (was folded into cookie patch)
- don't apply gssapi patches for the errata candidate
- clear supplemental groups list at startup

* Fri May 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix an error parsing the new default sshd_config
- add a fix from Markus Friedl (via openssh-unix-dev) for ssh-keygen not
  dealing with comments right

* Thu May 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- add in Simon Wilkinson's GSSAPI patch to give it some testing in-house,
  to be removed before the next beta cycle because it's a big departure
  from the upstream version

* Thu May  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish marking strings in the init script for translation
- modify init script to source /etc/sysconfig/sshd and pass $OPTIONS to sshd
  at startup (change merged from openssh.com init script, originally by
  Pekka Savola)
- refuse to do X11 forwarding if xauth isn't there, handy if you enable
  it by default on a system that doesn't have X installed

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.9
- drop various patches that came from or went upstream or to or from CVS

* Wed Apr 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- only require initscripts 5.00 on 6.2 (reported by Peter Bieringer)

* Sun Apr  8 2001 Preston Brown <pbrown@redhat.com>
- remove explicit openssl requirement, fixes builddistro issue
- make initscript stop() function wait until sshd really dead to avoid 
  races in condrestart

* Mon Apr  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- mention that challengereponse supports PAM, so disabling password doesn't
  limit users to pubkey and rsa auth (#34378)
- bypass the daemon() function in the init script and call initlog directly,
  because daemon() won't start a daemon it detects is already running (like
  open connections)
- require the version of openssl we had when we were built

* Fri Mar 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- make do_pam_setcred() smart enough to know when to establish creds and
  when to reinitialize them
- add in a couple of other fixes from Damien for inclusion in the errata

* Thu Mar 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2p2
- call setcred() again after initgroups, because the "creds" could actually
  be group memberships

* Tue Mar 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2p1 (includes endianness fixes in the rijndael implementation)
- don't enable challenge-response by default until we find a way to not
  have too many userauth requests (we may make up to six pubkey and up to
  three password attempts as it is)
- remove build dependency on rsh to match openssh.com's packages more closely

* Sat Mar  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove dependency on openssl -- would need to be too precise

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Mon Feb 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- Revert the patch to move pam_open_session.
- Init script and spec file changes from Pekka Savola. (#28750)
- Patch sftp to recognize '-o protocol' arguments. (#29540)

* Thu Feb 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- Chuck the closing patch.
- Add a trigger to add host keys for protocol 2 to the config file, now that
  configuration file syntax requires us to specify it with HostKey if we
  specify any other HostKey values, which we do.

* Tue Feb 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- Redo patch to move pam_open_session after the server setuid()s to the user.
- Rework the nopam patch to use be picked up by autoconf.

* Mon Feb 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- Update for 2.5.1p1.
- Add init script mods from Pekka Savola.
- Tweak the init script to match the CVS contrib script more closely.
- Redo patch to ssh-add to try to adding both identity and id_dsa to also try
  adding id_rsa.

* Fri Feb 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- Update for 2.5.0p1.
- Use $RPM_OPT_FLAGS instead of -O when building gnome-ssh-askpass
- Resync with parts of Damien Miller's openssh.spec from CVS, including
  update of x11 askpass to 1.2.0.
- Only require openssl (don't prereq) because we generate keys in the init
  script now.

* Tue Feb 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- Don't open a PAM session until we've forked and become the user (#25690).
- Apply Andrew Bartlett's patch for letting pam_authenticate() know which
  host the user is attempting a login from.
- Resync with parts of Damien Miller's openssh.spec from CVS.
- Don't expose KbdInt responses in debug messages (from CVS).
- Detect and handle errors in rsa_{public,private}_decrypt (from CVS).

* Wed Feb  7 2001 Trond Eivind Glomsrxd <teg@redhat.com>
- i18n-tweak to initscript.

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- More gettextizing.
- Close all files after going into daemon mode (needs more testing).
- Extract patch from CVS to handle auth banners (in the client).
- Extract patch from CVS to handle compat weirdness.

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- Finish with the gettextizing.

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- Fix a bug in auth2-pam.c (#23877)
- Gettextize the init script.

* Wed Dec 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- Incorporate a switch for using PAM configs for 6.x, just in case.

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Incorporate Bero's changes for a build specifically for rescue CDs.

* Wed Nov 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Don't treat pam_setcred() failure as fatal unless pam_authenticate() has
  succeeded, to allow public-key authentication after a failure with "none"
  authentication.  (#21268)

* Tue Nov 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to x11-askpass 1.1.1. (#21301)
- Don't second-guess fixpaths, which causes paths to get fixed twice. (#21290)

* Mon Nov 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- Merge multiple PAM text messages into subsequent prompts when possible when
  doing keyboard-interactive authentication.

* Sun Nov 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- Disable the built-in MD5 password support.  We're using PAM.
- Take a crack at doing keyboard-interactive authentication with PAM, and
  enable use of it in the default client configuration so that the client
  will try it when the server disallows password authentication.
- Build with debugging flags.  Build root policies strip all binaries anyway.

* Tue Nov 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- Use DESTDIR instead of %%makeinstall.
- Remove /usr/X11R6/bin from the path-fixing patch.

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add the primes file from the latest snapshot to the main package (#20884).
- Add the dev package to the prereq list (#19984).
- Remove the default path and mimic login's behavior in the server itself.

* Fri Nov 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Resync with conditional options in Damien Miller's .spec file for an errata.
- Change libexecdir from %%{_libexecdir}/ssh to %%{_libexecdir}/openssh.

* Tue Nov  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to OpenSSH 2.3.0p1.
- Update to x11-askpass 1.1.0.
- Enable keyboard-interactive authentication.

* Mon Oct 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to ssh-askpass-x11 1.0.3.
- Change authentication related messages to be private (#19966).

* Tue Oct 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- Patch ssh-keygen to be able to list signatures for DSA public key files
  it generates.

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add BuildPreReq on /usr/include/security/pam_appl.h to be sure we always
  build PAM authentication in.
- Try setting SSH_ASKPASS if gnome-ssh-askpass is installed.
- Clean out no-longer-used patches.
- Patch ssh-add to try to add both identity and id_dsa, and to error only
  when neither exists.

* Mon Oct  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update x11-askpass to 1.0.2. (#17835)
- Add BuildPreReqs for /bin/login and /usr/bin/rsh so that configure will
  always find them in the right place. (#17909)
- Set the default path to be the same as the one supplied by /bin/login, but
  add /usr/X11R6/bin. (#17909)
- Try to handle obsoletion of ssh-server more cleanly.  Package names
  are different, but init script name isn't. (#17865)

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.2.0p1. (#17835)
- Tweak the init script to allow proper restarting. (#18023)

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 20000823 snapshot.
- Change subpackage requirements from %%{version} to %%{version}-%%{release}
- Back out the pipe patch.

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p4, which includes fixes for config file parsing problems.
- Move the init script back.
- Add Damien's quick fix for wackiness.

* Wed Jul 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p3, which includes fixes for X11 forwarding and strtok().

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- Move condrestart to server postun.
- Move key generation to init script.
- Actually use the right patch for moving the key generation to the init script.
- Clean up the init script a bit.

* Wed Jul  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Fix X11 forwarding, from mail post by Chan Shih-Ping Richard.

* Sun Jul  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p2.
- Use of strtok() considered harmful.

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- Get the build root out of the man pages.

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add and use condrestart support in the init script.
- Add newer initscripts as a prereq.

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- Build in new environment (release 2)
- Move -clients subpackage to Applications/Internet group

* Fri Jun  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.2.1p1

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- Patch to build with neither RSA nor RSAref.
- Miscellaneous FHS-compliance tweaks.
- Fix for possibly-compressed man pages.

* Wed Mar 15 2000 Damien Miller <djm@ibs.com.au>
- Updated for new location
- Updated for new gnome-ssh-askpass build

* Sun Dec 26 1999 Damien Miller <djm@mindrot.org>
- Added Jim Knoble's <jmknoble@pobox.com> askpass

* Mon Nov 15 1999 Damien Miller <djm@mindrot.org>
- Split subpackages further based on patch from jim knoble <jmknoble@pobox.com>

* Sat Nov 13 1999 Damien Miller <djm@mindrot.org>
- Added 'Obsoletes' directives

* Tue Nov 09 1999 Damien Miller <djm@ibs.com.au>
- Use make install
- Subpackages

* Mon Nov 08 1999 Damien Miller <djm@ibs.com.au>
- Added links for slogin
- Fixed perms on manpages

* Sat Oct 30 1999 Damien Miller <djm@ibs.com.au>
- Renamed init script

* Fri Oct 29 1999 Damien Miller <djm@ibs.com.au>
- Back to old binary names

* Thu Oct 28 1999 Damien Miller <djm@ibs.com.au>
- Use autoconf
- New binary names

* Wed Oct 27 1999 Damien Miller <djm@ibs.com.au>
- Initial RPMification, based on Jan "Yenya" Kasprzak's <kas@fi.muni.cz> spec.
