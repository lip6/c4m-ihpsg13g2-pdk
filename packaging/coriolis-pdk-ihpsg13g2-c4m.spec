%global python3_pkgversion 3.11
%if 0%{?rhel} >= 9 || 0%{?fedora} >= 39
%global python3_pkgversion 3
%endif
%if 0%{?is_opensuse}
%global python3_pkgversion 311
%endif
%global         dateVersion    2024.10.15

Name:           coriolis-pdk-ihpsg13g2-c4m
Version:        %{dateVersion}
Release:        1
Summary:        C4M Standard Cells for IHP SG13G2
License:        GPL-2.0-or-later
%if 0%{?is_opensuse}
Group:          Productivity/Scientific/Electronics
%endif
URL:            https://github.com/lip6/coriolis-pdk-ihpsg13g2-c4m
Source0:        coriolis-pdk-ihpsg13g2-c4m-%{dateVersion}.tar.gz
Source1:        venv-al9-2.5.5.tar.gz
Source2:        patchvenv.sh
Source10:       %{name}-rpmlintrc
Requires:       coriolis-eda
Requires:       python%{python3_pkgversion}-coriolis-pdk-ihpsg13g2
Requires:       yosys
Requires:       klayout

BuildArch:      noarch
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:  ninja-build
BuildRequires:  pyproject-rpm-macros
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%if "%{python3_pkgversion}" != "3"
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
%endif

%if 0%{?is_opensuse}
%global _pyproject_wheeldir %{_builddir}/coriolis-pdk-ihpsg13g2-c4m-%{version}/build
%global python3_sitearch /usr/lib64/python3.11/site-packages

BuildRequires:  meson
BuildRequires:  %{python_module devel}
BuildRequires:  %{python_module setuptools}
%endif

# ALmaLinux 8
%if 0%{?rhel} == 8
%global python3_sitearch /usr/lib64/python3.11/site-packages

BuildRequires:  python%{python3_pkgversion}-rpm-macros
%endif

# ALmaLinux 9
%if 0%{?rhel} >= 9 || 0%{?fedora} >= 39
BuildRequires:  python-unversioned-command
BuildRequires:  python3-build
%endif


%global _description %{expand:
Chips4Makers (c4m) standard cell library for IHP SG13G2 technology}


%description
%_description


%package -n python%{python3_pkgversion}-coriolis-pdk-ihpsg13g2-c4m
Summary:        %{summary}


%description -n python%{python3_pkgversion}-coriolis-pdk-ihpsg13g2-c4m
%_description


%prep
%autosetup -p1 -n coriolis-pdk-ihpsg13g2-c4m-%{version} -a 1


%build
 cp $RPM_SOURCE_DIR/patchvenv.sh .
 chmod u+x patchvenv.sh
 patchVEnvArgs="--use-system-packages"
 if [    \( 0%{?fedora} -ge 39 \) \
      -o \( 0%{?rhel}   -eq  8 \) \
      -o \( 0%{?suse_version}%{?sle_version} -ne 0 \) ]; then
   patchVEnvArgs="${patchVEnvArgs} --remove-venv-watchfiles"
 fi
 ./patchvenv.sh ${patchVEnvArgs}
 source .venv/bin/activate
 pip list
 %__mkdir_p %{_pyproject_wheeldir}
 python3 -m pip wheel --no-deps --no-cache-dir \
	 --disable-pip-version-check --progress-bar off --verbose \
         --no-build-isolation --no-clean \
         --wheel-dir=%{_pyproject_wheeldir} \
	 .


%install
 source .venv/bin/activate
%if 0%{?is_opensuse}
 python3 -m pip install --root %{buildroot} --prefix %{_prefix} --no-deps \
	 --disable-pip-version-check --progress-bar off --verbose \
	 --ignore-installed --no-warn-script-location \
	 --no-index --no-cache-dir %{_pyproject_wheeldir}/`ls %{_pyproject_wheeldir}`
%else
%{pyproject_install}
%endif
 echo "Installed in %{buildroot}"
 find %{buildroot} -type d


%files -n python%{python3_pkgversion}-coriolis-pdk-ihpsg13g2-c4m
%doc README.rst
%license LICENSE
%dir %{python3_sitearch}/pdks
%{python3_sitearch}/pdks/ihpsg13g2_c4m
%{python3_sitearch}/coriolis_pdk_ihpsg13g2_c4m-%{dateVersion}.dist-info


%changelog
* Wed Nov  6 2024 Jean-Paul Chaput <Jean-Paul.Chaput@lip6.fr> - 2024.10.15-1
- Initial packaging.
