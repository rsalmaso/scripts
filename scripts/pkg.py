# Copyright (C) Raffaele Salmaso <raffaele@salmaso.org>
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

import datetime
import os
import os.path
import sys

from stua import commands


class Command(commands.Command):
    help = """(C) Raffaele Salmaso
This program is distribuited under the MIT/X License
You are not allowed to remove the copyright notice

Create an archive file and (optionally) compress it."""

    default = "txz"
    formats = {
        "gz": {
            "help": "create a gzip archive",
            "cmd": lambda data: 'gzip "%(pkg)s"' % data,
        },
        "zip": {
            "help": "create a zip archive",
            "cmd": lambda data: 'zip -r "%(name)s".zip "%(pkg)s"' % data,
        },
        "cbz": {
            "help": "create a cbz archive",
            "cmd": lambda data: 'zip -r "%(name)s".cbz "%(pkg)s"' % data,
        },
        "tgz": {
            "help": "create a tar.gz archive",
            "cmd": lambda data: 'tar c "%(pkg)s" | gzip > "%(name)s".tar.gz' % data,
        },
        "bz2": {
            "help": "create a bz2 archive",
            "cmd": lambda data: 'bzip2 "%(pkg)s"' % data,
        },
        "tz2": {
            "help": "create a tar.bz2 archive",
            "cmd": lambda data: 'tar c "%(pkg)s" | bzip2 > "%(name)s".tar.bz2' % data,
        },
        "tz": {
            "help": "create a tar.zst archive",
            "cmd": lambda data: 'tar c "%(pkg)s" | zstd > "%(name)s".tar.zst' % data,
        },
        "tar": {
            "help": "create a tar archive",
            "cmd": lambda data: 'tar c "%(pkg)s" > "%(name)s".tar' % data,
        },
        "dmg": {
            "help": "create a dmg archive",
            "cmd": lambda data: 'hdiutil create -srcfolder "%(pkg)s" "%(pkg)s".dmg' % data,
        },
        "jar": {
            "help": "create a jar archive",
            "cmd": lambda data: 'cd "%(pkg)s" && zip -r ../"%(name)s".jar *' % data,
        },
        "xpi": {
            "help": "create an xpi archive",
            "cmd": lambda data: 'cd "%(pkg)s" && zip -r ../"%(name)s".xpi *' % data,
        },
        "epk": {
            "help": "create an epk archive",
            "cmd": lambda data: 'cd "%(pkg)s" && zip -r ../"%(name)s".epk *' % data,
        },
        "epub": {
            "help": "create an epub archive",
            "cmd": lambda data: 'cd "%(pkg)s" && zip -r ../"%(name)s".epub *' % data,
        },
        "btgz": {
            "help": "create a tar.gz archive (preserve permissions)",
            "cmd": lambda data: 'tar --create --preserve-permissions "%(pkg)s" | gzip > "%(name)s".tar.gz' % data,
        },
        "bbz2": {
            "help": "create a tar.bz2 archive (preserve permissions)",
            "cmd": lambda data: 'tar --create --preserve-permissions "%(pkg)s" | bzip2 > "%(name)s".tar.bz2' % data,
        },
        "txz": {
            "help": "create a tar.xz archive",
            "cmd": lambda data: 'tar c "%(pkg)s" | xz > "%(name)s".tar.xz' % data,
        },
        "xz": {
            "help": "create an xz archive",
            "cmd": lambda data: 'xz "%(pkg)s"' % data,
        },
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--tm",
            action="store_true",
            dest="timestamp",
            help="add a timestamp to filename",
        )
        for key in self.formats.keys():
            parser.add_argument(
                "--{}".format(key),
                action="store_true",
                dest=key,
                help=self.formats[key]["help"],
            )
        parser.add_argument(
            "dir",
            nargs="+",
            help="dir(s)",
        )

    def handle(self, command, options):
        tm = datetime.datetime.now().strftime("_%Y%m%d-%H%M%S") if options.get("timestamp") else ""

        commands = [self.formats[key]["cmd"] for key in self.formats.keys() if options.get(key)]
        if not commands:
            commands = [self.formats[self.default]["cmd"]]

        for pkg in options.get("dir"):
            if pkg.endswith("/"):
                pkg = pkg[:-1]
            pkgname = os.path.basename(pkg)
            if tm:
                pkgname += tm
            for cmd in commands:
                os.system(cmd({"name": pkgname, "pkg": pkg}))


def main():
    cmd = Command()
    cmd.run(sys.argv)
