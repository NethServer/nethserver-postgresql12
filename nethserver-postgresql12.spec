Summary: NethServer PostgresSQL 12.0 configuration
Name: nethserver-postgresql12
Version: 1.0.0
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name} 
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

Requires: rh-postgresql12
Requires: nethserver-base

BuildRequires: nethserver-devtools 

%description
NethServer PostgresSQL 12.0 configuration

%prep
%setup

%build
perl createlinks

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-filelist

%post

%preun

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update

%changelog
* Wed Sep 16 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.0-1
- Mattermost 5.26.2 - NethServer/dev#6263
