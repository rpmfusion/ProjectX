Name: ProjectX
Version: 0.91.0
# RPM Fusion doesn't support autorelease.
Release: 22%{?dist}
Summary: DVB video editing and demultiplexing tool
Summary(sv): Verktyg för redigering och demultiplexning av DVB-video

License: GPL-2.0-or-later
URL: http://project-x.sourceforge.net/

Source0: http://downloads.sourceforge.net/project/project-x/project-x/%{name}_%version.00/%{name}_%version.zip
Source1: http://gentoo.sbriesen.de/distfiles/projectx-idctfast.tar.xz
Source2: projectx.appdata.xml
Patch0: %name-0.90.4.00-20100801cvs.sysjava.patch
Patch1: %name-0.90.4.00-20100806cvs.desktop.patch
Patch2: %name-0.90.4.00-20100806cvs.helpfiles.patch
Patch3: projectx_0.91.0.08_IDCTFast.patch

ExclusiveArch: %java_arches

BuildRequires: gcc
BuildRequires: java-devel >= 1.2.2
BuildRequires: jakarta-oro
BuildRequires: apache-commons-net
BuildRequires: jpackage-utils
BuildRequires: desktop-file-utils
BuildRequires: dos2unix
BuildRequires: libappstream-glib
Requires: java >= 1.2.2
Requires: jakarta-oro
Requires: apache-commons-net
Requires: jpackage-utils

%description
In many countries digital radio and television uses the Digital Video
Broadcasting (DVB) standard to broadcast its data. Project X is a tool
to analyze and manipulate these DVB MPEG data streams. It can cut and
demultiplex them and it tries its best to handle and repair many
stream types and show what went wrong on reception.

%description -l sv
I många länder använder digital radio och television DVB-standarden
(Digital Video Broadcasting) för att sända sina data. Project X är ett
verktyg för att analysera och hantera dessa DVB-MPEG-dataströmmar.
Det kan dela upp och demultiplexa dem och det gör sitt bästa för att
hantera och reparera många strömtyper och visa vad som gick fel vid
mottagningen.


%prep
%setup -q -n Project-X_%version
# Source 1 unpacks into  a version-less directory.  Unpack it inside the real
# directory, and move things up.
%setup -q -n Project-X_%version -T -D -a 1
mv Project-X/lib/PORTABLE lib
mv Project-X/src/net/sourceforge/dvb/projectx/video/IDCTFast.java \
   src/net/sourceforge/dvb/projectx/video
%patch 0
%patch 1
%patch 2
# Patch 3 uses clean newlines, but the files it patches uses CRLF as distributed.
# Fix the documentation files similarily.
dos2unix noguisources.lst sources.lst \
         src/net/sourceforge/dvb/projectx/video/MpvDecoder.java \
         Copying ReadMe.txt ReleaseNotes_0.91.0.txt
%patch 3 -p2
sed -i '/Class-Path/d' MANIFEST.MF


%build
sh -ex build.sh
make -C lib/PORTABLE PROJECTX_HOME=%_builddir/Project-X_%version \
%ifarch i686 x86_64 ia64
    IDCT=idct-mjpeg-mmx \
%endif
    CPLAT="%optflags -fPIC" \
    CINC="-I%_jvmdir/java/include -I%_jvmdir/java/include/linux"


%install
install -d %buildroot%_jnidir %buildroot%_libdir/%name %buildroot%_bindir
install -p -m u=rw,go=r %name.jar %buildroot%_jnidir
install -p lib/PORTABLE/libidctfast.so %buildroot%_libdir/%name
%jpackage_script net.sourceforge.dvb.projectx.common.Start "-Djava.library.path=%_libdir/%name" "" ProjectX:commons-net:jakarta-oro projectx true
desktop-file-install --dir=%buildroot%_datadir/applications projectx.desktop
install -d %buildroot%_datadir/metainfo
cp -p %SOURCE2 %buildroot%_datadir/metainfo


%check
appstream-util validate-relax --nonet \
    %buildroot%_datadir/metainfo/projectx.appdata.xml

%files
%license Copying
%doc ReadMe.txt ReleaseNotes_0.91.0.txt
%_bindir/projectx
%_jnidir/%name.jar
%_libdir/%name
%_datadir/applications/projectx.desktop
%_datadir/metainfo/projectx.appdata.xml


%changelog
%autochangelog
