%{!?dotnet_assembly_path: %define dotnet_assembly_path %{_datadir}/assembly}

%if 0%{?tizen_build_devel_mode}
%define BUILDCONF Debug
%else
%define BUILDCONF Release
%endif

Name:       csapi-network-iotconnectivity
Summary:    Tizen IoT Connectivity API for C#
Version:    1.0.0
Release:    1
Group:      Development/Libraries
License:    Apache-2.0
URL:        https://www.tizen.org
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

# Mono
BuildRequires: mono-compiler
BuildRequires: mono-devel

%if 0%{?_with_corefx}
AutoReqProv: no
BuildRequires: corefx-managed-32b-ref
%endif

# P/Invoke Build Requires
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(iotcon)

# C# API Requires
BuildRequires: csapi-tizen

%description
Tizen IoTConnectivity API for C#

%prep
%setup -q
cp %{SOURCE1} .

%define Assemblies Tizen.Network.IoTConnectivity

%build
for ASM in %{Assemblies}; do
xbuild $ASM/$ASM.csproj \
        /p:Configuration=%{BUILDCONF} \
        /p:ReferencePath=%{dotnet_assembly_path}
done

%install
# Assemblies
mkdir -p %{buildroot}%{dotnet_assembly_path}
for ASM in %{Assemblies}; do
install -p -m 644 $ASM/bin/%{BUILDCONF}/$ASM.dll %{buildroot}%{dotnet_assembly_path}
done

%files
%manifest %{name}.manifest
%attr(644,root,root) %{dotnet_assembly_path}/*.dll
%license LICENSE

