%define distname spring_%{version}

# No shared library, and the cmake build currently has internal linking
# issues - AdamW 2008/12
%define _disable_ld_no_undefined	1

Summary:	Realtime strategy game (inspired by Total Annihilation)
Name:		spring
Version:	0.79.0.2
Release:	%mkrel 1
Source0:	http://spring.clan-sy.com/dl/%{name}_%{version}_src.tar.lzma
# use system font:
Patch1:		spring-0.79.0.2-font.patch
# (Anssi 01/2008) put unitsync.log into ~/.spring, it ends up in pwd when some
# external tools dlopen unitsync.so:
# FIXME: the code completely changed with 0.78. I'm not sure if it still
# needs to be patched, but if so, it needs to be re-diffed. Patch is
# disabled below - AdamW 2009/01
Patch2:		spring-0.77-unitsynclog.patch
# Fix a string literal error (from dev alphabeta on irc)
Patch3:		spring-0.79.0.2-literal.patch
License:	GPLv2+
Group:		Games/Strategy
URL:		http://taspring.clan-sy.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	SDL-devel
BuildRequires:	boost-devel
BuildRequires:	desktop-file-utils
BuildRequires:	devil-devel
BuildRequires:	freetype2-devel
BuildRequires:	glew-devel
BuildRequires:	mesaglu-devel
BuildRequires:	openal-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxcursor-devel
BuildRequires:	python-devel
BuildRequires:	cmake
BuildRequires:	zip
BuildRequires:	zlib-devel
%if %{mdkversion} >= 200810
BuildRequires:	java-rpmbuild
%else
BuildRequires:	jpackage-utils
BuildRequires:	java-devel-icedtea
%define java_home %{_jvmdir}/java-icedtea
%endif
Obsoletes:	%{name}-data < 0.75
Requires:	fonts-ttf-freefont
# Some mod is required, this is the one that was shipped with
# spring-data:
Suggests:	spring-mod-nanoblobs
# Some map is required, these are the default maps from the
# installer:
Suggests:	spring-maps-default
# Internet lobby and springsettings:
Suggests:	springlobby

%description
Spring is a 3D realtime strategy game. It was inspired by Total
Annihilation and has the same features Total Annihilation had, and
more.

%prep
%setup -q -n %{distname}
%patch1 -p1 -b .font
# See above FIXME notice - AdamW 2009/01
#patch2 -p1
%patch3 -p1 -b .literal
sed -i -e 's,%{name}.png,%{name},g' installer/freedesktop/applications/spring.desktop

cat > README.install.urpmi <<EOF
If you want to install additional mods and maps that are not available as
Mandriva packages, you can install them inside your homedir in subdirectories
.spring/maps and .spring/mods.
EOF

%build
# Spring has both scons and cmake build systems. The cmake one is newer
# (so presumably preferred upstream), the scons one has problems in
# install phase (some stuff won't install to buildroot), and cmake is
# just...nicer. - AdamW 2008/12
%cmake -DBINDIR=%{_gamesbindir} -DLIBDIR=%{_lib}/%{name} -DJAVA_INCLUDE_PATH=%{java_home}/include -DJAVA_INCLUDE_PATH2=%{java_home}/include/linux -DJAVA_AWT_INCLUDE_PATH=%{java_home}/include
%make

%install
rm -rf %{buildroot}
pushd build
%makeinstall_std
popd

perl -pi -e 's|^Exec=.*|Exec=%{_gamesbindir}/%{name}|' %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install \
  --vendor="" \
  --remove-category="Application" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -d -m755 %{buildroot}%{_sysconfdir}/%{name}
echo '$HOME/.spring' > %{buildroot}%{_sysconfdir}/%{name}/datadir
echo '%{_gamesdatadir}/%{name}' >> %{buildroot}%{_sysconfdir}/%{name}/datadir

install -d -m755 %{buildroot}%{_gamesdatadir}/%{name}/{mods,maps}

%if %mdkversion < 200900
%post
%update_mime_database
%endif
%if %mdkversion < 200900
%postun
%clean_mime_database
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Documentation/Spring*.txt Documentation/userdocs/* Documentation/cmds.txt
%doc README.install.urpmi
%{_sysconfdir}/%{name}
%{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-dedicated
%{_gamesdatadir}/%{name}
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_libdir}/%{name}

