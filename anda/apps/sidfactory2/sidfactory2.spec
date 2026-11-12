%global name sidfactory2
%global appid com.github.%{name}
%global name_pretty SIDFactoryII
%global appstream_component desktop-application
%global developer "Jens Christian Huus, "
# The below is required because %description doesn't provide a macro to infer from
%global _description %{expand:
A Music Editor for the Commodore C64 SID,
made by the demo scene for the world.}

Name:          %{name}
Version:       20260314
Release:       1%{?dist}
Summary:       A Commodore C64 SID Music Cross-Editor, made by the C64 Demoscene
License:       GPLv2
Group:         Multimedia
URL:           https://github.com/Chordian/%{name}
Source0:       com.github.sidfactory2.appdata.xml
Source1:       com.github.sidfactory2.desktop

BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: sdl2-compat-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: desktop-file-utils
BuildRequires: terra-appstream-helper
Requires:      sdl2-compat
Requires:      (jack-audio-connection-kit or pipewire-jack-audio-connection-kit)
Requires:      desktop-file-utils
Packager:      Stefan Kaps <st0ff.npl@gmail.com>

%description %_description

%prep
%global clone_dir release_%{version}
%global dist %{clone_dir}/RPMDIST
git clone -c advice.detachedHead=false --depth 1 --recurse-submodules --shallow-submodules -j '%getncpus' %url %{clone_dir}

%build
cd %{clone_dir}
%make_build dist DIST_FOLDER=RPMDIST

%install
mkdir -pm 755   %{buildroot}%{_bindir} \
                %{buildroot}%{_docdir}/%name \
                %{buildroot}%{_libexecdir}/%name \
                %{buildroot}%{_datadir}/%name
install -Dm 755 %{dist}/%name_pretty              %{buildroot}%{_libexecdir}/%name/%name_pretty
ln -sf          %{_libexecdir}/%name/%name_pretty %{buildroot}%{_bindir}/%name
install -Dm 644 %{dist}/COPYING                   %{buildroot}%{_docdir}/%name/
install -Dm 644 %{clone_dir}/macos/icon.svg       %{buildroot}%{_scalableiconsdir}/%{name_pretty}.svg
cp -a           %{dist}/documentation             %{buildroot}%{_docdir}/%name
cp -a           %{dist}/drivers                   %{buildroot}%{_libexecdir}/%name
cp -a           %{dist}/color_schemes             %{buildroot}%{_libexecdir}/%name
cp -a           %{dist}/music                     %{buildroot}%{_libexecdir}/%name
cp -a           %{dist}/overlay                   %{buildroot}%{_libexecdir}/%name
cp -a           %{dist}/config                    %{buildroot}%{_libexecdir}/%name

%desktop_file_install %{SOURCE1}
%terra_appstream -o %{SOURCE0}

%files
%license %{_docdir}/%name/COPYING
%{_docdir}/%name/
%{_datadir}/%name/
%{_libexecdir}/%name/
%{_metainfodir}/%{appid}.metainfo.xml
%{_appsdir}/%{appid}.desktop
%{_scalableiconsdir}/%{name_pretty}.svg
%{_bindir}/%name

%post
%update_desktop_database

%postun
%update_desktop_database

%changelog
* Sun Nov 01 2026 Stefan Kaps <st0ff.npl@gmail.com> - 1.0.0
- Initial package
