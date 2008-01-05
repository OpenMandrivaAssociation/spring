%define name spring
# (Anssi 01/2008) AFAICS "b" stands for build, not beta, so it is correctly
# part of %version.
%define version 0.76b1
%define rel 1
%define release %mkrel %{rel}

%define distname spring_%{version}

Summary: Realtime strategy game (inspired by Total Annihilation)
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://spring.clan-sy.com/dl/%{distname}_src.tar.bz2
# use system luxi:
Patch1: spring-0.76-luxi.patch
# add javapath to the list of commandline variables:
Patch2: spring-0.76-javapath.patch
# (Anssi 01/2008) put unitsync.log into ~/.spring, it ends up in pwd when some
# external tools dlopen unitsync.so:
Patch3: spring-0.76-unitsynclog.patch
License: GPLv2+
Group: Games/Strategy
Url: http://taspring.clan-sy.com/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: SDL-devel
BuildRequires: boost-devel
BuildRequires: desktop-file-utils
BuildRequires: devil-devel
BuildRequires: freetype2-devel
BuildRequires: glew-devel
BuildRequires: mesaglu-devel
BuildRequires: openal-devel
BuildRequires: libogg-devel
BuildRequires: libvorbis-devel
BuildRequires: python-devel
BuildRequires: scons
BuildRequires: zip
BuildRequires: zlib-devel
%if %{mdkversion} >= 200810
BuildRequires: java-rpmbuild
%else
BuildRequires: jpackage-utils
BuildRequires: java-devel-icedtea
%define java_home %{_jvmdir}/java-icedtea
%endif
Obsoletes: %{name}-data < 0.75
Requires: x11-font-bh-ttf
# Some mod is required, this is the one that was shipped with
# spring-data:
Suggests: spring-mod-nanoblob
# Some map is required, these are the default maps from the
# installer:
Suggests: spring-maps-default
# Internet lobby and springsettings:
Suggests: springlobby

%description
Spring is a 3D realtime strategy game. It was inspired by Total
Annihilation and has the same features Total Annihilation had, and
more.

%prep
%setup -q -n %{distname}
%patch1 -p1 -b .luxi
%patch2 -p1
%patch3 -p1
perl -pi -e 's,%{name}.png,%{name},g' rts/%{name}.desktop

cat > README.install.urpmi <<EOF
If you want to install additional mods and maps that are not available as
Mandriva packages, you can install them inside your homedir in subdirectories
.spring/maps and .spring/mods.
EOF

%build
# (Anssi 01/2008) scons does not like ccache, configure checks fail as if headers weren't there
export PATH=${PATH//ccache/foo}
scons configure prefix=%{_prefix} installprefix=%{buildroot}%{_prefix} libdir=%{_lib}/%{name} javapath=%{java_home}/include strip=0
scons %_smp_mflags

%install
rm -rf %{buildroot}
scons install

perl -pi -e 's|^Exec=.*|Exec=%{_gamesbindir}/%{name}|' %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install \
  --vendor="" \
  --remove-category="Application" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -d -m755 %{buildroot}%{_sysconfdir}/%{name}
echo '$HOME/.spring' > %{buildroot}%{_sysconfdir}/%{name}/datadir
echo '%{_gamesdatadir}/%{name}' >> %{buildroot}%{_sysconfdir}/%{name}/datadir

install -d -m755 %{buildroot}%{_gamesdatadir}/%{name}/{mods,maps}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.html Documentation/Spring*.txt Documentation/userdocs/* Documentation/cmds.txt
%doc README.install.urpmi
%{_sysconfdir}/%{name}
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_libdir}/%{name}

