Name: ProjectX
Version: 0.91.0
# RPM Fusion doesn't support autorelease.
Release: 24%{?dist}
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


# RPM Fusion doesn't support autochangelog.
%changelog
* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.91.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun May 21 2023 Göran Uddeborg <goeran@uddeborg.se> 0.91.0-23
- Revert use of autochangelog, not supported on RPM Fusion BZ6689

* Sun May 21 2023 Göran Uddeborg <goeran@uddeborg.se> 0.91.0-22
- Update to current packaging standards

* Sat Aug 06 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.91.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Tue Feb 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.91.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.91.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Feb 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.91.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 10 2020 Leigh Scott <leigh123linux@gmail.com> - 0.91.0-17
- Fix appdata

* Tue Sep  1 2020 Göran Uddeborg <goeran@uddeborg.se> 0.91.0-16
- Remove inccorrectly commited source from git.

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.91.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.91.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.91.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.91.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.91.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.91.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 19 2017 Göran Uddeborg <goeran@uddeborg.se> 0.91.0-9
- Appdata added.

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.91.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.91.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 25 2015 Göran Uddeborg <goeran@uddeborg.se> - 0.91.0-6
- Use MMX instructions only on architectures that have them (BZ3549)

* Fri Feb 13 2015 Göran Uddeborg <goeran@uddeborg.se> - 0.91.0-5
- Build with fast-math (BZ3499)
- Separate licence from documentation files
- Skip obsolete defattr declaration
- Include the release notes in the documentation
- Use standard line endings in the documentation and license files
- Fix some minor lint

* Sat Oct 25 2014 Sérgio Basto <sergio@serjux.com> - 0.91.0-4
- add %{?dist} tag

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.91.0-3
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.91.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Göran Uddeborg <goeran@uddeborg.se> - 0.91.0
- New upstreams version.  This is an official release, not a snapshot
  any more.

* Mon Jun 13 2011 Göran Uddeborg <goeran@uddeborg.se> - 0.90.4.00-10.20100806cvs
- Adjust to updated packaging guidelines:
- + Build wrapper script using the jpackage_script macro.
- + Remove support for GCJ.

* Fri Oct 15 2010 Göran Uddeborg <goeran@uddeborg.se> - 0.90.4.00-9.20100806cvs
- jakarta-commons-net has been replaced with apache-commons-net.  Requirements
  updated.

* Fri Oct 15 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.90.4.00-8.20100806cvs
- Rebuilt for gcc bug

* Tue Aug 10 2010 Göran Uddeborg <goeran@uddeborg.se> 0.90.4.00-7.20100806cvs
- Remove the requirement on Java 1.6.  GCJ (ECJ) is fine for bytecode
  compilation.

* Sat Aug  7 2010 Göran Uddeborg <goeran@uddeborg.se> 0.90.4.00-6.20100806cvs
- Added version number to sysjava patch, indicating for which version it was
  made.
- Require Java 1.6, to get a newer compiler than GCJ's.
- Omit "lib" subdirectory and other bits not needed on Linux from the archive.
  Takes away the need to remove "lib" in "prep" section.
- Compress the archive with xz rather than bzip2.
- Update to snapshot from cvs 2010-08-06.
- Made a separate patch file for the desktop file modifications.
- Put the html help documentation in the jar archive, so it can be found in
  installed mode.

* Mon Aug  2 2010 Göran Uddeborg <goeran@uddeborg.se> 0.90.4.00-5.20100801cvs
- Include the cvs date in the source package.
- Explicitly prune empty directories when checking out from CVS.
- Include a little script that creates the tar file.
- Make the wrapper script a separate source file.
- Changed BuildArchitectures tag to BuildArch.

* Sun Aug  1 2010 Göran Uddeborg <goeran@uddeborg.se> 0.90.4.00-4.20100801cvs
- Switch to single character spacing of sentences in the description.
- Add comment on how to recreate the tar archive.
- Update to snapshot from cvs 2010-08-01.
- Do double line spacing between major sections.
- Removed cleaning in install and clean sections, no longer needed from F13.

* Mon Dec  7 2009 Göran Uddeborg <goeran@uddeborg.se> 0.90.4.00-3.20091201cvs
- BuildRequires entries on separate lines
- Don't point out Europe in the description, DVB is used in more places.
- Build wrapper script using jpackage-utils.
- Add a desktop file.
- Explicitly remove supplied libs.
- Add GCJ AOT libraries.
- Update to snapshot from cvs 2009-12-01.

* Sun Nov 29 2009 Göran Uddeborg <goeran@uddeborg.se> 0.90.4.00-3
- Adapted to Fedora packaging standards in preparation for submission to
  RPM Fusion.

* Tue Jan  8 2008 Göran Uddeborg <goeran@uddeborg.se> 0.90.4.00-2
- Escape dollar in here-script.
- Use system version of libraries.

* Sun Jan  6 2008 Göran Uddeborg <goeran@uddeborg.se> 0.90.4.00-1
- Initial build.

