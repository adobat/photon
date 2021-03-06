Summary:	Apache Tomcat
Name:		apache-tomcat
Version:	7.0.68
Release:	3%{?dist}
License:	Apache
URL:		http://tomcat.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:	http://mirrors.gigenet.com/apache/tomcat/tomcat-7/v7.0.68/bin/%{name}-%{version}.tar.gz
%define sha1 apache-tomcat=3e8481f74968d80cb9cb0b7ca1a0ed40e4a707e7
Requires: openjre >= 1.8.0.45

%define _prefix /var/opt/%{name}-%{version}
%define _bindir %{_prefix}/bin
%define _confdir %{_prefix}/conf
%define _libdir %{_prefix}/lib
%define _webappsdir %{_prefix}/webapps

%description
The Apache Tomcat package contains binaries for the Apache Tomcat servlet container.

%prep

%setup -qn %{name}-%{version}
%build

%install

install -vdm755 %{buildroot}/var/opt/%{name}-%{version}
mv -v %{_builddir}/%{name}-%{version}/* %{buildroot}/var/opt/%{name}-%{version}/
rm -rf %{buildroot}/var/opt/%{name}-%{version}/webapps/examples
rm -rf %{buildroot}/var/opt/%{name}-%{version}/webapps/work
rm -rf %{buildroot}/var/opt/%{name}-%{version}/webapps/temp
rm -rf %{buildroot}/var/opt/%{name}-%{version}/webapps/docs
rm -rf %{buildroot}/var/opt/%{name}-%{version}/temp
rm -f %{buildroot}/var/opt/%{name}-%{version}/RUNNING.txt
rm -f %{buildroot}/var/opt/%{name}-%{version}/RELEASE-NOTES

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_prefix}/LICENSE
%{_prefix}/NOTICE
%{_bindir}/*
%{_confdir}/*
%{_libdir}/*
%{_webappsdir}/*

%changelog
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 7.0.68-1
-   Upgraded to version 7.0.68
*	Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 7.0.63-3
-	Change path to /var/opt.
*	Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 7.0.63-2
-	Updated dependency after repackaging openjdk. 
*	Wed Jul 8 2015 Sriram Nambakam <snambakam@vmware.com> 7.0.63
-	Initial build.	First version
