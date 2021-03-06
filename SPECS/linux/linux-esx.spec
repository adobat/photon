%global security_hardening none
Summary:       Kernel
Name:          linux-esx
Version:       4.2.0
Release:       17%{?dist}
License:       GPLv2
URL:           http://www.kernel.org/
Group:         System Environment/Kernel
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       http://www.kernel.org/pub/linux/kernel/v4.x/linux-4.2.tar.xz
%define sha1 linux=5e65d0dc94298527726fcd7458b6126e60fb2a8a
Source1:       config-esx-%{version}
Patch0:        RDS-race-condition-on-unbound-socket-null-deref.patch
Patch1:        KEYS-Fix-keyring-ref-leak-in-join_session_keyring.patch
Patch2:        ovl-fix-permission-checking-for-setattr.patch
Patch3:        double-tcp_mem-limits.patch
Patch4:         veth-do-not-modify-ip_summed.patch
Patch5:        01-clear-linux.patch
Patch6:        02-pci-probe.patch
Patch7:        03-poweroff.patch
Patch8:        04-quiet-boot.patch
Patch9:        05-pv-ops.patch
BuildRequires: bc 
BuildRequires: kbd
BuildRequires: kmod
BuildRequires: glib-devel
BuildRequires: xerces-c-devel
BuildRequires: xml-security-c-devel
BuildRequires: libdnet
BuildRequires: libmspack
BuildRequires: Linux-PAM
BuildRequires: openssl-devel
BuildRequires: procps-ng-devel
Requires:      filesystem kmod coreutils

%description
The Linux kernel build for GOS for VMware hypervisor.

%package devel
Summary:       Kernel Dev
Group:         System Environment/Kernel
Requires:      python2
Requires:      %{name} = %{version}-%{release}
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:       Kernel docs
Group:         System Environment/Kernel
Requires:      python2
Requires:      %{name} = %{version}-%{release}
%description docs
The Linux package contains the Linux kernel doc files

%prep
%setup -q -n linux-4.2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
make mrproper
cp %{SOURCE1} .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-esx-%{version}
install -vdm 755 %{buildroot}/etc/modprobe.d
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}
make INSTALL_MOD_PATH=%{buildroot} modules_install
cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-esx-%{version}
cp -v System.map        %{buildroot}/boot/system.map-esx-%{version}
cp -v .config            %{buildroot}/boot/config-esx-%{version}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/linux-esx-%{version}

# TODO: noacpi acpi=off noapic pci=conf1,nodomains pcie_acpm=off pnpacpi=off
cat > %{buildroot}/boot/%{name}-%{version}-%{release}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd rcupdate.rcu_expedited=1 rw systemd.show_status=0 quiet noreplace-smp cpu_init_udelay=0 plymouth.enable=0
photon_linux=vmlinuz-esx-%{version}
EOF

# cleanup dangling symlinks
rm -f %{buildroot}/lib/modules/%{version}-esx/source
rm -f %{buildroot}/lib/modules/%{version}-esx/build

# create /use/src/linux-esx-headers-*/ content
find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy
find arch/x86/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy

# copy .config manually to be where it's expected to be
cp .config %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}
# symling to the build folder
ln -sf /usr/src/%{name}-headers-%{version}-%{release} %{buildroot}/lib/modules/%{version}-esx/build

%post
/sbin/depmod -aq %{version}-esx
ln -sf %{name}-%{version}-%{release}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/system.map-esx-%{version}
/boot/config-esx-%{version}
/boot/vmlinuz-esx-%{version}
%config(noreplace) /boot/%{name}-%{version}-%{release}.cfg
/lib/modules/*
%exclude /lib/modules/%{version}-esx/build
%exclude /usr/src

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-esx-%{version}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{version}-esx/build
/usr/src/%{name}-headers-%{version}-%{release}

%changelog
*   Tue Mar 09 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-17
-   Enable ACPI hotplug support in kernel config
*   Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-16
-   veth patch: don’t modify ip_summed
*   Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
-   Double tcp_mem limits, patch is added.
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-14
-   Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
*   Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
-   Fix for CVE-2016-0728
*   Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-12
-   CONFIG_HZ=250
-   Disable sched autogroup.
*   Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-11
-   Remove rootfstype from the kernel parameter.
*   Tue Dec 15 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
-   Skip rdrand reseed to improve boot time.
-   .config changes: jolietfs(m), default THP=always, hotplug_cpu(m)
*   Tue Nov 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
-   nordrand cmdline param is removed.
-   .config: + serial 8250 driver (M).
*   Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
-   Change the linux image directory.
*   Tue Nov 10 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-7
-   Get LAPIC timer frequency from HV, skip boot time calibration.
-   .config: + dummy net driver (M).
*   Mon Nov 09 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-6
-   Rename subpackage dev -> devel.
-   Added the build essential files in the devel subpackage.
-   .config: added genede driver module.
*   Wed Oct 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-5
-   Import patches from kernel2 repo.
-   Added pv-ops patch (timekeeping related improvements).
-   Removed unnecessary cmdline params.
-   .config changes: elevator=noop by default, paravirt clock enable,
    initrd support, openvswitch module, x2apic enable.
*   Mon Sep 21 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-4
-   CDROM modules are added.
*   Thu Sep 17 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-3
-   Fix for 05- patch (SVGA mem size)
-   Compile out: pci hotplug, sched smt.
-   Compile in kernel: vmware balloon & vmci.
-   Module for efi vars.
*   Fri Sep 4 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-2
-   Hardcoded poweroff (direct write to piix4), no ACPI is required.
-   sd.c: Lower log level for "Assuming drive cache..." message.
*   Tue Sep 1 2015 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-1
-   Update to linux-4.2.0. Enable CONFIG_EFI
*   Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-5
-   Added MD/LVM/DM modules.
-   Pci probe improvements.
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-4
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-3
-   Added environment file(photon.cfg) for a grub.
*   Tue Aug 11 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-2
    Added pci-probe-vmware.patch. Removed unused modules. Decreased boot time. 
*   Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-1
    Initial commit. Use patchset from Clear Linux. 

