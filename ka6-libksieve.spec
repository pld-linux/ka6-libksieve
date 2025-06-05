#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.2
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		libksieve
Summary:	Libksieve
Name:		ka6-%{kaname}
Version:	25.04.2
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	5f45ad6e27dfff0b90735fa38f20ede7
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Network-devel >= 5.11.1
BuildRequires:	Qt6Positioning-devel >= 5.11.1
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Qml-devel >= 5.11.1
BuildRequires:	Qt6Quick-devel >= 5.11.1
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6WebChannel-devel >= 5.11.1
BuildRequires:	Qt6WebEngine-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	cyrus-sasl-devel
BuildRequires:	gettext-devel
BuildRequires:	ka6-kidentitymanagement-devel >= %{kdeappsver}
BuildRequires:	ka6-kimap-devel >= %{kdeappsver}
BuildRequires:	ka6-kmailtransport-devel >= %{kdeappsver}
BuildRequires:	ka6-kmime-devel >= %{kdeappsver}
BuildRequires:	ka6-kpimtextedit-devel >= %{kdeappsver}
BuildRequires:	ka6-libkdepim-devel >= %{kdeappsver}
BuildRequires:	ka6-pimcommon-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-knewstuff-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-syntax-highlighting-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExcludeArch:	x32 i686
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This lib manages sieve support.

%description -l pl.UTF-8
Ta biblioteka obsługuje sieve.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{ko,sr}
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKPim6KManageSieve.so.*.*
%ghost %{_libdir}/libKPim6KManageSieve.so.6
%attr(755,root,root) %{_libdir}/libKPim6KSieve.so.*.*
%ghost %{_libdir}/libKPim6KSieve.so.6
%attr(755,root,root) %{_libdir}/libKPim6KSieveCore.so.*.*
%ghost %{_libdir}/libKPim6KSieveCore.so.6
%attr(755,root,root) %{_libdir}/libKPim6KSieveUi.so.*.*
%ghost %{_libdir}/libKPim6KSieveUi.so.6
%{_datadir}/knsrcfiles/ksieve_script.knsrc
%{_datadir}/qlogging-categories6/libksieve.categories
%{_datadir}/qlogging-categories6/libksieve.renamecategories
%{_datadir}/sieve

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/KManageSieve
%{_includedir}/KPim6/KSieve
%{_includedir}/KPim6/KSieveCore
%{_includedir}/KPim6/KSieveUi
%{_libdir}/cmake/KPim6KManageSieve
%{_libdir}/cmake/KPim6KSieve
%{_libdir}/cmake/KPim6KSieveCore
%{_libdir}/cmake/KPim6KSieveUi
%{_libdir}/libKPim6KManageSieve.so
%{_libdir}/libKPim6KSieve.so
%{_libdir}/libKPim6KSieveCore.so
%{_libdir}/libKPim6KSieveUi.so
