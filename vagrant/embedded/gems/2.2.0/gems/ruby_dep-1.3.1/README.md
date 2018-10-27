# RubyDep

[![Gem Version](https://img.shields.io/gem/v/ruby_dep.svg?style=flat)](https://rubygems.org/gems/ruby_dep) [![Build Status](https://travis-ci.org/e2/ruby_dep.svg)](https://travis-ci.org/e2/ruby_dep)

## Description

RubyDep helps users avoid incompatible, buggy and insecure Ruby versions.

It's for gem owners to add to their runtime dependencies in their gemspec.

1. It automatically sets your gemspec's `required_ruby_version` based on rubies tested in your `.travis-yml`
2. It warns users of your project if they're using a buggy or vulnerable version of Ruby

NOTE: RubyDep uses it's own approach on itself. This means it can only be installed on Ruby versions tested here: [check out the Travis build status](https://travis-ci.org/e2/ruby_dep). If you need support for an different/older version of Ruby, open an issue with "backport" in the title and provide a compelling case for supporting the version of Ruby you need. 
When in doubt, open a new issue or [read the FAQ on the Wiki](https://github.com/e2/ruby_dep/wiki/FAQ).


## Problem 1: "Which version of Ruby does your project support?"

Your gem shouldn't (and likely doesn't) support all possible Ruby versions.

So you have to tell users which versions your gem supports.

But, there are at least 3 places where you list the Rubies you support:

1. Your gemspec
2. Your README
3. Your .travis.yml file
 
That breaks the principle of single responsibility.

Is it possible to just list the supported Rubies in just one place?

Yes. That's what RubyDep helps with.

## Solution to problem 1

Since Travis doesn't allow generated `.travis.yml` files, option 3 is the only choice.

With RubyDep, your gemspec's `required_ruby_version` can be automatically set based on which Rubies you test your gem on.

What about the README? Well, just insert a link to your Travis build status page!

Example: do you want to know which Ruby versions RubyDep can be installed on? Just look here: https://travis-ci.org/e2/ruby_dep

If you're running Travis builds on a Ruby you support (and it's not in the "allow failures" section), it means you support that version of Ruby, right?

RubyDep intelligently creates a version constraint to encompass Rubies listed in your `.travis.yml`.

## Usage (to solve Problem 1)

### E.g. in your gemspec file:

```ruby
  begin
    require "ruby_dep/travis"
    s.required_ruby_version = RubyDep::Travis.new.version_constraint
  rescue LoadError
    abort "Install 'ruby_dep' gem before building this gem"
  end

  s.add_development_dependency 'ruby_dep', '~> 1.1'
```

### In your `README.md`:

Replace your mentions of "supported Ruby versions" and just insert a link to your Travis build status page.

If users see their Ruby version "green" on Travis, they'll see those are the versions you support and test, right?

(Or, you can link to your project's rubygems.org page where the required Ruby version is listed).

### In your `.travis.yml`:

To add a "supported Ruby", simply add it to the Travis build. 

To test a Ruby version, but not treat it as "supported", simply add that version to the `allowed_failures` section.


## Problem 2: Users don't know they're using an obsolete/buggy/insecure version of Ruby

Users don't track news updates on https://ruby-lang.org, so they may not know their ruby has known bugs or even serious security vulnerabilities.

And sometimes, that outdated/insecure Ruby is bundled by their operation system to begin with!

## The solution to problem 2

RubyDep has a small "database" of Ruby versions with information about which are buggy and insecure.

If you like, your gem can use RubyDep to show those warnings - to encourage users to upgrade and protect them from nasty bugs or bad security holes.

This way, when most of the Ruby community has switched to newer versions, everyone can be more productive by having faster, more stable and more feature-rich tools. And less time will be wasted supporting obsolete versions that users simply don't know are worth upgrading.

This also helps users understand that they should nudge their hosting providers, managers and package maintainers to provided up-to-date versions of Ruby to that everyone can benefit.

### Usage (to solve Problem 2)

In your gemspec:

```ruby
s.add_runtime_dependency 'ruby_dep', '~> 1.1'
```

Somewhere in your library: 

```ruby
require 'ruby_dep/warnings'
RubyDep::Warning.show_warnings
ENV['RUBY_DEP_GEM_SILENCE_WARNINGS'] = '1' # to ignore repeating the warning if other gems use `ruby_dep` too
```

That way, as soon as there's a severe vulnerability discovered in Ruby (and RubyDep is updated), users will be notified quickly.


## Tips

1. To disable warnings, just set the following environment variable: `RUBY_DEP_GEM_SILENCE_WARNINGS=1`
2. If you want to support a newer version of Ruby, just add it to your `.travis.yml` (e.g. ruby-2.3.1)
3. To support an earlier version of Ruby, add it to your `.travis.yml` and release a new gem version.
4. If you want to support a range of Rubies, include the whole range without gaps in minor version numbers (e.g. 2.0, 2.1, 2.2, 2.3) and ruby_dep will use the whole range. (If there's a gap, older versions will be considered "unsupported").
5. If you want to drop support for a Ruby, remove it from the `.travis.yml` and just bump your gem's minor number (Yes! Bumping just the minor if fine according to SemVer).
5. If you just want to test a Ruby version (but not actually support it), put it into the `allow failures` part of your Travis build matrix. (ruby_dep ignores versions there).

When in doubt, open an issue and just ask.

## Roadmap

Pull Requests are welcome.

Plans include: reading supported Ruby from `.rubocop.yml` (`TargetRubyVersion` field).


## Development

Use `rake` to run tests.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/e2/ruby_dep.

## License

The gem is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
