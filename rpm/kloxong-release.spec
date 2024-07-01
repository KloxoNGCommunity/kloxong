%define repohost repo.kloxong.org
%define mirrorhost raw.githubusercontent.com/KloxoNGCommunity/KloxoNG-rpms/dev/kloxong/mirror
Summary: KloxoNG release file and package configuration
Name: kloxong-release
Version: 0.1.1
Release: 14
License: AGPLV3
Group: System Environment/Base
URL: http://kloxong.org/

BuildArch: noarch
Packager: John Parnell Pierce <john@luckytanuki.com>
Vendor: Kloxo Next Generation Repository, http://%{repohost}/
#BuildRequires: redhat-rpm-config
Obsoletes: mratwork-release > 0 , mratwork-testing > 0

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
# switch to add and exclude repos for EL8
%global with_pre8_repos  0
%else
%global with_pre8_repos  1
%endif



%description
Kloxo Next Generation rpm release. This package contains yum configuration for the Kloxo Next Generation RPM Repository.

%prep

%build

cat > kloxong.repo << _EOF_
[kloxong-copr]
name=kloxong master Copr repo 
baseurl=https://copr-be.cloud.fedoraproject.org/results/kloxong/kloxong/epel-\$releasever-\$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/kloxong/kloxong/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1

[kloxong-copr-httpd24]
name=kloxong httpd24 Copr repo 
baseurl=https://copr-be.cloud.fedoraproject.org/results/kloxong/httpd24/epel-\$releasever-\$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/kloxong/httpd24/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1

[kloxong-copr-curl]
name=kloxong curl repo 
baseurl=https://copr-be.cloud.fedoraproject.org/results/kloxong/Curl/epel-\$releasever-\$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/kloxong/Curl/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1


[kloxong-release-version-arch]
name=KloxoNG - release-version-arch
baseurl=https://%{repohost}/kloxong/release/centos\$releasever/\$basearch/
mirrorlist=https://%{mirrorhost}/kloxong-release-centos\$releasever-\$basearch-mirrors.txt
skip_if_unavailable=True
enabled=0
gpgcheck=0

[kloxong-srpms]
name=KloxoNG - srpms
baseurl=https://%{repohost}/kloxong/SRPMS/
#mirrorlist=https://%{mirrorhost}/kloxong-SRPMS-mirrors.txt
skip_if_unavailable=True
enabled=0
gpgcheck=0

# ==================================

[kloxong-remi]
name=KloxoNG - Les RPM de remi pour Enterprise Linux $releasever
#baseurl=http://rpms.famillecollet.com/enterprise/\$releasever/remi/$basearch/
mirrorlist=http://cdn.remirepo.net/enterprise/\$releasever/remi/mirror
gpgcheck=0
enabled=1
#includepkgs=php-ffmpeg php-ioncube-loader
exclude=php5* php7* php80* php-* mysql5* mysql56*  mariadb* postfix32u*



# ==================================

[kloxong-epel]
name=KloxoNG - Extra Packages for EL \$releasever
#baseurl=http://download.fedoraproject.org/pub/epel/\$releasever/\$basearch
mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=epel-\$releasever&arch=\$basearch
enabled=1
gpgcheck=0
exclude=postfix* exim* ssmtp* pdns*

# ==================================

# for hiawatha
[kloxong-centosec]
name=KloxoNG - CentOS \$releasever Packages from CentOS.EC
baseurl=http://centos\$releasever.ecualinux.com/\$basearch
enabled=0
gpgcheck=0
exclude=cairo*

# ==================================

# for nginx
[kloxong-nginx]
name=KloxoNG - nginx repo
baseurl=http://nginx.org/packages/mainline/centos/\$releasever/\$basearch/
enabled=1
gpgcheck=0

# for nginx-stable
[kloxong-nginx-stable]
name=KloxoNG - nginx-stable repo
baseurl=http://nginx.org/packages/centos/\$releasever/\$basearch/
enabled=1
gpgcheck=0

# ==================================

# for mariadb
[kloxong-mariadb]
name=KloxoNG - mariadb repo
#baseurl=http://yum.mariadb.org/10.2/centos/\$releasever/\$basearch/
baseurl=https://archive.mariadb.org/yum/10.2/centos/\$releasever/\$basearch/
#baseurl=https://dlm.mariadb.com/repo/mariadb-server/10.2/yum/centos/\$releasever/\$basearch
enabled=1
gpgcheck=0

# ==================================

# for atrpms
[kloxong-atrpms]
name=KloxoNG - Fedora Core \$releasever - $basearch - ATrpms
baseurl=http://dl.atrpms.net/el\$releasever-\$basearch/atrpms/stable
enabled=0
gpgcheck=0
exclude=clam*

# ==================================

# for litespeed
[kloxong-litespeed]
name=KloxoNG - LiteSpeed Tech Repository for CentOS \$releasever - \$basearch
baseurl=http://rpms.litespeedtech.com/centos/\$releasever/\$basearch/
#failovermethod=priority
enabled=0
gpgcheck=0

[kloxong-litespeed-update]
name=KloxoNG - LiteSpeed Tech Repository for CentOS \$releasever - \$basearch
baseurl=http://rpms.litespeedtech.com/centos/\$releasever/update/\$basearch/
#failovermethod=priority
enabled=0
gpgcheck=0

# ==================================

# for mod-pagespeed
[kloxong-google-mod-pagespeed]
name=KloxoNG - google-mod-pagespeed
baseurl=http://dl.google.com/linux/mod-pagespeed/rpm/stable/\$basearch
enabled=1
gpgcheck=0

# ==================================

# for mod_mono
[kloxong-mod-mono]
name=KloxoNG - mod_mono
baseurl=http://download.mono-project.com/repo/centos/
enabled=0
gpgcheck=0

# ==================================

# for CentOS kernel
[kloxong-centos-kernel]
name=KloxoNG - CentOS kernel
baseurl=http://elrepo.org/linux/kernel/el\$releasever/\$basearch
enabled=0
gpgcheck=0

# ==================================

# for RSysLog
[kloxong-rsyslog-v8-devel]
name=KloxoNG - Adiscon Rsyslog v8-devel for CentOS-\$releasever-\$basearch
baseurl=http://rpms.adiscon.com/v8-devel/epel-\$releasever/\$basearch
enabled=0
gpgcheck=0

[kloxong-rsyslog-v8-stable]
name=KloxoNG - Adiscon Rsyslog v8-stable for CentOS-\$releasever-\$basearch
baseurl=http://rpms.adiscon.com/v8-stable/epel-\$releasever/\$basearch
enabled=0
gpgcheck=0

# ==================================

[kloxong-zfs]
name=KloxoNG - ZFS on Linux for EL \$releasever
baseurl=http://archive.zfsonlinux.org/epel/\$releasever/\$basearch/
enabled=0
gpgcheck=0

# ==================================

[kloxong-gleez]
name=KloxoNG - Gleez repo for CentOS-\$releasever-\$basearch
baseurl=https://yum.gleez.com/\$releasever/\$basearch/
enabled=0
gpgcheck=0
includepkgs=hhvm*

# ==================================

[kloxong-ulyaoth]
name=KloxoNG - Ulyaoth Repository
baseurl=http://repos.ulyaoth.net/centos/\$releasever/\$basearch/os/
enabled=0
gpgcheck=0

# ==================================

[kloxong-rpmforge]
name=KloxoNG - RHEL \$releasever - RPMforge.net - dag
baseurl=http://apt.sw.be/redhat/el\$releasever/en/\$basearch/rpmforge
mirrorlist=http://apt.sw.be/redhat/el\$releasever/en/mirrors-rpmforge
enabled=0
gpgcheck=0

[kloxong-rpmforge-extras]
name=KloxoNG - RHEL \$releasever - RPMforge.net - extras
baseurl=http://apt.sw.be/redhat/el\$releasever/en/\$basearch/extras
mirrorlist=http://apt.sw.be/redhat/el\$releasever/en/mirrors-rpmforge-extras
enabled=0
gpgcheck=0

_EOF_


%if %{with_pre8_repos}
cat >> kloxong.repo << _EOF_
# ==================================

[kloxong-ius]
name=KloxoNG - IUS Community Packages for EL \$releasever
baseurl=https://repo.ius.io/\$releasever/\$basearch
enabled=1
gpgcheck=0
exclude=mysql51* mysql56* mariadb* postfix32u*

[kloxong-ius-archive]
name=KloxoNG - IUS Community Packages for EL \$releasever (archive)
baseurl=https://repo.ius.io/archive/\$releasever/\$basearch
enabled=1
gpgcheck=0
exclude=mysql51* mysql56*  mariadb* postfix32u*

[kloxong-ius-testing]
name=KloxoNG - IUS Community Packages for EL \$releasever (testing)
baseurl=https://repo.ius.io/testing/\$releasever/\$basearch
enabled=0
gpgcheck=0
exclude=mysql51* mysql56*  mariadb* postfix32u*

# ==================================

# for Webtatic
[kloxong-webtatic]
name=KloxoNG - Webtatic for CentOS \$releasever - \$basearch
#baseurl=http://repo.webtatic.com/yum/el\$releasever/\$basearch
mirrorlist=http://mirror.webtatic.com/yum/el\$releasever/\$basearch/mirrorlist
enabled=1
gpgcheck=0
exclude=mysql* nginx* php55* php56* php7*

[kloxong-webtatic-archive]
name=KloxoNG - Webtatic for CentOS \$releasever Archive - \$basearch
#baseurl=http://repo.webtatic.com/yum/el\$releasever-archive/\$basearch
mirrorlist=http://mirror.webtatic.com/yum/el\$releasever-archive/\$basearch/mirrorlist
enabled=1
gpgcheck=0
exclude=mysql* nginx* php55* php56* php7*

[kloxong-webtatic-testing]
name=KloxoNG - Webtatic for CentOS \$releasever Testing - \$basearch
#baseurl=http://repo.webtatic.com/yum/el\$releasever/\$basearch
mirrorlist=http://mirror.webtatic.com/yum/el\$releasever-testing/\$basearch/mirrorlist
enabled=1
gpgcheck=0
exclude=mysql* nginx* php55* php56* php7*

# ==================================

# for varnish
[kloxong-varnish]
name=KloxoNG - Varnish for EL \$releasever
baseurl=https://packagecloud.io/varnishcache/varnish5/el/\$releasever/\$basearch
repo_gpgcheck=1
gpgcheck=0
enabled=1
gpgkey=https://packagecloud.io/varnishcache/varnish5/gpgkey
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300


_EOF_

%endif



%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/yum.repos.d/
install -m 755 kloxong.repo %{buildroot}%{_sysconfdir}/yum.repos.d/kloxong.repo


%{__rm} -rf %{_sysconfdir}/yum.repos.d/kloxo.repo
%{__rm} -rf %{_sysconfdir}/yum.repos.d/KloxoNG.repo
%{__rm} -rf %{_sysconfdir}/yum.repos.d/kloxo-custom.repo
%{__rm} -rf %{_sysconfdir}/yum.repos.d/lxcenter.repo
%{__rm} -rf %{_sysconfdir}/yum.repos.d/lxlabs.repo


%clean

%post

%files
%defattr(-, root, root, 0755)
%dir %{_sysconfdir}/yum.repos.d/
%{_sysconfdir}/yum.repos.d/kloxong.repo

%changelog
* Sun Jun 30 2024 John Parnell Pierce <john@luckytanuki.com>
- Due to install issues with latest Maria 10.5 packages have rolled back to 10.2

* Wed Sep 13 2023 John Parnell Pierce <john@luckytanuki.com> - 0.1.1-10
- go back to MariaDB 10.5

* Thu Sep 7 2023 John Parnell Pierce <john@luckytanuki.com> - 0.1.1-9
- add missing php excludes for webtastic

* Tue Sep 5 2023 John Parnell Pierce <john@luckytanuki.com> - 0.1.1-8
- add excludes for conflicting php versions

* Thu Aug 31 2023  John Parnell Pierce <john@luckytanuki.com> - 0.1.1-7
- Fix typo in remi mirror url

* Thu Aug 31 2023  John Parnell Pierce <john@luckytanuki.com> - 0.1.1-6
- Active remi repo for php 8.1 & 8.2

* Mon May 1 2023  John Parnell Pierce <john@luckytanuki.com> - 0.1.1-5
- Move Kloxong Curl to it own copr repo

* Fri Apr 15 2022  John Parnell Pierce <john@luckytanuki.com> - 0.1.1-4
- Add repo includes/excludes for EL8 builds

* Thu Oct 7 2021  John Parnell Pierce <john@luckytanuki.com> - 0.1.1-3
- Exclude IUS from Centos 8 version 

* Sat Jun 5 2021  John Parnell Pierce <john@luckytanuki.com> - 0.1.1-2
- Exclude postfix32u* as it conflicts with toaster packages 

* Fri Jun 26 2020 John Parnell Pierce <john@luckytanuki.com> 
- updating way testing repo is installed. This file has had yum entry for test repo removed

* Thu Apr 2 2020  John Parnell Pierce <john@luckytanuki.com> - 0.1.1-1
- updated changelog for changes over 12 months
- merge updates from Kloxo-MR
- add kloxong repo to release spec
- clean up spec file
- add gpg key for varnish repo (Thanks DK)
- update test repos
- remove old kloxong neutral and no arch repos

* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- rebrand to Kloxo Next Generation
- change product name to kloxong
- add obsolete for kloxomr 
- change MRatWork to kloxong

* Mon Dec 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 0.0.1-1
- first release
