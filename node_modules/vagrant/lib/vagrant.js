/*
 * Copyright (c) 2013, Yahoo! Inc. All rights reserved.
 * Copyrights licensed under the New BSD License.
 * See the accompanying LICENSE file for terms.
 */

var util = require('./util');
var spawn = require('child_process').spawn;

var which = require('which');
var path = require('path');

var _bin = null;
var _dir = null;

exports.debug = false;

exports.start = process.cwd();

var bin = exports.bin = function (b) {
    if (b) {
        _bin = b;
    }
    if (!_bin) {
        try {
            _bin = which.sync('vagrant');
            if (exports.debug) {
                console.log('using', _bin);
            }
        } catch (e) {
            throw('could not find vagrant bin in path, is it installed?');
        }
    }
    return _bin;
};


var config = exports.config = function(cb) {
    if (_dir) {
        return cb(null, _dir);
    }
    util.find(exports.start, 'Vagrantfile', function(err, file) {
        if (err) {
            throw err;
        }
        if (exports.debug) {
            console.log('using', file);
        }
        _dir = path.dirname(file);
        cb(null, _dir);
    });
};


var commands = [
    'box',
    'destroy',
    'halt',
    'init',
    'package',
    'plugin',
    'provision',
    'reload',
    'resume',
    'ssh',
    'ssh-config',
    'status',
    'suspend',
    'up'
];

exports.commands = commands;

var run = function(args, cb) {
    if (exports.debug) {
        console.log('proxying:', '"vagrant', args[0] + '"');
    }
    config(function(err, cwd) {
        if (exports.debug) {
            console.log('   ', bin(), args);
            console.log('   in ', cwd);
        }
        var child = spawn(bin(), args, {
            cwd: cwd,
            env: process.env,
            stdio: 'inherit'
        });

        child.on('exit', function(code) {
            cb(code);
        });
    });
};

var runWithArgs = function(name) {
    return function(args, cb) {
        if (cb === undefined) {
            cb = args;
            args = null;
        }
        if (!cb) {
            throw('callbacks are required!');
        }
        if (args) {
            if (!Array.isArray(args)) {
                args = [args];
            }
            args.unshift(name);
        } else {
            args = [name];
        }
        run(args, cb);
    };
};

exports._run = run;
exports._runWithArgs = runWithArgs;


commands.forEach(function(name) {
    exports[name] = runWithArgs(name);
});

