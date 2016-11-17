%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from shoulda-3.5.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name shoulda

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 3.5.0
Release: 5%{?dist}
Summary: Making tests easy on the fingers and eyes
Group: Development/Languages
License: MIT
URL: https://github.com/thoughtbot/shoulda
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix test suite to work with Rails 4.1 and locally installed gems.
Patch0: rubygem-shoulda-3.5.0-test-fixes.patch

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
Requires:      %{?scl_prefix}rubygem(shoulda-context) < 2
Requires:      %{?scl_prefix}rubygem(shoulda-context) >= 1.0.1
Requires:      %{?scl_prefix}rubygem(shoulda-matchers) >= 1.4.1
Requires:      %{?scl_prefix}rubygem(shoulda-matchers) < 3.0
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(aruba)
BuildRequires: %{?scl_prefix}rubygem(cucumber)
BuildRequires: %{?scl_prefix}rubygem(rails)
BuildRequires: %{?scl_prefix}rubygem(shoulda-context)
BuildRequires: %{?scl_prefix}rubygem(shoulda-matchers)
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildRequires: %{?scl_prefix}rubygem(gherkin)
BuildRequires: %{?scl_prefix}rubygem(rspec-rails)
BuildRequires: %{?scl_prefix}rubygem(ffi)
BuildRequires: %{?scl_prefix}rubygem(multi_test)
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Making tests easy on the fingers and eyes.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix wrong-file-end-of-line-encoding for rpmlint.
sed -i 's/\r$//' %{buildroot}%{gem_instdir}/MIT-LICENSE

%check
cp .%{gem_spec} .%{gem_instdir}/shoulda.gemspec

pushd .%{gem_instdir}
# Relax version dependencies.
sed -i -r 's/(dependency\(%q<.*>), \[".*"\]/\1/' shoulda.gemspec

# Drop useless dependency.
sed -i '/appraisal/d' shoulda.gemspec

# rspec-rails 3.x compatibility.
# https://github.com/thoughtbot/shoulda/pull/257

# -fs option was removed from RSpec.
sed -i '/SPEC_OPTS=-fs/ s/fs/fd/' features/rails_integration.feature

# RSpec Rails use rails_helper now.
# https://github.com/rspec/rspec-rails/tree/3-3-maintenance/features/upgrade#default-helper-files-created-in-rspec-3x-have-changed
sed -i 's/spec_helper/rails_helper/' features/rails_integration.feature

%{?scl:scl enable %{scl} - << \EOF}
cucumber
%{?scl:EOF}
popd

%files
%doc %{gem_instdir}/MIT-LICENSE
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Appraisals
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/features
%{gem_instdir}/gemfiles
%{gem_instdir}/shoulda.gemspec

%changelog
* Fri Apr 08 2016 Pavel Valena <pvalena@redhat.com> - 3.5.0-5
- Enable tests
- Add missing dependencies to BuildRequires (for tests)

* Mon Feb 29 2016 Pavel Valena <pvalena@redhat.com> - 3.5.0-4
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 26 2014 Vít Ondruch <vondruch@redhat.com> - 3.5.0-1
- Update to Shoulda 3.5.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 2.11.3-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 2.11.3-4
- Rebuilt for Ruby 1.9.3.

* Sun Jan 08 2012 <stahnma@fedoraproject.org> - 2.11.3-2
- Jumped in to help with FTBFS bz#715949

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 01 2010 Michael Stahnke <stahnma@fedoraproject.org> - 2.11.3-1
- New version
- Fix many broken tests 
- Split into -doc package

* Sat Jan  9 2010 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.10.2-2
- Fix BuildRequires
- First package
