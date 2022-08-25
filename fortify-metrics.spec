Summary: Get metrics on efficacy of _FORTIFY_SOURCE on a program
Name: fortify-metrics
Version: 0.1
Release: 1
URL: https://github.com/siddhesh/fortify-metrics
Source0: %{name}-%{version}.tar.gz

License: MIT

# We need to generate configure scripts because upstream does it at release
# time.
BuildRequires: gcc-c++
BuildRequires: gcc-plugin-devel
Requires: python3

%description

fortify-metrics is a set of tools that allow developers to inspect their
programs to determine how effective -D_FORTIFY_SOURCE has been in fortifying
them.

%prep
%autosetup

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} BINDIR=%{_bindir} LIBDIR=%{_libdir}

%files

%{_bindir}/fortify-metrics.py
%{_libdir}/fmetrics.so

%changelog
* Wed Aug 24 2022 Siddhesh Poyarekar <siddhesh@redhat.com> - 0.1.0-1
- New package
