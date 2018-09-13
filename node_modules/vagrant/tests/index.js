var vows = require('vows'),
    assert = require('assert'),
    path = require('path'),
    vagrant = require('../lib/vagrant'),
    methods = vagrant.commands;

vagrant.bin(path.join(__dirname, 'bin', 'vagrant'));
vagrant.start = __dirname;

methods.push('config', 'bin', '_run', '_runWithArgs');

var tests = {
    'should export methods': {
        topic: function() {
            return vagrant;
        }
    },
    'should export start': {
        topic: function() {
            return vagrant.start;
        },
        'and it should be __dirname': function(s) {
            assert.equal(s, __dirname);
        }
    },
    'should export debug': {
        topic: function() {
            return vagrant.debug;
        },
        'and it should be false': function(s) {
            assert.isFalse(s);
        }
    },
    'should execute a command with no arguments': {
        topic: function() {
            var self = this;
            vagrant.ssh(function(code) {
                
                self.callback(null, code);
            });
        },
        'should exit with a 0': function(topic) {
            assert.equal(topic, 0);
        }
    },
    'should set debug': {
        topic: function() {
            vagrant.debug = true;
            return vagrant.debug;
        },
        'and it should be true': function(s) {
            assert.isTrue(s);
        }
    },
    'should execute a command with Array of arguments': {
        topic: function() {
            var self = this;
            vagrant.ssh(['--foo', 'bar'], function(code) {
                
                self.callback(null, code);
            });
        },
        'should exit with a 0': function(topic) {
            assert.equal(topic, 0);
        }
    },
    'should execute a command with single argument': {
        topic: function() {
            var self = this;
            vagrant.ssh('bar', function(code) {
                
                self.callback(null, code);
            });
        },
        'should exit with a 0': function(topic) {
            assert.equal(topic, 0);
        }
    }
};

methods.forEach(function(name) {
    tests['should export methods'][name] = function(v) {
        assert.isFunction(v[name]);
    };
});

vows.describe('vagrant').addBatch(tests).export(module);
