# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       sdk-setup

# >> macros
%define systemd_post() \
# Initial installation \
/bin/systemctl -f preset %{?*} >/dev/null 2>&1 || : \
%{nil}

# << macros

Summary:    SDK setup packages for Mer SDK
Version:    0.62
Release:    1
Group:      System/Base
License:    GPL
BuildArch:  noarch
URL:        https://github.com/mer-tools/sdk-setup
Source0:    sdk-setup-%{version}.tar.gz
Source100:  sdk-setup.yaml
BuildRequires:  systemd

%description
Scripts, configurations and utilities to build Mer SDK and variants

%package -n sdk-chroot
Summary:    Mer SDK files for the chroot variant
Group:      System/Base
Requires(pre): rpm
Requires(pre): /bin/rm
Conflicts:  sdk-vm

%description -n sdk-chroot
Contains the mer_sdk_chroot script and supporting configs

%package -n sdk-vm
Summary:    Mer SDK files for the VM variant
Group:      System/Base
Requires:   sdk-utils == %{version}
Requires:   connman >= 1.14
Requires:   virtualbox-guest-tools
Requires:   openssh-server
Requires(post): /bin/ln
Conflicts:  sdk-chroot

%description -n sdk-vm
Contains the supporting configs for VMs

%package -n sdk-sb2-config
Summary:    Mer SDK files to configure sb2
Group:      System/Base
Requires:   scratchbox2 = 2.3.90

%description -n sdk-sb2-config
Contains the sdk build and install modes used by scratchbox2 in the SDK

%package -n sdk-utils
Summary:    Mer SDK utility scripts
Group:      System/Base
Requires:   rpm-build
Requires:   python-lxml
Requires:   sudo

%description -n sdk-utils
Contains some utility scripts to support Mer SDK development

%package -n sdk-mer-branding
Summary:    Mer Branding for the SDK Engine
Group:      System/Base
Requires:   plymouth-lite
Requires:   sdk-vm
Provides:   boot-splash-screen

%description -n sdk-mer-branding
Splash screen for the SDK Engine

%package -n connman-configs-mersdk-emul
Summary:    Connman configs for SDK Emulator
Group:      System/Base
Requires:   connman
Provides:   connman-configs

%description -n connman-configs-mersdk-emul
Connman configs for SDK emulator to ensure session is started

%prep
%setup -q -n src

# >> setup
# << setup

%build
# >> build pre
# << build pre



# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre

# all sdks
mkdir -p %{buildroot}%{_bindir}/
cp src/sdk-version %{buildroot}%{_bindir}/

# sdk-chroot
mkdir -p %{buildroot}/%{_sysconfdir}
cp src/mer-sdk-chroot %{buildroot}/
cp src/mer-bash-setup %{buildroot}/
echo "This file tells ssu this is a chroot SDK installation" > %{buildroot}/%{_sysconfdir}/mer-sdk-chroot

# sdk-vm
mkdir -p %{buildroot}/%{_unitdir}
cp --no-dereference systemd/* %{buildroot}/%{_unitdir}/
cp src/sdk-info %{buildroot}%{_bindir}/
cp src/sdk-setup-enginelan %{buildroot}%{_bindir}/
cp src/sdk-shutdown %{buildroot}%{_bindir}/
cp src/resize-rootfs %{buildroot}%{_bindir}/
# This should really be %%{_unitdir}/default.target but systemd owns that :/
mkdir -p %{buildroot}/%{_sysconfdir}/systemd/system/
ln -sf %{_unitdir}/multi-user.target  %{buildroot}/%{_sysconfdir}/systemd/system/default.target
echo "This file tells ssu this is a virtualbox SDK installation" > %{buildroot}/%{_sysconfdir}/mer-sdk-vbox

mkdir -p %{buildroot}/%{_sysconfdir}/mersdk

mkdir -p %{buildroot}/%{_sysconfdir}/ssh/
mkdir -p %{buildroot}/%{_sysconfdir}/ssh/authorized_keys
cp ssh-env.conf  %{buildroot}/%{_sysconfdir}/ssh/
cp sshd_config_engine  %{buildroot}/%{_sysconfdir}/ssh/

mkdir -p %{buildroot}/home/deploy
chmod 1777 %{buildroot}/home/deploy

# Until login.prefs.systemd is ready
cp mersdk.env.systemd  %{buildroot}/%{_sysconfdir}/

# sdk-sb2-config
mkdir -p %{buildroot}/usr/share/scratchbox2/modes/
cp -ar modes/* %{buildroot}/usr/share/scratchbox2/modes/

# sdk-utils
cp src/mb %{buildroot}%{_bindir}/
cp src/mb2 %{buildroot}%{_bindir}/
cp src/qb %{buildroot}%{_bindir}/
cp src/sdk-manage %{buildroot}%{_bindir}/
cp src/updateQtCreatorTargets %{buildroot}%{_bindir}/updateQtCreatorTargets

mkdir -p %{buildroot}/%{_sysconfdir}/ssh/
cp ssh_config.sdk  %{buildroot}/%{_sysconfdir}/ssh/

# sdk-mer-branding
install -D -m 644 branding/mer-splash.png %{buildroot}%{_datadir}/plymouth/splash.png
install -D -m 755 branding/splashfontcol %{buildroot}%{_sysconfdir}/sysconfig/splashfontcol

# connman-configs-mersdk-emul
mkdir -p %{buildroot}%{_sysconfdir}/connman
install -D -m 755  connman_main.conf %{buildroot}%{_sysconfdir}/connman/main.conf

# Make all bindir executable
chmod 755 %{buildroot}%{_bindir}/*

# << install pre

# >> install post
# << install post

%pre
# >> pre
%pre -n sdk-chroot
if ! rpm --quiet -q ca-certificates && [ -d /%{_sysconfdir}/ssl/certs ] ; then echo "Cleaning up copied ssl certs. ca-certificates should now install"; rm -rf /%{_sysconfdir}/ssl/certs ;fi
# << pre

%preun
# >> preun
%preun -n sdk-vm
%systemd_preun home-mersdk.service
%systemd_preun etc-mersdk-share.service
%systemd_preun etc-ssh-authorized_keys.mount
%systemd_preun host_targets.service
%systemd_preun information.service
%systemd_preun sdk-enginelan.service
# << preun

%post
# >> post
%post -n sdk-vm
%systemd_post home-mersdk.service
%systemd_post etc-mersdk-share.service
%systemd_post etc-ssh-authorized_keys.mount
%systemd_post host_targets.service
%systemd_post information.service
%systemd_post sdk-enginelan.service
%systemd_post sdk-refresh.service
%systemd_post sdk-refresh.timer
%systemd_post resize-rootfs.service
# this could be mounted read-only so to avoid a
# cpio: chmod failed - Read-only file system
if [ $1 -eq 1 ] ; then
[ -d %{_sysconfdir}/ssh/authorized_keys ] || install -d %{_sysconfdir}/ssh/authorized_keys 2>/dev/null || :
fi
# << post

%postun
# >> postun
%postun -n sdk-vm
%systemd_postun
# << postun


%files -n sdk-chroot
%defattr(-,root,root,-)
/mer-sdk-chroot
/mer-bash-setup
%{_bindir}/sdk-version
%{_sysconfdir}/mer-sdk-chroot
# >> files sdk-chroot
# << files sdk-chroot

%files -n sdk-vm
%defattr(-,root,root,-)
%{_bindir}/sdk-version
%{_bindir}/sdk-info
%{_bindir}/sdk-setup-enginelan
%{_bindir}/sdk-shutdown
%{_bindir}/resize-rootfs
%{_unitdir}/information.service
%{_unitdir}/sdk-enginelan.service
%{_unitdir}/host_targets.service
%{_unitdir}/home-mersdk.service
%{_unitdir}/etc-mersdk-share.service
%{_unitdir}/etc-ssh-authorized_keys.mount
%{_unitdir}/sdk-refresh.service
%{_unitdir}/sdk-refresh.timer
%{_unitdir}/resize-rootfs.service
%config %{_sysconfdir}/systemd/system/default.target
%config %{_sysconfdir}/ssh/ssh-env.conf
%config %{_sysconfdir}/ssh/sshd_config_engine
%config %{_sysconfdir}/mersdk.env.systemd
%dir /home/deploy
%{_sysconfdir}/mer-sdk-vbox
%attr(-,mersdk,mersdk) %{_sysconfdir}/mersdk/
# >> files sdk-vm
# << files sdk-vm

%files -n sdk-sb2-config
%defattr(-,root,root,-)
%{_datadir}/scratchbox2/modes/*
# >> files sdk-sb2-config
# << files sdk-sb2-config

%files -n sdk-utils
%defattr(-,root,root,-)
%{_bindir}/mb
%{_bindir}/mb2
%{_bindir}/qb
%{_bindir}/sdk-manage
%{_bindir}/updateQtCreatorTargets
%config %{_sysconfdir}/ssh/ssh_config.sdk
# >> files sdk-utils
# << files sdk-utils

%files -n sdk-mer-branding
%defattr(-,root,root,-)
%{_datadir}/plymouth/splash.png
%{_sysconfdir}/sysconfig/splashfontcol
# >> files sdk-mer-branding
# << files sdk-mer-branding

%files -n connman-configs-mersdk-emul
%defattr(-,root,root,-)
%{_sysconfdir}/connman/main.conf
# >> files connman-configs-mersdk-emul
# << files connman-configs-mersdk-emul
