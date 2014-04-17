# Don't provides private modules
%if %{_use_internal_dependency_generator}
%define __noautoprov '(.*)\\.so$'
%endif

%define distname spring_%{version}

%define Werror_cflags %nil

Summary:	Realtime strategy game (inspired by Total Annihilation)
Name:		spring
Version:	91.0
Release:	5
License:	GPLv2+
Group:		Games/Strategy
Url:		http://springrts.com
Source0:	http://sourceforge.net/projects/springrts/files/springrts/%{name}-%{version}/%{name}_%{version}_src.tar.lzma
Source10:	%{name}.rpmlintrc
# use system font:
Patch1:		spring-89.0-font.patch
Patch5:		spring-89-dso.patch
Patch6:		spring-90-e323ai-boost.patch
Patch7:		spring_91.0-static-libs.patch
BuildRequires:	asciidoc
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-style-xsl
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:	java-rpmbuild
BuildRequires:	icoutils
BuildRequires:	p7zip
BuildRequires:	xerces-j2
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
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(zlib)
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
%setup -qn %{name}_%{version}
%patch1 -p1 -b .font
%patch5 -p0
%patch6 -p1
%patch7 -p1

cat > README.install.urpmi <<EOF
If you want to install additional mods and maps that are not available as
Rosa packages, you can install them inside your homedir in subdirectories
.spring/maps and .spring/mods.
EOF


  sed -i "s/FE_DFL_ENV/FE_DFL_ENV_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp rts/lib/streflop/SMath.cpp
  sed -i "s/FE_INVALID/FE_INVALID_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_DENORMAL/FE_DENORMAL_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_DIVBYZERO/FE_DIVBYZERO_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_OVERFLOW/FE_OVERFLOW_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_UNDERFLOW/FE_UNDERFLOW_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_INEXACT/FE_INEXACT_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_ALL_EXCEPT/FE_ALL_EXCEPT_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_DOWNWARD/FE_DOWNWARD_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_TONEAREST/FE_TONEAREST_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_TOWARDZERO/FE_TOWARDZERO_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/FE_UPWARD/FE_UPWARD_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp
  sed -i "s/feclearexcept/feclearexcept_/g" rts/lib/streflop/FPUSettings.h rts/System/Sync/FPUCheck.cpp rts/System/myMath.cpp rts/Lua/LuaParser.cpp

%build
export CFLAGS="%{optflags} -fpermissive"
export CXXFLAGS="%{optflags} -fpermissive"
export LDFLAGS="-ldl"
%cmake -DBINDIR=%{_gamesbindir} -DLIBDIR=%{_lib}/%{name} -DJAVA_INCLUDE_PATH=%{java_home}/include -DJAVA_INCLUDE_PATH2=%{java_home}/include/linux -DJAVA_AWT_INCLUDE_PATH=%{java_home}/include
%make

%install
%makeinstall_std -C build

# Nanar:
# need by spring dedicated server
# it is not installed 

mkdir -p %{buildroot}%{_libdir}/

rm -fr %{buildroot}%{_datadir}/doc

install -m755 \
    build/libspringserver.so \
    %{buildroot}%{_libdir}/libspringserver.so

mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{32x32,64x64,128x128,256x256}/apps
cd rts
icotool -x %{name}.new.ico
mv %{name}*32x32*.png %{name}.png
install -m 644 %{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
mv %{name}*64x64*.png %{name}.png
install -m 644 %{name}.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
mv %{name}*128x128*.png %{name}.png
install -m 644 %{name}.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
mv %{name}*256x256*.png %{name}.png
install -m 644 %{name}.png %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png

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

# Looks like it's not needed
rm -rf %{buildroot}%{_gamesbindir}/pr-downloader
rm -rf %{buildroot}%{_libdir}/%{name}/libpr-downloader_shared.so
rm -rf %{buildroot}%{_libdir}/%{name}/libpr-downloader_static.a
rm -rf %{buildroot}%{_libdir}/%{name}/pkgconfig/libspringdownloader.pc
rm -rf %{buildroot}%{_includedir}/spring/Downloader/pr-downloader.h

