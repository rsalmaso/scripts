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

import os
import os.path
import sys

from stua import commands


class Command(commands.Command):
    @property
    def help(self):
        return """(C) Raffaele Salmaso
This program is distribuited under the MIT/X License
You are not allowed to remove the copyright notice

Uncompress multiple archive files with one command.

Can recognize these extensions: {}""".format(" ".join([format[0] for format in self.formats]))

    formats = [
        [".tar.bz", 'bzip -cd "%s" | tar xvf -'],
        [".bz", 'bzip -d "%s"'],
        [".tar.bz2", 'bzip2 -cd "%s" | tar xvf -'],
        [".bz2", 'bzip2 -d "%s"'],
        [".tar.xz", 'xz -cd "%s" | tar xvf -'],
        [".xz", 'xz -d "%s"'],
        [".tar.Z", 'tar Zxvf "%s"'],
        [".taz", 'tar Zxvf "%s"'],
        [".Z", 'gunzip "%s"'],
        [".tar.gz", 'tar zxvf "%s"'],
        [".tgz", 'tar zxvf "%s"'],
        [".bpp", 'tar zxvf "%s"'],
        [".etheme", 'tar zxvf "%s"'],
        [".tz", 'tar zxvf "%s"'],
        # ['.pax.gz', 'gunzip "%s" | cpio -i'],
        # ['.pax', 'cpio -i < "%s"'],
        [".pax.gz", 'gunzip "%s" | pax -r -pe'],
        [".pax", 'pax -r -pe -f "%s"'],
        [".gz", 'gunzip "%s"'],
        [".tar", 'tar xvf "%s"'],
        [".zip", 'unzip -C "%s"'],
        [".cbz", 'unzip -C "%s"'],
        [".epub", 'unzip -C "%s"'],
        [".xpi", 'unzip -C "%s"'],
        [".deb", 'alien -t -c -g "%s"'],
        [".rpm", 'alien -t -c -g "%s"'],
        [".dsc", 'dpkg-source -x "%s"'],
        [".rom", 'unzip -C "%s"'],
        [".rar", 'unrar x "%s"'],
        [".cbr", 'unrar x "%s"'],
        [".ace", 'unace e "%s"'],
        [".cab", 'cabextract "%s"'],
        [".jar", 'unzip -C "%s"'],
        [".war", 'unzip -C "%s"'],
        [".lha", 'lha x "%s"'],
        [".lhz", 'lha x "%s"'],
        [".7z", '7za x "%s"'],
        [".zipx", '7z x "%s"'],
        [".tar.zst", 'zstd -cd "%s" | tar xvf -'],
        [".zst", 'zstd -d "%s"'],
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "archive",
            nargs="+",
            help="archive(s)",
        )
        parser.add_argument(
            "dest",
            nargs="?",
            help="destination",
        )

    def handle(self, command, options):
        source = os.getcwd()
        dest = options.dest
        pkgs = options.archive

        if not os.path.isfile(pkgs[-1]):
            dest = pkgs[-1]
            pkgs = pkgs[:-1]
            if dest.endswith("/"):
                dest = dest[:-1]

        if dest is not None:
            if not os.path.exists(dest):
                os.makedirs(dest)
            os.chdir(dest)

        for pkg in pkgs:
            pkg = os.path.join(source, pkg)
            try:
                for row in self.formats:
                    suffix, action = row[0], row[1]
                    if pkg.endswith(suffix):
                        os.system(action % pkg)
                        raise StopIteration
                print("package type for %s not supported" % pkg)
            except StopIteration:
                pass


def main():
    cmd = Command()
    cmd.run(sys.argv)
