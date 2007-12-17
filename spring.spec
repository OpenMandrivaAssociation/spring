%define name spring
%define version 0.75
%define beta b2
%define rel 1
%define release %mkrel 0.%{beta}.%{rel}

%define distname spring_%{version}%{beta}

Summary: Realtime strategy game (inspired by Total Annihilation)
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownload.berlios.de/taspring-linux/%{distname}_src.tar.bz2
Patch1: spring-0.74-luxi.patch
License: GPLv2+
Group: Games/Strategy
Url: http://taspring.clan-sy.com/
BuildRequires: SDL-devel
BuildRequires: boost-devel
BuildRequires: desktop-file-utils
BuildRequires: devil-devel
BuildRequires: freetype2-devel
BuildRequires: glew-devel
BuildRequires: mesaglu-devel
BuildRequires: openal-devel
BuildRequires: python-devel
BuildRequires: scons
BuildRequires: zip
BuildRequires: zlib-devel
BuildRequires: classpath-devel java-1.7.0-icedtea
Requires: %{name}-data
Requires: x11-font-bh-ttf

%description
Spring is a 3D realtime strategy game. It was inspired by Total
Annihilation and has the same features Total Annihilation had, and
more.

%prep
%setup -q -n %{distname}
%patch1 -p1 -b .luxi
perl -pi -e 's,%{name}.png,%{name},g' rts/%{name}.desktop

%build
scons configure prefix=%{_prefix} installprefix=%{buildroot}%{_prefix} libdir=%{_lib}/%{name}
scons

%install
rm -rf %{buildroot}
scons install

# these files also exist in spring-data, I think those versions should
# be correct so remove from here - AdamW 2007/09
rm -f %{buildroot}%{_gamesdatadir}/%{name}/base/spring/bitmaps.sdz
rm -f %{buildroot}%{_gamesdatadir}/%{name}/base/springcontent.sdz

perl -pi -e 's|^Exec=.*|Exec=%{_gamesbindir}/%{name}|' %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install \
  --vendor="" \
  --remove-category="Application" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -d -m755 %{buildroot}%{_sysconfdir}/%{name}
echo '$HOME/.spring' > %{buildroot}%{_sysconfdir}/%{name}/datadir
echo '%{_gamesdatadir}/%{name}' >> %{buildroot}%{_sysconfdir}/%{name}/datadir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/%{name}
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_libdir}/%{name}

