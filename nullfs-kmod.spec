# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod

%global debug_package %{nil}

Name:           nullfs-kmod
Version:        0.19
Release:        1%{?dist}
Summary:        A virtual file system that behaves like /dev/null
License:        GPLv3+
URL:            https://github.com/abbbi/nullfsvfs

Source0:        %{url}/archive/v%{version}.tar.gz#/nullfsvfs-%{version}.tar.gz
%if 0%{?rhel} == 9
# https://github.com/abbbi/nullfsvfs/commit/63661607ded4e3ee0ba35cf50e1166a2b203daeb
Patch0:     nullfs-el9.patch
%endif

# Get the needed BuildRequires (in parts depending on what we build for):
BuildRequires:  kmodtool

Provides:       %{name}-common == %{version}-%{release}

# kmodtool does its magic here:
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
A virtual file system that behaves like /dev/null. It can handle regular file
operations but writing to files does not store any data. The file size is
however saved, so reading from the files behaves like reading from /dev/zero
with a fixed size.

Writing and reading is basically an NOOP, so it can be used for performance
testing with applications that require directory structures.

%prep
# Error out if there was something wrong with kmodtool:
%{?kmodtool_check}
# Print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -p1 -n nullfsvfs-%{version}

for kernel_version in %{?kernel_versions}; do
  mkdir _kmod_build_${kernel_version%%___*}
  cp -fr nullfs.c Makefile _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
  pushd _kmod_build_${kernel_version%%___*}/
    %make_build -C "${kernel_version##*___}" M=$(pwd) modules
  popd
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 _kmod_build_${kernel_version%%___*}/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Wed Jun 18 2025 Simone Caronni <negativo17@gmail.com> - 0.19-1
- Update to 0.19.

* Wed Apr 16 2025 Simone Caronni <negativo17@gmail.com> - 0.18-1
- Update to 0.18.

* Wed Apr 03 2024 Simone Caronni <negativo17@gmail.com> - 0.17-3
- Rebuild.

* Wed Nov 29 2023 Simone Caronni <negativo17@gmail.com> - 0.17-2
- Rename to nullfs.

* Wed Nov 29 2023 Simone Caronni <negativo17@gmail.com> - 0.17-1
- Update to 0.17.

* Wed Nov 29 2023 Simone Caronni <negativo17@gmail.com> - 0.15-2
- Drop custom signing and compressing in favour of kmodtool.

* Mon May 08 2023 Simone Caronni <negativo17@gmail.com> - 0.15-1
- Update to 0.15.

* Mon Nov 21 2022 Simone Caronni <negativo17@gmail.com> - 0.13-1
- Update to 0.13.

* Fri Dec 31 2021 Simone Caronni <negativo17@gmail.com> - 0.12.1-1
- Update to 0.12.1.

* Thu Sep 23 2021 Simone Caronni <negativo17@gmail.com> - 0.10-1
- Update to 0.10.

* Tue Sep 14 2021 Simone Caronni <negativo17@gmail.com> - 0.8-2
- Add automatic signing workaround.

* Wed Aug 18 2021 Simone Caronni <negativo17@gmail.com> - 0.8-1
- Update to 0.8.
- Update SPEC file.

* Thu Jun 03 2021 Simone Caronni <negativo17@gmail.com> - 0.5-1
- Update to 0.5.

* Wed Jan 13 2021 Simone Caronni <negativo17@gmail.com> - 0.3-1
- Update to 0.3.

* Thu Dec 10 2020 Simone Caronni <negativo17@gmail.com> - 0.2-1
- First build.
