vagrant_cloud
=============
Ruby client for the [Vagrant Cloud API](https://www.vagrantup.com/docs/vagrant-cloud/api.html).

[![Build Status](https://img.shields.io/travis/hashicorp/vagrant_cloud/master.svg)](https://travis-ci.org/hashicorp/vagrant_cloud)
[![Gem Version](https://img.shields.io/gem/v/vagrant_cloud.svg)](https://rubygems.org/gems/vagrant_cloud)


This client allows to create, modify and delete *boxes*, *versions* and *providers*.
The main entry point is an object referencing your *account*.

Usage
-----
Example usage:
```ruby
account = VagrantCloud::Account.new('<username>', '<access_token>')
box = account.ensure_box('my_box')
version = box.ensure_version('0.0.1')
provider = version.ensure_provider('virtualbox', 'http://example.com/foo.box')

version.release
puts provider.download_url
```

__NOTE:__ As of version 2.0.0, the CLI has been deprecated in favor of the `vagrant cloud`
command. More information about how to use the `vagrant cloud` command can be found
on the [Vagrant documentation](https://www.vagrantup.com/docs/cli/cloud.html).

Example CLI usage:
Create a version and provider within an existing Box, upload a file to be hosted by Vagrant Cloud, and release the version
```sh
vagrant_cloud create_version --username $USERNAME --token $VAGRANT_CLOUD_TOKEN --box $BOX_NAME --version $BOX_VERSION
vagrant_cloud create_provider --username $USERNAME --token $VAGRANT_CLOUD_TOKEN --box $BOX_NAME --version $BOX_VERSION
vagrant_cloud upload_file --username $USERNAME --token $VAGRANT_CLOUD_TOKEN --box $BOX_NAME --version $BOX_VERSION --provider_file_path $PACKAGE_PATH
vagrant_cloud release_version --username $USERNAME --token $VAGRANT_CLOUD_TOKEN --box $BOX_NAME --version $BOX_VERSION
```
If you installed vagrant_cloud with bundler, then you may have to invoke using `bundle exec vagrant_cloud`

Development & Contributing
--------------------------
Pull requests are very welcome!

Install dependencies:
```
bundle install
```

Run the tests:
```
bundle exec rspec
```

Check the code syntax:
```
bundle exec rubocop
```

Release a new version:

1. Bump the version in `vagrant_cloud.gemspec`, merge to master.
2. Push a new tag to master.
3. Release to RubyGems with `bundle exec rake release`.

History
-------
This gem has been developed and maintained by [Cargo Media](https://www.cargomedia.ch) since April 2014.
HashiCorp became the official maintainer in October 2017.
