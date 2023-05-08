# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels akmod

%global debug_package %{nil}

%global mok_algo sha512
%global mok_key /usr/src/akmods/mok.key
%global mok_der /usr/src/akmods/mok.der

%define __spec_install_post \
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__mod_install_post}

%define __mod_install_post \
  if [ $kernel_version ]; then \
    find %{buildroot} -type f -name '*.ko' | xargs %{__strip} --strip-debug; \
    if [ -f /usr/src/akmods/mok.key ] && [ -f /usr/src/akmods/mok.der ]; then \
      find %{buildroot} -type f -name '*.ko' | xargs echo; \
      find %{buildroot} -type f -name '*.ko' | xargs -L1 /usr/lib/modules/${kernel_version%%___*}/build/scripts/sign-file %{mok_algo} %{mok_key} %{mok_der}; \
    fi \
    find %{buildroot} -type f -name '*.ko' | xargs xz; \
  fi

Name:           nullfsvfs-kmod
Version:        0.15
Release:        1%{?dist}
Summary:        A virtual file system that behaves like /dev/null
License:        GPLv3+
URL:            https://github.com/abbbi/nullfsvfs

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  kmodtool

Provides:       %{name}-common == %{version}-%{release}

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
A virtual file system that behaves like /dev/null. It can handle regular file
operations but writing to files does not store any data. The file size is
however saved, so reading from the files behaves like reading from /dev/zero
with a fixed size.

Writing and reading is basically an NOOP, so it can be used for performance
testing with applications that require directory structures.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -p1 -n nullfsvfs-%{version}

for kernel_version in %{?kernel_versions}; do
  mkdir _kmod_build_${kernel_version%%___*}
  cp -fr * _kmod_build_${kernel_version%%___*}
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
