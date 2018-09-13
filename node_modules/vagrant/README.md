Vagrant for Node.js
===================

This module is a programatic wrapper around the [`vagrant`](http://vagrantup.com) CLI tool.

__Note: `vagrant` must be installed to use this, it's only a wrapper__

Installation
------------

`npm i vagrant`

Usage
-----

All commands are run with `child_process.spawn` and the `stdio` is set to `inherit` passing along `process.env`.

```javascript

var vagrant = require('vagrant');

//From a dir with a Vagrantfile, this will ssh into the VM
vagrant.ssh(function(code) {
    //vagrant is done
});

vagrant.up(function(code) {
    //vagrant is done
});

//Arguments passed as an array
vagrant.init(['foo', 'http://foobar.com'], function(code) {
    //vagrant is done
});

```


Build Status
------------

[![Build Status](https://secure.travis-ci.org/davglass/vagrant.png?branch=master)](http://travis-ci.org/davglass/vagrant)

Node Badge
----------

[![NPM](https://nodei.co/npm/vagrant.png)](https://nodei.co/npm/vagrant/)
