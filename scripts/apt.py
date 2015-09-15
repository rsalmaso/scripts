#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 1999-2015, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import os.path
import sys
import subprocess

def system(*args, **kwargs):
    env = kwargs.pop('env', None)
    return subprocess.call(list(args), env=env)

class Command(object):
    command = None
    cmd = []
    verbose_name = ''
    help_text = ''

    def __init__(self, apt):
        self.apt = apt
        self.name = self.command or self.__class__.__name__.lower()
    def run(self, params, *args, **kwargs):
        cmd = list(self.cmd)
        cmd.extend(params)
        system(*cmd)
    def parse(self, params):
        opts, args = self._parse(params)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.usage()
                sys.exit(0)
            else:
                self.parse_param(opt, arg)
    def help(self):
        print('''  %(name)s%(extra)s: %(help)s''' % {
            'name': self.name,
            'extra': self.verbose_name,
            'help': self.help_text,
        })

class GenCaches(Command):
    cmd = ['apt-cache', 'gencaches']
    verbose_name = ''
    help_text = '''Build both the package and source cache'''
class Showpkg(Command):
    cmd = ['apt-cache', 'showpgk']
    verbose_name = ''
    help_text = '''Show some general information for a single package'''
class Showsrc(Command):
    cmd = ['apt-cache', 'showsrc' ]
    verbose_name = ''
    help_text = '''Show source records'''
class Stats(Command):
    cmd = ['apt-cache', 'stats']
    verbose_name = ''
    help_text = '''Show some basic statistics'''
class Dump(Command):
    cmd = ['apt-cache', 'dump']
    verbose_name = ''
    help_text = '''Show the entire file in a terse form'''
class DumpAvail(Command):
    cmd = ['apt-cache', 'dumpavail']
    verbose_name = ''
    help_text = '''Print an available file to stdout'''
class Unmet(Command):
    cmd = ['apt-cache', 'unmet']
    verbose_name = ''
    help_text = '''Show unmet dependencies'''
class Search(Command):
    cmd = ['apt-cache', 'search']
    verbose_name = 'search a package name'
    help_text = '''Search a package name'''
class Show(Command):
    cmd = ['apt-cache', 'show']
    verbose_name = ''
    help_text = '''Show a readable record for the package'''
class Depends(Command):
    cmd = ['apt-cache', 'depends']
    verbose_name = ''
    help_text = '''Show raw dependency information for a package'''
class RDepends(Command):
    cmd = ['apt-cache', 'rdepends']
    verbose_name = ''
    help_text = '''Show reverse dependency information for a package'''
class PkgNames(Command):
    cmd = ['apt-cache', 'pkgnames']
    verbose_name = ''
    help_text = '''List the names of all packages in the system'''
class Dotty(Command):
    cmd = ['apt-cache', 'dotty']
    verbose_name = ''
    help_text = '''Generate package graphs for GraphViz'''
class Xvcg(Command):
    cmd = ['apt-cache', 'xvcg']
    verbose_name = ''
    help_text = '''Generate package graphs for xvcg'''
class Policy(Command):
    cmd = ['apt-cache', 'policy']
    verbose_name = ''
    help_text = '''Show policy settings'''

class Refresh(Command):
    cmd = ['apt-get', 'update', '&&', 'apt-get', 'dist-upgrade', '-dy']
    verbose_name = ''
    help_text = '''Refresh packages'''
class Install(Command):
    cmd = ['apt-get', 'install']
    verbose_name = ''
    help_text = '''Install new packages (pkg is libc6 not libc6.deb)'''
class Update(Command):
    cmd = ['apt-get', 'update']
    verbose_name = ''
    help_text = '''Retrieve new lists of packages'''
class Upgrade(Command):
    cmd = ['apt-get', 'update']
    verbose_name = ''
    help_text = '''Perform an upgrade'''
class DistUpgrade(Command):
    cmd = ['apt-get', 'dist-upgrade']
    command = 'dist-upgrade'
    verbose_name = ''
    help_text = '''Distribution upgrade'''
class Remove(Command):
    cmd = ['apt-get', 'remove']
    verbose_name = ''
    help_text = '''Remove packages'''
class AutoRemove(Command):
    cmd = ['apt-get', 'autoremove']
    verbose_name = ''
    help_text = '''Remove automatically all unused packages'''
class Purge(Command):
    cmd = ['apt-get', 'remove', '--purge']
    verbose_name = ''
    help_text = '''Remove packages and config files'''
class Clean(Command):
    cmd = ['apt-get', 'clean']
    verbose_name = ''
    help_text = '''Erase downloaded archive files'''
class AutoClean(Command):
    cmd = ['apt-get', 'autoclean']
    verbose_name = ''
    help_text = '''Erase old downloaded archive files'''
class Check(Command):
    cmd = ['apt-get', 'check']
    verbose_name = ''
    help_text = '''Verify that there are no broken dependencies'''
class ChangeLog(Command):
    cmd = ['apt-get', 'changelog']
    verbose_name = ''
    help_text = '''Download and display the changelog for the given package'''
class Download(Command):
    cmd = ['apt-get', 'download']
    verbose_name = ''
    help_text = '''Download the binary package into the current directory'''

class AddKey(Command):
    cmd = ['apt-key', 'add']
    verbose_name = ''
    command = 'add-key'
    help_text = '''add the key contained in <file> ('-' for stdin)'''
class DelKey(Command):
    cmd = ['apt-key', 'del']
    verbose_name = ''
    command = 'del-key'
    help_text = '''remove the key <keyid>'''
class ImportKey(Command):
    cmd = ['apt-key', 'adv', '--keyserver', 'keyserver.ubuntu.com', '--recv-keys']
    verbose_name = ''
    command = 'import-key'
    help_text = '''import a ppa gpg key'''
class AdvKey(Command):
    cmd = ['apt-key', 'adv']
    verbose_name = ''
    command = 'adv-key'
    help_text = '''pass advanced options to gpg (download key)'''
class UpdateKey(Command):
    cmd = ['apt-key', 'del', '--keyserver', 'keyserver.ubuntu.com', '--recv-keys']
    verbose_name = ''
    command = 'update-key'
    help_text = '''update keys using the keyring package'''
class ListKey(Command):
    cmd = ['apt-key', 'list']
    verbose_name = ''
    command = 'list-keys'
    help_text = '''list keys'''
class FingerKey(Command):
    cmd = ['apt-key', 'finger']
    verbose_name = ''
    command = 'finger-key'
    help_text = '''list fingerprints'''
class ExportKey(Command):
    cmd = ['apt-key', 'export']
    verbose_name = ''
    command = 'export-key'
    help_text = '''output the key <keyid>'''
class ExportKeys(Command):
    cmd = ['apt-key', 'exportall']
    verbose_name = ''
    command = 'export-keys'
    help_text = '''output all trusted keys'''

class AddRepository(Command):
    cmd = ['apt-add-repository']
    verbose_name = ' <sourceline>'
    command = 'add-repository'
    help_text = '''The apt repository source line to add. This is one of:
    a complete apt line in quotes,
    a repo url and areas in quotes (areas defaults to 'main')
    a PPA shortcut.
'''
class RemoveRepository(Command):
    cmd = ['apt-add-repository', '--remove']
    verbose_name = ' <sourceline>'
    command = 'remove-repository'
    help_text = '''add the key contained in <file> ('-' for stdin)'''

class Help(Command):
    def run(self, *args, **kwargs):
        pkgname = os.path.basename(sys.argv[0])
        print('''%(pkgname)s (C) 1999-2015, Raffaele Salmaso
This program is distribuited under the MIT License
You are not allowed to remove the copyright notice

Wrapper for apt-cache, apt-get, apt-key, apt-add-repository.

usage: %(pkgname)s <command> [options] args
''' % {'pkgname': pkgname})
        for name in sorted(self.apt.commands.keys()):
            self.apt.commands[name].help()
    def help(self):
        pass

COMMANDS = [
    Help,

    # apt-cache
    GenCaches, Showpkg, Showsrc, Stats, Dump, DumpAvail, Unmet,
    Search, Show, Depends, RDepends, PkgNames, Dotty, Xvcg, Policy,
    # apt-get
    Install, Update, Upgrade, DistUpgrade, Remove, AutoRemove, Purge,
    Clean, AutoClean, Check, ChangeLog, Download,

    # custom apt-get
    Refresh,

    # apt-key
    AddKey, DelKey, ImportKey, AdvKey, UpdateKey, ListKey, FingerKey,
    ExportKey, ExportKeys,

    # apt-add-repository
    AddRepository, RemoveRepository,
]
class Apt(object):
    def __init__(self):
        self.commands = {}
        for command in COMMANDS:
            name = command.command or command.__name__.lower()
            cmd = command(self)
            self.commands[name] = cmd

    def run(self, args):
        try:
            name = args[0]
        except (KeyError, IndexError):
            name = 'help'
        self.commands[name].run(args[1:])

def main():
    apt = Apt()
    apt.run(sys.argv[1:])

if __name__ == "__main__":
    main()
