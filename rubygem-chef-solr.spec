# Generated from chef-solr-0.10.0.rc.1.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname chef-solr
#%define prerelease 
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}%{?prerelease}

Summary: Search indexing for Chef
Name: rubygem-%{gemname}
Version: 10.14.2
Release: 1%{?buildstamp}%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://wiki.opscode.com/display/chef
Source0: http://rubygems.org/downloads/%{gemname}-%{version}%{?prerelease}.gem
Source1: chef-solr.init
Source2: chef-solr.sysconfig
Source3: chef-solr.logrotate
Source4: config.rb

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: rubygems
Requires: rubygem(chef) = %{version}%{?prerelease}
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}%{?prerelease}

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts

%description
Search indexing for Chef

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/var/log/chef
mkdir -p %{buildroot}%{_sysconfdir}/chef
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/var/run/chef
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d

gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

cp %{SOURCE1} %{buildroot}/etc/rc.d/init.d/chef-solr
chmod +x %{buildroot}/etc/rc.d/init.d/chef-solr
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/chef-solr
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/chef-solr
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/chef/solr.rb

%clean
rm -rf %{buildroot}

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add chef-solr

if [ -z "`/usr/bin/id chef 2> /dev/null`" ]; then
	%{_sbindir}/adduser chef >/dev/null 2>&1 
	chown -R chef %{_sysconfdir}/chef
fi

# Run chef-solr-installer for the first time
if ! [ -d /var/chef/solr/data ]; then
	chef-solr-installer > /dev/null 2>&1
fi

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service chef-solr >/dev/null 2>&1
    /sbin/chkconfig --del chef-solr
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service chef-solr restart >/dev/null 2>&1 || :
fi

%files
%defattr(-, root, root, -)
%{_bindir}/chef-solr
%{_bindir}/chef-solr-installer
%{gemdir}/gems/%{gemname}-%{version}%{?prerelease}/
%doc %{gemdir}/doc/%{gemname}-%{version}%{?prerelease}
%{gemdir}/cache/%{gemname}-%{version}%{?prerelease}.gem
%{gemdir}/specifications/%{gemname}-%{version}%{?prerelease}.gemspec
%config(noreplace) %{_sysconfdir}/sysconfig/chef-solr
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-solr
%config(noreplace) %{_sysconfdir}/chef/solr.rb
%{_sysconfdir}/rc.d/init.d/chef-solr


%changelog
* Tue Sep 11 2012 Sean P. Kane <spkane00@gmail.com> - 10.14.2-1
- bumped version 10.14.2

* Mon Sep 10 2012 Sergio Rubio <rubiojr@frameos.org> - 10.14.0-1
- bumped version 10.14.0

* Wed Aug 31 2012 Sean P. Kane <spkane00@gmail.com> - 10.12.0-1
- bumped version 10.12.0

* Wed Dec 14 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.6-1
- bumped version 0.10.6

* Wed Jul 27 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.4-1
- preparing for 0.10.4

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-4
- updated release version format

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-3
- added buildstamp to release

* Mon Jul 04 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-2
- depend on 0.10.2 chef gems

* Mon Jul 04 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-1
- upstream update

* Fri May 06 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-2
- solr data now stored in /var/chef

* Tue May 03 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-1
- upstream update

* Mon May 02 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.2-1
- upstream update

* Fri Apr 29 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-2
- add init script
- create default dirs
- add logrotate and solr.rb configs
- create chef user

* Thu Apr 28 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-1
- Initial package
