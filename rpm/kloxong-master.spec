# Scriptlet Ordering
# 01. %pretrans of new package
# 02. %pre of new package
# 03. (package install)
# 04. %post of new package
# 05. %triggerin of other packages (set off by installing new package)
# 06. %triggerin of new package (if any are true)
# 07. %triggerun of old package (if it's set off by uninstalling the old package)
# 08. %triggerun of other packages (set off by uninstalling old package)
# 09. %preun of old package
# 10. (removal of old package)
# 11. %postun of old package
# 12. %triggerpostun of old package (if it's set off by uninstalling the old package)
# 13. %triggerpostun of other packages (if they're setu off by uninstalling the old package)
# 14. %posttrans of new package 

# Syntax
#             install      upgrade       uninstall
# %pretrans   $1 == 0      $1 == 0       (N/A)
# %pre        $1 == 1      $1 == 2       (N/A)
# %post       $1 == 1      $1 == 2       (N/A)
# %preun      (N/A)        $1 == 1       $1 == 0
# %postun     (N/A)        $1 == 1       $1 == 0
# %posttrans  $1 == 0      $1 == 0       (N/A) 

%define _binaries_in_noarch_packages_terminate_build   0

%define debug_package %{nil}
%define kloxopath /usr/local/lxlabs/kloxo
%define productname kloxong 
%define build_timestamp %{lua: print(os.date("%Y%m%d"))}

Name: %{productname}
Summary: Kloxo Next Generation web panel
Version: 0.1.3
Release: 8
#Release: beta.%{build_timestamp}
License: GPL
Group: Applications/Internet

Source0:  https://github.com/KloxoNGCommunity/kloxoNG-CP/archive/master/%{name}-master.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildArch: noarch

Obsoletes: kloxomr >= 6.5.1, kloxomr7 > 0
#Obsoletes: kloxomr-addon-extjs, kloxomr-addon-yui-dragdrop
Conflicts: kloxomr <= 6.5.0

#Provides: kloxomr-editor-fckeditor, kloxomr-editor-ckeditor

%description
Kloxo Next Generation. This is a community release of a fork of Kloxo-MR. Kloxo-MR is a Fork of the original Kloxo

%prep
%autosetup -n %{name}-master

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p -m0755 %{buildroot}%{kloxopath}
%{__cp} -rp kloxo/* %{buildroot}%{kloxopath}/
%{__rm} -rf %{buildroot}%{kloxopath}/rpm
%{__ln_s} -f %{kloxopath}/pscript %{buildroot}/script


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(755,root,root,755)
%defattr(644,lxlabs,lxlabs,755)
%{kloxopath}/*
%defattr(644,root,root,755)
/script


%pretrans
## MR -- always delete because trouble for downgrade
#if [ -d /script ] ; then
	%{__rm} -rf /script 2>/dev/null
#fi

%pre
echo 'pre' >> /tmp/scriptlet.txt
/usr/sbin/useradd -s /sbin/nologin -M -r -d /home/lxlabs/ \
    -c "KloxoNG Website Control Panel" lxlabs &>/dev/null || :

%post

read -r -d '' for_cleanup << EOF
._/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/.
._/                                                                          _/.
._/  ..:: Kloxo Next Generation Web Panel ::..                                            _/.
._/                                                                          _/.
._/  Attention:                                                              _/.
._/                                                                          _/.
._/  - Run 'sh /script/cleanup' for to make sure running well                _/.
._/    or 'sh /script/cleanup-simple' (cleanup without fix services configs) _/.
._/                                                                          _/.
._/  - In many situations, just enough run 'sh /script/fix-configs-files'    _/.
._/    and then 'sh /script/fix-all' and 'sh /script/restart-all'            _/.
._/                                                                          _/.
._/  - If trouble when execute 'sh /script/cleanup' (missing directory),     _/.
._/    try 'yum reinstall kloxong -y'                                       _/.
._/                                                                          _/.
._/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/.
EOF

read -r -d '' for_upcp << EOF
._/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/.
._/                                                                          _/.
._/  ..:: Kloxo Next Generation Web Panel ::..                               _/.
._/                                                                          _/.
._/  Attention:                                                              _/.
._/                                                                          _/.
._/  - Run 'sh /script/upcp' to install completely                           _/.
._/                                                                          _/.
._/ 	To use test repo use sh /script/upcp -t                              _/.
._/                                                                          _/.
._/                                                                          _/.
._/  - Some file downloads may not show a progress bar so please             _/.
._/    do not interrupt the process.                                         _/.
._/                                                                          _/.
._/  - Then, go to 'Switch Program' to enable web and other programs         _/.    
._/                                                                          _/.
._/  If php74 / php80 is not available then run the command:                 _/.
._/  # sudo sh /script/fix-service-list                                      _/.
._/  This should update the list of available php versions.                  _/.
._/                                                                          _/.
._/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/.
EOF

read -r -d '' for_hostname << EOF
* WARNING: your hostname is '$(hostname)' and not match to FQDN
  - It's must be like 'server1.domain.com' instead 'server1'
 
  - For VPS, change 'hostname' in VPS panel and then reboot
  - For Dedicated Server, change 'HOSTNAME' in '/etc/sysconfig/network'
    and then reboot
EOF

# this is for fresh install
#if [ $1 -eq 1 ] ; then
	if [ -d /var/lib/mysql/kloxo ] ; then
		# but previous version already exists
		echo
		echo "${for_cleanup}"
		echo
	else
		# real fresh install
		echo
		echo "${for_upcp}"
		echo

		if [ "$(hostname)" == "$(hostname -s)" ] || [ "$(hostname -s)" == "" ] ; then
			echo
			echo "${for_hostname}"
			echo
		fi
	fi
#elif [ $1 -eq 2 ] ; then
#	# yum update
#	echo
#	echo "${for_cleanup}"
#	echo
#fi


%changelog
* Sun Jun 30 2024 John Parnell Pierce <john@luckytanuki.com>
- Due to install issues with latest Maria 10.5 packages have rolled back to 10.2

* Wed Sep 6 2023 John Parnell Pierce <john@luckytanuki.com> - 0.1.3-7
- Fix broken paths for fcgi handler

* Tue Sep 5 2023 John Parnell Pierce <john@luckytanuki.com> - 0.1.3-6
- adjust excluded php packages
- ensure mysql modules are active

* Fri Sep 1 2023 John Parnell Pierce <john@luckytanuki.com> - 0.1.3-5
- fixing parsing of remi package names
- fix rewriting of remi php symlinks

* Thu Aug 31 2023 John Parnell Pierce <john@luckytanuki.com> - 0.1.3-4
- php install now loads remi php packages
- add php8.1 and php8.2 to list if available php versions

* Thu Apr 14 2022 John Parnell Pierce <john@luckytanuki.com> - 0.1.3-3
- Fix wrong brackets and variable in Fix-outgoingips
- Fix typo in fixdomainkey
- Move Kloxong Curl into its own yum repo to fix build errors

* Thu Apr 14 2022 John Parnell Pierce <john@luckytanuki.com> - 0.1.3-2
- Block loading of postfix32u as this conflicts with toater packages
- Remove old webmail packages
- support for php80
- Update mariadb-upgrade script to work with the new version of mariadb
- Update MariaDB repo to version 10.5
- Fix Remi repo address
- Fix domain key folder permission issues
- remove extra slash from djbdns comd

* Tue May 25 2021 John Parnell Pierce <john@luckytanuki.com> - 0.1.3-1
- test for null domain records when building DNS configuration files
- allow list of remap ips for AWS or NAT hosting - include pairs public_ip:internal_ip in manualoutgoingips.flg file
- add support for IUS php74
- fix "overwriting servercert.pem when it is a symlink" problem - issue #67
- fix permission problem for logrotate of httpd logs as required for new logrotate versions in centos 7
- with Spamassassin - delete any spam with 10 or more stars - no matter what the spam retention settings

* Sat Sep 22 2020 John Parnell Pierce <john@luckytanuki.com> - 0.1.2.2-final
- exclude install of kloxong-testing.rpm from wild card yum install
- Fix gpg key
- add line to change permission of log file folder for named to try to resolve issue #59
- Add chown to set named as owner of /var/log/named
- code fix for secondary check/detection of missmatch on repositories
- Don't overwrite qmails certificate if it is a symlink - issue #67
- Add Clamav resurce usage warning to Virus scanner select check box

* Sat Jun 27 2020 John Parnell Pierce <john@luckytanuki.com> - 0.1.2.2-beta
- update release numbers
- update kloxoversion file
- fix location of initial yum repo rpm. Should alway be located at https://github.com/KloxoNGCommunity/kloxong/raw/initial-rpm/kloxong-release.rpm issue #56
- refactored command line options in upcp script
- added install yum test repo command line option (-t or -test) to upcp
- kloxo-testing to be only installed by -t/--test option
- remove conflicting obsoletes and conflicts from kloxo-release and kloxo-testing
- remove test repo from kloxo-testing
- remove all but the test repo from kloxo-release

* Mon Mar 30 2020 John Parnell Pierce <john@luckytanuki.com> - 0.1.2.1-beta
- Fix for httpd fails to start with missing mod_authn_alias.so error - issue #48

* Fri Jan 24 2020 John Parnell Pierce <john@luckytanuki.com> - 0.1.2-beta
- update release numbers

* Tue Dec 3 2019 John Parnell Pierce <john@luckytanuki.com> 
- setup file to use copr autp build service

* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Tue Sep 12 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017091201.mr
- remove unwanted files
- add sendlimiter for qmail (based on qmail-antispam) with detect smtp and send
- mod enable-selinux script
- add contactemail.php (used by sendlimiter)
- add disable-selinux script
- fix sendlimiter (related to detect domain)

* Sun Sep 10 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017091001.mr
- add more extension for fastcgi under hiawatha
- fix domains.conf.tpl for pdns
- make to disable clamav will remove their rpms
- fix/mod ioncube-installer
- add disable/enable-service script
- fix/mod disable-firewall

* Wed Aug 30 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017083001.mr
- mod/fix defaults.conf.tpl for apache (make possible custom.portnip.conf)
- make enable 'disable notify' for all clients
- fix echo for pure-ftpd-without-clamav
- mod run-kexec
- add fix-pdns-db script for powerdns

* Fri Aug 25 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017082501.mr
- remove setup-runkexec
- add run-kexec
- mod/fix for run script of qmail
- add CustomHeader for hiawatha.conf.base
- fix install-pure-ftpd-without-cap

* Wed Aug 23 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017082302.mr
- add pure-ftpd-without-clamav script
- fix enable/disable 'virus scan'
- mod/fix varnish configs (related to change 5.1 version)
- fix servermail__qmaillib.php (missing ';')

* Tue Aug 22 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017082201.mr
- add trim for '.' in dns domains.conf.tpl (to make sure no '.' at the end of value)
- change file_put_contents to lfile_put_contents (because remove for '\r')
- mod lfile_put_contents for remove '\r' (make sure to linux format)
- back to use file_put_contents instead lfile_put_contents
- revert to previous lfile_put_contents function

* Sun Aug 20 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017082002.mr
- add .py for cgi (beside .cgi and .pl) in webserver
- fix enable clamav; add pure-ftpd-with-clamav script
- disable execute postUpdate in updateform in servermaillib.php
- fix/mod log list for mysql/mariadb
- change detect port 3306 to 'pgrep ^mysql' in watchdog for mysql
- add '!@#$%&*?_-.' for password chars
- fix spamdyke.conf (change dos to linux text format)

* Tue Aug 15 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017081502.mr
- add virtual-info script (detect for vps type)
- change to use virtual-info script instead 'grep envID /proc/self/status'
- mod some message for script (related to openvz)

* Mon Aug 14 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017081401.mr
- fix ssl (panel ssl also for pure-ftpd beside for qmail)
- fix servermaillib.php (appear for 'smtp relay')
- change detect for container vps (not for OpenVZ only)

* Thu Aug 09 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017080901.mr
- fix install-pure-ftpd-without-cap script
- use old mp.php instead dbadmin.php (because the same content)
- add merestore script (restore for mebackup)

* Sun Aug 06 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017080603.mr
- add mariadb-upgrade script (to 10.2 by default)
- add install-pure-ftpd-without-cap (with cap may trouble in LXC container)
- use exit status for rpmdev-vercmp in mariadb-upgrade and phpm-installer
- fix getSSLParentList function (bug for use /* */ between "*" var)

* Tue Aug 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017080103.mr
- add '--force' for letsencrypt-renew script
- fix letsencrypt-renew
- add '--force' for acme-cron.sh
- add copy cron ssl to fix-cron-ssl

* Sun Jul 30 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017073002.mr
- fix dns config (back not to use convert)
- add enable php52m for php-fpm (default is disable)

* Thu Jul 27 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017072703.mr
- set random password if not include password for reset-mysql-root-password.php
- fix acme.sh.tpl (add --force for create new letsencrypt ssl)
- separate make-master from make-slave
- add missing make-master
- fix lxftp_connect function in linuxfslib.php (change ftp_url to ftp_protocol)
- mod/fix lxftp_connect (with using parse_url)
- mod/fix fix-missing-admin

* Sun Jul 23 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017072303.mr
- use try-catch for session_start in default_index.php
- use image list in 'control panel configure' like 'appearance'
- fix domains.conf.tpl for nsd/bind/yadifa
- add help message to mail forward (how to set forward to php piping)
- fix domains.conf.tpl for nsd/bind/yadifa (related to ns record key)

* Tue Jul 11 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017071101.mr
- add identrust ca for letsencrypt
- add mail (as alias for webmail) in webserver configs
- mod php-fpm.service (add execstop and execstoppre)
- fix display dns settings/template

* Wed Jun 28 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017062801.mr
- fix default_index.php (for non login pages)

* Fri Jun 23 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017062301.mr
- make possible no random background image (and setting via 'control panel configure')
- mod/fix sysinfo.php (delete phpXYm without version file)
- fix delete domainkeys dir if not exists in mmail__qmaillib.php
- remove unwanted call xprint in dns/dnsbaselib.php

* Tue Jun 16 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017061602.mr
- fix messagelib.php (related to 'web features')
- fix remotelib.php (need adjustment for php 5.6)
- set make-slave always need admin password (do not use admin as password)
- change to use '@' for __base__ in dns settings
- add '.' of certain records entries
- mod 'web features' help
- back to use old page entry for password_contact_check (in coredisplaylib.php)
- fix display dns settings (related to 'cname record')
- add 'fixdomainkey' process for 'mailserver configure'

* Fri Jun 08 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017060801.mr
- fix setup-afterlogic (change php exit position)
- fix setup-roundcube (add copy for missing files)

* Thu Jun 07 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017060702.mr
- fix apache-optimize (script and panel)
- fix add-rainloop-domains (related to data dir)
- more info for apache-optimize

* Tue Jun 06 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017060601.mr
- fix ~lxcenter.conf.tpl (add line after ThreadsPerChild for worker)
- fix add/del-rainloop-domains

* Thu Jun 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017060101.mr
- make appear password for ftp (for backup)
- add enable/isable 'keepalive' for 'apache optimize'
- add 'blacklist headers' for spamdyke
- disable ban for hiawatha (temporary)
- set 'ftp_pasv' for remote self backup
- disable using installer.php in setup.sh
- fix detect lxphp.exe for fix-urgent

* Thu May 18 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017051802.mr
- hide for php56s install process in fix-urgent
- add 'as absolute path' under admin for sendmailbanlib.php
- also exclude pear1u for php depencencies in phpm-installer
- fix priorities repo in phpm-installer

* Wed May 17 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017051705.mr
- fix phpm-installer (related to libmemcached)
- add setup-runkexec script (for fast reboot service)
- fix fix-urgent (related to php56s install)
- fix setup-roundcube (wrong mysql user)
- add 'srv record' (only work in bind, nsd, yadifa and pdns)
- fix mailaccountlib.php (related to updateform)

* Tue May 16 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017051601.mr
- add clearswap script
- add dbadmin.php; move mod_remoteip to remoteip.conf and disabled it
- use pure sh script for some setup script (like setup-rainloop) but need dbadmin.php
- install php56s if not exists and use it for CentOS 6/7 in fix-urgent
- fix cron-clearcache; fix add-rainloop-domains
- fix convert_message function in htmllib.php
- use randomstring for crypt in md5 format (prevent php 5.6+ warning)
- add 'syncserver' select for 'secondary dns'
- change some description (for mailaccount, dnsslave and time_out)
- add getTimeoutDefault function in weblib.php
- fix getServiceDetails function logic in service__redhatlib.php
- disable rotateLog function in mailtrafficlib.php (because using logrotate)
- change if to switch for updateform function in mailaccountlib.php
- remove phpcfg (because still using phpini and php-fpm) in file directory
- remove double entry for env[path] in php-fpm pool
- fix setup-afterlogic/rainloop/roundcube/t-dah/tht
- fix add-rainloop-domains
- include add-rainloop-domains in setup-rainloop (where include in fixwebmail)
- change using date from urandom for certain setup script (because urandom trouble in openvz)
- fix comment without # in step2.inc
- fix detec openvz in fix-sysctl
- add cron-restart-mail script (restart if mail queue exists)
- fix apps setup scripts
- add chown to apache for apps setup script
- mod setup-rainloop (related to need access to webmail)
- modified description var dan value (make more constant)
- mod fix-sysctl script
- combine set-fs, fix-sysctl and set-ulimit to set-limits script and run under fix-urgent

* Mon May 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017050104.mr
- implementing web-console for web based ssh (for admin only)
- fix setup-telaen.php
- fix nolog in setup-*.php 
- fix add-rainloop-domains
- include add-rainloop-domains in setup-rainloop (where include in fixwebmail)

* Sun Apr 30 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017043001.mr
- fix reset-mysql-root-password.php (move tmp dir and add '--skip-grant-tables')
- add mod_remoteip in defaults.conf.tpl in apache 2.4 (if reverseproxy)
- mod ~lxcenter.conf.tpl (ThreadsPerChild using $mcfactor)
- add rate_limit in named.options.conf for bind
- add options for 'security.limit_extensions' in 'php configures'
- remove old code in phpinilib.php and phpini_sync.lib.php

* Sun Apr 23 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017042301.mr
- fix display 'multiple php enable' in 'webserver configure'
- change pm from dynamic to ondemand on 'default' (apache user) for php-fpm
- prepare hpkp for ssl (in fixssl script)
- disable create hphk files in fixssl til full implementing for web

* Sat Apr 22 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017042201.mr
- reformat yadifa configs
- fix fix-configs-files script (related to apache configs)
- fix cron-clearcache (related to disable restart-all)

* Fri Apr 21 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017042101.mr
- fix stats apps in sysinfo script; mod yadifa configs
- move 'enable multiple php' from 'php configure' to 'webserver configure'
- prepare to use 'web-console' beside jcterm for ssh client
- back to disable cron under admin
- setup.sh also remove opensmtp (make trouble for smtp under qmail)
- disable restart-all in cron-clearcache (may trouble)
- add ini.lst in php-branch-installer
- no add hostname if not found IP (usually for dhcp mode)

* Mon Apr 10 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017041002.mr
- add ftp info in sysinfo script; add write_ini (prepare feature configs)
- change 'port and redirect configure' to 'control panel configure'
- add 'select wrapper' to 'control panel configure'
- add 'seLocalConfig = no' for kloxo-web config
- add logic to prevent install to CentOS 5 in setup.sh
- add functions.inc (with 'ini_parser' and 'ini_writer' at this moment)
- fix redirect panel (related to 'ssl')
- optimize redirect.php code

* Thu Apr 06 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017040602.mr
- make disable reading .hiawatha if choose back-end instead front-end in hiawatha-proxy
- fix yadifad.conf for 'allow-transfer' and 'allow-notify' to 'slave' 
- fix yadifa (add yadifad_noslave.conf as base for non-slave)

* Tue Apr 04 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017040402.mr
- mod to make sure only djdbns and maradns will running dnsnotify
- fix djbdns.init and setup-djbdns (related to setup)

* Mon Apr 03 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017040302.mr
- fix djbdns setup in djbdns.init and setup-djbdns script
- install dhclient package if using dhcp in fix-urgent
- re-create default ssl (with 100 year expire; use 2048bits)
- fixssl also copy to pure-ftpd

* Sun Apr 02 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017040203.mr
- fix setup-djbdns (missing ppath declare)
- move delete .sock file from start to stop for php-fpm init service
- add install redhat-lsb in fix-urgent
- add fix-sysctl (move code from step2.inc)

* Sat Apr 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017040102.mr
- fix checkServiceOn in service__redhatlib.php (related to detect service on/off)
- mod yadifad.conf (make match to version 2.2.x); mod log list (adjustment for yadifa)
- fix/mod apache conf.tpl related to pagespeed (just using 'disable_pagespeed' with 'IfModule'
- set apache for default, cp, webmail and stats always not using pagespeed

* Fri Mar 31 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017033103.mr
- fix enable/disable-php-fpm script
- include 'expect' install in setup.sh (contains 'mkpasswd')
- add max_allowed_packet in set-mysql-default script
- mod php-fpm init/init.base related to delete .sock file in start
- fix set-mysql-default (add missing '||')
- mod log_cleanup message for httpd in lib.php

* Thu Mar 30 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017033005.mr
- combine ssl_base.conf and ssl_base24.conf in ssl_base.conf
- use 'getLinkCustomfile' for detect custom file in web conf.tpl files
- add remove sock files in 'ExecStartPre' for php-fpm/phpm-fpm.service.base (for faster start/restart)
- disable using getSslCertnameFromIP for IP ssl (use eth0-0 instead eth0_0 for example)
- mod deplist.sh
- mod installer.php and convert to step2.inc (make install using full bash script)
- remove kloxo-mr-bugfix-6.5.0.sh and kloxo-mr-dev.sh
- add missing setAllWebServerInstall for enable/disable pagespeed in 'switch programs'
- fix disable-firewall script (related to get service name)
- fix 'setAllInactivateWebServer' (use 'getAllRealWebDriverList' instead 'getAllWebDriverList') in lib.php
- fix spawn-fcgi process list
- fix yadifad.conf (related to uid and gid)
- fix setActivateDnsServer (related to yadifa) in lib.php
- fix step2.inc (related to detect primary IP and old dirs)
- disable ExecStartPre for remove sock files in CentOS 7 (look likr no impact)
- fix detect httpd24u in step2.inc
- fix copy _inactive_.conf to pagespeed.conf for setAllWebServerInstall in lib.php
- fix php-fpm conf to /opt/configs
- use 'rpm -qa' instead 'rpm -q' for getRpmVersion in lib.php

* Mon Mar 27 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017032701.mr
- fix httpd24 state in 'switch programs'
- Set rpms version to '0.0.0' if not exists
- remove 'opt/php' if exists in cleanup process

* Sun Mar 26 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017032605.mr
- mod add-rainloop-domains and del-rainloop-domains to use pure ssh code
- copy djbdns setup from init to setup-djbdns script (because trouble in CentOS 7)
- make install all dns servers (like web servers)
- disable mydns service from list
- change checkServiceInRc to new checkServiceOn to detect service on/off in service list
- remove spamdyke-utils install (because conflict with djbdns)
- fix sysinfo script (related to detect php-fpm service in CentOS 7)
- disable mydns as dns server
- add firewalld and remove mydns in service list
- disable execute setWebServerInstall in installMeTrue function (enough via cleanup script)
- disable removeOtherDrivers in removeOtherDriver for web
- make install all dns package (like web services)
- use include 'rhel.inc' to get driver lists
- mod merge_array_object_not_deleted function logic
- add disable-firewall and use by installer.php
- install all dns server (like web server)
- move restart process from .conf to dosyncToSystemPost function for dns server
- make driver list taken from rhel.inc (and change from 'include_one' to 'include') in lib.php
- add hash for crypt in weblib.php; fix add-rainloop-domains script
- add set-initial-services script
- fix fixwebcache.php (change to use 'getAllRealWebCacheDriverList' instead 'getAllWebCacheDriverList')
- fix dns/dns__lib.php related to driver list
- mod pserverlib.php related unused httpd24ready variable
- remove web__apache::setWebserverInstall in pserverlib.php (because function remove and handle with cleanup process)
- fix web__lib.php related to webserver proxy
- mod merge_array_object_not_deleted logic again
- add missing disable-firewall script
- fix web server install/uninstall logic
- fix dns server install/uninstall logic
- mod dns__lib.php (use 'setAllInactivateDnsServer' for uninstallMe dan add 'restart' in installMe)
- mod and fix web__lib.php (use 'setAllInactivateDnsServer' for uninstallMe dan add 'restart' in installMe)
- fix 'use_apache24' logic in pservercorelib.php
- fix logic for setCopyWebConfFiles in lib.php
- mod installer.sh (will install kloxomr7 in not exists)
- fix setInitialAllDnsConfigs (call wrong function)
- fix setAllWebServerInstall (call 'getAllRealWebDriverList' instead 'getAllWebDriverList') in lib.php

* Mon Mar 20 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017032001.mr
- add 'caa record' for dns (default value = 'letsencrypt.org')
- add issuer info for ssl data
- disable use 'isWebProxyOrApache' for httpd in updateSwitchProgram function
- fix clearcache script (related to CentOS 7)
- always overwrite 00-base.conf for httpd (related to httpd24u)

* Sun Mar 19 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017031902.mr
- fix del-rainloop-domains.php
- fix apache24 logic in pservercorelib.php
- fix fix-service-list logic (use php-cli instead php for detecting)
- mod php-branch-installer.inc (php 7.1 using mod_php71u/w instead php71u/w)
- fix phpm-installer (related to php 7.1)
- mod fix-service-list (add sort for 'yum info' result)

* Fri Mar 17 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017031701.mr
- remove newInstallFixIpaddress.php (do like fixIpAddress.php)
- add fix-ipaddress (do as 're-read ip')
- add delete .sock files in start of php-fpm init (no need for systemd)
- add validate for resource plan name (rule as the same as client name)

* Thu Mar 16 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017031601.mr
- decrease max_childrens from 10 to 6
- change pool name with add their php name (using 'php54m-default' instead 'default')
- increase 'stop_timeout' from 15 to 30 (in seconds)
- fix set-php-branch logic
- make accurate help fpr set-php-fpm

* Wed Mar 15 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017031503.mr
- make faster service-list process (full script; get per-set instead one-by-one)
- certain service taken from other list instead using yum info
- fix phpini__synclib.php in install process
- disable session delete (because not exist) for check_blocked_ip in index.php
- mod php-branch-installer.inc
- fix restart-list.inc (related to php-fpm service)
- mod throw for 'no_dns_template'
- remove set.mysql.lst
- fix double header of setRealServiceBranchList function

* Mon Mar 13 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017031302.mr
- set delay from 10s to 15s for stop php-fpm ini init files
- set pm.process_idle_timeout from 20s to 10s in php-fpm pools
- appear active php-branch in 'php modules status'
- make multiple select in 'php modules status'
- read real ssh port in 'ssh configure'
- make possible redirect after change port for panel
- phpm-config-setup also handle php-branch configs
- phpm-installer also handle php-branch install
- make possible install all modules for php-branch
- add php-branch-installer, php-branch-installer.inc and php-branch-updater
- add select-kloxo-wrapper (make use 'kloxo.exe' or 'lxphp.exe')
- make set-php-branch as pure ssh script (remove set-php-branch.php)
- back to disable multiple select in 'php mpdules status'
- use sh php-branch-installer in Kloxo-MR install process
- fix for default configs for php-fpm configs in phpm-config-setup
- fix include in php53-fpm.conf


* Fri Mar 10 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017031002.mr
- fix/mod phpm-installer (make more info for log)
- make remove phpm remove also remove their php-fpm service
- disable/minimize using isRpmInstalled function
- add disable-yum-cache script

* Wed Mar 08 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017030803.mr
- fix/mod sysinfo for detecting services; mod php-fpm.init for appearing '(PHP Used)'
- remove watchdog table from db-structure-update.sql
- mod addDefaultWatchdog for webcache and webproxy
- change execute setWatchdogDefaults from updatelib.php to lib.php (in cleanup process)
- fix/mod enable-php-fpm script
- fix/mod fix-urgent (related to ~/.rpmmacros)
- fix/mod phpm-config-setup (related to .nonini files)
- fix phpm-config-setup (make sure default ini using .nonini instead _unused.nonini)
- fix set-php-fpm and phpm-config-setup (related to 'php used')

* Thu Mar 02 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017030201.mr
- change 'ps --no-headers -o comm 1' instead 'command -v systemctl' for detect CentOS 7
- add missing 'switch driver' in 'updateSwitchProgram'

* Wed Mar 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017030102.mr
- add '/etc/ssl/certs' in fixweb script
- mod README.md (Kloxo-MR 7.0 ready for CentOS 7)
- clean up fixlogdir.php
- fix sysinfo.php (related to php-fpm detect)
- fix fix-urgent script (related to ~/.rpmmacros)

* Tue Feb 28 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017022802.mr
- mod message in phpm-fpm.init.base
- add blank 'pureftp.passwd' in fixftpuser.php
- mod/fix switch program (especially for httpd)
- change cron-clearcache default value to 0.90
- fix phpm-config-setup (related to .nonini issue)

* Mon Feb 27 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017022701.mr
- add '>/dev/null 2>&1' for chkconfig process (disable 'note' if running in CentOS 7)
- mod sysinfo script (prepare for CentOS 7)
- mod ~lxcenter.conf.tpl ('free -m' is different between CentOS 7 and below version)
- separate kloxo service to kloxo-php, kloxo-web and kloxo-wrapper
- remove kloxo-wrapper.cron (because using kloxo-wrap service)
- remove webused.txt (because panel for hiawatha only)
- change 'blocked hosts' to 'blocked IP Address'
- move process php-fpm enable logic to run enable-php-fpm in phpinilib.php
- move apache-optimize stamp from serverweb__lib.php to ~lxcenter.conf.tpl
- use php56s instead php54s if exists
- add disable phpXYs-fpm in restart script if using php-cgi
- mod restart-list.inc (especially for php-fpm issue
- fix kloxo-wrapper.sh (add cd to httpdocs of kloxo dir);
- fix os_create_program_service (related to kloxo services)
- fix kloxo-php.init (remove also_mysql)
- add echo for start dan stop for kloxo-wrap.init
- remove kloxo.service
- fix fixlxphpexe logic
- remove kloxo and php-fpm process files
- set 'chkconfig on' for php-fpm in installer.sh/setup.sh
- add chkconfig on for kloxo services in restart-service
- remove list_web in list_all in restart-list.inc
- remove php-fpm/phpm-fpm logic in restart.inc
- fix pure-ftpd service file
- fix link for kloxo service file in os_create_program_service function
- add yum remove for httpd24u in setup.sh/installer.sh
- make hidden note for chkconfig
- remove php service file in phpm-config-setup
- add set-php-fpm and enable-php-fpm in phpm-installer
- add symlink for kloxo-hiawatha and kloxo-phpcgi in restart script
- fix list_phpfpm logic for systemd
- mod set-php-fpm for handle service files (moving from phpm-config-setup)
- add missing kloxo-wrap.service file
- add log_cleanup to fix-qmail-assign.php
- remove array_unique in phpini__synclib.php
- mod for use_apache24 select
- fix updateform in serverweblib.php
- use isRpmInstalled instead grep from 'rpm list'
- fix using isRpmInstalled for getRpmBranchInstalled function
- use httpd24u if exists in install process
- mod message for fixmail-all
- fix set-php-fpm if process phpXYs (no create service file)
- fix apache24 options logic in 'switch program'
- fix 'grep pagespeed' in web__lib.php
- re-enable setRealServiceBranchList and setCheckPackages function in lib.php
- mod 'yum remove' for i386 and i686 under x86_64 os
- mod install process (install apache before php instead after)
- make simple disable iptables/firewalld
- fix merge php52-fpm .confs step
- fix create use_apache24.flg file
- mod/fix enable-php-fpm
- move chkvonfig process from set-php-fpm to phpm-config-setup
- mod message in phpm-installer
- add remove-php-fpm script
- add disable-php-fpm script
- add pure-ftpd.service
- fix phpm-fpm.init.base
- fix install phpXYm in setup.sh/installer.sh
- add sudo install in installer.sh/setup.sh and fix-urgent (run by cleanup)
- remove phpm-fpm in service list
- make automatic install pagespeed if select in 'switch program'
- fix detect pagespeed in web/web__lib.php
- create '__blank__.conf' for apache
- fix detect and install php in installer.php
- add '--skip-broken' for php install in install process
- back to use 'old fashion' mailforward (make possible un-create account to forward to other account)
- include httpd24u-mod_security2 for install httpd24u
- enable/disable 'use apache24' and 'use pagespeed' will automatically install/replace their packages
- add 'update multiple php' in cleanup
- hidden dhparam process in fixweb
- create flag dir if not exists in install process
- fix php install in install process (wrong 'skip-broken')
- add 'sslverify=false' for yum.conf in fix-urgent ('Peer cert cannot be verified or peer cert invalid' iaaue); add fix-urgent process in fixrepo
- remove '--type=sysv' from 'chkconfig' (trouble in CentOS 5)
- add remove 32bit packages for 64bit OS (in fix-urgent)
- add '%_query_all_fmt' to .rpmmacros in fix-urgent (make only install 64bit packages in 64bit OS)
- remove 'phpm-fpm' in db-structure-update.sql
- mod remove phpm-fpm from '/etc/init.d'
- back to use 'setPhpUpdate' function instead run phpm-updater in cleanup
- mod log_cleanup messages

* Fri Feb 10 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017021003.mr
- fix scavenge.php (related to 'clearsession.php')
- fix restart.inc (related to pgrep)
- fix and recompile kloxo.c (using 'SSLv23_method' instead 'TLS1_method')
- fix create letsencrypt ssl (mod acme-challenge.conf) under apache
- use '-y' for phpm-installer under phpm-install-process.sh
- mod changeport.php (related to include file)
- combine function.sh and kloxo-wrapper
- mod kloxo.init
- mod kloxo-wrapper.sh (always use lxphp.exe instead kloxo.exe in low memory)

* Sat Feb 04 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017020402.mr
- change from 'libmemcached10' to 'libmemcached' dependencies for phpm
- fix kloxo.init

* Fri Feb 03 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017020301.mr
- use 'pgrep' instead 'service status' for detect running service (prepare to CentOS 7)
- use php 5.6 if php 5.4 not exists for panel

* Sun Jan 29 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.c-2017012901.mr
- change to list of mail account for MailForward
- use php56u instead php54 if php54 not exists in install process (also prepare for CentOS 7)
- change status from 'b' (beta) to 'c' (candidate)

* Wed Jan 25 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2017012502.mr
- mod apache configs related to pagespeed on/off
- disable keep-alive for nginx-proxy and reduce keep-alive for nginx
- move keep-alive to server level
- separated php-fpm-error.log and php-error.log for multiple php
- add 'current login ip' in 'information' table
- add 'getRemoteIp' function
- mod ser-fs script related to 'open files'
- add mount sudoers in set-kloxo-php script
- mod help for set-php-branch
- add missing spamdyke_rbl.txt.original
- fix domains.conf.tpl for nginx (related to pagespeed for nginx)

* Wed Jan 11 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2017011101.mr
- mod/fix cron-clearcache (add restart-all)
- fix clearcache-pagespeed
- change ttl for dns from '86000' to '1209600' (rfc1912)
- reduce keepalive_timeout for nginx from 180 to 15 (handle for slowread attack)
- remove '--keep-alive' in reverse-proxy for hiawatha (handle for slowread attack)
- increasing 'LimitInternalRecursion' from 100 (default: 10) to 256 for apache
- add logrotate for php-error.log

* Fri Jan 06 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2017010601.mr
- remove 'mysql.allow_persistent' from php/php-fpm configs
- increasing req_limit_per_ip to 50r/s for nginx
- increasing rlimit_files for php-fpm
- change port from '21' to '/etc/init.d/pure-ftpd status' for watchdog
- mod for suphp2.conf (add tpl)
- mod 'check_if_port_on' function
- disable 'rpm -qa qmail-toaster' for __path_mail_root
- change log name and path for kloxo-hiawatha
- mod kloxo.init (related to detect kloxo-hiawatha run or not)
- add letsencrypt-renew script
- add mysql-purge-logs (still need root password)

* Wed Dec 28 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016122801.mr
- change log_level from 'notice' to 'error' for php52-fpm-global-pre.conf.tpl
- disable 'events.mechanism' (make auto detect) for php53-fpm-global.conf.tpl
- adjust double 'catch_workers_output = yes' in php53-fpm-pool.conf.tpl
- update phpmsiler (not implementing yet)
- add '--skip-broken' for 'yum' in phpm-installer

* Fri Dec 23 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016122302.mr
- enable pagespeed under nginx (beside under apache)
- add status.conf for server-info and server-status under apache
- add change-qmail-ssl script for change default ssl to one of domain ssl
- add kill-zombie script; add enable-selinux (in permissive mode aka for log only)
- make enable update Kloxo-MR 7.0 under panel
- make 'request_terminate_timeout' as the same as 'max_execution_time' for php-fpm (timeout issue)
- mod dovecot.toaster.conf related to ssl
- make the same 'show stats' icon for webalizer and awstats
- mod stats url for 'createShowAlist' in domainlib.php

* Fri Dec 16 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016121602.mr
- add renew cron in fix-cron-ssl
- move ssl renew cron from crontab to /etc/cron.d/letsencrypt_renew and startapi_renew
- always run acme.sh-installer in cleanup
- always remove renew ssl cron from crontsb in acme.sh-installer

* Tue Dec 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016121301.mr
- fix for delete 'main' ftpuser

* Mon Dec 12 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016121201.mr
- make using '/usr/bin/contab' instead 'contab' in fixcron
- convert '--all--' to '*' om crontab
- select '--all--' automatically if not choose options in complex cron (handle 'can_not_be_null' error)

* Sun Dec 11 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016121101.mr
- fix setup-afterlogic (change 'setting.xml' to 'setting.xml.php')
- fix etc_suphp.conf.tpl (related to secodary php)
- remove php*.fcgi and then use php.fcgi.tpl inside phpini__synclib.php

* Sat Dec 10 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016121002.mr
- mod smtp in 'switch programs' (disable/enable include 'send')
- add $sgbl global for handle path in weblib.php
- disable delete php error log in fixlogdir (because using all-in-one error.log)
- fix phpm-installer (using detect phpXYz-cli instead phpXYz; need for php 7.0+)
- fix phpm-installer (related to version detect and exclude nginx dependencies)

* Sun Dec 04 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016120401.mr
- fix grep logic for dnsnotify (need by djbdns)
- fix encrypt mail (rename tlshosts to tlshosts.old)
- increase '__for_phpm__upload_max_filesize' to '64MB' in php.ini.base
- disable letsencrypt-auto install in cleanup

* Thu Dec 01 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016120101.mr
- fix listen ssl for nginx (trouble in IPv6)
- mod set.web.lst (related to nginx)

* Wed Nov 30 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016113001.mr
- disable header logic in apache domains.conf.tpl (because trouble with hiawatha in proxy)
- add ossec log in 'log manager' (need atomic.repo)
- mod lxgpath logic for lxguard
- back to add list in hosts.deny, tcp.smtp and spamdyke blacklist_ip for lxguard

* Sun Nov 20 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016112001.mr
- fix backup process with include detect unbackup.lst
- move backup temp from /tmp to serverfile

* Sun Nov 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016111301.mr
- fix no_need_token file path
- add 'LimitInternalRecursion 100' to domains.conf.tpl of apache
- set to '/' for blank ftpuser path
- fix double mysqldb icon for client
- fix validate_ipaddress
- add unbackup.lst to list unbackup clients

* Sun Oct 09 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016100902.mr
- fix domains.conf.tpl for 'ns' (make like 'a')
- increase 'nice' value for webtraffic
- change time for fix-cron-ssl from per-month days to per-week
- move session_start to top of login index.php
- add 'go back to php login' for token_not_match message

* Mon Oct 03 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016100303.mr
- back to use http/30080 for ssl proxy (because sometimes weird for https/30443)
- fix setInstall for acme.sh and startapi.sh in lib.php
- disable 'performance_schema=on' in server.cnf (to reduce memory usage) in installer.php
- fix static_files_expire_text in nginx
- back to use https/30443 for ssl proxy but disable custom header for apache in proxy
- back to 'http/30080' for nginx (need 'proxy_set_header X-Forwarded-SSL on' for https)

* Fri Sep 30 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016093001.mr
- fix installer.php (add 'libcurl-devel' install beside 'cult-devel')
- remove change 'releasever' in mratwork.repo in install process
- fix phpm-config-setup (related to zend_extension path)

* Thu Sep 29 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016092901.mr
- disable open_file_cache in nginx (trouble with add/update file in apps)
- increase limit conn from 25 to 50
- mod restart for spawn-fcgi

* Wed Sep 28 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016092802.mr
- add 'clear cache' for pagespeed in 'webserver configure'
- add 'clearcache-pagespeed' script
- mod blowfish_secret for phpmyadmin
- mod/fix nginx related to gzip
- mod proxy config in nginx related to pagespeed
- add gzip for lighttpd
- fix lighttpd related to gzip and prettyurls
- fix proxy for nginx related to 'Accept-Encoding'

* Tue Sep 27 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016092701.mr
- fix create '/root/.ssh' in writeAuthorizedKey function in sshauthorizedkey__synclib.php
- fix download_from_* functions in lib.php

* Sun Sep 25 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016092502.mr
- add 'sendmail to ban' feature (still no fix script)
- fix phpm-config-setup (related to zen_extension)
- fix Sendmailban if select file instead dir
- fix data in lxguardhit table
- mod file_put_between_comments to remove 'blank' newlines
- mod block IP only using 'null routing' (without hosts.deny and spamdyke blacklist_ip)

* Fri Sep 23 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016092301.mr
- fix fcgid2.conf
- fix error_log for nginx (bug if using stats_log.conf)
- fix init.d for spawn-fcgi

* Wed Sep 21 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016092101.mr
- fix httpry logrotate
- fix syslog logrotate
- fix session_start in login_inc.php
- fix if using 'default' skin (set as 'feather' skin)
- fix 'rpm -qa' logic
- fix web server conf.tpl (related to static_files_expire)

* Sat Sep 17 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016091702.mr
- mod remove 32bit apps in 64bit OS in installer.php
- move 'token_not_match' handle from inc.php in login path to index.php in lib/php path
- fix kloxo logrotate
- fix phpm-config-setup (related to ioncube/sourceguard installer)

* Fri Sep 16 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016091601.mr
- add fix-configs-files script
- merge docroot, dirindex and configure_misc (www and https redirect) to webbasics
- fix microcache_insert_into if insert 0 (reset) value
- add pretext for docroot and microcache_insert_into

* Thu Sep 15 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016091501.mr
- make header and expire set per-domain
- fix logic for set 'header' in domains.conf.tpl
- add 'disable pagespeed' in 'web features'
- fix defaults.conf.tpl in apache (remove 'header' code)
- mod default_index.php (for message for 'token_not_match' and 'blocked')
- mod phpm-config-setup (related to ioncube and sourceguardian binary)
- mod restart to always copy php files in login
- use session instead query for blocked login
- add time remain if blocked login
- fix time to blocked login

* Tue Sep 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016091302.mr
- mod default_index.php (for 'token_not_match' and 'login_error')
- mod cp, webmail and stats always use 'front-end' in web proxy
- fix domains.conf.tpl for nginx and lighttpd (because wrong using commenting)

* Mon Sep 12 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016091201.mr
- fix session path for kloxo-php-fpm.conf
- mod/fix ioncube-installer
- add sourceguardian-installer
- mod/fix panel login
- mod mmail/mmail__qmaillib.php
- disable 'xinetd restart'
- disable 'fix awstats'

* Thu Sep 08 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016090802.mr
- fix lxguard (if remove blocked IP)
- set to 'whitelist' also remove IP connection in lxguard
- fix php-fpm.init and php-fpm.init.base (related to PHP_INI_SCAN_DIR)
- fix set.database.lst
- add set.mysql.lst

* Wed Sep 07 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016090702.mr
- remove database.lst and add set.database.lst
- prepare unbackup certain users (add unbackup.lst)
- add error page for 400 and 502
- mod url for mratwork.com from http:// to // in error pages and default_index
- disable webhandler and webmimetype
- mod validate_prefix_domain (add stats)
- mod validate_server_alias (remove __base__)
- remove stats_dir_protect under 'web for' in hiawatha (because moving to stats.)
- move proxy_temp_path and fastcgi_temp_path from /temp/nginx to /var/cache/nginx
- fix getAndUnzipSkeleton in weblib.php
- prepare fastcgi for 'secondary php' (beside suphp and fcgid; TODO)
- fix defaults.conf.tpl for hiawatha (related to error pages)

* Mon Sep 05 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016090501.mr
- fix/mod sysinfo script
- fix validate_server_alias (related to wildcards)
- disable 'custom error' (TODO)

* Thu Sep 03 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016090305.mr
- move 'domain.com/stats' to 'stats.domain.com'
- fix all web configs (related to 'stats' address)
- add 'remark' in cleanup (related to 'stats' address)
- mod 'web selected' text under client
- add setCopyIndexFileToAwstatsDir function in lib.php
- fix installMeTrue in web__lib.php (related to fixweb)
- add 'stats' in 'SAN' for add letsencrypt and startapi ssl
- fix apache and hiawatha (related to startprotext)
- fix hiawatha (related to always use php-fpm for awstats)
- add missing fixdnsaddrecord script
- mod fixssl also update ssl in kloxo database
- mod fixssl also check update_ssl in /etc/cron.d
- add fix-cron-ssl for running ssl in every month
- fix redirect stats in nginx
- fix stats url (related to not use permalink)

* Thu Sep 01 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016090101.mr
- set no unzip skeleton if index.html exists in document root
- fix shell_access under client (no change setting and just appear)
- fix menu in 'simplicity' (related to 'ftp session')
- add fix-mysql-tmp (prepare to change tmp dir)
- add ioncube-installer (prepare change installing without rpm; still only for 'multiple php')

* Tue Aug 30 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016083001.mr
- use '127.0.0.1' instead 'mail.domain.com' for domain setting for rainloop
- use mailqueue script instead direct qmHandle
- fix lxbackuplib.php (for delete old backup files)
- mod mailqueue
- mod allow_url_include_flag to off as default
- remove unused php in bin
- add 'advanced php configure' icon/menu
- mod 'web selected' and 'php selected' info in 'web features'
- make possible hostname with _ (underscore) in dns setting/template
- add missing fixftpuserclient.php
- rename fixsimpldocroot.php to fixsimpledocroot.php
- add fixdnsaddrecord/fixdnsaddrecord.php
- add expire in header_base.conf in apache
- fix 'cache_expire' and move from domains.conf.tpl to defaults.conf.tpl in hiawatha

* Fri Aug 26 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016082601.mr
- add fix-rainloop-domains (add domains ini automatically in rainloop)
- change fix to add/del-rainloop-domains and include in add/del domain
- back to use $obj->was() in fix
- fix phpini_synclib.php related to phps

* Wed Aug 24 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016082402.mr
- add enablephp logic in domains.conf.tpl in apache
- fix fix-qmail-assign.php related to 'remote mail'
- remove unused global object in lib.php
- fix upload page (disable * in css)
- mod mem-usage
- add download_from_remote and download_from_scp in lib.php
- back to use previous fix-qmail-assign.php

* Thu Aug 18 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016081802.mr
- fix 'webmail for parked' in domains.conf.tpl for nginx
- add missing 'webmail for redirected' in domains.conf.tpl for nginx
- add missing 'dirindex' in nginx

* Wed Aug 17 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016081704.mr
- more accurate add exclude to /etc/yum.conf in cleanup process
- add warning in counter-start.inc if lxphp.exe not exists
- fix add 'exclude=' in /etc/yum.repos (no add if not exits)
- merge cleanup code to cleanup.inc
- move 'urgent' portion from cleanup to fix-urgent
- move detect lxphp.exe from counter-start.inc to cleanup.inc

* Tue Aug 16 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016081602.mr
- change 'schedule backup' based on scavenge to cron (file inside /etc/cron.d)
- mod db_get_value to possible passing with array args
- add setCronBackup in cleanup
- add execute 'fix-cron-backup' in postUpdate in lxbackup.php
- disable schedulebackup.php (always return null)
- rename backup_main to restore_main in restore.php
- disable 'program_interrupted' stage (still using original 'doing')
- enable hidden 'restore from ftp' (with mod and fix)

* Mon Aug 15 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016081504.mr
- fix schedulebackup.php
- fix appear in 'index manager'
- make simple for dirindex logic in weblib.php
- mod again for schedulebackup.php related to time logic

* Sun Aug 14 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016081403.mr
- implementing custom web config with customs dir
- change backup file to 'kloxomr70-scheduled'
- fix mebackup related to remove 'engine'
- add 'time to backup' feature for clients
- use pdns.sql with compatible to 3.4 version
- add 'parked domain' in 'san' of letsencrypt
- make domain able access via 'ip/domainname'
- re-chown '/var/bogofilter' dir
- fix nginx domains.conf.tpl
- reupload hiawatha domains.conf.tpl (because wrong file that using lighttpd)
- mod backup time only possible by admin only
- change default time backup (6 for admin and 18 for clients)
- mod setup.sh/installer.sh related to install mysqlclient


* Sat Aug 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016081301.mr
- fix webserver conf.tpl (especially for nginx)
- add install 'yum-presto' in cleanup

* Thu Aug 11 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016081102.mr
- change 'usage:' note for backup/restore
- change prefix backup from 'kloxo-scheduled-7.0' to 'kloxomr70-scheduled'
- make slim web server tpl (remove duplicates entries)
- disable 'rotate' in httpry and kloxo logrotate
- add 'php module status' in 'menu' for simplicity skin
- fix error warning for 'webstatisticsprogram', 'extrabasedir' and 'webmail_system_default' if not exists
- remove unused declare in defaults.conf.tpl of hiawatha
- fix fixssl for program ssl (related to broken-link files)

* Wed Aug 10 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016081001.mr
- add 'chkconfig on' for bind in list.transfered.conf.tpl
- change some icons (especially for start/stop/restart/enable/disable)
- implementing enable/disable php module

* Mon Aug 08 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016080801.mr
- add update-afterlogic, update-rainloop and update-roundcube (update without 'yum')
- mod sysinfo (add info for stats program)
- change set.mysql.lst to set.database.lst
- delete set.nginx.lst (set.httpd.lst still exists and need for detect apache 2.2 or 2.4)
- mod component list (base on set.list)
- fix domains.conf.tpl for hiawatha (related to indexfile for domain)
- add smtp_relay column in servermail table
- fix sshterm-applet path
- fix weblastvisitlib.php (related to 'Time' exists or not)
- use index.lst as 'default' indexfile for web
- disable chmod for '/var/bogofilter' (because not exists)
- mod phpm-config-setup (more accurate and detect for _unused.nonini)
- prepare for 'php module status' (for active/inactive module)
- mod domains.conf.tpl for hiawatha (stats_dir_for only declare if enablestats)
- fix phpm-config-setup (activate all various mysql modules)

* Mon Aug 02 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016080201.mr
- fix/mod resource appear (like 'memory_usage')
- mod getGBOrMB to process TB beside MB and GB
- add 'getNumericValue' (related to 'isQuotaGreaterThanOrEq' and 'isQuotaGreaterThan')

* Mon Aug 01 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016080101.mr
- disable 'request_header_access Proxy deny all' for squid (not work)
- mod/fix image appear in file manager
- mod upload_overwrite_warning message

* Sun Jul 31 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016073101.mr
- set overwrite always 'on' for upload file
- add redirect (using js) in upload file
- mod installer.php

* Sat Jul 30 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016073003.mr
- fix microcache value when set to '0' will be change to '5' (as default value)
- implementing 'progress bar' in upload process (need support html5 for browser)
- fix 'upload' (related to implementing 'progress bar)
- change 'overwrite' options to warning in upload file;
- mod js, css and form in upload file
- disable overwrite in upload process
- change warning color

* Thu Jul 28 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016072801.mr
- change db_schema format from serialize to php array
- fix phpm-config-setup (related php-fpm.ini for phpXYs)
- mod width and height for textarea for file edit
- change back to use microcache_insert_into (especially for hiawatha)

* Tue Jul 26 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016072602.mr
- increasing burst from 25 to 250 for limit_req in nginx
- mod mod_evasive.conf
- fix servermail (related to spamdyke blacklist_ip and dns_blacklists)
- change 'server mail settings' to 'mail server settings'
- move create log dir for httpry from lib.php to httpry-installer script
- mod httpry-installer related to httpry exists or not (no exists in CentOS 5)
- mod installer.php (related to disable iptables)
- mod disable BanOnMaxReqSize for hiawatha

* Sat Jul 23 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016072301.mr
- move http_proxy handle from php-fpm*.conf and proxy*.conf to header_base.conf in nginx
- add blocked mechanism in nginx for httpoxy vul
- fix 'include' for header_base.conf for apache

* Fri Jul 22 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016072203.mr
- add fix for httproxy vul in panel (where using hiawatha)
- mod setInitialServices for webserver (fix in install process)
- fix httproxy vul in squid (possible) and Varnish (no need for ATS)
- fix httproxy vul for reverseproxy in hiawatha-proxy

* Thu Jul 21 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016072106.mr
- fix webserver related to httpoxy (Vulnerability Note VU#797896)
- fix defaults.conf.tpl of lighttpd (replace to httpoxy vul)

* Thu Jul 21 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016072104.mr
- fix stats configs; mod httpry.init
- fix lighttpd alias
- move log url to stats_log.conf for nginx and hiawatha
- fix switch for web servers
- move partial code from setAllWebserverInstall to setAllInactivateWebServer and setActivateWebServer
- extract skeleton to httpdocs panel
- fix image urls of error pages
- fix installMeTrue in web__lib.php
- fix wrong var in setActivateWebServer in lib.php

* Tue Jul 19 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016071902.mr
- mod stats config to customize (in weblib.php)
- add random password for stats in create website
- disable always stats dir protect
- mod httpry.init

* Mon Jul 18 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016071802.mr
- fix pagespeed.conf (related to deflate)
- add error handler in lighttpd
- fix default_index.php if not panel login page
- fix webserver switch
- fix error pages (related to image links)
- fix activate spawn-fcgi
- fix/optimize webserver switch

* Sun Jul 17 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016071703.mr
- fix pagespeed.conf for apache
- fix uninstall process (just inactived) for webserver
- add httpry
- add 'rpms' (beside 'backuper') as exclude user backup
- fix select file in restore process
- add httpry in restart-syslog
- add mod_evasive.conf for apache
- add 'httpry' in 'log manager'
- fix restart-list.inc
- mod setInstallHttpry in lib.php

* Thu Jul 14 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016071402.mr
- mod lighttpd, nginx and hiawatha configs to handle ddos attack
- add startapi.sh log in 'log manager'
- fix all webservers installing
- add 'net.ipv4.tcp_synack_retries' in sysctl.conf in install process
- fix 'php_ini_scan_dir' for 'php branch' in php-fpm.init

* Wed Jul 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016071301.mr
- disable easyinstaller in domain icon
- fix acme.sh-installer and startapi.sh-installer for missing log dir
- disable driver_app declare in fixdns.php

* Mon Jul 11 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016071102.mr
- move create lighttpd logdir from fixweb to defaults.conf.tpl
- mod/fix sysinfo.php; add 'microcache' in 'web features'
- move 'X-Hiawatha-Cache' from add header in php file to domains.conf
- move microcache declare from globals to domains
- add microcache column in 'web' for kloxo database
- prepare php modules activate
- change lxguard rotate from 3 to 1 month
- add blackhole blocked for lxguard (possible no need hosts.deny and tcp.smtp to blocked)
- add header for 'X-Hiawatha-Cache' in apache (importance for hiawatha-proxy)

* Sun Jul 03 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016070304.mr
- fix nolog in lib.php
- fix disable_functions in php-fpm (make php-fpm.sh using php-fpm.ini instead php.ini)
- fix php-fpm.ini (related to __extension_dir__)
- add set.ftp.lst
- add ftp in 'component' list 
- fix phpm-updater (related to php-fpm.ini)

* Sat Jul 02 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016070204.mr
- re-enable 'component' button (with more accurate and fast process)
- change 'Component' class from 'Lxdb' to 'Lxclass' extends
- remove 'component' table from kloxo database
- change from 'Component Info' to 'component' for __desc in 'component' class
- fix set.php.lst (remove duplicate)
- add 'type' column for Component list
- make sure no duplicate for component list


* Fri Jul 01 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016070102.mr
- add 'W' (warning) input form (implementing for StartAPI SSL)
- add setPhpUpdate (update for branch and multiple)
- include setPhpUpdate in cleanup
- mod php.sh.base (change $* to "$@"; fix '-r' issue)

* Thu Jun 30 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016063002.mr
- add warning in StartAPI for issue, re-issue and revoke
- fix/mod acme.sh, startapi.sh and letsencrypt-installer

* Wed Jun 29 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016062904.mr
- add StartAPI SSL (alternative for Let's Encrypt)
- fix stats_awstats.conf for nginx
- fix acme.sh-installer
- mod switch-apache (sync to setAllWebserverInstall in lib.php)
- add missing __desc_upload_v_link in sslcertlib.php
- fix switch-apache (related to rpm detecting)
- fix startapi.sh-account

* Tue Jun 28 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016062804.mr
- mod phpm-installer (make devel also installing)
- add 'use pagespeed' in 'switch program'
- use 'optimize' .conf for installing pagespeed
- fix setAllWebserverInstall (missing spawn-fcgi and fcgiwrap)
- Fix inactivating webserver appear in setAllWebserverInstall
- fix stats dirprotect (must separated for awstats and webalizer)

* Mon Jun 27 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016062702.mr
- fix syslog logrotate
- prepare pdns 3.4
- fix nginx listen files
- fix 'web features' appear (related to 'php selected')
- mod redirect.php
- move header_ssl for lighttpd from defaults to domains.conf.tpl

* Sat Jun 25 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016062502.mr
- prepare easyinstaller (successor of installapp; possible change their name)
- fix/mod fixssl.php; mod sysinfo.php
- move 'Strict-Transport-Security' to header_ssl
- add 'X-Support-By Kloxo-MR 7.0' in header_base
- change max-age from 604800 to 2592000 for 'Strict-Transport-Security'
- add 'php-fpm type' in 'php configure'
- enable 'extrabasedir' for php.ini (espacially for php-fpm conf)
- add info 'login as' before 'click help'
- add blocked IP in spamdyke for smtp (beside in hosts.deny and tcp.smtp)
- disable CSRFToken in create_xml (because double)
- add 'chkconfig httpd on' in setup.sh (because inactive)
- add '--nocron' in acme.sh-installer
- move .db_schema to from '/file' to '/file/sql'
- change header 'X-Support-By' to 'X-Supported-By'
- reduce start, minspare and maxspare of pm in php-fpm

* Wed Jun 22 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016062202.mr
- mod add-debug and remove-debug; fix debug if commands.php have LF
- change parse_mail_log to parse_smtp_log and mailLogString to smtpLogString for lxguard
- change identify from 'vpopmsil' to 'vchkpw-smtp' for detecting smtp in maillog
- set 'invaliduser' and 'nopassword' as 'fail' (beside original 'fail') for smtp detect in lxguard
- add LF for default ssl files (make sure no '-----END CERTIFICATE----------BEGIN CERTIFICATE-----')
- fix sysinfo related to 'pop3'

* Tue Jun 21 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016062102.mr
- fix remove 'engine' in mysql dump for backup process
- change from if to switch for zip scripts in linuxfslib.php
- back to add process/detect for tgz till tar.xz (already fix in prevous issue)
- mod run files for qmail able to customize
- fix lxguard for exclude localhost IP
- change '= fail' to '!= success' for count_fail in lxguardincludelib.php 

* Mon Jun 20 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016062004.mr
- prepare change courier-imap and dovecot in 'switch programs'
- disable 'component' button
- fix sslipaddress__synclib.php for .ca file
- change using 'MariaDB' instead 'MariaDB-server' for install process
- mod mailincoming driver (for courier-imap and dovecot; ready to action)
- add mailoutgoing driver (for qmail; ready to action)
- change mailincoming to pop3/imap4 and mailoutgoing to smtp
- disable imap4_driver (make simple to uae pop3_driver for pop3 and imap4)
- mod sysinfo.php (to detect pop3/imap4 and smtp)
- add missing 'authlib' in pop3__courierlib.php
- fix default slavedb driver in installer.php
- fix login in setSyncDrivers for setting driver
- change save_xinetd_qmail to save_control_qmail function
- fix declare of smtp_driver in driver_define.php
- mod message of changeDriverFunc function
- remove slave_save_db process in setWatchdogDefaults
- fix logic in setSyncDrivers and add slave_save_db inside
- make short error message in lx_exception_handler
- mod dprint info for lx_core_lock in lib.php
- fix passing for slave for setSyncDrivers in lib.php
- add add-debug and remove-debug script
- fix remove engine in backup dump file
- disable detect new tgz till tar.xz in lxshell_zip_core (backup process problem)

* Sun Jun 19 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016061901.mr
- add cache_expire for hiawatha
- fix redirect (like /webmail) for nginx
- prepare for implementing dovecot as courier-imap alternative
- prepare for using pop3 from courier-imap instead qmail-toaster
- add remote mail for lxguard (beside ssh and ftp; not include webmail login)
- prepare change courier-imap and dovecot in 'switch programs'
- disable 'component' button; fix sslipaddress__synclib.php for .ca file
- change using 'MariaDB' instead 'MariaDB-server' for install process

* Wed Jun 15 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016061502.mr
- mod sysinfo.php
- fix nofixconfig (disabled because not used)
- change webserver model (install all web server together)
- add setAllWebserverInstall function (execute in cleanup or change web server)
- add tgz, tbz2, txz and p7z in lxshell_zip_core function (prepare for zip selected in 'file manager')
- mod kloxo.init (remove for hiawatha init remove)
- mod nsd configs
- remove reload in nsd restart (because include init for restart)
- mod always use useLocalConfig (pure and proxy)

* Mon Jun 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016061303.mr
- make the same dirprotect rule for all stats
- make the same url for all stats
- fix secondary dns in nsd (set restart dns equal to reload and restart)
- fix php-fpm restart (make stop, delete sock files and start)
- add 'notify-retry 5' for slave dns in nsd
- change default ssl with CN as 'Kloxo-MR' and expire until 100 years
- delete program ssl in /file/ssl
- delete fix_self_ssl function

* Mon Jun 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016061301.mr
- add 'secondary php' info in sysinfo.php
- fix '/.well-known' dir (related to create letsencrypt ssl)

* Sun Jun 12 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016061203.mr
- enable 'Strict-Transport-Security' for ssl with '1 week' age
- mod conf.tpl code for apache
- fix ssl for lighttpd (now running well; using socket instead scheme)

* Sun Jun 12 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016061202.mr
- fix ssl for apache (no 'SSLCompression Off' for apache 2.2)
- mod SSLCipherSuite for apache (make more secure)
- add checking 'http_v2_module' for nginx (because no exists in nginx for CentOS 5)
- fix/mod file_exists logic in webserver configs

* Sat Jun 11 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016061105.mr
- move fixweb and restart-web process from ssl .sh to sslcertlib.php
- reconstruct 'default' ssl file (using root ca from cacert.org)
- fix ssl for apache (using secure cipher)
- move static ssl text to ssl_base.conf for apache
- fix copy spawn-fcgi to sysconfig dir
- fix copy webserver init in web__lib.php
- mod defaults.conf.tpl and domains.conf.tpl for lighttpd (ssl still not work)
- add missing httpd24.init
- mod/fix lighttpd globals confs
- add 'rename' in 'tab' of 'file manager'
- change 'cron scheduled task' to 'cron task'
- add 'all clients' in 'tab' of 'all'
- add missing .ca and .csr of default and program ssl

* Fri Jun 10 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016061002.mr
- fix update process for acme.sh-installer and letsencrypt-installer
- add 'column' for alter in db-structure-update.sql
- split permissions and ownership page in 'file manager'
- fix acme.sh-installer
- mod installer and remover for acme.sh and letsencrypt

* Thu Jun 09 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016060903.mr
- fix sysinfo.php (related to spam apps)
- fix return page for 'remove' file in 'file manager'
- mod zip extract (different action for .tar.gz and gz; also for bz2 and xz)
- extract tar.gz with options extract to tar (also for bz2 and xz)
- change different name format for NewArchive (action from ZIP in 'file manager')
- rename coreFfilelib.php to coreffilelib.php
- action as 'insert into' instead 'update' in db_set_value if data not exists
- add delay 10 for stop/reload of php-fpm and phpm-fpm; add '\n' in merge ssl files to .pem in fixssl.php
- fix php_selected convert

* Tue Jun 07 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016060703.mr
- better 'web features' appear (maybe change if implementing 'multiple webserver')
- back to enable setWebserverInstall and always copy init for webserver
- fix acme.sh-installer (related remove cron created by acme.sh)
- add acme.sh-remover

* Mon Jun 06 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016060603.mr
- fix fixssl.php (ssl file must content '-----BEGIN' to next process)
- use cp instead ln in acme.sh.tpl and letsencrypt.sh.tpl
- list letsencrypt for acme.sh and certbot in 'log manager'
- mod sslcertlib.php (make acme.sh as priority if installed instead letsencrypt-auto)
- implementing callWithSudo (thanks smierke)
- fix acme.sh-installer and letsencrypt-installer
- fix acme.sh.tpl (use 'bogus_command' trick for return value)
- use copy ssl files instead symlink for acme.sh and certbot
- remove unused code; deleteSpecific always delete old ssl files for acme.sh and certbot together
- fix $extrabasedir return value in web__lib.php
- also copy dile config for acme.sh in /opt/configs
- disable sudo code in remotelib.php
- fix acme.sh.tpl (related to error message; include 'skip renew')

* Sun Jun 05 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016060505.mr
- fix djbdns dir (no move from /home to /opt/configs)
- fix httpd.init
- disable setWebserverInstall (for custom web init)
- change webselector to webfeatures var
- fix setup.sh and installer.sh related to MariaDB installing
- fix acme.sh-installer (certain trouble in CentOS 5)
- mod/fix sysinfo.php
- fix sysinfo.php (fix 'php used' logic)
- change Alias/ScriptAlias to AliasMatch/ScriptAliasMatch in domains.conf.tpl for apache

* Sat Jun 04 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016060408.mr
- mod fixssl (not fix program ssl if symlink)
- mod sslcertlib.php (set as symlink for program ssl if taken from domain ssl)
- fix/mod fixssl.php and sslcertlib.php (make simple logic using array; disable unused var)
- mod fixssl (also recreate ipaddress ssl)
- mod fixssl.php (no process for ipaddress ssl if symlink; like program ssl)
- fix fixlxphpexe (wrong logic for php target)
- fix phpm-fpm.init (if '/opt/configs/php-fpm/php*m' no exist)
- mod phpini__synclib.php (disable unused var)
- fix getMultiplePhpList (return blank array if empty)
- fix lloglib.php (related to letsencrypt log)
- fix pserverlib.php (disable no_fix_config)

* Fri Jun 03 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016060305.mr
- fix djbdns conf.tpl and init
- mod fixssl (add fix for domains based on data from kloxo database)
- fix sslcertlib.php in deleteSpecific
- add fix.lst (make customize fix process list in cleanup)
- change getRpmBranchListOnList to getListOnList

* Fri Jun 03 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016060302.mr
- fix fixlxphpexe (must input with prefix 'php')
- mod restart.inc (related to php-fpm)
- add help for set-kloxo-php; fix 'multiple php' install and remove list
- mod defaults.conf.tpl for nginx
- disable reset to fpm mode if running cleanup
- fix sslcertlib.php (related to deleteSpecific)
- fix acme.sh.tpl and letsencrypt.sh.tpl (related to run fixweb)

* Wed Jun 01 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016060105.mr
- set no 'reinstall' letsencrypt-auto in cleanup
- make always copy phpm-fpm in fixphp
- make possible customize for 'spawn-fcgi' in defaults.conf.tpl of nginx
- fix phpm-fpm for fresh install (no domain created)
- add 'chown 755' for phpm-fpm
- use sed to change 'exclude=mysql51*' to 'exclude=mysql5*' for install process
- add fix 'exclude=mysql51*' to 'exclude=mysql5*' under IUS repo for mratwork.repo in cleanup script
- fix letsencrypt-installer
- add restart-web in postUpdate in weblib.php

* Mon May 30 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016054002.mr
- fix/mod phpm-fpm.init (enable 'multiple php' but no install phpXYm; php52m service start)
- fix domains.conf.tpl for nginx (related to stats)
- set timeout together fastcgi and proxy in nginx conf (no need fixweb for switch between them)
- mod phpm-fpm.init

* Sun May 29 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052907.mr
- fix wrong delete conf for php-fpm if client deleted
- mod restart.inc (stop unwanted services)
- fix client__synclib.php related to delete php-fpm user
- mod nginx (can handle cgi via spawn-fcgi + fcgiwrap; but awstats still not work)
- fix nginx for proxy location

* Sun May 29 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052903.mr
- mod postUpdate function in phpinilib.php to use set-php-fpm
- delete ssl also delete file inside /etc/letsencrypt
- mod getInitialPhpFpmConfig to execute set-php-fpm also use_phpXY.flg
- mod acme.sh-installer and letsencrypt-installer to add '-O master.zip' in wget process
- mod set-php-fpm to use add-restart-queue instead restart-php-fpm
- add start-php-fpm and stop-php-fpm script
- make simple logic for install php for 'multiple php'
- add feature for remove php for 'multiple php'
- change to use suphp for handle cgi (because no need cgi module)
- mod nginx proxy conf for only passing to apache only for php, pl, py, rb and cgi
- fix phpini__synclib.php (mkdir for 'php/php-fpm.d' if not exists also in client level)
- change 'perm' to permission', 'ren' to 'rename' and 'dn' to download in 'file manager'
- make clickable for 'owner' with as the same as 'permissions' link
- add 'spawn-fcgi' in 'restart-list.inc'
- use suphp instead using cgi module for execute cgi (like perl in awstats) in apache
- fix awstats in hiawatha and stats dirprotect
- mod lightpd php-fpm and awstats conf
- fix set for hiawatha webalizer directory
- mod fixweb tp always overwrite httpd.conf in /etc/httpd/conf

* Wed May 25 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052507.mr
- add fix and restart web in acme.sh.tpl and letsencrypt.sh.tpl
- mod php-fpm.init.base and php-fpm.init.base
- mod nginx related to ssl
- mod ssl_base.conf for nginx (add missing 'ssl on;')
- add missing add-restart-queue script

* Wed May 25 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052503.mr
- separated php-fpm and phpm-fpm init in multiple php-fpm
- fix execute getInitialPhpFpmConfig if phpm-fpm not exists in /etc/init.d
- mod php-fpm.init.base
- mod restart.inc
- mod set-php-fpm
- always copy phpm-fpm.init to /etc/rc.d/init.d in cleanup process

* Tue May 24 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052501.mr
- add missing 'listen.owner' and 'listen.group' in 'default' pool of php-fpm

* Tue May 24 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052409.mr
- change setInitialPhpFpmConfig to getInitialPhpFpmConfig (because return active 'php-fpm' value)
- fix php_used logic with using getInitialPhpFpmConfig
- change php-fpm.init.base from customize to basic code
- set phpm-installer always execute phpm-config-setup
- fix set-php-fpm for php_target; add 'phpm-fpm' in 'services' list
- set no execute set-php-fpm if flag file exists for 'php used'
- add change flag for set-php-fpm
- fix merge files in acme.sh.tpl and letsencrypt.sh.tpl (bash bug?)
- fix getInitialPhpFpmConfig logic (related to active php detect)
- fix getInitialPhpFpmConfig again (related to 'custom_name')

* Tue May 24 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052404.mr
- enable php52m in 'multiple php'
- set to 1/3 of maxchildren value for php52m (because only 'static' instead 'dynamic'/'ondemand')
- convert 'php branch' to 'php' in getPhpSelected
- use 'php' as default and no impact if enable 'multiple php' for set-php-fpm
- enable 'php52m' option in 'php selector'
- fix set-php-fpm (reduce double logic related to 'multiple php')
- fix restart-list.inc (missing phpm-fpm in list_services and list_all)
- fix setInitialPhpFpmConfig logic
- mod setInitialPhpFpmConfig for phpXYm
- add logic for php-fpm in restart.inc

* Mon May 23 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052303.mr
- implementing 'multiple php' for php-fpm (except for php52m because still trouble)
- 'multiple php' using 'phpm-fpm' init instead 'php-fpm' init
- make 'return' for all function commandlinelib_old.php
- move pool configs for 'php branch' from /etc/php-fpm.d to /opt/configs/php-fpm/conf/php/php-fpm.d
- fix fixphp related to php-fpm
- add missing php<52/53>-fpm-default.conf.tpl
- fix phpm-fpm (for disable php52m)
- add missing 'php in list of all php in phpm-fpm

* Sun May 22 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052206.mr
- set http/2 for nginx
- fix getCleanRpmBranchListOnList function (for the same value)
- fix os_set_quota
- add init_set for memory_limit for sqlitelib.php
- fix letsencrypt-installer for set cron
- fix ~lxcenter.conf.tpl
- fix letsencrypt-installer
- upload missing letsencrypt-cron.sh
- mod acme-cron.sh
- disable install acme.sh
- fix copy letsencrypt config
- fix defaults.conf.tpl for nginx (related switch_*.conf)
- mod phpm-config-setup
 
* Sat May 21 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052103.mr
- use letsencrypt-auto instead acme.sh (bug?)
- use '--webroot' for letsencrypt
- add http/2 feature for apache
- add merge and symlink info to log for letsencrypt
- mod pure-ftpd.init
- install acme.sh and letsencrypt-auto together
- prepare 'keep-alive' setting for apache
- fix install_if_package_not_exist function
- fix changeport.php
- fix letsencrypt-installer script

* Sat May 21 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016052101.mr
- mod install_if_package_not_exist
- fix acme-cron.sh
- mod acme.sh.tpl
- fix/mod acme.sh-installer (related to add cron)
- mod fix-yum; acme.sh.tpl also create symlink to /home/kloxo/ssl
- remove unwanted code in phpinilib.php
- mod 'memory_limit' to '-1' in kloxo-php-fpm.conf and php.ini.bsse
- patch for HTTPPort from '80' to '60080' in acme.sh (because using 'standalone' instead 'webroot')
- fix fixssl (also handle letsencrypt ssl)
- fix acme.sh.tpl (related to symlink)
- prepare phpini__synclib.php (related to 'multiple php-fpm')
- change 'web / php selector' to 'web options'
- add 'timeout' beside 'web selector' and 'php selector' (prepared)
- change default index files sort
- change 'microcache' time from 10s to 5s
- fix acme.sh.tpl (related to error exit)
- fix domains.conf.tpl for hiawatha
- fix 'fastcgi pass' for '/__kloxo' in lighttpd
- fix passing timeout value (bug?) in nginx
- fix include declare in domains.conf.tpl for lighttpd

* Wed May 18 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016051801.mr
- fix kloxo logrotate
- fix acme.sh.tpl (log for error)
- fix install_if_package_not_exist function in lib.php
- re-enable setCheckPackages in cleanup
- add lxjailshell install in installer.php

* Tue May 17 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016051704.mr
- fix acme.sh-installer (for CentOS 5)
- fix/mod restart process
- add ocsp stapling for apache and nginx
- change '--Use PHP Branch--' to '--PHP Branch--' in serverweb
- prepare for add 'timeout' for web
- change ssl ready for client (beside admin and domain)
- fix menu (related to ssl); prepare spam.lst
- mod packer.sh
- disable ssl stapling (not work especially in Apache)
- fix php-fpm restart process

* Sat May 14 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016051401.mr
- fix acme.sh-installer (related to /root/.acme.sh dir and cron job)
- fix data issue for sslcert (importance for ssl update feature)
- fix/mod nomodify appear
- fix ssl for text and file upload process

* Fri May 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016051305.mr
- merge acme-cron.sh and acme-pem.sh to acme-cron.sh
- use /usr/bin/acme.sh (need symlink) instead /root/.acme.sh/acme.sh
- remove letsencrypt-auto if exists
- fix/mod acme.sh-installer
- merge acme.sh-installer and acme.sh-setting to acme.sh-installer
- fix/mod fixsslpath

* Fri May 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016051303.mr
- change ssl path; disable pkill in hiawatha restart process
- disable Strict-Transport-Security header (trouble if other apps not use valid ssl)
- add username in sslcert table
- ssl in admin only for 'self assign' and in website for 'upload', 'letsencrypt' and 'link'
- adjustment for list appear for ftpuser, mailforward, mailinglist dan ddatabase
- fix .pem (key+crt instead crt+key)
- change error appear from text input to textarea
- mod warning if not FQDN qualified in install process
- using acme.sh instead letsencrypt-auto for letsencrypt ssl
- add missing acme.sh-installer
- change letsecrypt log
- fix change from letsencrypt-auto to acme.sh
- split acme.sh-installer to acme.sh-installer and acme.sh-setting
- fix acme.sh.tpl
- add missing fixsslpath script (move to new ssl files path)
- add letsencrypt-remover (because using acme.sh)
- fix acme.sh-installer
- fix acme.sh-setting
- fix fixsslpath
- fix letsencrypt-installer

* Wed May 04 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016050403.mr
- fix MaxRequestSize for hiawatha (2047 x 1024)
- fix sslcertlib updateform
- prepare 'all' list for ssl
- mod/fix letsencrypt-installer

* Wed May 04 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016050402.mr
- add 'Access-Control-Allow-Origin:*' header in webserver configs
- fix mysql-optimize.php for 'error message'
- mod description for 'CSR' of 'self assign ssl'
- remove 'Copy of' gif
- mod/fix 'MaxRequestSize' for hiawatha
- mod mem-usage script
- fix fetchmailticket.sh
- fix cleanspamdyke.php (change xinetd to ftp)
- disable cgi module in apache (security reason)
- add/fix watchdog for ftp
- fix wddx config for php 5.4
- fix restart-services
- mod letsencrypt.sh.tpl
- ready for letsencrypt ssl
- mod/fix nomodify appear
- fix letsencrypt-installer
- enable header_base if .ca file exists
- disable RequiredCA in hiawatha (trouble for https access)
- combine .key, .crt and .ca to .pem
- fix header_base.conf format
- ready for 'link' ssl
- fix header_base.conf for nginx

* Thu Apr 07 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016040705.mr
- add webserver 'header' to make more secure website
- make webserver include file use 'customize rule'
- fix acme-challenge include logic in apache
- fix add header in lighttpd
- move add header to https portion in webserver
- fix header_base.conf for webserver
- fix db-structure-update.sql
- fix lighttpd conf.tpl
- fix freshclam restart
- fix/rename headerbase to header_base param in webserver tpl 
- fix db-structure-update.sql (related to frontpage)
- fix freshclam inactivated
- disable 'Strict-Transport-Security' header

* Tue Apr 05 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016040502.mr
- fix symlink for chkconfig in cleanup
- make maximize MaxUploadSize and MaxRequestSize for hiawatha
- disable domain related for icons under customer (the same way for admin and reseller)
- disable cgi module for apache
- change x-httpd-php link for suphp
- fix run for smtp-ssl
- fix db-structure-update.sql (for backward compatibility)
- mod sslcertlib.php
- fix setInitialServer
- mod nomodify display
- fix warning for phpm-installer
- fix ~lxcenter.conf for lighttpd (no need errorloghack for latest version
- mod defaults.conf.tpl and domains.conf.tpl for lighttpd (use http-scheme instead server-socket for ssl)
- add validate for 'my name' in 'server mail settings'
- fix secure setup-rainloop.php

* Sun Mar 27 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016032701.mr
- make sure restart mean 'restart -y' in lxserverlib
- update process make restart as stop, pkill and start
- mod restart processes (remove start if pid not exists)
- fix syncserver in getUserList() at web__lib.php
- make stop upcp if hoatname not FQDN qualified
- make symlink for chkconfig to /usr/bin
- fix redirect in nginx
- fix display in 'php used' if phpXYm not installed
- add symlink for chkconfig in cleanup (fix for running chkconfig in cron)
- fix redirect cp, webmail and kloxo in hiawatha and nginx
- always force install php54s in install process
- fix 'not_ready_to_use' for 'enable apache 2.4'
- disable 'no_fix_config'
- change application.ini to application.ini.php and default admin password for rainloop
- mod set.php.lst; mod mysql restart process
- mod php-fpm.conf.tpl (for php 5.2)
- mod db-structure-update.sql
- mod sslcertlib.php
- mod phpm-config-setup (related to mysql modules)
- mod mailqueue script
- fix for select 'php-fpm' for 'php type'
- remove handling perl module in apache
- fix MaxRequestSize for hiawatha

* Wed Mar 02 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016030202.mr
- mod sysinfo.php
- add rar and 7z extract in 'file manager'
- make root able extract to current dir; fix set-kloxo-php
- add install rar and 7z in installer.php
- add-zips script for add additional compression apps

* Fri Feb 26 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016022601.mr
- fix uninstallMeTrue for httpd
- fix 'log manager' path in 'address'

* Wed Feb 24 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016022403.mr
- remove 'COLUMN' and set NULL value for ALTER for db-structure-update.sql
- mod sysinfo (prepare for multiple web server)
- fix defaults.conf.tpl if httpd 2.4 not installed

* Tue Feb 23 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016022302.mr
- fix fix-qmail-assign.php (account prefix as the same as domain prefix)
- fix phpm-installer (change priority to phpXYu, phpXY and then phpXYw)
- add z-memcached in phpm-config-setup

* Mon Feb 22 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016022202.mr
- fix shexec and move to sbin in kloxo path
- change 127.0.0.1 to localhost for proxy_fcgi in apache
- change absolute path to relative for kloxo path
- mod 'php type' list with depend on apache version
- mod shexec function
- fix to copy for .fcgi file
- mod 'rule' for enable 'web / php selector'
- add set-kloxo-php in cleanup (that mean use php-fpm until implementing shexec)
- add proxy_fcgi for 'php type' in httpd 2.4
- fix db-structure-update.sql
- fix defaults.conf.tpl related to httpd 2.4 mpm
- add fixskeleton in cleanup
- mod note for raw-restore
- mod help info in fix.inc

* Sun Feb 14 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016021403.mr
- mod/fix apache configs (relate to mod24u modules)
- use httpd.init from apache 2.4
- fix hiawatha.conf
- prepare for use hiawatha-monitor
- add param for gzip of nginx
- add 'multiple_php_already_installed' in phpinilib.php
- fix 'switch programs' (related to apache24)
- fix defaults.conf.tpl for detect httpd24
- fix pserver/pserverlib.php related to web server
- mod/add mod24u_fastcgi in installMeTrue in apache
- mod apache for use the same 'php type' modules (disable proxy_fcgi in apache 2.4)

* Fri Feb 12 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016021202.mr
- fix menu for 'all_mailinglist'
- change MinSSLversion to MinTLSversion (related to hiawatha 10.1)
- change RequireSSL to RequireTLS (related to hiawatha 10.1)

* Wed Feb 10 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016021005.mr
- fix phpini related to add/mod .htaccess
- fix phpini related to user detect
- mod/fix pure-ftpd if running cleanup and fixftp
- fix list in 'multiple php already installed'
- fix acme-challenge.conf include position in apache

* Mon Feb 08 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016020801.mr
- change hiawatha reload to restart in process
- mod letsencrypt.sh.tpl
- fix lighttpd 'default' ssl
- fix phpm-all-install and phpm-all-setup
- mod restart-list.inc (add perl-fastcgi)

* Sat Feb 05 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016020503.mr
- fix syslog logrotate
- fix acme-challenge.conf in nginx
- fix sslcert for self-assign
- add replace_to_space function
- change install mratwork repo from 'wget' to 'rpm -Uvh'
- add install-hiawatha-addons script
- prepare to use perl-fastcgi
- fix acme-challenge path
- change webroot-path of letsencrypt
- fix acme-challenge alias
- add letsencrypt.sh.tpl
- mod openssl.sh for domain
- fix throw in sslcertlib.php

* Mon Feb 01 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016020101.mr
- make possible spamdyke use custom spamdyke.conf template
- fix defaults.conf.tpl for nginx related to chown log and temp dir
- mod hiawatha related to reverseproxy (fix awstats issue)

* Sat Jan 30 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016013001.mr
- remove double location declare for nginx
- copy pbp-fpm_standard*.conf to php-fpm_wildcards*.conf for nginx
- back to enable the same hostname for multiple ip for 'A record'
- fix warning for phpm-config-setup and phpm-installer
- fix stats dir protect in hiawatha
- back to disable proxy_cache_use_stale in nginx-proxy

* Wed Jan 27 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016012701.mr
- add php70m for suphp in 'secondary php'
- make simple fix-chownchmod
- mod how-to-install.txt (use 'rpm -Uvh' instead download and 'rpm -ivh' for mratwork rpm)
- fix phpm-all-install and phpm-all-setup for --help
- make branchlist for custom possibility

* Thu Jan 21 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016012103.mr
- cleanup domains.conf.tpl for apache
- move gzip from lxcenter.conf to gzip.conf in globals for nginx
- change nginx user from nginx to apache
- prepare for tengine config
- prepare for pagespeed plugins in tengine
- fix page error for nginx
- fix installatron-install
- cleanup mem-usage
- hidden chown process in defaults.conf.tpl for nginx
- fix/mod fixweb.php
- fix chown in defaults.conf.tpl for nginx

* Tue Jan 19 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016011904.mr
- disable detect 'uname -m' in fixphpini.php because already exists in phpinilib.php
- mod sysinfo script
- add 'enable ssl/tls' in pure-ftpd
- change lxshell_return to exec for chkconfig
- change 'php configure' for domain to 'web selector' but 'php selected still disable
- remove 'multiple php ratio'
- make simple rpm add/remove for apache
- change 'blocked ip' and 'allowed ip' to 'blocked login' and 'allowed login'
- remove '--nolog' in fix scripts
- add 'validate_filename'
- use sh script instead rpm for installatron-install
- mod phpm-config-setup for copy www.conf
- add php53-fpm-global.conf.tpl
- fix defaults.conf.tpl for hiawatha related to phpselected
- fix sysinfo.php
- fix/set default value for webselected and phpselected

* Thu Jan 14 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016011401.mr
- fix fix-chownchmod related to apache:apache
- add openssl.sh.tpl (prepare create cert based on sh instead php)

* Wed Jan 13 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016011301.mr
- fix install/reinstall httpd24
- fix httpd.init

* Tue Jan 12 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016011202.mr
- move basic ssl part to ssl_base.conf in nginx
- change 'listen default' to 'listen default_server' in nginx
- change nginx ssl_ciphers in ssl_base.conf
- fix paths in nginx config templates

* Mon Jan 11 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016011106.mr
- fix php-fpm.init.base related to 'default' php
- fix/mod 'php configure' for web related to 'php selected'
- fix nginx configure related to phpselected
- fix default.conf for php-fpm
- fix php-fpm.init.base
- fix fixweb if httpd not installed
- fix nginx configs related to missing var_phpselected for 'web for'
- fix nginx configs related to php-fpm ssl
- fix detect httpd version/type
- fix detect phpselected

* Mon Jan 11 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016011101.mr
- fix make-slave script
- add 'acme-challenge' for web configs (prepare for letsencrypt)
- use port 30443 in web configs if web access using https
- message info to warning set IP assign to domain if server only have 1 IP
- set fix-chownchmod to except apache:apache ownership
- prepare for multiple php for use different pid and using special init (phpm-fpm.init)
- use new function for 'multiple php' list
- prepare php53-fpm-pool.conf.tpl for 'multiple php'
- change 'common name' entry type in create self-assign ssl
- fix webconfig related to phpselected
- fix switch programs (related to init)

* Tue Jan 05 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016010501.mr
- add https redirect beside www redirect
- fix initial pure-ftpd config

* Mon Jan 04 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016010404.mr
- add php70 for apache setHandler
- change php_rc from dir to direct to php.ini file path
- change use initd instead xinetd for pure-ftpd (prepare for CentOS 7)
- add pure-ftpd in service list
- set Quiet and ReallyQuiet as yes for webalizer
- add 'reverse' to 'make-slave' script
- fix inform and set 'chmod 755' for pure-ftpd init
- change disablephp to reverse enable php in domains.conf.tpl for apache
- fix 'bind' in pure-ftpd.conf

* Sat Jan 02 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2016010201.mr
- no list for ruid2 and itk if php (only php-cli) rpm not install in php-branch
- fix/add extrabasedir in php-fpm
- prepare for letsencrypt
- include install net-tools (ifconfig app) because not include in CentOS 7 (still in progress)
- add getdriver script

* Fri Dec 25 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015122501.mr
- change 'port configure' to 'port and redirect configure'
- add possible redirect panel to certain domain/ip

* Tue Dec 22 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015122202.mr
- possible install php70 (need enable webtatic repo)
- implementing maldetect (installer and fix 'log manager')

* Mon Dec 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015122102.mr
- prepare to 'ssl link' for web
- fix ssl for hiawatha and kloxo-hiawatha
- fix default.pem and program.pem
- fix htmllib to display help link
- translate for information list text
- mod sysinfo (need '-y' to run 'fix-service-list')
- add self rootCA
- add letsencrypt-installer and cli.ini.tpl (implementation still in progress)
- add tldextract.php
- set 'secondary php' for fcgid only under proxy because trouble under apache standalone
- back use .pem instead -all.pem (prepare for letsencrypt)
- mod sysinfo

* Fri Dec 11 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015121102.mr
- fix domains.conf.tpl for apache (missing extra linebreak in location of blockips)
- fix spamdyke value after update

* Thu Dec 10 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015121001.mr
- disable expire in kloxo-hiawatha (fix compatibility issue for hiawatha 9 and 10)

* Wed Dec 09 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015120903.mr
- add 'upgrade' option in mysql-optimize
- remove 'Allow from all' for Location in apache
- disable 'UseGZfile' and change 'IgnoreDotHiawatha' to 'UseLocalConfig' (prepare for Hiawatha 10.x)
- change 'display_startup_errors' from 'on' to 'off' for php.ini
- change default dmarc value for 'percentage_filtering' ('50' to '20') and 'receiver_policy' ('quarantine' to 'none')
- fix 'dns blacklists' appear for mail
- disable exception for restore (possible restore without detect client)
- disable fixdomainkey from fixmail-all (resolve cloudflare trouble)
- mod 'mem-usage'
- mod restart.inc
- mod/fix set-hosts
- mod set-php-branch
- fix change permissions and ownership for file in 'file manager'
- fix phpini warning after client created
- mod uinstall web driver (no need uninstall mod_*)
- disable static files expire for kloxo-hiawatha until v10.1 release

* Fri Oct 30 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015103001.mr
- make fix and restart to customize
- set switch dns and web without overwrite init file (trouble for httpd for init overwrite)
- mod httpd.init

* Fri Oct 23 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015102301.mr
- add 'perl' in mailqueue script (no worry if qmHandle set with 755 or not)
- fix and mod httpd init
- fix web__lib.php

* Thu Oct 08 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015100801.mr
- fix httpd init (especially for httpd24 from ius)

* Thu Sep 24 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015092401.mr
- fix httpd.init for different pid file location for httpd and IUS httpd24
- add note for clientbaselib.php for commandlinelib.php
- fix php-fpm children for change resource plan

* Sat Sep 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015091201.mr
- mod web__lib.php where create php-fpm for current user if not exists

* Sun Aug 30 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015083001.mr
- add 'try_files $uri =404' for security issue
- add note in apache config where mod_ruid2 not work for mod_userdir
- add new phpmailer for prepare send with attachment
- mod commandlinelib.php (use lx_array_merge instead array_merge and change error message
- add commandlinelib_old.php
- mod mem-usage
 
* Sun Aug 16 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015081601.mr
- fix commandlinelib.php related to 'add' and set only admin/auxiliary permit for certain commands
- fix default_index.php for login page
- add note for cpu-time, cpu-usage and mem-usage

* Tue Aug 11 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015081101.mr
- move SSLCompression from httpd.conf to ssl.conf
- add page param in default_index.php and login_inc2.php
- fix mem-usage where use smem rpm

* Tue Aug 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015080401.mr
- back to use php-fpm reload
- add 'aio threads' and 'directio 4m' for nginx
- add '--daemonize' for php-fpm start
- increase pm.process_idle_timeout to 20s for php-fpm
- add missing 'text_spf_redirect' column for mmail table in kloxo database

* Thu Jul 30 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015073001.mr
- add cpu-time, cpu-usage and mem-usage script
- fix restart.inc related to php-fpm pkill
- add MaxServerLoad and CustomeHeader for 'X-Frame-Options:sameorigin' in hiawatha
- disable maxserverload but give notes for hiawatha

* Sun Jul 26 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015072602.mr
- enable chroot for php-fpm
- disable 'SPF record' for dns
- split dkim for dns (especially for bind)
- set fcgid for httpd 2.2
- fix uninstallMeTrue for web
- remove unused code in setup/installer.sh
- back to disable chroot for php-fpm (still trouble)

* Tue Jul 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015072103.mr
- use restart instead graceful for apache
- use restart for php-fpm
- add ProxyRequests and etc for mod_proxy_fcgi
- remove fix-outgoingips in add and delele domain in mmail__qmaillib.php
- fix commandlinelib.php (thanks for noamr@beyondsecurity.com for this security issue)
- fix restart.inc
- fix switch web server (related to hiawatha)

* Tue Jul 14 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015071402.mr
- mod note for .htaccess.tpl
- add spf redirect
- add DocumentRoot in web/webmail redirect (to prevent "Got error 'Primary script unknown\n'" in httpd24)
- add ErrorLogFormat in httpd24.conf (add domain info)
- mod commandlinelib.php for temporary fix where only permit for admin or aux

* Fri Jul 10 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015071002.mr
- fix sysinfo (forget reset $out before detect hiawatha service on or off)
- fix/mod htaccess.tpl for fcgid infoadd inform in clearallowedblockedip.php
- fix fix-outgoingips.php for handle IPv6
- fix update-ckeditor

* Wed Jul 08 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015070802.mr
- mod gettraffic (add try-catch for web and mail stats)
- change 'check_vhost_docroot=false' for suphp (trouble for ~user url if 'true')
- add update-ckeditor script
- disable 'no_fix_config' in 'switch programs' (because only 'defaults' level executed)
- disable 'AddDefaultCharset' in apache and also tengine

* Sun Jul 05 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015070503.mr
- mod fix-outgoingips.php to handle IPv6
- change php5.fcgi to php.fcgi
- make possible secondary php using fcgid beside suphp
- fix php.ini path for php.fcgi
- add info for secondary php using fcgid
- fix cp path for fcgid

* Fri Jul 03 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015070303.mr
- remove 'proxy_set_header Host' from proxy configs in nginx (trouble with httpd 2.4)
- use 'proxy_set_header Host $host;' for nginx proxy
- mod/fix switch-apache
- fix ip detect for OpenVZ issue

* Thu Jul 02 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015070203.mr
- set 'HostnameLookups Off' in httpd/httpd24.conf
- disable 'lbmethod_heartbeat_module' module for httpd24
- copy latest run script from qmail-toaster rpm
- mod switch-apache for install mod24u_session also
- add fix-yum script
- add 'port: 53' in nsd.conf (watchdog always think not running without it)
- partial fix for cron
- change 'port: 53' to 'ip@53' + add localhost in nsd.conf 

* Wed Jul 01 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015070101.mr
- add fix error 'Directory / is not owned by admin' in defaults.conf.tpl of apache
- fix info for SetHandler in .htaccess
- fix/adjust session_path in php.ini.base

* Tue Jun 30 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015063003.mr
- add checking /var/log/named in list.transfered.conf.tpl of bind
- mod info in fixtraffic; fix ip detected (use 'ip addr' instead 'ifconfig')
- mod better ip detect
- still continue if 'database_user_already_exists' for database in restore process

* Sat Jun 27 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015062702.mr
- always check /var/lib/php/session in fixphp
- mod 'sed' in certain scripts
- fix default init.conf for apache
- mod defaults.conf.tpl in apache
- mod nsd to add 'ip-address' in /etc/nsd/nsd.conf
- mod default.vcl for handle ssl port in varnish
- add 'serverips' in dns config
- remove getAllIps() in web/web__lib.php
- change 'Always need selected' to 'Select to execute' in desclib.php
- back to use 'interface_template.dump' in createDatabaseInterfaceTemplate()
- remove getIPs_from_ifconfig() and add getIPs_from_ipaddr and use it in os_get_allips()
- add update-phpmyadmin for update phpmyadmin for panel
- fix/remove \\n after {$end} in list.transfered.conf.tpl of nsd

* Thu Jun 25 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015062501.mr
- fix sysinfo (using for detecting php-cli instead php because httpd 2.4 issue)
- fix sysinfo (detect hiawatha for web server)
- mod defaults.conf.tpl of hiawatha (fix cgihandler for php)

* Wed Jun 24 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015062401.mr
- always copy suphp.conf to /etc every execute fixweb
- disable 'ProxySet enablereuse=on' for mod_proxy_fcgi (fix error 503 issue)
- increasing timeout for web configs (importance for long process like big size file upload)
- Change SSL to TLS in parameter to hiawatha

* Tue Jun 23 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015062301.mr
- mod messagelib.php for .httaccess info for secondary php
- change uninstall from 'rpm -e --nodeps' to 'yum remove' for web server

* Mon Jun 22 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015062202.mr
- add 'Click Help for more info' in every pages
- switch-apache also add/remove use_apache24.flg
- fix deleteDir related to stats data

* Sun Jun 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015062104.mr
- mod conf.tpl for add timeout for mod_fastcgi and mod_proxy_fcgi
- change session path for phpXYs
- Remove 'ProxyTimeout' and enough using 'ProxySet timeout' for mod_proxy_fcgi
- add 'use apache 2.4' in 'switch programs'
- special handling in 'webserver configure' if enable apache 2.4
- move additional httpd module from lib.php to web__lib.php
- fix/mod for handling install/uninstall for httpd/htttpd24

* Sat Jun 20 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015062006.mr
- change LogLevel from warn to error in httpd24
- no change for disable in 00-optional.conf
- set max=25 (as the same as ThreadsPerChild value) for proxy of mod_proxy_fcgi
- add stop server before switch to other version in switch-apache script
- fix/mod custom error pages
- back to add set.httpd.lst and set.nginx.lst
- combine remoteip and rpaf to rpaf.conf
- change %h to %a in LogFormat at httpd24.conf (mod_remoteip issue)
- add htcacheclean in restart-web and restart-all
- mod create /etc/sysconfig/httpd in defaults.conf.tpl

* Fri Jun 19 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015061902.mr
- mod defaults.conf.tpl for httpd for handle httpd24u configs
- mod mod_proxy_fcgi setting for optimize performace
- add /var/run/php-fpm dir if not exists (deleted if php rpm removed)
- add switch-apache script for change apache 2.2 to 2.4 and vice-versa

* Thu Jun 18 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015061802.mr
- change addhandler to sethandler in httpd (for security reason)
- set load module if not load in certain modules in httpd
- prepare secondary php using mod_fcgid
- httpd 2.4 ready to use with php-fpm (using mod_proxy_fcgi
- still trouble with secondary php with suphp)
- remove ThreadStackSize from ~lxcenter.conf (trouble with httpd 2.4)
- mod htaccess.tpl for using secondary php with httpd 2.4 compatible

* Tue Jun 16 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015061701.mr
- move php-fpm restart before web server
- remove unwanted code in mmail
- remove ThreadStackSize and MaxMemFree from ~lxcenter.conf (trouble with httpd 2.4)
- mod and optimize httpd code related to 'define' module
- remove 'suPHP_AddHandler x-httpd-php52' from suphp.conf
- disable 'SSLMutex' from ssl.conf (trouble with httpd 2.4)
- remove double php5.fcgi; mod sysinfo for 'php used'
- back to disable chroot in suphp because not work

* Thu Jun 11 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015061103.mr
- fix mysql-convert.php if cnf not exists
- fix appear for kloxo process if using cgi
- fix php-fpm process with always use restart instead reload
- mod define.conf because already exists in httpd 2.4
- fix display for cronlib; mod lib.php to execute all webmail setup script
- add memcached restart in restart-all and restart-web
- add fixcron script
- update setup script (need '-y' to force install)
- add width in 'go' of list

* Tue Jun 09 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015060902.mr
- prepare httpd config for handle dual version
- fix fix-qmail-assign.php if no domain
- remove useless code in fixskeleton.php
- display webmail process with change exec to system
- fix php-fpm state if use php-fpm or not
- remove unwanted code in watchdog script
- fix copy process of php-fpm configs
- fix kloxo.init if not start process
- add 'set-kloxo-php cgi' in setup.sh/installer.sh

* Tue Jun 09 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015060901.mr
- fix sysinfo.php if no php-type declare
- back to use restart instead stop+pkill+start because trouble if panel using php-fpm
- fix kloxo.init if no kloxo_php_active
- set panel use php-cgi instead php-fpm (less memory usage in idle state)

* Mon Jun 08 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015060802.mr
- mod php-fpm where reload=restart
- restart script using stop+pkill+start instead restart
- mod setting for mod_proxy_fcgi (prepare httpd24)
- execute fixlxphpexe only if start kloxo service
- mod fixmail-all for fix me, defaultdomain and defaulthost also
- fix phpm-extension-installer
- disable charset to utf-8 in nginx

* Fri Jun 05 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015060501.mr
- mod fix-outgoingips.php to possible manual modified
- add default charset to utf-8 in apache, nginx and php (no need for hiawatha)
- mod selectshow for file manager

* Sun May 31 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015053102.mr
- change php-branch script to set-php-branch
- fix ip address detect (mostly related to OpenVZ problem)
- fix gateway detect for ip address

* Thu May 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015052801.mr
- add mailqueue script for execute qmHandle
- mod setup-*.php where exit if no index.php for application directory

* Wed May 27 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015052703.mr
- fix afterlogic setup (remove settings.xml if exists)
- reconstruct domains.conf.tpl for assigned IP
- change 'setup-php-fpm' to 'set-php-fpm' in certain files
- fix ipalloc (set only for non-reverseproxy)

* Mon May 25 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015052501.mr
- mod sysinfo and add disk space info
- fix set-php-fpm if select php branch

* Sun May 24 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015052403.mr
- mod installatron-install
- remove wrong file
- more info in sysinfo script
- change switch-php-fpm to set-php-fpm
- uninstall nginx also include tengine
- add changeport beside defaultport script for panel
- add kloxo-to-kloxomr7 script
- add hostname info in sysinfo script
- remove tengine from nginx uninstalled because based on rpmbranchlist

* Thu May 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015052102.mr
- set no status for php if kloxo using cgi instead php-fpm
- set no initial phpini for web and domain (just for pserver and client)
- fix multiple_php_flag
- add space before '>' in VirtualHost (prevent for "directive missing closing '>'")
- disable phpini in client login because still not work

* Tue May 19 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015051903.mr
- fix image path for error pages
- change suphp52.conf to suphp2.conf (because 'secondary php' for 'multiple php' instead 'php 5.2' only)
- add warning if hostname not match to FQDN
- rename suphp52.conf to suphp2.conf

* Mon May 18 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015051802.mr
- fix fixphpini.php if phpini for pserver not exists
- note in nsd4.conf if declare ip must include 127.0.0.1
- fix phpinilib.php where fixphpIniFlag() also execute setUpInitialValues()
- disable all code related to installapp
- fix set_login_skin_to_simplicity for background
- mod alert from 200 to 100 from top
- mod mysql-convert and mysql-optimize also read '--help'
* Mon May 18 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015051801.mr
- fix mysql-convert.php for tokudb and add note for reboot
- mod phpm-updater if symlink to phpXYm-cli exists

* Sun May 17 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015051701.mr
- remove defaultValue for skin (appear error in debug)
- check phpini setting only under simplicity skin (still trouble in feather skin)

* Sat May 16 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015051601.mr
- fix detect phpini for server, admin and clients
- set default value for skin

* Fri May 15 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015051502.mr
- nginx init using tengine.conf instead nginx.conf if exists in /etc/nginx/conf
- fix dns setting, especially for third ns or more or sub ns

* Fri May 15 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015051501.mr
- fix check_if_port_on for socket file and add detected by service status
- fix php.ini alert always appear in client login

* Tue May 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015051202.mr
- fix set-hosts; add 'fastcgi_request_buffering off;' and 'proxy_request_buffering off;' to nginx
- add '#reuse_port on;' to nginx (work with tengine) if enable
- add detect pid for watchdog
- add restart-php-fpm
- restructure file inside /file dir and adjusment call for new location
- add '::' for 'Hostname' beside '0.0.0.0' in hiawatha
- fix copy apache configs

* Mon May 11 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015051101.mr
- add ipv6 support for nginx
- fix hiawatha for ip assign to domain
- add 'update all' for 'switch programs'
- add 'customize' stamp in ~lxcenter.conf and detected by 'webserver configure'
- fix copy php-fpm files; change 'alert' appear from 350 to 100px from top

* Sat May 09 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015050901.mr
- fix mpm calculation in ~lxcenter.conf.tpl 
- fix installWebmailDb.php for install webmails
- use xml.php instead xml if exists for afterlogic
- set default of 'php used' as 'php54m' in php.ini of website
- fix getAnyErrorMessage for handling phpini for server and client
- add function db_del_value(); add return value for delRow() in sqlitelib.php
- remove copy php.ini using php.ini.base process

* Thu May 07 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015050703.mr
- set phptype_not_set and phpini_not_set only (without _pserver and _client)
- if phpini not set in pserver, click phpini in admin will go to phpini in server
- move detect phpini not set in pserver from setUpInitialValues to initPhpIni
- add missing phpm-all-setup

* Wed May 06 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015050604.mr
- fix validate_mail (add max domain ext from 6 to 16 like validate_domain_name)
- add 'stamp' for ~lxcenter.conf to identify 'apache optimize' selected
- remove '--no change--' in 'webserver configure' (automatically change to built-in '--select on--')

* Wed May 06 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015050603.mr
- Panel possible using php-cgi instead php-fpm (less memory usage)
- add set-kloxo-php for switch php-fpm or php-cgi for panel
- overhaul change for phpXYm and phpYXs setting
- add process to update phpXYm and phpXYs in cleanup
- entering short IPv6 format automatically convert to long format
- add jk_init.ini (prepare for jailkit implementation)
- add kloxo_sqlite.sql (prepare change to sqlite from mysql for kloxo database)
- mod fixlxphpexe (install php54s if not exists) and set-kloxo-php (default as 'fpm')
- mod separate var for mem and timeout between phpXYm and phpXYs

* Mon May 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015050401.mr
- make simple report for fix-outgoingips.php, fixdnschangeip.php and fixdnsremoverecord.php
- make hiawatha/nginx always report to all logs
- remove/disable proxy_cache_use_stale in nginx
- fix display for favorites in feather skin
- possible using php-cgi instead php-fpm in panel (less memory usage) if exists 'kloxo_use_php-cgi' file
- change log path for panel to /var/log/hiawatha

* Sun May 03 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015050301.mr
- move resetQmailAssign() from lib.php to fix-qmail-assign.php (make slim lib.php)
- add fix-outgoingips
- add and delete domain in mmail also execute fix-outgoingips
- add fix-outgoingips to fixmail-all

* Sat May 02 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015050201.mr
- mysql-convert.php also handle tokudb storage-engine
- change disablephp to enablephp and add enablessl and enablessl in webserver configs
- disable 'create ...' in logrotate
- disable reading IP from ifcfg (because need 'perfect' format) and use read 'ifconfig' and 'ip' only

* Wed Apr 30 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015043001.mr
- mod without set to myisam for mysql in install process (minimize trouble for update from Kloxo or Kloxo-MR 6.5)

* Tue Apr 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042903.mr
- add 'include' for spf

* Tue Apr 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042902.mr
- mod admin.sql
- add 'enable_spf_autoip' column in mmail table of kloxo database
- make possible remove a__base__ record (prepare for aaa__base__ for IPv6)
- add 'automatic add IP' in SPF record; enable 'update all' for 'limit'
- change 'a record' parameter from ttype_hostname_param to ttype_hostname

* Tue Apr 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042901.mr
- add '--client' for fixdnsremoverecord
- fix message for setup horde; add missing setup-rainloop
- disable 'proxy_cache_use_stale' for nginx

* Tue Apr 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042803.mr
- move webmail setup to sh script from lib.php
- fix inactivate iptables
- fix display private._domainkey

* Tue Apr 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042801.mr
- fix chown and chmod in 'file manager' (missing path declare)
- fix sslcertlib for 'nname' under client 

* Mon Apr 27 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042703.mr
- fix fixdnsremoverecord.php
- more info for fixdnschangeip and fixdnsremoverecord
- change argument names for fixdnsremoverecord
- back to use previous code for dnsbaselib because impossible to use hostname with double underline
- add proxy in nginx for ssl
- fix dnsbaselib.php (especially in 'ns record')

* Sun Apr 26 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042601.mr
- back to use old trick because 'chkconfig off' and 'chkconfig --del' not enough for iptables after reboot
- set 'webmail apps' as '--choose--' instead 'select one'
- delete unwanted fixdns.php in /bin/misc
- hidden certain process in installer.php

* Sat Apr 25 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042503.mr
- mod 'txt record' possible record name with '_'
- change 'chkconfig off' to 'chkconfig --del' for iptables
- mod fixdnschangeip
- add fixdnsremoverecord script (still experimental)
- add setup-tht script (thehostingtool billing; still experimental)
- fix fixdnschangeip and fixdnsremoverecord logic
- more info for setup-tht

* Fri Apr 24 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042401.mr
- fix mysql-convert for MariaDB
- mod more space for 'txt record value' in add/update dns
- fix mysql-convert

* Thu Apr 23 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042301.mr
- mod note for phpm-installer; inactivate iptables in install process
- fix dmarc in 'txt record' in dns
- auto-convert if in 'txt record' found '__base__' or '<%domain%>' in domains.conf.tpl
- change mail_feedback in dmarc add/update from 'admin@domain.com' to 'admin@__base__'

* Tue Apr 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042104.mr
- add phpm-all-install for install php branch for phpm; add sendmail-limiter.sql
- move all .sql to /file/sql
- mod inactive iptables in install process
- separated var name for standard and start dirprotect for nginx
- fix sendmail-wrapper
- fix 'exclude_all_others' title
- replace sendmail-wrapper file because wrong file

* Mon Apr 20 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015042003.mr
- fix cronlib.php (add db write in postAdd)
- fix 'file manager' if file with space
- change minimum ttl from 1800 to 3600 (RFC 2308)
- fix strpos logic in simplicity menu
- make sure re-install will be to user default services
- add vpopmail.sql (just for archive)
- set minimum ttl in dns config template from 1800 to 3600
- list all IPs (include hostname IP) in dns syncCreateConf
- mod sendmail-wrapper (possible add addons script instead specific for sendmail-limiter only)

* Sun Apr 19 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015041901.mr
- back to use previous ffile__common because problem not the code but user level
- change session path for client to /home/kloxo/client/<user>/session

* Fri Apr 17 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015041602.mr
- mod update.sql (remove ftp from watchdog and other mods)
- add smtp, imap and pop fname records in dns template
- remove restart/kill service from kloxo and syslog logrotate
- change tls_protocol from ssl23 to tls1 in imapd-ssl and pop3d-ssl
- back to use 'setdriver' in the end of install process because certain os template need it
- mod update.sql (use 'add column if not exists' and 'change column if exists')

* Wed Apr 15 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015041504.mr
- back to separate logic for spamassassin and bogofilter in maildrop
- make possible delete for file with space (still not work for copy-paste)
- mod message for 'invalid password'

* Wed Apr 15 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015041503.mr
- mod 'add watchdog' message
- mod sendmail-wrapper to possible ban subdir under pwd
- add missing 'default_port_ftp' translate
- mod suphp config for handle php51m-php56m
- mod description for 'secondary php'
- mod description for htaccess.tpl

* Mon Apr 13 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015041302.mr
- fix hostname and server_alias validate with possible 1 alpanumeric char
- fix sendmail-limiter
- remove ns and change ftp from 'cname' to 'a' record for base dns template
- use try-catch for create cronjob
- disable password change for localhost (but not work)
- prepare using session_login instead record to 'loginattempt'
- fix phpm-extension-installer if directory not exists
- change fail login from 'error' to 'login_fail' log
- fix prepare session_login code

* Sat Apr 11 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015041104.mr
- always combine bogofilter and spamassassin code in .maildroprc file
- no appear for 'multile php ratio' if disable 'multiple php enable'
- fix ssl name for upload ssl

* Sat Apr 11 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015041103.mr
- fix 'default' drivers in install process
- change php ratio from '0:6:0:0:0' (5.3 as default) to '0:0:6:0:0' (5.4 as default)
- fix synchronize driver in cleanup process
- fix changedriver
- fix setSyncDrivers again

* Fri Apr 10 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015041001.mr
- change SSLCipherSuite (use from Mozilla recommendation) for apache
- use maxpar instead minpar for calculate MaxClients in apache
- remove pure-ftpd log for kloxo.logrotate (because pure-ftpd logrotate exists)
- also change ssl_ciphers for nginx; prepare php-fpm chroot
- make appear default timezone in 'php configure' for admin
- mod 'date' appear for lxguard in begin newer than end
- redirect to 'password' page if password as 'admin'
- add 'net.ipv4.tcp_syncookies = 1' and 'net.ipv4.tcp_max_syn_backlog = 2048' in sysctl.conf to prevent server as flood
- change changedriver to setdriver in the end of install process
- add setdriver script
- fix detect driver in lib.php
- remove setdriver in install process
- disable/no need 'default' driver value in install process
- rename validate_password_add to validated_password
- possible change ssh root password in 'ssh configure'
- fix missing to put sshd_config 'template' content
- truncate 'information' list data if > 20 chars
- add title in 'information' list data
- change 'ftp user' to 'username' in 'information' list data

* Tue Apr 07 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015040701.mr
- make hidden changedriver in install process
- add rename mod_*.conf to .nonconf for httpd module configs
- read log if hitlist.info not exists for lxguard

* Mon Apr 06 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015040601.mr
- mod sysinfo (add 'also as webserver' for hiawatha)
- prepare watchdog if change change port for ftp
- possible change port and action in watchdog update
- mod error pages to match latest index.html (small logo appear)
- add help for watchdog add
- also record ssh success access
- add changedriver to default value for end of setup.sh (in install process)

* Sat Apr 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015040402.mr
- make possible change pure-ftpd port 21 to other (via 'ftp configure')
- change min and max port for passive ftp from 30000-50000 to 45000-65000
- change syslog from end to begin in list of restart-all

* Sat Apr 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015040401.mr
- use closeallinput instead closeinput (source code taken from hypervm)
- fix kloxo.c related to execl

* Fri Apr 03 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015040302.mr
- change arg in lxguard_main
- add for remove access.info and hitlist.info in lxguard.php
- fix lxguard_main for handle ssh and ftp log
- mod fixlxguard with delete access.info and hitlist.info before execute lxguard_main

* Thu Apr 02 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015040201.mr
- create fixlxguard script
- separated process for ssh and ftp for lxguard because different log
- add parse_ssh_log for handling ssh log parse
- optimize process for lxguard for reading log
- fix lxguard logic if certain files not exists
- add declare missing static data in pserverlib dan lxguard
- add '-p' in webalizer process
- fix merge_array_object_not_deleted if not multi-dem array
- add 'since' param for lxguard_main
- fix bind log dir permissions in installer process
- fix phpm-config-setup and php-extension-installer for handling extension conf

* Sun Mar 29 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015032901.mr
- fix 'edit mx' (must priority 10; old code trouble for multiple mx)
- fix resetQmailAssign (virtualdomains must content without remote type)

* Sat Mar 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015032801.mr
- fix mysql-convert (using server.cnf instead my.cnf in /etc/my.cnf.d)
- click webmail apps will be appear in new tab/windows

* Fri Mar 27 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015032701.mr
- fix zend_extension path in phpm install/update process
- add sysstat install in install process

* Thu Mar 26 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015032603.mr
- fix sendmail-wrapper (according to latest qmail-toaster)
- make phpm-installer faster process (don't care dependencies installed or not)
- change phpm-installer logic to found dependencies
- mod prefork.inc.tpl with default values
- prepare tpl in phpcfg
- prepare sendmail-wrapper for sendmail-limiter
- mod diskquota check with nice and ionice
- mod installer.php with remove smail and add ncdu (realtime du)
- mod/fix phpm-extension-installer and phpm-installer
- viruscan possible using customize dir target
- make possible use phpm-extension-installer for 'standard' php beside phpm
- fix detect uname in phpm-extension-installer
- more info in phpm-extension-installer process
- use counter in phpm-extension-installer and phpm-installer

* Sun Mar 22 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015032202.mr
- fix phpm-installer (missing like 15-*.ini)
- separated logic for mysql and mariadb installing
- mod uninstall spamassassin must exclude simscan and ripmime
- enable 'virus scan' will be install clamav and clamd
- disable 'virus scan' will uninstall clamav and clamd only
- no uninstall clamav and clamd if disable 'virus scan' because possible to used by other purpose

* Sat Mar 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015032101.mr
- warning in nsd4.conf where need declare IP in server with multiple IP
- fix/mod watchdog list
- back to use default syslog.logrotate (add add rsyslog repo in mratwork.repo)
- possible restart syslog if using syslog-ng
- add phpm-updater
- add bench script
- fix fixrepo (wrong var)
- mod soft-reboot (identify initrd for kdump)

* Fri Mar 20 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015032001.mr
- fix logic for .ca if exists
- fix info in phpm-installer
- add again 'spf record' in dns because bind may warning without it
- fix crftoken to csrftoken
- change 'ionice -c 2 -n 7' to 'nice -n +10 ionice -c3' backup/restore process
- use call fixrepo instead direct login in installer.php
- fix fixrepo logic
- mod raw-backup and add raw-restore
- fix/change isCRFToken to isCSRFToken in coredisplaylib.php

* Sun Mar 15 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015031501.mr
- remove 'engine' declare from database dump in backup and restore process
- set all error log as error.log in php-fpm conf
- change ripmime-toaster to ripmime reference
- change postmaster to admin in mail feedback of dmarc
- create nsd or other dir in /etc if not exists

* Fri Mar 13 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015031301.mr
- fix hostmaster insert in dns (especially for 'old' setting)
- add insert totalinode_usage in client table of kloxo database
- change email in domainkeys from postmaster to admin

* Thu Mar 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015031202.mr
- prepare inode quota
- fix/update paths in createDir
- fix service list for mydns and yadifa
- disable declare other object in mailaccount (make trouble in backup/restore)

* Thu Mar 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015031201.mr
- change unzip_with_throw to unzip in restore process
- change all php error log to php-error.log
- add libgearman in php dependencies of phpm-installer
- separate zip process for mysql and home in raw-backup
- more logs report

* Mon Mar 09 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015030901.mr
- add httpd24u in set.web.lst
- mod sendmail-wrapper (implementing to qmail-toaster)
- fix/add for list and extract of tar.gz, tar.bz2 and tar.xz
- fix mysql-optimize script
- add viruscan script (for /home at this time)
- add hostmaster in 'general settings' in 'manage dns'
- implementing dmarc beside spf in 'email auth'
- make blank for rcpthosts because move to morercpthosts

* Sun Mar 01 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015030101.mr
- mod mysql-to-mariadb and mariadb-to-mysql to make possible change without enable repo
- enable spamdyke and clamav will be installing their rpm
- fix bind in install process
- fixmail-all also execute 'qmailctl cdb'
- fix detecting mariadb if installed

* Sat Feb 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015022101.mr
- use mariadb instead mysql in install process (trouble with mysql after IUS release MySQL56u)
- install spamdyke if enabled
- fix pure-ftpd removed in install process
- add user list in raw-backup
- add 'performace_schema=on' in set-mysql-default (also use by install process)

* Wed Feb 18 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015021801.mr
- add closeallinput.c (taken from hypervm 2.1 beta)
- remove libmysqlclient together with mysql in setup.sh

* Sun Feb 15 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015021501.mr
- fix cron in install process (CentOS 5 using vixie-cron but CentOS 6 using cronie)
- add version-full script (as the same as 'version --vertype=full')
- fix bind (create missing /var/log/named)

* Tue Feb 10 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015021001.mr
- fix tpl for bind
- fix default.pem (move private key to top)
- only use morercpthosts (make blank rcpthosts)
- 'TXT record' accept underline chars (importance like _dmarc)

* Wed Feb 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015020401.mr
- mod and add info to redirect to ssl in default_index.php
- set httpd to disable SSLv3 support
- add ChallengeClient in hiawatha for better DDos protect
- add badsendmailfrom file for sendmail-wrapper
- php54+ use mysqlnd install mysql module
- mod soft-reboot
- add change-root-password script

* Tue Jan 27 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015012701.mr
- fix wrong logic for mysql service
- add soft-reboot (not work in openvz container)
- change error log level in nginx from warn to error
- fix unzip for zip filename with space
- add chmod for stats dir in fix-chownchmod (nginx issue)
- prepare encrypt and decrypt for form passing data (emulate https for http scheme)
- re-enable backup log for 'Setting parent of' process
- change from php 5.3 to 5.4 as default php for panel and website
- prepate for also using webtatic php-branch (phpXYw beside phpXY/phpYXu)

* Wed Jan 14 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015011402.mr
- fix 2 doublequote in installer.php
- use 'rndc-key' instead 'rndckey' for bind
- create /var/log/named if not exists in cleanup process

* Tue Jan 13 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015011302.mr
- change gwan to monkey
- fix bind related to rndckey
- fix hiawatha for execute cgi in cgi-bin dir
- change phpini from after to before phptype
- fix telaen in cleanup process
- fix libcurl in CentOS 6 (install curl-devel in install process; php-common need libcurl)
- fix telaen for replace configs

* Fri Jan 09 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015010905.mr
- move domain ssl from /home/<user>/ssl to /home/kloxo/client/<user>/ssl
- fix to not use quote in langkeywordlib.php (not appear in quote exist)
- not permit to create subdomain as webmail/mail/lists/cp/default/www
- also not permit for lists subdomain
- move domain ssl dir using fixweb instead cleanup (because still trouble)
- fix domain ssl path in apache domains.conf.tpl
- fix wrong validate function name
- mod keyword related to 'no permit as subdomain'

* Thu Jan 08 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015010802.mr
- fix/mod phpm-installer (related to zend_extension path)
- fix web conf.tpl (related to ip for domain)
- mod info in phpm-installer process

* Tue Jan 06 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015010601.mr
- better report for sendmail-wrapper
- fix hiawatha-proxy config (remove useToolkit if using ReverseProxy)

* Sun Jan 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2015010401.mr
- back to enable morercpthosts in spamdyke.conf
- make morercpthosts as the same content of rcpthosts (easy implementing)
- set installatron opening in new tab/window
- new install also include php gd and ioncube (need by installatron)
- mod installatron-install

* Mon Dec 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014122901.mr
- reduce proxy_cache from 1000m to 100m (fix for upload issue)
- move panel redirect logic to redirect.php
- process for redirect_to_ssl and redirect_to_hostname for panel
- mod pdns.sql to accept pdns 3.4.x
- pending update pdns 3.3.1 to 3.4.1 (trouble with rpm compile)

* Thu Dec 25 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014122501.mr
- fix quota if select unlimited (quota exceed appear in openvz)

* Wed Dec 24 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014122401.mr
- set apache, hiawatha and domains always listen '*' IP
- separated validate_server_alias (add '*' to validate) from validate_hostname_name
- fix logrotate for kloxo and syslog

* Sun Dec 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014122102.mr
- use tar.gz instead zip in raw-backup
- changeport.php also create port-ssl and port-nonssl file (used by redirect in login)
- panel redirect to ssl only need create redirect-to-ssl in login dir (no need custom-inc2.php)
- enable 'Redirect...' in 'Port configure' will create redirect-to-ssl automatically
- use kloxobck instead kloxo.bck for kloxo database in raw-backup process

* Fri Dec 19 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014121901.mr
- fix sendmail-wrapper report
- fix qmail restart 
- enable and mod breadcomb in 'file manager'
- fix proxy_standard.conf in nginx (remove $proxy_port)

* Tue Dec 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014121601.mr
- fix ezmlm for add ml
- mod to 'proxy_set_header X-Host $host:$proxy_port' for nginx-proxy

* Sat Dec 13 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014121301.mr
- mod 'AccessLogFile=/dev/null' to 'AccessLogFile=none' for disable accesslog (need hiawatha 9.9.0-f.2+
- add sendmail-wrapper to report caller of php mail() in maillog (need update qmail-toaster)
- fix domains.conf.tpl for domain-based customize rewrite rule
- mod sendmail-wrapper
- correcting // to / for path in file manager

* Mon Dec 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014120802.mr
- possible custom rewrite file (similar with php-fpm config in globals do) for nginx
- add 'path' values in php-fpm tpl
- prepare for inode quota
- add dns-blacklist-entry in spamdyke
- change 'Last login date' format in 'information'
- change '-' value to '0' in client list
- change/fix block_shellshock in hiawatha
- mod spamdyke where using spamdyke_rbl.txt as external rbl list

* Wed Dec 03 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014120301.mr
- use re-process instead show warning in add mail account
- set z-index for logo to -9999 (mean always in below)
- fix nginx to use .ca file if exists;
- add errorlog and accesslog (to /dev/null) for cp and webmail of every domains in hiawatha

* Thu Nov 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014112003.mr
- fix default.conf.tpl in apache
- fix client list appear
- trim username and password for whitespace in login process
- fix telaen webmail

* Mon Nov 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014111701.mr
- add message for 'session_timeout'
- set inode to 1/100 and convert to integer

* Sun Nov 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014111601.mr
- disable convert 'rndc-key' to 'rndckey' in list.transfered.conf.tpl because back to use 'rndc-key'

* Fri Nov 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014111401.mr
- add script for remove /home/httpd/*/httpdocs (also conf dirs)
- set createDir() not include create httpdocs dir
- fix createDatabaseInterfaceTemplate()
- mod fix.inc and restart.inc
- mod skin-set-for-all to possible to select skin
- mod defaults.conf.tpl of hiawatha to off accesslog
- back to use 'rndc-key' instead 'rndckey' for bind
- fix for master-slave for detect rpm in component__rpmlib
- remove OldUpdate() from ipaddress__redhatlib
- make possible detect ip with 'bootproto=dhcp'
- modified ip detect with ifcfg- and ifconfig command


* Fri Nov 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014110701.mr
- disable config-mysql in spamdyke.conf (because not used)
- add utf-8 charset in error pages
- short 'for help' in scripts

* Thu Nov 06 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014110602.mr
- fix mysql restart process
- fix spamdyke.conf
- remove 'spam status' from mail login
- prepare dhcp ip detect
- fix image url for error pages
- change from 'default domain' to 'contact email' in client list
 
* Sun Nov 02 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014110202.mr
- fix and add 'IgnoreDotHiawatha' for proxy in hiawatha configs
- fix dns related to parked/redirect domain
- fix process also for 'none' driver
- optimize fixdns for speed
- combine syncAddFile() to createConfFile() in dns__lib
- getDnsMasters() include parked/redirect domains
- fix webmail redirect in hiawatha

* Wed Oct 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102901.mr
- fix ftpuser (wrong declare quota) and mod detect status

* Mon Oct 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102703.mr
- make logo image smaller (from height 75 to 50) and add margin padding
- mod lxguard raw connection list
- set session dir to chmod 777 for user-level
- set 'backuper' user as 'special' client (will not including in backup)
- install process also remove epel.repo
- mod help message for phpini

* Mon Oct 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102701.mr
- fix mysql restart process
- move cp from default.conf.tpl to domains.conf.tpl in apache
- mod sql related to watchdog list
- mod check_if_port_on() for accept unix socket
- add 'telnet' installing in install process

* Sun Oct 26 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102603.mr
- make only one time process in fix-chownchmod if the same docroot

* Sun Oct 25 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102602.mr
- mod set-hosts with using 'hostname -i' instead 'ifconfig' to detect 'primary' IP
- accept php56m in 'php ratio' at 'php configure'
- mod to create sock dir before copy php-fpm configs
- fix 'default' ~lxcenter.conf
- remove fix_chownchmod from web__lib because change approach in fix-chownchmod script
- change chmod from 750 to 751 in createUser()
- remove maradns from setInitialAllDnsConfigs()
- change from 'none' to default value in 'empty' driver in slavedb

* Sat Oct 25 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102504.mr
- add php56m for 'multiple php'
- mod phpm-config-setup for accept php56m
- add setEnableQuota (still manual add usrquota/grpquota to /etc/fstab)
- mod to list all ip list in dns; mod restore help
- mod nsd configs (using createRestartFile)
- mod nsd configs (createRestartFile for master and slave list also)
- disable setEnableQuota (until auto-edit /etc/fstab ready)

* Fri Oct 24 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102402.mr
- set pureftpd tp disable sslv2 and sslv3
- mod Autoresponder list
- mod skeleton.zip (make smaller logo)
- fix redirect to ssl in panel
- mod help message for php configure
- prepare 'web select' (beside 'php select' for 'multiple php')

* Thu Oct 23 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102302.mr
- fix docroot for cp in apache; use '<Location "/">' instead '<Location />' in apache
- fix Autoresponder list
- fix sp_specialplay if login via mailaccount
- add 'password' in mailaccount login
- fix menu in mailaccount login
- make simple setInitial for web, webcache and dns (prepare fix script for including)

* Thu Oct 23 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102301.mr
- fix for update from Kloxo 6.1.19+
- fix setSyncDrivers() (add try-catch; importance if update from 6.1.x/6.5.x)

* Wed Oct 22 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102203.mr
- set error page as the same as default page appear
- set logo with transparent background in panel
- setDefaultPages() including process error pages and remove setCopyErrorPages()
- make shorter message in error pages
- enable custom error in apache

* Tue Oct 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102103.mr
- fix bind with rndc-key (add sed in list.transfered.conf.tpl)
- fix reversedns ns update
- disable 'spf record' because deprecated (RFC7208)
- Add setSyncDrivers() to make sure driver data is synchronize between slavedb and table
- set click phpini warning will be going to php configure in server-level

* Mon Oct 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014102004.mr
- fix named.options.conf in bind (use 'rndckey' instead 'rndc-key')
- prepare shexec (sh script for passing all php exec process)
- prepare reversedns
- move process to remove rndc.conf from master to transfer tpl (for bind)
- fix if dns zonelists not exists
- fix dns zonelists (use 'echo' instead 'cat'; the same effect but 'cat' will be warning)

* Sun Oct 19 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101902.mr
- fix dns configs (need db write in dbactionAdd and dbactionDelete)
- mod dns libs (as the same as web libs 'style')
- rm_rec use do_exec_system instead exec
- fix fix-qmail-assign (forget \n for rcpthosts and virtualdomains)

* Sat Oct 18 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101802.mr
- fix domains.conf.tpl for apache (because not make '127.0.0.1' in proxy)
- mod error page for nginx
- cleanup php-fpm.conf for nginx
- remove fix-chownchmod in user-level
- file manager able to change permissions and ownership
- fix document path in ffilelib.php; make simple text in .htaccess
- os_get_group_from_gid()
- mod restart-all and restart-web (make apache in last position)
- fix ip define in apache
- add missing cp redirect in lighttpd
- add missing cp redirect in nginx
- remove error page declare in proxy in nginx (moving to generic.conf)

* Fri Oct 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101705.mr
- fix user-assign also fix rcpthosts and virtualdomains for qmail
- may trouble with hugh domains amount because not using morercpthosts
- mod file_permissions in file manager (todo: file_ownership) 

* Fri Oct 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101703.mr
- enable fix-chownchmod in user-level with right detect
- fix detect pserver in server-level phpini
- fix multiple_php_list if not exists
- fix detect for 'webserver configure' (related to 'fix-chownchomod')

* Fri Oct 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101701.mr
- remove TODO from fix-chownchmod.php for client-based fix
- fix fixweb.php (missing quote for lighttpd)
- fix defaults.conf.tpl for apache for ~lxcenter.conf exception
- disable user-based fix-chownchmod.php in panel (still not work)

* Thu Oct 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101601.mr
- mod fix-chownchmod to make possible for user
- add 'webserver config' for user (for 'fix-chownchmod')
- set all ssl to disable SSLv2 and SSLv3 (only enable for TLS1.0+)
- mod domain.conf.tpl related to 'Define'
- hidden nsd identity; hidden 'breadcombs' for file select
- change digest_alg value from 'SHA1' to 'SHA256'
- prepare symlink of __backup dir to their user path

* Wed Oct 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101504.mr
- add missing list.transfer.conf.tpl for mydns
- fix httpd configs related to mod_define work
- only overwrite ~lxcenter.conf if exists their custom file
- fix for missing define ip and port for proxy 

* Wed Oct 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101502.mr
- add php_defines in php-fpm of php 5.2
- fix php session path for server
- fix timezone selected in php
- fix nsd configs because using root as user
- fix yadifa because no keys and xfr dirs

* Tue Oct 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101403.mr
- move htaccess.tpl from phpini/tpl to apache/tpl
- set htaccess.tpl only have info related to secondary php
- move php_value and _flag from .htaccess to prefork.inc
- set include prefork.inc to apache domain configs
- set nginx configs to no limit_conn for localhost
- add deny localhost for BanListMask in hiawatha
- set serverlimit = MaxClients for prefork and itk
- fix fixphp script related to .htaccess

* Tue Oct 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101402.mr
- move blocksize from setQuota to syncNewquota and os_set_quota for calculate quota
- change inode as 1/10 total blocksize to total disk space
- change initial value of client php from static to server php value
- mod restart process of qmail
- set maxclients = minspareservers * 5 in prefork/itk and maxclients = minspareservers * threadsperchild

* Mon Oct 13 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101303.mr
- add directory toolkits for hiawatha (implementing .hiawatha)

* Mon Oct 13 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101302.mr
- yadifa running well now (have bug in 1.0.3 related to '_' char)
- mod domains.conf.tpl in nsd (using by bind, nsd and yadifa)
- mod domains.conf.tpl for nsd (again)
- NOTE: yadifa 1.0.3 have bugs for double-quote in TXT and unsupport SPF record

* Sun Oct 12 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101206.mr
- set watchdog for __driver_ to use restart with '--force'
- roundcude in cleanup also process update sqls
- update yadifa configs (running but still no read zones)

* Sun Oct 12 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101204.mr
- fix directory permissions for master and slave configs
- back to use restart instead reload in bind because slave problem
- fix and make simple change 'php-type'
- add itk.conf as 'emulate' httpd module
- remove restart in set_phpfpm in change php-type
- warning if php-type not php-fpm and select phpXYm in 'php used'

* Sat Oct 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101106.mr
- using restart --force in 'command center'
- fix bind configs (related to 'share' domains configs with nsd and yadifa)
- mod yadifa configs (still in progrss)

* Sat Oct 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101103.mr
- back to user root as user in nsd because too much permissions denies
- add yadifa as dns server
- make more info 'reload' nsd
- use the nsd domain configs for bind, nsd and yadifa (because the same structure)

* Sat Oct 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014101102.mr
- move 'apache optimize' calculation from apache-optimize.php to ~lxcenter.conf.tpl
- mod help for apache optimize
- fix equation of apache optimize

* Thu Oct 09 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100905.mr
- force using kloxomr7 packages in install process
- fix install process related to thirdparty for kloxomr7 
- fix installer related to vpopmail password
- remove lxphp.sh 

* Thu Oct 09 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100902.mr
- fix setQuota() because wrong refer to getFSBlockSize() instead getFSBlockSizeInKb
- remove restart in cleanup-simple
- fix restart related to scavenge

* Wed Oct 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100807.mr
- fix mariadb-to-mysql convert
- fix mariadb in service list
- fix blank 'php configure'
- fix error if reversedns driver lib not enable
- fix topbar_right related to status color 

* Wed Oct 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100804.mr
- remove force-restart
- add '--help' in restart
- add '--force' to running 'real restart' instead custom restart process
- set setup/installer/cleanup using 'restart' with '--force'
- fix list.master/slave.conf.tpl of dns config
- add getFSBlockSizeInKb() to detect filesystems blocksize
- fix setQuota (depend on blocksize)
- set inode as 1/10 of blicksize in setquota

* Wed Oct 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100802.mr
- cleanup code (appear warning/error in debug mode)
- fix restart dns (because no prevent for execute rndc)
- fix lighttpd configs (missing pid)
- mod ips, dns master and dns slave depend on server
- remove getIpfromARecord() in dnslib.php (because move to lib.php)
- mod getAllClientList() depend on server
- fix/mod kloxo.init related to reload
- add kloxo, lighttpd, mysql, nginx and xinetd in restart process
- add force-restart script
- fix in dns__lib.php (bug in domain appear)
- mod redirect in hiawatha config

* Tue Oct 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100709.mr
- fix execute 'rndc reload' if running 'restart-all'
- mod restart and process script
- fix hiawatha.init
- fix ftpuser (use 'useradd' instead 'useradd' + 'usermod' in fix process)
- add php-fpm and mod hiawatha and httpd restart process
- add restart-syslog
- add restart-syslog to restart-all
- mod to watchdog to inteprete '__driver_' to 'restart-'

* Tue Oct 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100706.mr
- fix upcp (related to php52s/php53s)
- make short text for 'Copy all contents...'
- fix nsd because nsd.db must under nsd:nsd
- fix nsd4.conf (need add control-interface and port for certain OS environment)
- modified nsd restart process
- move mydns.sql (because wrong place) 

* Tue Oct 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100704.mr
- fix 'restart' process in nsd configs
- fix mydns tpl (still not work)
- more customize for restart process
- fix/mod restart scripts
- back to use 'restart' instead graceful/condrestart in restart process
- fix nginx back in webcache (need overwrite default.conf in /etc/conf.d)

* Tue Oct 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100701.mr
- prepare for mydns (need testing)
- mod reserved.lst because certain dirs move to /opt/configs
- disable removeotherdrives process until better approach (problem with proxy and without class)

* Mon Oct 06 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100601.mr
- disable maradns (possible change to mydns)
- reconstruct dns configs (all with the same 'model')
- fix pdns in service list

* Sun Oct 05 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100502.mr
- set list.transfer as latest process in fixdns
- mod djbdns to able as master and slave dns
- set return not exists dnsslave_tmp dir
- fix 'warning' if not exists slave file in djbdns
- fix dns configs if djbdns not exists
- fix pdns configs if slave not set

* Sat Oct 04 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100404.mr
- use 'nsd-control' instead 'nsd' service for update domains
- fix directory chown of bind
- add log in bind
- fix rndc config
- use 'text' instead 'raw' format for bind slave files
- fix 'restart' dns service (check service exists or not)
- make simple for dns record display
- remove rndc.conf if exists
- fix entry for mx record

* Sat Oct 04 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100402.mr
- fix initial nsd in cleanup process
- add 'fix-missing-admin' script
- fix copy nsd.conf in cleanup process
- use php instead bash for fix-missing-admin
- change maindomain_nun, pserver_num and vps_num to unlimited
- fix cname/fcname in dns configs (forgot end dot) 

* Fri Oct 03 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100303.mr
- remove ddns (old var) from domains.conf.tpl in dns configs
- use strpos instead cse (custom function) in domains.conf.tpl in dns configs
- remove fixphpfm (because include in fixphp)
- fix dns__lib.php (missing '{' in after 'else')
- fix list.slave.conf.tpl in nsd

* Thu Oct 02 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100206.mr
- add monkey in web and knot in dns list
- mod appear ns record if original data is '__base__'
- fix uninstall maradns
- mod nsd configs for accept nsd 4.1.0 
- fix nsd configs (nsd-control from v4 not work if no setting for remote-control
- fix nginx configs (related to port) 

* Thu Oct 02 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100202.mr
- fix dns configs to handle 'old' data in 'ns records'

* Thu Oct 02 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100201.mr
- fix httpd configs related to php-type
- fix pdns when installed

* Wed Oct 01 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100110.mr
- replace wrong domains.conf.tpl for pdns
- mod domains.conf.tpl for pdns
- back to use 'work' domains.conf.tpl of pdns

* Wed Oct 01 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100108.mr
- fix curl execute in panel (add CURLOPT_SSLVERSION and CURLOPT_SSL_CIPHER_LIST)
- remove certain useless files
- mod dns configs and data entry to accept 'delegate' dns for subdomain to other server
- fix urltookit to urltoolkit in defaults.conf.tpl of hiawatha
- also add block_shellshock urltoolkit for hiawatha for panel
- fix dns configs if using more than 2 ns
- fix dns configs if delete ns and then create new on

* Wed Oct 01 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014100103.mr
- fix trimming input data (with use new trimming function)
- fix validate_hostname (with accept '__base__')
- fix phpinilib.php error in debug related to 'multiple_php_ready'
- fix web/web__lib.php error in debug for add domain 

* Tue Sep 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014093002.mr
- add block_shellshock urltoolkit for hiawatha
- add 'screen' in install process
- change timezone will be symlink instead copy file
- default php timezone based on /etc/localtime (after symlink)
- fix validate for 'ns records'

* Mon Sep 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092904.mr
- fix missing nolog var in tmpupdatecleanup.php
- set 'recursive no' in bind
- merge validate_ipaddress and validate_ip_address
- fix validate_ipaddress
- prepare 'new' demo (admin just set 'as demo' for certain client)
- remove indexcontent.php
- fix demoinit.php

* Mon Sep 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092902.mr
- fix bind (related to named/rndc.conf location)
- fix trim for input (no action for multidimensional array)
- fix delete .flg files in generallib.php

* Sun Sep 28 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092804.mr
- disable print_r in mailtoticket.php (only for debug purpose)
- use general validate functions in lib.php instead validate directly in dnsbaselib and weblib
- trim inputs in add/update functions (declare in lxclass.php)

* Sun Sep 28 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092803.mr
- make simple where delete all slave dns before re-create
- ready for bind, nsd and pdns
- fix bind tpl script
- fix pdns (for awhile always delete before add/update)

* Sat Sep 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092702.mr
- fix allow-transfer for bind, djbdns and maradns
- fix add to sysctl.conf
- mod fix.inc to appear --target
- mod set-fs
- remove double declare for action in dns__lib.php
- mod README.md
- fix qmail info in sysinfo and component list in panel

* Fri Sep 26 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092607.mr
- add 'secondary/slave dns' feature (already testing for bind and nsd)
- add fixdns to dnsslavelib.php
- disable php-cgi checking in cleanup process
- mod bind and nsd for slave dns
- add 'blank' list.slave.conf.tpl for djbdns
- change createRestartFile to use 'restart' script instead specific driver
- modified validate_domain_name to accept bypass parameter
- hidden stop process for kloxo-wrapper

* Fri Sep 26 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092602.mr
- fix create new mailaccount
- mod note for phpm-installer 
- fix bind related to allow-notify

* Thu Sep 25 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092501.mr
- fix user-logo.png link in 'user logo'
- make smaller height of logo images (from 60 to 40)
- add allow-notify for bind
- fix nsd related to different version
- fix ftpuser if 'docroot' not exists
- fix mailaccount related to 'garbage' account
- back to use 'long' keepalive for hiawatha for panel

* Mon Sep 22 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092203.mr
- fix execute set-mysql-default in install process in setup.sh 
- fix xinetd (need install if not exists)
- decrease maxclients in apache mpm to 400 (max for serverlimit 16) 

* Sun Sep 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092103.mr
- use the same source for timezone for php and system
- mod restore.php info
- add fixdnschangeip (possible change ip in dns)
- add missing fastcgi_cache_key in nginx
- change nginx.init based latest version
- fix web/web__lib.php for cp
- back to execute disable-mysql-aio in install process
- disable-mysql-aio only process for openvz only
- remove copy init file in defaults.conf.tpl for web

* Sat Sep 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014092002.mr
- remove certain unwanted files
- move certain css class/id from each skin to common.css
- add certain css class
- fix for default timezone in php 

* Fri Sep 19 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091902.mr
- move function.sh to ./sbin dir (the same dir for kloxo-wrapper.sh
- delete process.php (because for windows)
- mod installer.php for hostname ip
- create set_restart() and execute in dosyncToSystemPost() only
- possible use custom.kloxo.php (execute in function.sh)
- mod list.master.conf.tpl (for dns configs) related to 'restart'
- fix s.gif url from extjs.com to current url
- move certain style to css (make easy to customize for .css and js)

* Wed Sep 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091704.mr
- add mysql in services list
- create lxadmin dir in fixmail-all if not exists
- mod fixrepo; add set-fs (increase open files limit in sysctl and limit)
- add set-hosts (add declare hostname in /etc/hosts)
- fix install process (especially for update from lower version)
- disable 'yum clean all' in install process (make faster)
- fix set-hosts script (issue related to CentOS 6)

* Wed Sep 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091702.mr
- fix isRpmInstalled (taken from 6.5.0)
- move for create symlink for /script from installer.php to setup/installer.sh
- change skin-set-all-client to skin-set-for-all
- add execute skin-set-for-all in setup/installer.sh

* Tue Sep 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091602.mr
- fix installer.php (related to rpm installed)
- remove libmhash (because using mhash) in install process

* Tue Sep 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091601.mr
- fix serverweb (back to use 'old style')
- remove pdns install in PreparePowerdnsDb
- back to use lxshell_return in isRpmInstalled

* Mon Sep 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091501.mr
- add 'Header unset ETag' and 'FileETag None' in httpd.conf (according to yslow)
- fix djbdns configs if djbdns not install or portable
- dns configs created for all drivers now (like web driver do)
- fix dns and web configs for add/delete domains
- fix multiple_php_install
- fix getDirIndex in web
- fix isRpmInstalled
- mod php-branch script

* Sun Sep 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091403.mr
- remove default.ca/program.ca because relatef to lxlabs.com (expired)
- fix fixweb (fixweb for domain/client will NOT delete all domains configs)
- add Rainloop webmail to install in cleanup process

* Sun Sep 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091402.mr
- fix ssl issue in hiawatha (not work domain ssl with subjectAltName/v3_req)
- mod to not copy .ca from default.ca if .ca not exists

* Sun Sep 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091401.mr
- use always 'none' driver for serverweb
- set stats always protected
- add getDirIndex (nginx still in progress)
- fix in linuxfslib.php
- fix execbackupphp (use string instead array)

* Fri Sep 12 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091204.mr
- mod defaults.conf.tpl for apache
- fix missing SSLEngine on in defaults.conf.tpl for apache
- mod using 'static' password to random password for postmaster
- disable 'Reply-To' in smessagelib.php
- set possible running changeport.php in slave (use by kloxo.init)
- fix hiawatha configs related to ssl
- change lxshell_return to exec for rm in certain pages
- fix setCopyErrorPages
- mod hiawatha.conf.base
- move SSLCompression from virtualhost to httpd.conf (fix issue in centos 5)
- fix changeport.php (enable initProgram)

* Thu Sep 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091103.mr
- disable MinSSLversion in hiawatha (because not work) 

* Thu Sep 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091103.mr
- mod packages branch list
- move setCopyErrorPages process to top setInitialServices
- mod hiawatha.conf.base (hiawatha for panel base config)
- add specific parameter for ssl in web configs
- fix wrong defaults.conf.tpl for nginx

* Thu Sep 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091101.mr
- fix missing process from copy dirprotect_stats.conf in nginx and lighttpd
- mod hiawatha configs (also add 'SecureURL = no')
- add and execute setCopyErrorPages in cleanup

* Wed Sep 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014091001.mr
- optimize cleanup proses (make faster)
- back to use rm instead 'rm' because lxshell_ already add ''
- mod fixweb to delete 1x domains configs
- use graceful instead restart for httpd
- hiawatha possible running in normal install or 'portable' version
- add select 'timezone' for server/client level
- change io process from all 'nice' to 'ionice'
- fix installer.php (missing var in rm_if_exists)

* Tue Sep 09 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014090905.mr
- disable chown/chmod in fixweb to make faster (using fix-chownchmod for this purpose)
- fix mysql-convert and mysql-optimize script
- add set.web.lst (but delete set.httpd.lst and set.nginx.lst)
- add vpopmail_fail2drop.pl to protect brute-force for mail

* Tue Sep 09 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014090903.mr
- fix switch-php-fpm
- fix default_index.php
- change from static user_sql_manager.flg to 'include' sqlmgr.php for 'sql manager' url

* Tue Sep 09 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014090902.mr
- fix kloxo.init and phpm-installer
- add alternative sql manager url

* Mon Sep 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014090802.mr
- fix phpmyadmin link
- run 'upcp -y' will be set skin as 'simplicity' skin (to make sure update from 6.5.0)

* Mon Sep 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014090801.mr
- fix kloxo.init (missing 'special' php.ini path)

* Sat Sep 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014090601.mr
- change to use \\rm to 'rm' for temporary unalias for cp/mv/rm; fix kloxo port for thirdparty if not 7778/7777
- fix enable/disable perl in hiawatha
- fix ssl port in nginx
- enable secondary-dns in nsd (in progress)
- mod ip list not include hostname ip in dns (related to notify)
- input always trimming before validated
- fix php5.fcgi path
- make more info and short meassage in log (with remove path)
- remove fixservice in cleanup because always 'chkconfig on' for all services
- remove detect for custom php.ini in kloxo.init but add copy custom to php.ini in fixlxphpexe
- disable process 'disable-alias' in cleanup; mod clearcache

* Fri Sep 05 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014090503.mr
- fix fixwebcache
- back to use notify insted restart in nsd
- remove double session.save_path in php53-fpm-pool.conf.tpl
- remove setup init in webcache in defaults.conf.tpl
- fix switch in dns
- fix syslog.conf for /var/log
- mod for accept for nsd 4.x in list.master.conf.tpl
- change \rm to rm in all sh script
- fix packer.sh
- fix dns install for enable 'chkconfig on'

* Thu Sep 04 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014090401.mr
- change back \rm to rm because conflict with \r escape char (fortunely still work without \)
- remove watchdog for syslog (port 514 not work)
- fix initial value for php.ini (change null to '')
- fix public_html symlink in weblib
- fix disable log in rsyslog/syslog config
- fix get_kloxo_port
- fix fixwebcache
- back to use notify insted restart in nsd
- remove double session.save_path in php53-fpm-pool.conf.tpl
- remove setup init in webcache in defaults.conf.tpl
- fix switch in dns
- fix syslog.conf for /var/log

* Wed Sep 03 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014090301.mr
- fix all cp/rm/mv to their 'temporal unalias'
- in program changedriver (need running dns-, webcache- and web-installer)
- fix all dir from /home to /opt/configs for all configs
- mod all dns_lib
- fix mailqueuelib if mail no exists
- mod to domainkey.txt always overwrite
- fix appear 'switch programs', especially for fresh install issue
- disable reversedns (because only ready for bind)

* Wed Aug 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082703.mr
- fix dns issue when switch
- fix fixdns and fixweb when using 'none' driver
- add unalias for cp/mv/rm in upcp

* Wed Aug 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082701.mr
- remove magic_quote and safe_mode from php-fpm config and php ini
- fix restore and switchserver
- mod fixwebcache; fix web conf.tpl
- fix url path in nginx (generic and awstats)
- fix for webcache switch related to web
- fix web__lib related to webdriverlist
- fix common.inc related to 'none' driver
- mod packer.sh
- fix fixlxphpexe
- back to use 'listen' include for nginx 

* Sun Aug 24 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082402.mr
- fix defaults.conf.tpl logic for hiawatha.conf copy
- remove cp/mv/rm alias
- set default.conf.tpl for copy init and main conf 
- fix defaults.conf.tpl
- mod setUpdateConfigWithVersionCheck()
- disable copy conf file in setCopyWebConfFiles() to /etc because move to defaults.conf.tpl

* Sat Aug 23 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082301.mr
- mod webserver init with add custom file inside /etc/sysconfig
- fix hiawatha init to possible using custom hiawatha.conf

* Fri Aug 22 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082201.mr
- prepare use mod_macro for apache
- set to use 'real' kloxo port in web configs instead use 7778/7777 only
- move /home/openssl to /opt/configs

* Thu Aug 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082105.mr
- set 'conflicts' for kloxomr-6.5.0 and 'obsoletes' for kloxomr-6.5.1

* Thu Aug 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082104.mr
- fix hiawatha-proxy
- moving cp. declare in nginx and lighttpd (like hiawatha do) 

* Thu Aug 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082102.mr
- fix ReleaseNote
- fix missing mod_define in apache 
- fix Update Info

* Wed Aug 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082002.mr
- mod packer.sh for accept kloxomr7

* Wed Aug 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.0.b-2014082001.mr
- change version from 6.5.1 to 7.0.0
- change/move driver configs (web, webcache and dns) from /home to /opt/configs
- optimize web config to make faster fixweb and switch driver
- create all web configs together and switch web just modified 'defaults' portion
- use mod_define to make apache able set 'var'
- optimize speed for fixftpuser (2x)
- remove certain codes for windows os
- add webcache driver in service list
- fix list display if click sort
- add 'custom' php.ini for kloxo init
- add 'timewatch' for certain fix script

* Tue Jul 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014072901.mr
- fix installing process related to phpm-installer

* Mon Jul 28 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014072801.mr
- change system() to exec() in fixvpop.php
- fix hiawatha service when running cleanup if hiawatha as active webserver

* Sun Jul 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014072701.mr
- just using phpm-installer for install all phpXYm/s
- mod/fix all php bin for general path
- change session path based on user
- validate username and password for add ftp user

* Wed Jul 09 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014070901.mr
- auto chown 755 for pl/cgi/py/rb if upload or fix-chownchmod 

* Tue Jul 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014070801.mr
- fix update ssh script
- disable .htaccess fix in fixweb 

* Mon Jul 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014070704.mr
- check mod_perl in cleanup process
- back to use previous reverseproxy for nginx and hiawatha
- add keep-alive and reduce timeout to 90 in hiawatha-proxy
- change reverseproxy passing from all to except pl/cgi/py/rb/shmtl (because handle by cgi-wrapper)
- reduce timeout value in nginx

* Sun Jul 06 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014070601.mr
- use hiawatha's cgi-wrapper instead apache's cgi in hiawatha-proxy
- mod/add index order (accept index.cgi also)
- using mod_perl instead mod_cgi for apache
- enable taint in perl for security reason

* Fri Jul 04 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014070402.mr
- fix enable-cgi (also warning 'not implementing yet' in nginx)

* Fri Jul 04 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014070401.mr
- fix/mod certain throw messages
- mod htmltextarea space
- enable/disable cgi for webserver
- use cgi-wrapper for hiawatha
- change openbasedir for 'apache' user
- use directly cgi-assign to perl instead perlsuexec for lighttpd
- fix lighttpd conf.tpl

* Mon Jun 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014063001.mr
- remove 'output_buffering = 4096' and stay with '= off' in php.ini 
- change throw value from array to string

* Fri Jun 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014062702.mr
- fix throw for mailing list
- convert to string if message as array (related to getThrow)
- mod certain throw messages

* Fri Jun 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014062701.mr
- use phpXYm for suphp in secondary php
- fix ssl reloop for nginx-proxy
- fix ckeditor for only save body content
- enable phar, intl, geoip, fileinfo and tidy module in php fix logrotate

* Tue Jun 24 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014062401.mr
- add getThrow() for translate throw message
- update all throw message with getThrow; fix logrotate config

* Sat Jun 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014062102.mr
- change addon-ckeditor/fckeditor to editor-ckeditor/fckeditor
- change addon-fckeditor to editor-*

* Sat Jun 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014062101.mr
- remove obsolete for fckeditor and ckeditor
- remove fckeditor/ckeditor from core code
- install ckeditor if not exists when running cleanup
- add provide for fckeditor and ckeditor

* Fri Jun 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014062001.mr
- add $this->write in postUpdate to make sure db write before next process
- prepare 'multiple php' (but still in progrss)

* Thu Jun 19 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014061903.mr
- add try-catch in default_index.php
- fix fixlxphpexe 
- also run rkhunter update in install process
- use ckeditor instead fckeditor if installed
- include ckeditor

* Tue Jun 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014061701.mr
- fix 'phptype_not_set' alert
- increasing connection in nginx and hiawatha until 10x (for high-traffic)
- use 'new' permalink for lighttpd
- prepare 'new' ip validate

* Sun Jun 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014061502.mr
- use callInBackground for lx_mail
- possible disable send notify for quota with flag
- add 'disable notify' for 'disable policy'
- add 'enable cron for all' in 'general settings'
- fix change 'webmail system default' (no need 2x click update again)
- increase types_hash_bucket_size in nginx for long domain name issue

* Sat Jun 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014061403.mr
- add default.conf for nginx for prevent when using webcache in front of nginx
- prevent delete main ftpuser
- fix 'server alias' for wildcard
- fix web_lib.php related to nginx

* Wed Jun 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014061101.mr
- mod scavenge send mail with Y/m/d format; mod djbdns tpl
- add some env to php53-fpm-pool.conf.tpl
- prepare phpm-fpm template
- mod kloxo.init to accept custom sh/conf/ini
- upload 'new' phpm-fpm template
- mod php-fpm-part.conf.tpl
- use symlink instead copy from pscript to /script
- mod php-fpm tpl to change php_value to php_flag for on/off
- change php_active to kloxo_php_active and adjustment for kloxo.init and fixlxphpexe

* Sun Jun 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014060802.mr
- add enable gzip in hiawatha
- change X-Forwarded-For in nginx
- mod php-fpm.conf.tpl (fpm for php52)
- enable send mail for scavenge
- fix loqout in feather skin
- add expire in hiawatha for panel
- add php-fpm conf/init/sh in php52m/php52s
- fix scavenge.php

* Wed Jun 04 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014060401.mr
- change CGIHandler from php to pl in hiawatha
- enable alias to cgi-bin in hiawatha; fix cron for client
- change root@ to admin@
- fix 'go' button in list
- set cursor to certain css tag
- mod htmllib related to cursor 
- change 'idle-timeout' for 'FastCGIExternalServer' of mod_fastcgi from 180 to 90

* Fri May 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014053003.mr
- fix header in lx_mail()
- mod to possible stmprelay/smarthost to outside smtp server
- mod to enable cron for users if exists '/usr/local/lxlabs/kloxo/etc/flag/enablecronforall.flg' file
- mod apache disable dirlist
- mod message for cron list
- fix nginx config (inactivate for 'disable_symlinks') because troube with static file path
- change sender from kloxo@ to root@

* Sat May 24 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014052401.mr
- mod/fix lx_mail() to accept utf8 and html and remove pre from message

* Mon May 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014052103.mr
- set /tmp dir as upload and save dir for phpmyadmin
- add 'max_input_vars' in php.ini and php-fpm config (set '3000' as default)
- add 'max input vars' in 'advanced php configure'
- send message as html and with utf8 charset

* Mon May 19 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014051901.mr
- add www.conf (blank) for php-fpm because latest php always create this file
- fix crf_token
- delete unused certain php files

* Tue May 13 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2014051301.mr
- add '-pass-header Authorization' in domains.conf.tpl of apache
- fix syncserver in web__lib.php
- prettier php code in certain files

* Mon May 12 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2014051201.mr
- separate warning for php.ini to client and pserver
- feather skin also appear background image (but still not use)
- no convert for '\n' to '<br />\n' (fix ticket list appear)

* Sat May 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2014051004.mr
- change listen.mode from 0660 to 0666 in php-fpm pool
- mod fixmail-all 

* Sat May 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014051002.mr
- mod/fix phpm-installer
- mod installatron-install
- fixmail-all also fix chown and chmod of /home/lxadmin/mail
- fixmail-all also checking postfix user and change to vpopmail if exists
- fix/mod installer related to postfix user
- fix php-fpm related to php53/php54 release -28 (add listen.owner, .group and .mode);
- fix/mod installer (related to fix process) and fix-all

* Mon May 5 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014050502.mr
- fix 'php used' in 'webserver configure' in master-slave environment

* Mon May 5 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014050501.mr
- fix default_index.php for using login page
- add syncserver for input array (importance for pdns in master-slave environment)
- fix dns class lib (add __construct like web class lib do)
- fix php.ini warning if not set (server and admin level)
- fix 'switch program' fpr master-slave environment
- fix 'webcache' input array in web lib
- fix click in php.ini warning
- change restart httpd in latest step in restart-all/restart-web

* Wed Apr 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014043002.mr
- set/enable phprc in php-cli (fix issue for missing .so in lxphp.exe)

* Wed Apr 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014043001.mr
- set mywebsql as 'sql manager' if exists in 'httpdocs/thirdparty'
- fix installatron-install if webmin exists
- fix php53m-extension-installer (also remove full path of extension)
- fix phpm-config-setup with remove full path of extension

* Tue Apr 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042902.mr
- increasing MaxUploadSize to 2000 in hiawatha and MaxClients to 1000 in httpd
- fix custombutton not show icon in client
- make possible php54s beside php53s (resolve mariadb 10.0 issue; compile with mysqlnd for '--with-mysqli')

* Mon Apr 28 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042803.mr
- overwrite /etc/php.ini in upcp (prevent missing .so in lxphp.exe)
- remove postfix user before re-/install qmail-toaster in upcp
- add install yum-plugin-replace in upcp
- mod phpm-config-setup
- fixmail-all also remove postfix user and install qmail-toaster if not exists
- move 'default' php.ini (because wrong place)

* Sun Apr 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042702.mr
- move process update mratwork.repo to fixrepo and then execute in upcp (including change $releasever to OS version)

* Sun Apr 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042701.mr
- fix web config template (forgot open bracket for .ca logic)
- fix upcp for 'mratwork-' execute

* Sat Apr 26 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042601.mr
- still trouble with php for openssl (not perfect for SAN) and then mod to minimize problem
- little fix lighttpd config (still problem with ssl)

* Thu Apr 24 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042401.mr
- external apps access via post (like phpmyadmin)
- fix to mariadb may not work if /var/lib/mysqltmp not exists
- implementing SAN for domain-based ssl cert
- cleanup will be copy openssl.cnf.tpl to /home/openssl
- fix button appear for client login

* Tue Apr 22 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042202.mr
- fix reset-mysql-kloxo-password.php
- fix lighttpd conf.tpl related to .ca ssl
- change all lpform method to 'get'

* Mon Apr 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042101.mr
- disable implementing update/add/delete in get for 'csrf token' because too much exception

* Sun Apr 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042008.mr
- set 'cgi.rfc2616_headers = 0' in phpm series (because problem with mod_fastcgi)
- mod mysql-to-mariadb.php and mariadb-to-mysql.php
- change extension from mysql to mysqli in phpmyadmin_config.inc.php
- fix issue related to csrf for service action
- fix restore process for 'csrf token' (change 'get' to 'post')

* Sun Apr 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042004.mr
- add/delete domain-based cert also fixweb and restart-web
- disable php module flag and update in phpinilib.php
- disable setInstallPhpFpm when switch web (aka install web driver) 

* Sun Apr 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014042001.mr
- add no permit for add/delete/update with get instead post 
- prepare domain-based ssl without assign to IP address
- fix delete in list related to 'csrf token'
- fix/change kloxo-php-fpm as root
- fix topbar_right (remove undefined param)
- fix certain form to post (related to 'csrf_token')
- implementing domain-based ssl certificate (delete still not remove files)
- mod web config related to domain-based ssl cert
- change using .crt to .pem in all web config
- fix delete cert also delete cert files
- change is__table to getClass (because the same purpose)
- fix sshconfig ini in show
- mod messagelib.php related to domain-based cert

* Fri Apr 18 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041802.mr
- set to make sure all add/delte/update in form must be under post and add csrf_token

* Fri Apr 18 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041801.mr
- mod property for 'limit' and 'custombutton'
- fix phpm-config-setup (related to php55m for symlink)

* Thu Apr 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041704.mr
- disable fix_self_ssl in update process
- enable for disable_functions in phpXYm php.ini
- add mysql56u in set.mysql.lst
- fix ftpuser if docroot not exists
- add/mod message in messagelib
- mod/fix phpini initialValue
- fix frame_left for client level (disable quickaction logic)
- mod/fix for handle update situation for mysql and php53s
- 'yum remove' for php53s also 'rpm -e --noscripts' for php53s-fpm

* Wed Apr 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041602.mr
- separate delete warning for customer and admin/reseller
- fix/mod for detect use yum and rpm in sh script

* Wed Apr 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041601.mr
- fix/mod 'nice' params
- mod csrf_token logic
- update and phpm install not work in panel (found yum problem in centos 6 64bit)

* Tue Apr 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041504.mr
- fix display issue related to token validate where only add/update/delete with 'post' method
- fix phpini because getlist for pserver only work under admin and then change to parent
- add warning in deletion list
- move deletion warning to top because possible not appear in long list

* Tue Apr 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041501.mr
- validate token able to disable
- fix add cron job (update still not work) 

* Mon Apr 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041402.mr
- recompile with fix wrong domainlib.php file

* Mon Apr 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041401.mr
- remove mysql from mysql.lst and for only mysql55 beside mariadb
- mariadb-to-mysql will be convert to mysql55
- disable installapp reference in ddatabaselib
- set initPhpIni() only use values from setUpINitialValues()
- add missing 'selected' keyword
- update 'limit' will be update will execute fixphp
- fix domainlib issue (isOn change to '=== 'on') in client domain
- to make sure quota value in 'float' format
- fix preAdd() with add params
- fix 'checked' in display

* Sun Apr 13 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041303.mr
- fix php53s.ini for using special setting for panel

* Sun Apr 13 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041301.mr
- add isTokenMatch() for 'csrf token'
- change protect from 'remote post' to 'csrf token'
- fix htaccess.tpl and php.ini.tpl (add 'default value')
- fix issue if select 'multiple php' and user click 'php configure' in domain
- mod phpm-instaler/-config-setup
- to make sure '/tmp/multiple_php_install.tmp' owned by root 

* Sat Apr 12 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041203.mr
- mod/fix langkeyword/message data
- mod multiselect list able to use keyword for title
- change redirect for 'change owner' from 'a=resource' to 'new client'

* Sat Apr 12 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041201.mr
- add ftpChangeOwner() because call by web__lib
- add db_set_value()
- fix do_remote_exec() with create remote object if not set (effect for 'change owner')
- fix ftpuser owner for 'change owner'

* Fri Apr 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041104.mr
- mod/update phpm-installer/-config-setup (all config parts move to -config-setup)
- mod 'searchall' button
- set 'php configure' not appear if not enable 'multiple php'
- fix preUpdate in objectactionlib.php
- add fix-yum-cache
- change from 300 to 30 for timeout in /etc/yum.conf

* Fri Apr 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041101.mr
- add more disable modules for phpm-installer (minimize trouble when using php52 as php-branch)

* Thu Apr 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041003.mr
- forgot submit mod lxclass.php (related to preAdd()/preUpdate())
- mod preUpdate in serverweblib.php (consistence with declare preUpdate in lxclass)

* Thu Apr 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014041001.mr
- add new preAdd()/preUpdate() function to process before add()/update()
- install 'multiple php' runnind well now from panel and in background process (need a trick)
- mod lxa.js related to multiselct

* Wed Apr 9 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040901.mr
- move mratwork-* detect from cleanup to upcp

* Tue Apr 8 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040801.mr
- fix directory protect for hiawatha (forgot add 'basic' in 'passwordfile' param)
- add log for phpm install process
- mod php5.fcgi 
- prepare install 'multiple php' via panel
- fix switch-php-fpm
- add option in 'webserver configure' for switch-php-fpm ('multiple php install' still not work)
- add 'Fix - PHP' in 'command center'
- change form color

* Sun Apr 6 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040601.mr
- also disable magic_quotes, register_long_arraya and register_globalsin htaccess
- disable allow_call_time_pass_reference in php
- prepare add token in add/delete/update form
- add validate for 'server alias'
- better 'die' display
- mod xprint for display data of object, array or string
- implementing protect from 'remote post' instead using 'csrf token' (need more investigate)
- back to declare all php module in apache because selected module need fixweb every php-type changed
- fix mod_rewrite issue in apache
- fix chmod for php5.fcgi
- fix isRemotePost (change 'SERVER_NAME' to 'HTTP_HOST')
- fix directory declare in hiawatha related to directory protect
- fix phpm-installer (wrong declare for redis)

* Fri Apr 4 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040405.mr
- fix php53s-installer

* Fri Apr 4 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040404.mr
- enable unzip in docroot (no warning)
- back to set 'cgi.rfc2616_headers = 0' because trouble in wordpress in apache/-proxy
- back to not use ' -pass-header Authorization' in mod_fastcgi because must be 'cgi.rfc2616_headers = 0'

* Fri Apr 4 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040403.mr
- now install with php53s by default

* Fri Apr 4 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040402.mr
- remove pear channel update

* Fri Apr 4 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040401.mr
- back to use 'cgi.fix_pathinfo = 1' because many apps not work if 0
- magic_quotes, register_globals and safe_mode always disable (make simple for multiple php)
- remove double post_max_size
- php*-enchant also not enable (bug issue)
- set no options for magic_quotes, register_globals and safe_mode in panel
- mod kloxo.init
- mod sh script for php
- php52s and php53s only for panel and use m version for general purpose (use switch-php-fpm)
- symlink /usr/lib64/php to /usr/lib/php (make simple for 64bit)
- mod fixlxphpexe, cleanup, cleanup-simple and cleanup-nokloxorestart
- mod packer.sh

* Wed Apr 2 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040201.mr
- fix php.ini.tpl
- fixlxphpexe (better rm for symlink to make sure)
- when install in 64bit, phpm-installer only install 64bit dependencies

* Tue Apr 1 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040109.mr
- fix php.ini.tpl
- php52s/php53s install using 'standard' php52/php53u

* Tue Apr 1 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040108.mr
- fix run cleanup after update Kloxo-MR
- fix packer.sh

* Tue Apr 1 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040106.mr
- running fixphp include fix extension_dir path (crucial for multiple php system)

* Tue Apr 1 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040105.mr
- run fixlxphpexe include copy kloxo.init (guarantee always new)
- add missing kloxo-php-fpm.conf (special)

* Tue Apr 1 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014040104.mr
- fix typo in php53-fpm-pool.conf.tpl
- disable 'customemode' option in 'appearance'
- fix php.conf to inactive if switch to php-fpm in httpd
- disable 'export PHPRC=' in all php script (not needed)
- change php-error.log name depend on multiple php-type
- always use 'extension_dir' in all php.ini to mininize wrong php modules loaded
- add switch-php-fpm to make possible one of 'multiple php' for single purpose
- add reset-mysql-kloxo-password (alternative for fix-program-mysql)
- correct double param in php53-fpm-pool.conf.tpl
- correct/mod extension_dir in php.ini.tpl/php.ini.tpl
- fix php52s-installer
- also fix php-fpm-pool.conf.tpl in future phpcfg for typo and double param

* Sun Mar 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014033004.mr
- fix fix-qmail-assign
- running 'fix-qmail-assign' also create '.qmail-default' if not exists

* Sun Mar 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014033003.mr
- disable 'PATH_TRANSLATED' in nginx config because set 'cgi.fix_pathinfo = 0' in php.ini
- fix url for 'driver' list
- mod related to 'createListAddForm' and 'addListForm' function
- fix related to 'click here to add' in 'printListAddForm'
- change color for active tab and breadcumb
- fix/mod fix-qmail-assign to more info
- add 'help' in 'feather' (simple skin already exists)
- fix-chownchmod also fix mail dirs/files

* Sat Mar 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014032907.mr
- back to previous idea for phpXYm script
- fix extension_dir for phpXYm
- separated config-setup to file from phpm-installer
- add run phpm-config-setup to cleanup

* Sat Mar 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014032905.mr
- fix/mod sshauthorizedkey
- fix appear for 'selectshow'
- set to 'no disabled' for 'admin'
- mod/fix script for phpXYm and phpXYm
- already appear 'multiple php' options but unfinished yet
- fix/mod 'StW' type display (using textarea instead table)
- make simple sshauthorizedkey code
- change 'multiple php enable' to 'multiple php ready'
- prepare for 'multiple php' template script
- back to php.ini under web but only for 'php selected' and enable 'multiple php'
- add/change 'alert' if php.ini not set under 'pserver'

* Tue Mar 25 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014032502.mr
- fix detect php 5.4/5.5 which 'php -v' not work if using php 5.2/5.3 ini
- add 'try again' in 'alert' for fail to add domain
- remove 'disable installapp' in 'general'
- fix to setup roundcube 1.0.rc
- fix copy php-fpm.conf

* Tue Mar 25 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014032501.mr
- fix image/font appear depend on button type
- change to lxguardhit appear different column for fail and success
- fix permissions (from 0600 to 644) for user-logo
- fix version check
- fix restart if hiawatha status as not running
- gen-hashed.sh (for qmail user assign (based on 'real' bash)

* Sun Mar 23 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014032301.mr
- mod how-to-install.txt
- mod/change phpXY-installer
- create log file for escape segfault in install
- php.ini now based on user-level
- able setting php max children in resource plan
- mod fixweb/fixphp to adopt user-level php.ini
- install process with more info/message
- move php.ini/php5.fcgi from /home/httpd/<domain> to /home/kloxo/client/<client>
- fix fcgid to config adopt user-level php.ini
- max children appear 'unlimited' but intepret as '6'
- fix dns serial
- fix wrong text for load-wrapper calling
- php-fpm config include php configure from panel as 'php_admin_value'
- no admin/domain mode for admin (just appear admin mode)
- fix detect phpversion
- delete client also delete php-fpm config
- fix issue if dnssyncserver not array
- add is_cli() for debug purpose (different appear in cli and cgi mode)
- fix issue in sqlite.php if object not exist
- modified simplicity skin where breadcumb move from top to bottom of tab
- fix mailinglist where wrong url because as object
- fixweb and fixphp is separate process now
- fix fixlxphpexe script
- 2 type of multi-php (phpXYm and phpXYs)
- mod upcp and install scripts
- add options for install (-y/-force, --with-php53s/-53s and --remove-kloxo-database/-r)

* Mon Mar 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014031701.mr
- fix cleanup (no need restart phpXs)
- change to use php52 instead php53 for install step
- fix kloxo.inits
- fix phpXs-installer
- installer have options with '--force'/'-y', '--remove-kloxo-database' and '--use-php53s'
- delete disable-mysql-aio and add set-mysql-default (with more options)

* Sun Mar 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014031602.mr
- add missing default driver content
- phpXs-installer will be detect target php

* Sun Mar 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014031601.mr
- fix dependencies for phpXs-installer
- cleanup also convert special php53s to php53s based on php53u
- fix and also convert php52s in cleanup

* Sat Mar 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014031501.mr
- fix detect phpversion
- mod status appear in simplicity skin
- panel using php53u (via php53s-installer) instead special php53s
- add php*s-installer (prepare for multi-php)
- disable register_long_arrays in php 5.3+ (problem for 5.4+)
- possible execure php-cli with softlimit
- increase listen.backlog in nginx
- install able with '--force' and '--use-php52s' (default using php53s)

* Wed Mar 12 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014031203.mr
- rename softlimit to softlimit.sample because something wrong under centos 6 64bit (bug?)

* Wed Mar 12 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014031202.mr
- add 'proxy_set_header X-Forwarded-Protocol $scheme;' to nginx proxy.conf
- change menu file/dir for simplicity skin
- add soflimit in php*-cli.sh (automatically for lxphp.exe)
- change 'vm.vfs_cache_pressure' value 100 (tend to slow cached memory created)
- pending select php.ini from menu for client in simplicity skin 

* Mon Mar 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014031002.mr
- disable dtree for delete client
- fix for delete database username 

* Mon Mar 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014031001.mr
- make enable clientname as database username
- fix/mod image to font icon if select 'button_type' as font
- fix initial roundcube
- fix spamdyke config
- add -pass-header Authorization in mod_fastcgi of httpd
- fix for double userdir rule in nginx
- back to user 'default' restart for services
- delete domain also delete docroot if no other domain use the same docroot

* Sat Mar 1 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014030101.mr
- disable UserDirectory in hiawatha (to purpose userdir but not work)
- disable 'enable_php_fastcgi' in resourceplan
- move php logic for topbar to their php
- add 'wait' in 'status' top bar when click add/update

* Fri Feb 28 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014022801.mr
- fix tab bar for 'Client Processed Logs' page
- fix tab bar for 'lxguard' page
- fix font-icons in lxguard pages
- move left/right top bar of 'simplicity' to include_one with 'custom rule'
- fix icons in list if using 'image' as 'button type'

* Thu Feb 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014022701.mr
- mod packer.sh with also remove .pid files
- make already appear tab bar
- mod dprint/dprint_r with 'pre'
- add xprint (like dprint without debug mode)
- add database without prefix name and also database username for admin
- fix userdir in httpd with make declare userdir outside 'default' virtualhost

* Sun Feb 24 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014022404.mr
- add fixftp-all
- add 'standard command' like fixdns in 'command center'
- remove installapp
- fix quota/normal view with more detail
- add more detil in login history but bug still unreseolvced
- remove livesupport (unfinish work original Ligesh)
- fix list pagesize/pagenum
- use * instead *.lxlabs.com certificate
- upload new certificate

* Sat Feb 23 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014022305.mr
- fix userdir in httpd
- add fixftp-all
- add 'standard command' like fixdns in 'command center'

* Sat Feb 23 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014022303.mr
- resubmit certain restart scripts because wrong files 

* Sat Feb 23 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.b-2014022302.mr
- mod clock also hour with 2 digit format
- fix all restart and cleanup scripts
- move clock js code to clock.js file
- all include, js and css ready for 'custom rule'
- set Kloxo-MR 6.5.1 as b (beta)

* Sat Feb 22 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014022204.mr
- fix validate for new client
- set smaller menu, tab-bar and link-path in 'simplicity' skin
- more detail message and validate for add client and database 

* Sat Feb 22 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014022202.mr
- fix fix-userlogo (related to domainroot)
- fix all cleanups
- fix message and ticket (related to send mail) with add <pre>
- fix list if data is array (date in cron list still not fix)
- add clock in 'simplicity' top bar

* Fri Feb 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014022102.mr
- fix userlogo and default_index.php
- add left-side userlogo in panel
- add 'ticket' in 'simplicity' top bar
- fix non-admin send ticket
- reduce menu text width

* Fri Feb 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014022101.mr
- add alert when click status in 'simplicity' top bar
- change clientname length to 31 (according to centos and pure-ftpd)
- spawn-fcgi only auto-install under php52s in kloxo.init

* Thu Feb 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014022002.mr
- fix display_init
- better status title display in 'simplicity' skin
- restore css for default because wrong css

* Thu Feb 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014022002.mr
- remove double php53s-snmp in php53s-install
- add 'message' and 'status' in 'simplicity' top bar
- add db_get_count() in lib.php
- change "#" to "javascript://" for href in 'simplicity' index.php
- reduce menu container with (800 to 700px) to accept width 1024px display
- move 'status' bar from top-left to top-right

* Wed Feb 19 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014021901.mr
- fix sysinfo.php
- add squid in webcache list
- change client/database name to 64 chsrs and database username to 16 chars
- vslidate for client/database name and database username
- warning if 'switch program' and 'php-type' not set
- change default php-type to php-fpm_worker
- back to use default web, dns and spam server like 6.5.0 version
- mysql_conver also include change to utf-8 charset in panel (like in command-line)
- change '--- none ---' to '--- No Change ---'
- use db_get_value for php-type value
- fix issue if log not create
- fix getRpmBranchInstalled() if list file not exists
- mod randomString()
- add convert_message() fot handling like '[%_server_%]' and implementing also for error/alert message
- fix drop menu align in simplicity skin
- mod changeport.php for compatible with 6.5.0 and 6.5.1
- kloxo stop also checking php52s and php53s running or not
- installer still using php52s (because less memory usage)
- installer also php53s install and restart services before finish

* Sat Feb 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014021502.mr
- fix issue related to lxphp.exe
- fix restarts and kloxo.init
- set 755 for php*-cli.sh and php*-cgi.sh

* Sat Feb 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014021502.mr
- fix php53s-install (replace php53s to php53s-cli to escape conflict with regular php)
- prepare for random prefix for databasename

* Sat Feb 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014021501.mr
- fix nginx config related to disable_symlinks

* Fri Feb 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014021401.mr
- fix php53s-install and restart-all script

* Wed Feb 12 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014021201.mr
- add SymLinksIfOwnerMatch to apache config and equivalent param for other webservers
- change dynamic to ondemand for pm in php-fpm
- panel execute under php 5.2 or php 5.3 but install process still in php 5.2
- prepare jailed code (still disabled)
- run php53s-install if want running panel under php 5.3

* Mon Feb 3 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014020301.mr
- update cron_task (make client only able to list and delete their cron)

* Sun Feb 2 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014020201.mr
- fix install process (add looping to make sure kloxo database created)

* Fri Jan 31 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014013101.mr
- kloxo service using spawncgi (make kloxo-phpcgi under lxlabs user like kloxo-hiawatha)
- disable perl until fix hardlinks issue related to perl
- mod permissions update display

* Wed Jan 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014012902.mr
- fix some issues to make better update from Kloxo official 

* Wed Jan 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014012901.mr
- fix hiawatha config for dirprotect
- fix docroot where update not work 

* Tue Jan 28 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014012802.mr
- fix kloxo sql
- mod file list column 

* Tue Jan 28 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014012801.mr
- mod kloxo sql to using myisam as storage-engine
- fix ownership in filemanager

* Mon Jan 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014012702.mr
- back to use tcp/ip instead sock

* Mon Jan 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014012701.mr
- fix select-all in dns/mysql list
- fix docroot
- fix fastcgi (add ide-timeout)
- fix clearcache
- make update script as the same as cleanup
- fix nsd tpl
- use sock instead tcp/ip to access mysql in panel

* Fri Jan 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014011001.mr
- fix mysql-aio issue in openvz
- add disable-mysql-aio script
- mod how-to-install.txt for additional step when update from Kloxo 6.1.12
- no add certain param in sysctl.conf if openvz

* Tue Jan 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2014010701.mr
- fix install problem in openvz (wrong detect centos version)
- also remove exim in convert-to-qmailtoaster
- add try-catch in default_index.php

* Fri Jan 03 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014010301.mr
- mod again ionice (become not using '-n')
- fix hiawatha for proxy (404 and 504 error)

* Wed Jan 01 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2014010101.mr
- change ionice value
- detect hiawatha as web server when running restart-web/-all
- fix try-cache process in appear
- fix logic for nowrap in list table

* Thu Dec 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013122602.mr
- fix hiawatha service after hiawatha update

* Thu Dec 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013122601.mr
- fix mysql conflict because wrong detect centos 6
- fix web config for disable domain
- fix clearcache logic
- fix appear if restore from previous version

* Fri Dec 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013122002.mr
- fix wrong logic of lxphp detect

* Fri Dec 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013122001.mr
- add keyword text for updateall message and adjusment updateallWarningfunction js
- fix/mod certain infomsg
- change submit naming from frm_change to frm_button/frm_button_all and add frm_change hidden input
- add id for hidden input tags beside name
- fix all_client appear
- add warning to need add 'innodb_use_native_aio=0' in /etc/my.cnf to update to mysql to 5.5 if running cleanup
- cleanup process also fix if lxphp exist
- reupload abstract_012.jpg
- mod certain text in messagelib.php

* Tue Dec 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013121703.mr
- fix install and cleanup related to mratwork.repo

* Tue Dec 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013121702.mr
- fix logic for custom php-fpm in nginx 

* Tue Dec 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013121701.mr
- add/mod certain keyword/message
- fix 'webmail system default'
- mod message box (remove image)
- fix login page if 'session timeout' state

* Mon Dec 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013121603.mr
- fix security bug for php-fpm (add open_basedir)
- mod php-fpm open_basedir

* Mon Dec 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013121601.mr
- change kloxo-mr.repo to mratwork.repo via rpm and sdjustment in install and cleanup script
- change 'processed logs' to 'client processed logs' and 'stats configuration' to 'domain processed logs'
- fix error in debug file if 'property' not exist

* Sat Dec 14 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013121402.mr
- fix tree appear in feather skin 
- fix infomsg in 'Feather' skin
- fix certain infomsg
- remove useless code in display
- fix appear if no infomsg
- fix link in show
- split %client% to %client% and %loginas% in infomsg
- add certain infomsgs

* Wed Dec 11 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013121104.mr
- no permit if docroot with '..'
- change colors for version in login page
- beside when add domain, validate docroot also in 'docroot update' and 'redirect docroot'

* Wed Dec 11 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013121102.mr
- change to use jcterm instead sshterm-template for ssh access

* Mon Dec 9 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013120904.mr
- fix spamdyke disable/enable (need update qmail-toaster also)
- fix tls issue in smtp
- update panel port also create .ssl.port .nonssl.port files in /home/kloxo/httpd/cp
- port in cp also change if panel port change

* Mon Dec 9 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013120901.mr
- use 'post' instead 'get' if form have enctype
- change certain text (like 'show') to keywords
- fix htmledit appear and change height from 200 to 500
- switch to apache also install all necessary module (fix mod_fastcgi issue)
- prepare to change pure-ftp service from xinetd to init
- fix ie8 issue (possible)
- also change 'edit' beside 'html_edit' from 600 to 900px
- fix simplicity skin in IE8 
- mod/add certain infomsg
- prepare qmail stmp run (but still include in qmail rpm)
- fix pagenum/pagesize list

* Fri Dec 6 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013120601.mr
- update running cleanup-nokloxorestart instead cleanup
- add remark in messagelib.php for 'customize' var
- back to use action var instead get in form except for pagenum/pagesize in list

* Thu Dec 5 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013120503.mr
- change 'maxuploadsize' in kloxo-hiawatha from 100 to 2000 (MB)
- fix/mod 'simplicity' menu
- help/infomsg now able to use full html tags (like ul/ol/p)
- fix/mod space in certain list
- fix dbadmin and skeleton reference
- mod certain infomsg with rich html (unfinish jobs)
- mod width to wrap percentage (from 100 to 25)
- finishing reformat help messages (some messages still 'No information')
- fix messagelib.php
- combine add and list for ipaddress and adjustment menu

* Tue Dec 3 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013120301.mr
- note inside hiawatha.conf.base where able upload until 2GB if using hiawatha-9.3-2+

* Mon Dec 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013120201.mr
- move html.php from lib to theme
- add findindexfile in kloxo-hiawatha
- fix menu related to login-as-cancel
- fix sitepreview (also hn_urlrewrite) related to access php file directly
- fix hiawatha default.conf.tpl
- add getDescription function beside get getKeyword
- mod 'Comments' to without textarea
- combine resourplan 'information' and 'account on plan'
- fix/move infomsg for resourceplan
- add squid.conf (missing in previous)

* Fri Nov 29 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013112902.mr
- fix menu (wrong file 'version')

* Fri Nov 29 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013112901.mr
- fix hiawatha config if site access with '?s=a'
- translate certain text messages
- reversedns only able access by admin
- delete certain useless files
- fix/mod port checking
- disable licensecheck
- menu appear tree 'style' when admin/reseller access their customer

* Sat Nov 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013112305.mr
- fix update from panel (just enough running cleanup)
- mod 'ionice' from '-c3' (idle) to '-c2' (best-effort)

* Sat Nov 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013112304.mr
- mod hiawatha log format to extended (the same as apache log format)
- fix getContent in ffilelib.php
- better appear list in weblastvisit
- fix toggleVisibilityByClass in lxa.js
- fix branch list functions
- mod to not appear 'Consumed Login' when select 'Login As'
- fix/mod menu and buttons
- fix naming js function (to toggleVisibilityById)
- add 'click here' for 'help' and 'logout'
- add 'Login As (Cancel)' in menu
- remove 'Home' in 'Backup/Restore' and 'Update' title

* Fri Nov 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013112201.mr
- fix menu link in 'simplicity' skin (to using 'real link')
- fix ownwerahip in filemanager
- add php55u branch
- remove all '__m_message_pre' in add/update form and infomsg appear depend on variable in messagelib.php
- remove commonmessagelib.php because useless
- fix getRpmVersionViaYum
- mod toggleVisibility to make possible display all infomsg in 1 page

* Tue Nov 19 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013111901.mr
- fix related to forcedeletedserver
- run cleanup when click update (that mean update kloxomr)
- better info in 'update home' and fix installed/check-update rpm
- using text instead image for 'mail disk usage'
- add domain from commandline no need 'domain owned' approve

* Mon Nov 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013111801.mr
- fix too small font in certain pages
- make more space in drop menu
- set index.php in menu file only able access by display.php
- fix menu in 'simplicity' skin

* Sat Nov 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013111601.mr
- menu in 'simplicity' skin ready to multi-languages
- fix/mod many aspects related to better appearance

* Tue Nov 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013111202.mr
- set 'simplicity' tab slight bigger
- 'password' and 'server roles' tab always appear in 'server'
- change 'symbol' char to char number < 256 (make compatible for pc without unicode font)
- set 'block title' to centered (simple solution for weird certain pages like 'server roles' page)
- merge/reorganize buttons 'groups' (example: merge 'domain' and 'domain adm'/'administer' to 'domain')
- remove 'postmaster@...' from mailaccount in title because always postmaster from first domain
- change 'config' to 'configure' and 'config ...' to '... configure' in title

* Sun Nov 10 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013111002.mr
- fix appearance php warning
- set isDefaultSkin() to 'simplicity'
- fix 'select folder' in 'ftp user'
- fix 'custombutton'
- fix set_login_skin_to_feather()
- remove unwanted files
- after running upcp always restart-all
- fix/mod install process (no need 'yes' answer
- auto restart-all) 
- 

* Sat Nov 9 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013110902.mr
- add 'reverse-font' (metro-like) for 'button type' of 'appearence'
- fix apache issue when enable secondary php

* Fri Nov 8 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013110802.mr
- set 3 options for 'show directions'
- back to use addondomainlib.php (combine list + add parked + add redirect still not work)
- mod 'vertical 2' and set higher width and height for buttons show (need because set bigger font)
- install already set /tmp to permissions 1777
- also check already hosted when add domain
- fix/mod web server config (permalink)
- fix error 500 issue in apache (not able set 'cgi.rfc2616_headers = 1' in php.ini)
- fix/mod add domain (add 'domain owner' option)
- set to hidden of 'infomsg' in 'feather' skin (also appear if mouseover to 'help' button)
- add 'button type' in appearance (button using font or image)
- fix display where height problem in content when using div-div and change to div-table

* Tue Nov 5 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013110502.mr
- fix wrong style.css
- set font-size to bigger (9pt instead 8pt)
- change 'PHPMyAdmin' to 'SQL Manager' (prepare to using sqlite format for database)
- add dragdivscroll.js (horizontal mouse scrolling for buttons)
- remove graph column (trouble with bigger font; unnecessary)

* Mon Nov 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013110404.mr
- fix space between part of content
- forgot submit for 'show direction' 

* Mon Nov 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013110402.mr
- fix/mod display
- add 'show direction' for appear where skin able select for 'buttons' direction
 
* Sun Nov 3 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013110302.mr
- horizontal buttons flow instead vertical in 'simplicity' skin
- enable/disable compressing in php.ini
- to make sure, also install traceroute and util-linux (ionice)

* Sat Nov 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013110202.mr
- fix infomsg issue in 'webserver config'
- make more bigger font size 
- fix updateform in appearancelib.php
- add desc_addondomain_l declare (to prevent no object warning)
- fix many issue related to theme
- set drop menu to 'centered', fix width drop menu to 500px
- fix menu for resolution 1024
- add/mode background images
- fix background selected
- add brightness color function (use in the future)
- 'feather' skin still use icon images but 'simplicity' use symbol chars
- set smaller box in 'simplicity' skin
- embeded menu instead div caller
- delete gray version of background images
- no separate breadcomb with tab and content
- no need execute 'lxLoadBody()' js in 'simplicity' skin

* Wed Oct 30 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013103005.mr
- change path from $os.inc to rhel.inc
- fix path for webcache driver
- change 'Domain Adm' to 'Administer' text
- change certain image icon to char font
- fix resourceclass width table
- fix infomsg issue in 'webserver config'
- make more bigger font size

* Wed Oct 30 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013103003.mr
- remove 'add form' in each 'all' list
- fix background logic 
- better confirm page (with background color)

* Wed Oct 30 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013103001.mr
- fix path for drivers which move at previous
- res and naming adjustment for background

* Tue Oct 29 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102903.mr
- disable installapp update in scavenge
- move files related to driver
- fix sitepreview

* Mon Oct 28 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102802.mr
- fix dns config (wrong code submit)
- fix fixdns and fixweb 

* Mon Oct 28 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102801.mr
- just fix html, css and js code for display
- add 'fs.aio-max-nr' and increase 'fs.file-max' value in install process
- make shadow effect for certain part

* Sat Oct 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102601.mr
- try other dropdown menu (like it)
- remove unwanted files
- fix some 'bad' display

* Fri Oct 25 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102502.mr
- move and rename header, bottom and lpanel.php to frame_ prefix and move to theme dir
- move functions related to lpanel from htmllib.php to frame_lpanel.php
- remove unwanted files/dirs
- add missing lst files
- fix packer process 

* Thu Oct 24 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102402.mr
- restructure image/button/icon dirs
- remove unwanted files/functions
- fix nsd issue when select without domain exist
- mod os_create_default_slave_driver_db()
- fix mailaccount display
- remove content of login dir

* Tue Oct 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102203.mr
- resubmit install script because wrong 'version'
- automatically change to 'simplicity' when still using 'default' skin
- 'simplicity' as default with background image
- fix password dialog for login with 'default' password (like 'admin')
- change (add/remove) background images

* Tue Oct 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102201.mr
- remove 'default' skin but add color to feather
- move certain functions from lib.php to htmllib.php
- change default color from 'b1c0f0' to 'EFE8E0'
- restructure skin dirs
- reduce background image with to 1600 px

* Mon Oct 21 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102103.mr
- disable web and dns installed by default
- mod setup.sh/installer.sh to handle 3x running installer.php when kloxo database fail to created

* Mon Oct 21 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102102.mr
- fix skeleton.zip (previous with un-transparent logo)
- fix to make infomsg to center in feather/default skin
- move 'show/hide' button from tab to header
- fix js script for show/hide toggle

* Mon Oct 21 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013102101.mr
- 'simplicity' near final
- adjustment for 'default' and 'feather' skin
- convert some table-base to div-base html codes (not final work)
- add base extjs script (importance for frame-based skin)

* Sat Oct 19 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013101901.mr
- move all files in panel dir to theme dir amd adjustment link
- 'message inbox' as 'help' in simplicity psnel
- delete fckeditor _samples
- 'simplicity' skin able change background
- prepare for re-write display code

* Thu Oct 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013101703.mr
- fix for simplicity panel (no need frame and no thick/thin skin) 
- fix default slavedb driver

* Thu Oct 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013101701.mr
- restructure panel dirs
- introduce simplicity panel (based on thin feather but with css menu)
- remove unwanted files (related to panel display)
- use simplicity as 'default' panel

* Tue Oct 15 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013101501.mr
- select simple skin automatically redirect to display.php (no need frame-base again)
- fix issue in 'default' skin
- fix many bugs in interface

* Sat Oct 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013101203.mr
- rename all .phps to .php
- move htmllib to panel dir
- integrate extjs, yui-dropdown and fckeditor without source, example and docs files
- disable install kloxomr-addon 

* Sat Oct 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013101201.mr
- fix tmpfs detect logic
- fix program appear in 'switch programs'
- add cache grace in varnish
- mod comment in hiawatha config
- add squid driver
- add message for hiawatha microcache
- restructuring files for drivers and lib categories (prepare for easy add driver)
- most link in panel already 'right-click' to open (one step to new theme)
- remove unused files

* Tue Oct 8 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013100801.mr
- fix sysinfo to adopt hiawatha info
- fix hiawatha config for reverse-proxy
- disable 'microcache' in lighttpd because no different
- fix/optimize lighttpd.conf settting
- also enable 'microcache' nginx-proxy
- change remap.config setting for trafficserver
- set 'default value' for web/webcache/dns/spam driver because add 'none' driver
- fix web config for sure using 'php-fpm_event' as 'default' phptype
- warning in installer when '/tmp' set as 'tmpfs' (trouble with backup/restore)
- set max ip connection to 25 (like nginx config)
- use 'boosted' config for varnish
- prepare for squid web cache

* Fri Oct 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013100403.mr
- use trafficserver 4 config for version 3 and 4 because running well
- fix webmail logic
- introduce 'none' driver for web, dns and spam (as the same as webcache model)

* Thu Oct 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013100302.mr
- back to add .db_schema which importance for panel display
- all web server include 'generic' permalink
- change user as 'ats' instead 'root' for trafficserver
- enable 'debug' for trafficserver
- no include php imagick for install
- fix copy config for 'nsd' dns server
- restart qmail with 'stop
- sleep 2 start' instead 'restart'
- add missing file (db_schema)

* Wed Oct 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013100204.mr
- fix httpd template if web cache enable
- fix web cache for 'none'
- fix 'userdir' logic in template of httpd 
- fix dns and weh config
- change ats to root for minimize permissions issue for trafficserver
- remove 'debug' file
- fix 'default' web server in installing process
- fix 'default' configs copy for webcache server

* Mon Sep 30 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013093003.mr
- fix varnish init and copy config
- mod mysql-convert.php 

* Mon Sep 30 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013093001.mr
- ready for testing varnish cache server
- add new 'class' as 'webcache'
- make simple 'removeOtherDrivers' function
- delete old config when switch web/dns to
- remove unused files
- restart qmail using 'restart' instead 'stop' and 'start'

* Sat Sep 28 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013092802.mr
- hiawatha already work for redirect 
- set enable gzip and fix urltoolkit setting for hiawatha
- using 'qmailcrl restart' instead 'qmailctl stop qmailctl start'
- make simple logic for webmail in web config
- fix webmail config (thanks for hiawatha with their strict path)
- change 'insert into' to 'insert ignore into' for sql to guarantee latest data 
- remove 'old style' sql data and function 

* Thu Sep 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013092606.mr
- change 'please contact'
- mod to web config only need init.conf (ssl, default and cp) and each domain config
- fix 'text record' for pdns (thanks SpaceDust)
- change apache ip to 127.0.0.1 in proxy 'mode'
- cleanup also remove /home/<webdrive>/conf/webmails
- fix dns uninstall
- use qmailctl instead service for stop/start qmail
- fix 'defaults' dir content remove
- remove unused function in web__lib.php and fix related to it
- fix lighttpd for running with 'new' config model

* Tue Sep 24 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013092403.mr
- better changedriver message
- disable qmail restart inside tmpupdatecleanup.php
- disable robots to cp, disable, default and webmail dirs
- ready testing for hiawatha and hiawatha-proxy (still unfinish work)
- reformat dns config tpl
- fix webmail and cp for hiawatha (move from 'generic' to each 'domain'config)
- emulate index files and permalink in urltoolkit for hiawatha

* Mon Sep 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013092302.mr
- add for 'lost' replace_between function
- change to better dnsnotify.pl and mod dnsnotify
- mod dnsnotify.pl for detail info
- add replace for maradns
- add backend-bind for pdns
- add error log for php.ini.tpl
- use faatcgi+php-fpm instead ruid2 as default httpd in install process

* Sun Sep 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013092202.mr
- optimize config and process ('reload/restart' process) for dns
- fix restart-all (have a problem when php-fpm restart before web server restart)
- mod pdns.sql
- fix wrong djbdns tpl
- fix maradns tpl (but change to ip4_bind_address script still not ready)
- maradns.init include change default 'ip4_bind_address' to hostname ip
- add 'notify=yes' in bind
- mod to small dns config because using 'origin' based
- fix action login in update dns config process
- remove 'srv record' in djbdns
- mod mararc for accept modified for xfr and zone list
- fix issue in dns switch (need stop server before unistall; found issue in maradns)
- back to use read db instead call var for__var_mmaillist in web__lib.php
- fix missing parameter in createListNlist
- add list.transfered.conf.tpl for maradns
- fix list.master.conf.tpl in maradns
- fix uninstall dns (wrong var)
- add 'dnsnotify' in maradns and djbdns with external script
- add supermasters process in pdns
- mod README.md

* Thu Sep 19 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013091903.mr
- fix nsd (add dns_nsdlib.php and disable include for slave conf)

* Thu Sep 19 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013091902.mr
- add double quote for 'txt record' of pdns
- fix issue fail install pdns-backend-mysql after install pdns
- mod pdns.sql for optimize to innodb
- maradns ready
- add and use setRpmRemovedViaYum for dns drivers
- disable process xfr on maradns
- fix maradns domain config
- try to use '0.0.0.0' for maradns ip bind
- prepare for NSD dns server
- convert all 'cname record' to 'a record' in dns server config
- mod watchdog list
- add 'nsd' in 'reserved', 'dns' and 'driver' list
- set for 'nsd' dns server
- fix latest nginx (cache dir)
- still using '0.0.0.0' for 'nsd' notify/provide-xfr 

* Tue Sep 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013091704.mr
- add convert to utf8 charset for mysql-convert
- automatically add 'SPF record' beside 'A record' for 'SPF'
- fix pdns for addon-domain
- fix warning when spam switch

* Tue Sep 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013091702.mr
- fix detect primary ip for hostname
- disable dnssec for powerdns because still not work
- add 'create database' in pdns.sql
- install pdns also install pdns-backend-mysql
- fix calling from powerdns to pdns

* Mon Sep 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1.a-2013091603.mr
- move fix/mod '/etc/hosts' from setup.ah/installer.sh to lib.php
- remove fixmail-all in tmpupdatecleanup.php (because duplicate)
- create powerdns database ready if switch to powerdns or running cleanup
- fix hiawatha process in cleanup
- change name driver from 'powerdns' to 'pdns'
- fix ugly button and other not 'standard' html tag in 'default' theme
- fix isPhpModuleInstalled() var
- include new features (no exists in 6.5.0)

* Thu Sep 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013091202.mr
- add option server/client/domain in fixdomainkey
- fix installer process (conflict between mysql from centalt and ius)
- fix php-fpm tpl for deprecated commenting
- fix html code for display/theme

* Wed Sep 11 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013091101.mr
- change procedural to object style of MySQLi API
- fix link in langfunctionlib.php

* Mon Sep 9 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090904.mr
- fix some display/theme
- add testing for reset-mysql-root-password
- fix insert 'universal' hostname
- install mariadb if exist instead mysql55
- fix installer (because php52s must install after mysql55 and php53u)
- fix getRpmVersion()

* Mon Sep 9 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090903.mr
- fix some bug on installer.php
- change install mysql55 instead mysql (from centos) because have trouble with MySQLi API in 5.0.x
- fix for php52s (add install net-snmp)
- adjutment installer.sh to match with setup.sh

* Mon Sep 9 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090901.mr
- change 'Kloxo' title to 'Kloxo-MR'
- beside 'fs.file-max' also add others (like 'vm.swappiness') to optimize
- instead warning for 'hostname', add 'universal' hostname to '/etc/hosts' in install process

* Sun Sep 8 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090801.mr
- mod service list
- mod reset-mysql-root-password
- remove 'javascript:' except for 'href'
- fix select all for client list
- add another var to sysctl.conf (for minimize buffers and cached memory)

* Sat Sep 7 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090704.mr
- fix install process (especially in centos 5)
- fix qmail-toaster initial
- fix/better update process
- chkconfig off for php-fpm when install (because using ruid2 as 'default' php-type)

* Sat Sep 7 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090702.mr
- fix identify hostname (use 'hostname' instead 'hostname -f')
- remove unused code
- fix updatelib.php for install process
- fix for ruid2 (need php.conf) for 'default' php-type

* Sat Sep 7 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090701.mr
- move hostname checking from installer.php to setup.sh/installer.sh

* Fri Sep 6 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090607.mr
- add function for checking hostname and stop install process if not qualified
- remove libmhash to checking
- no need check old.program.pem
- fix/better lxphp.exe checking when running upcp
- add '-y' to force to 'reinstall'
- fix setup.sh/installer.sh/upcp script for install process

* Fri Sep 6 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090603.mr
- add parse_ini.inc (prepare for kloxo config in ini format)
- fix 'default' default.conf
- mod fixdomainkey execute dns subaction for domain instead full_update
- change listen ip-port to socket in php-fpm.conf (for php 5.2)
- fix upcp script for fresh install 
- fix installer.php for 'default' web using ruid2 (need enable php.conf) 

* Tue Sep 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090302.mr
- make install setup (run 'sh /script/upcp' instead '/usr/local/lxlabs/kloxo/install'
- fix mysqli_query for webmail database
- better reset-mysql-root password and mysql-convert code

* Mon Sep 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090302.mr
- testing for 6.5.1.a
- convert mysql to mysqli API in Kloxo-MR code
- fix display/theme
- add/mod hash/bucket because nginx not started in certain conditions
- change lxphp to php52s in desclib.php

* Mon Sep 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013090201.mr
- fix display/theme (restore no domain list; wrong button title)
- add/mod hash/bucket for nginx.conf (nginx not start in certain conditions)
- add changelog content of first release 6.5.0.f

* Tue Aug 27 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013082704.mr
- taken code from 6.5.1.a (but maradns and hiawatha still disable)
- convert cname to a record for djbdns (because cname work work)
- fix error/warning for debug panel
- fix htmllib
- fix hiawatha service not execute after cleanup
- fix old link to /script
- fix web drivers list
- add hiawatha, maradns and powerdns in update services in cleanup

* Mon Aug 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013082602.mr
- fix html tags especially for deprecated tag like <font>

* Mon Aug 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013082601.mr
- make fixdns faster (synchronize and allowed_transfer change to per-client)
- add 'accept-charset="utf-8"' for <form>

* Sat Aug 24 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013082401.mr
- fix panel port (back to 7778/7777 from 37778/37777)

* Fri Aug 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013082302.mr
- fix clientmail.php (missing ';')

* Thu Aug 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013082301.mr
- set root:root to installatron symlink
- add graph for load average
- move files inside script to pscript
- fix readsmtpLog for read smtp.log to maillog
- fix mail forward with disable detect mail account
- get client list from db directly instead from client object

* Thu Aug 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013082201.mr
- fix dns config issue (update config not work)
- mod/change fix-all (include fixftpuser instead fixftp)
- add process for delete /etc/pure-ftpd/pureftpd.passwd.tmp (unfinish loop for cleanup)

* Wed Aug 21 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013082102.mr
- fix dns config (make faster and no memory leak if running fixdns/cleanup)
- fix installatron-install script

* Tue Aug 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013082002.mr
- fix mysql-to-mariadb bug
- better getRpmVersion
- use lib.php from dev but disable mariadb/powerdns/hiawatha initial
- mod suphp configs
- better apache tpl
- better getRpmVersionViaYum function

* Sun Aug 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013081801.mr
- php*-gd, -bcmath and -pgsql also detect when running cleanup
- all languages including in core (still compile separately)

* Sat Aug 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013081701.mr
- fix/add packages listing on 'services' and 'component list'
- make cp address as additional panel

* Fri Aug 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013081601.mr
- fix detect ftp for lxguard (because think as using syslog but possible using rsyslog)
- fix restart scripts (because old script not work for other then english
- add php*-gd and php*-pdo (because repo not make as 'default') as default ext
- add config for microcache for nginx

* Wed Aug 14 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013081402.mr
- update customize fastcgi_param for ngix
- add init file checking for dns initial
- no convert cname to a record for local domain
- fix remove lxphp.exe for lxphp (because change to php52s)

* Tue Aug 13 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013081304.mr
- fix error 500 on kloxo-hiawatha (back to use TimeForCGI)

* Tue Aug 13 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013081303.mr
- fix upload issue (increasing MaxRequestSize TimeForRequest and MaxKeepAlive)
- fix/mod restart scripts

* Mon Aug 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013081208.mr
- add allowed-transfer script for dns server (make possible dns server as 'master')
- fix some minor bugs for dns template
- fix some minor bugs for install process
- mod/add restart/clearcache script

* Tue Aug 7 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013080701.mr
- fix bind dns config (bind work now like djbsns)

* Tue Aug 6 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013080605.mr
- simple execute for djbdns list.master.conf.tpl
- fix 'make' execute for axfrdns of djbdns
- fix no conf directory issues when using djbdns (cleanup will be create this dirs)
- fix bind domains.conf.tpl (problem with ns declare)
- add 'make' install when install kloxo (djbdns need it)
- add 'sock' dir for php-fpm socket when running cleanup

* Tue Aug 6 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013080602.mr
- fix dns config especially 'server alias' issue
- switch to djbns also execute djbdns 'setup'

* Tue Aug 6 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013080601.mr
- bugfix for dns config (wrong ns and cname)
- bugfix for access panel via https/7777
- mod sysctl.conf when running cleanup

* Mon Aug 5 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013080502.mr
- based on until 6.5.1.a-2013080502
- change timestamp from 20130318xx to real timestamp release
- change lxphp + lxlighttpd to php52s + hiawatha (the first cp using it!)
- template-based for dns server (bind and djbdns)
- bugfix for add ip
- remove unwanted files (related to os detect/specific)
- because using hiawatha, socket error already fixed (related to php-cli wrapper)
- using closeinput instead closeallinput (no different effect found)
- remove unwanted skin images
- change /restart or /backendrestart to /load-wrapper (related to socket error issue)
- change helpurl from forum.lxcenter.org to forum.mratwork.com
- exclude bind from centalt because something trouble when using it
- add error page for panel
- remove lxphp-module-install and change to php5Xs-extension-install
- add/change set-secondary-php script

* Thu Jul 11 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031828.mr
- based on until 6.5.1.a-2013071102
- disable mysql51 and mysql55 from ius (make conflict)
- improve mysql-convert and mysql-optimize
- modified kloxo-mr.repo
- make setup process until 3x if kloxo database not created (normally enough 1-2x)

* Wed Jul 10 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031827.mr
- based on until 6.5.1.a-2013071001
- disable mysql from ius repo (make conflict) when install process
- change kloxo-mr.repo related to disable mysql from ius
- mysql-convert script will convert all database for storage-engine target
- move certain parameter of nginx from 'location /' to 'server'
- disable 'php_admin_value[memory_limit]' on php-fpm template
- restart will be execute start if not running for qmail service
- rename custom qmail run/log run of qmail-toaster
- increase value of TopCountries and others for webalizer
- fix web config, expecially for add/delete domain.

* Thu Jun 27 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031826.mr
- based on until 6.5.1.a-2013062801
- fix install process (need running setup.sh 2x in certain condition)
- fix wrong message for afterlogic when running cleanup/fixwebmail/fixmail-all
- back to use 'wget' instead 'wget -r' in how-to-install
- disable mirror for repo and just using for emergency

* Thu Jun 27 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031825.mr
- based on until 6.5.1.a-2013062701
- remove double install process for mysql and httpd
- fix conflict of mysql install
- set php53u and mysql51/mysql55 as default install
- fix telaen config copy
- fix webmail detect

* Wed Jun 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031824.mr
- based on until 6.5.1.a-2013062602
- fix restore message
- prepare for qmail-toaster custom-based run/log run

* Thu Jun 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031823.mr
- based on until 6.5.1.a-2013062301
- restart kloxo if found 'server 7779' not connected
- move maillog from /var/log/kloxo to /var/log
- remove smtp.log and courier.log
- dual log (multilog and splogger) for qmail-toaster
- remove unwanted files (espacially related to qmail-toaster)
- bug fix for reset-mysql-root-password script
- change to apache:apache for dirprotect dir
- fix segfault when install
- change kloxo sql without engine=myisam

* Sun Jun 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031822.mr
- fix clearcache script
- remove certain qmail config fix (becuase logic and code move to rpm)

* Sat Jun 15 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031821.mr
- based on until 6.5.1.a-2013061501
- back to disable mariadb from centalt (still have a problem install Kloxo-MR on centos 6 32bit)
- fix diprotect path for apache
- not need softlimit change (already set inside qmail-toaster)
- fix clearcache script for openvz host
- fix function.sh and lxphpcli.sh (add exec)
- back to use restart function instead stop and start for restart

* Tue Jun 11 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031820.mr
- based on until 6.5.1.a-2013061101
- install without asking 'master/slave' (always as 'master'; run make-slave for change to slave)
- more info backup/restore
- mod smtp-ssl_run for rblsmtpd/blacklist
- remove double process for softlimit change
- fix issue when install on openvz host
- enable gateway when add ip
- modified nginx config for dualstack ip (ipv4+ipv6)

* Tue Jun 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031819.mr
- based on until 6.5.1.a-2013060402
- fix fixmail-all ('cp' weird behaviour for copy dir)
- add info in sysinfo

* Mon Jun 3 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031818.mr
- based on until 6.5.1.a-2013060301
- fix web config for www-redirect and wildcards
- create mail account automatically create subscribe folders
- fix smtp issue
- possible customize qmail run script

* Fri May 31 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031817.mr
- fix restart-services
- fix userlist with exist checking
- fix mail config (smtp and submission already work!)
- remove for exlude mariadb from centalt repo
- based on until 6.5.1.a-2013053102

* Sun May 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031816.mr
- fix qmail init
- based on until 6.5.1.a-2013052101

* Sun May 19 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031815.mr
- fix kloxo database path
- based on until 6.5.1.a-2013051901

* Sat May 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031814.mr
- fix install process and reset password from ssh
- fix wildcards for website
- based on until 6.5.1.a-2013051804

* Thu May 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031813.mr
- fix sh permission to 755
- fix www redirect
- make simple awstats link
- add mariadb in mysql branch
- disable mariadb from centalt repo (conflict when install)
- based on 6.5.1.a-2013050502 and 6.5.1.a-2013051601

* Sun May 5 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031812.mr
- update suphp config (fix for possible security issue) and remove delete spamassassin dirs
- based on 6.5.1.a-2013050501 and 6.5.1.a-2013050502

* Fri Apr 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031811.mr
- fix packer.sh (remove lang except en-us)
- use ionice for du
- based on 6.5.1.a-2013042601 and 6.5.1.a-2013042602

* Sun Apr 21 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031810.mr
- fix some script based-on 6.5.1.a-2013042001 and 6.5.1.a-2013042101

* Mon Apr 8 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031809.mr
- fix some script based-on 6.5.1.a-2013040801

* Sat Mar 30 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031808.mr
- fix install issue on openvz

* Wed Mar 27 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031807.mr
- fix traffic issue and installer.sh/installer.php
- add some scripts

* Mon Mar 25 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031806.mr
- no need cleanup on installer/setup also change mysqli to mysql on reset password

* Mon Mar 25 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031805.mr
- no need running full installer.sh twice just function step2 if running setup.sh

* Mon Mar 25 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031804.mr
- fix bugs relate to install/setup

* Sat Mar 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031803.mr
- remove php modules (except php-pear) because conflict between centos and other repos

* Sat Mar 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031802.mr
- fix critical bug (don't install php-mysqli on install/setup process)

* Mon Mar 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.0.f-2013031801.mr
- first release of Kloxo-MR
- FIX - Security bug (possible sql-injection on login and switch 'safe' and 'unsafe' mode)
- FIX - Backup and restore (no worry about 'could_not_zip' and 'could_not_unzip')
- FIX - No password prompt when install spamdyke
- FIX - Add missing fetchmail when install
- FEATURE - Add Nginx, Nginx-proxy and Lighttpd-proxy
- FEATURE - Possible using different 'Php Branch' (for Php version 5.2, 5.3 and 5.4)
- FEATURE - Possible enable/disable 'Secondary Php' (using lxphp and suphp)
- FEATURE - More 'Php-type' (mod_php, suphp, fcgid and php-fpm) with different apache mpm
- FEATURE - Template-based web, php and php-fpm configs (use 'inline-php') and possible to customize
- FEATURE - Reverse DNS always appear
- FEATURE - Add select 'Ssl Key Bits' (2048, 1024 and 512) for 'Add Ssl Certificate'
- FEATURE - More logs on 'Log Manager'
- FEATURE - Enable logrotate
- FEATURE - Support for Centos 5 and 6 on 32bit or 64bit
- FEATURE - Possible install on Yum-based Linux OS (Fedora, ScientificLinux, CloudLinux and etc)
- FEATURE - Based-on multiple repo (Kloxo-MR owned, CentAlt, IUS, Epel and etc)
- FEATURE - Support different 'Mysql Branch' and MariaDB
- FEATURE - Add 'sysinfo' script to support purpose
- FEATURE - Add 'lxphp-module-install' script for installing module for lxphp
- FEATURE - Add and modified some scripts (convert-to-qmailtoaster, fix-qmail-assign, fixvpop and fixmail) for mail services
- FEATURE - Faster and better change mysql root password
- FEATURE - Add new webmail (afterlogic Webmail lite, T-Dah and Squirrelmail)
- FEATURE - Automatic add webmail when directory create inside /home/kloxo/httpd/webmail
- FEATURE - Change components to rpm format (addon, webmail, phpmyadmin and etc)
- FEATURE - Possible access FTP via ssl port
- FEATURE - Automatic install RKHunter and add log to 'Log Manager'
- CHANGE - Use qmail-toaster instead qmail-lxcenter (with script for convert)
- CHANGE - New interface for login and 'defaults' pages
- CHANGE - Use Kloxo-MR logo instead Kloxo logo
- CHANGE - Remove xcache, zend, ioncube and output compressed from 'Php Configs'
- CHANGE - Use php-fpm instead fastcgi or spawn-cgi for Lighttpd
- CHANGE - Use 'en-us' instead 'en' type for language
- CHANGE - Remove unwanted files and or code for windows os target
- CHANGE - Use '*' (wildcard) instead 'real' ip for web config and then no issue related to 'ip not found'
- CHANGE - Use 'apache:apache' instead 'lxlabs:lxlabs' ownership for '/home/kloxo/httpd' ('defaults' page')
- CHANGE - Use local data for 'Release Note' instead download
- CHANGE - Use tar.gz instead zip for compressing Kloxo-MR
- PATCH - bug fix for installer.sh (installer.sh for 'dev' step and yum install/update + setup.sh for final step)
- PATCH - remove php modules (except php-pear) because conflict between centos with other repos
