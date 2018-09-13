/*
 * Copyright (c) 2013, Yahoo! Inc. All rights reserved.
 * Copyrights licensed under the New BSD License.
 * See the accompanying LICENSE file for terms.
 */

var fs = require('fs'),
    path = require('path');

exports.exists = fs.exists || path.exists;
exports.existsSync = fs.existsSync || path.existsSync;

var find = function(dir, file, cb) {
    var files, found,
    next = path.join(dir, '../');

    try {
        files = fs.readdirSync(dir);
    } catch (e) {
        files = [];
    }

    found = files.some(function(f) {
        if (f === file) {
            cb(null, path.join(dir, f));
            return true;
        }
    });

    if (!found) {
        if (dir === next) {
            cb('not found', null);
            return;
        }
        find(next, file, cb);
    }
};

exports.find = find;
