Name: ProjectX
Version: 0.91.0
Release: 1
Summary: DVB video editing and demultiplexing tool
Summary(sv): Verktyg för redigering och demultiplexning av DVB-video

Group: Applications/Multimedia
License: GPLv2+
URL: http://project-x.sourceforge.net/

Source: http://downloads.sourceforge.net/project/project-x/project-x/%{name}_%version.00/%{name}_%version.zip
Patch0: %name-0.90.4.00-20100801cvs.sysjava.patch
Patch1: %name-0.90.4.00-20100806cvs.desktop.patch
Patch2: %name-0.90.4.00-20100806cvs.helpfiles.patch

BuildArch: noarch

BuildRequires: java-devel >= 1.2.2
BuildRequires: jakarta-oro
BuildRequires: apache-commons-net
BuildRequires: jpackage-utils
BuildRequires: desktop-file-utils
Requires: java >= 1.2.2
Requires: jakarta-oro
Requires: apache-commons-net
Requires: jpackage-utils

%description
In many countries digital radio and television uses the Digital Video
Broadcasting (DVB) standard to broadcast its data. Project X is a tool
to analyse and manipulate these DVB MPEG data streams. It can cut and
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
%patch0
%patch1
%patch2
sed -i '/Class-Path/d' MANIFEST.MF


%build
sh -ex build.sh


%install
install -d %buildroot%_javadir %buildroot%_bindir
cp -p %name.jar %buildroot%_javadir
%jpackage_script net.sourceforge.dvb.projectx.common.Start "" "" ProjectX:commons-net:jakarta-oro projectx true
desktop-file-install --dir=%buildroot%_datadir/applications projectx.desktop


%files
%defattr(-,root,root,-)
%doc Copying ReadMe.txt
%_bindir/projectx
%_javadir/%name.jar
%_datadir/applications/projectx.desktop


%changelog
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

* Mon Dec  6 2009 Göran Uddeborg <goeran@uddeborg.se> 0.90.4.00-3.20091201cvs
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
