# Don't provides private modules
%if %{_use_internal_dependency_generator}
%define __noautoprov '(.*)\\.so$'
%endif

%define distname spring_%{version}

%define Werror_cflags %nil

Summary:	Realtime strategy game (inspired by Total Annihilation)
Name:		spring
Version:	106.0.1
Release:	1
License:	GPLv2+
Group:		Games/Strategy
Url:		http://springrts.com
Source0:	https://github.com/spring/spring/archive/%{version}/%{name}-%{version}.tar.gz
Source10:	%{name}.rpmlintrc

BuildRequires:	asciidoc
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-style-xsl
BuildRequires:	jdk-current
BuildRequires:	icoutils
BuildRequires:	p7zip
#BuildRequires:	xerces-j2
BuildRequires:	xsltproc
BuildRequires:	zip
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(allegro)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(IL)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(zlib)
Obsoletes:	%{name}-data < 0.75
Requires:	fonts-ttf-freefont

Provides:	bundled(lua) = 5.1.4
Provides:	bundled(luasocket) = 2.0.1
Provides:	bundled(gflags) = 2.2.0

# Some mod is required, this is the one that was shipped with
# spring-data:
Suggests:	spring-mod-nanoblobs
# Some map is required, these are the default maps from the
# installer:
Suggests:	spring-maps-default
# Internet lobby and springsettings:
Suggests:	springlobby

%description
Spring is a 3D realtime strategy game. It was inspired by Total Annihilation
and has the same features Total Annihilation had, and more.

%files
%doc README.install.urpmi
%{_sysconfdir}/%{name}
%{_gamesbindir}/*
%{_gamesdatadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_libdir}/%{name}
%{_libdir}/libspringserver.so
%{_mandir}/man*/spring*

#----------------------------------------------------------------------------

%prep
%setup -qn %{name}-%{version}
%autopatch -p1

cat > README.install.urpmi <<EOF
If you want to install additional mods and maps that are not available as
OpenMandriva packages, you can install them inside your homedir in subdirectories
.spring/maps and .spring/mods.
EOF


#  sed -i "s/FE_DFL_ENV/FE_DFL_ENV_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp rts/lib/streflop/SMath.cpp
# sed -i "s/FE_INVALID/FE_INVALID_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_DENORMAL/FE_DENORMAL_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_DIVBYZERO/FE_DIVBYZERO_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_OVERFLOW/FE_OVERFLOW_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_UNDERFLOW/FE_UNDERFLOW_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_INEXACT/FE_INEXACT_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_ALL_EXCEPT/FE_ALL_EXCEPT_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_DOWNWARD/FE_DOWNWARD_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_TONEAREST/FE_TONEAREST_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_TOWARDZERO/FE_TOWARDZERO_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/FE_UPWARD/FE_UPWARD_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
#  sed -i "s/feclearexcept/feclearexcept_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp

%build
export CXXFLAGS="%{optflags} -fpermissive"
export LDFLAGS="%{ldflags} -ldl"

%cmake -DBINDIR=%{_gamesbindir} \
       -DLIBDIR=%{_lib}/%{name} \
       -DPRD_BINDIR=%{_gamesbindir} \
       -DPRD_JSONCPP_INTERNAL=OFF \
       -DJAVA_INCLUDE_PATH=%{java_home}/include \
       -DJAVA_INCLUDE_PATH2=%{java_home}/include/linux \
       -DJAVA_AWT_INCLUDE_PATH=%{java_home}/include \
       -DBUILD_STATIC_LIBS=ON \
       -DBUILD_SHARED_LIBS=OFF
%make_build

%install
%make_install -C build

# Nanar:
# need by spring dedicated server
# it is not installed

mkdir -p %{buildroot}%{_libdir}/

rm -fr %{buildroot}%{_datadir}/doc

# KAI is deprecated: http://spring.clan-sy.com/phpbb/viewtopic.php?f=20&t=18196
rm -f %{buildroot}%{_libdir}/%{name}/AI/Bot-libs/libKAI-0.2.so


pushd rts
icotool -x %{name}.ico
for size in 16x16 64x64 128x128 256x256; do
  mkdir -p %{buildroot}%{_iconsdir}/hicolor/${size}/apps
  install -m 644 %{name}*${size}x32.png %{buildroot}%{_iconsdir}/hicolor/${size}/apps/%{name}.png
done
mkdir -p %{buildroot}%{_iconsdir}/hicolor/scalable/apps
install -m 644 %{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
popd

perl -pi -e 's|^Exec=.*|Exec=%{_gamesbindir}/%{name}|' %{buildroot}%{_datadir}/applications/%{name}.desktop
perl -pi -e 's|true|false|' %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install \
  --vendor="" \
  --remove-category="Application" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop


install -d -m755 %{buildroot}%{_sysconfdir}/%{name}
echo '$HOME/.spring' > %{buildroot}%{_sysconfdir}/%{name}/datadir
echo '%{_gamesdatadir}/%{name}' >> %{buildroot}%{_sysconfdir}/%{name}/datadir

install -d -m755 %{buildroot}%{_gamesdatadir}/%{name}/{mods,maps}

rm -rf %{buildroot}%{_datadir}/pixmaps/*.png

%files
%doc README.install.urpmi
%{_sysconfdir}/%{name}
%{_gamesbindir}/*
%{_gamesdatadir}/%{name}/
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_libdir}/%{name}/
%{_mandir}/man*/spring*

