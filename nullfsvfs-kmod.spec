# Define the kmod package name here.
%global	kmod_name nullfsvfs

# If kversion isn't defined on the rpmbuild line, define it here. For Fedora,
# kversion needs always to be defined as there is no kABI support.

# RHEL 7.9
%if 0%{?rhel} == 7
%{!?kversion: %global kversion 3.10.0-1160.11.1.el7}
%endif

# RHEL 8.3
%if 0%{?rhel} == 8
%{!?kversion: %global kversion 4.18.0-240.1.1.el8_3}
%endif

Name:           %{kmod_name}-kmod
Version:        0.3
Release:        1%{?dist}
Summary:        A virtual file system that behaves like /dev/null
License:        GPLv3+
URL:            https://github.com/abbbi/nullfsvfs

Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source10:       kmodtool-%{kmod_name}-el6.sh

BuildRequires:  elfutils-libelf-devel
BuildRequires:  gcc
BuildRequires:  redhat-rpm-config
BuildRequires:  kernel-devel %{?kversion:== %{kversion}}
BuildRequires:  kernel-abi-whitelists %{?kversion:== %{kversion}}
BuildRequires:  kmod

# Magic hidden here.
%global kmodtool sh %{SOURCE10}
%{expand:%(%{kmodtool} rpmtemplate %{kmod_name} %{kversion}.%{_target_cpu} "" 2>/dev/null)}

# Disable building of the debug package(s).
%global	debug_package %{nil}

%description
This package provides the proprietary NVIDIA OpenGL kernel driver module.
It is built to depend upon the specific ABI provided by a range of releases of
the same variant of the Linux kernel and not on any one specific build.

%prep
%autosetup -p1 -n %{kmod_name}-%{version}

echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
make -C %{_usrsrc}/kernels/%{kversion}.%{_target_cpu} M=$PWD modules

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}
make -C %{_usrsrc}/kernels/%{kversion}.%{_target_cpu} M=$PWD modules_install

install -d %{buildroot}%{_sysconfdir}/depmod.d/
install kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
# Remove the unrequired files.
rm -f %{buildroot}/lib/modules/%{kversion}.%{_target_cpu}/modules.*

%changelog
* Wed Jan 13 2021 Simone Caronni <negativo17@gmail.com> - 0.3-1
- Update to 0.3.

* Thu Dec 10 2020 Simone Caronni <negativo17@gmail.com> - 0.2-1
- First build.
