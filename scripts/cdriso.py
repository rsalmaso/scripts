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

import getopt
import os
import os.path
import sys

shortopts = "hql:"
longopts = ["help", "quiet", "label="]

exe = "mkisofs"
if os.uname()[0] == "Darwin":
    exe = "hdiutil"

cmdline = {
    "hdiutil": 'hdiutil makehybrid -ov -iso -hfs -joliet -udf -o "%s"',
    "mkisofs": (
        "mkisofs -allow-lowercase -relaxed-filenames -allow-multidot -allow-leading-dots "
        '-joliet -rational-rock -disable-deep-relocation -full-iso9660-filenames -output "%s"'
    ),
}

quietOption = {"hdiutil": "-quiet", "mkisofs": "-quiet"}
quietOptionDefault = {"hdiutil": "-verbose", "mkisofs": "-verbose"}
quiet = quietOptionDefault[exe]

labelOption = {"hdiutil": '-default-volume-name "%s"', "mkisofs": '-V "%s"'}
label = ""


def usage():
    pkgname = os.path.basename(sys.argv[0])
    print(
        """%s (C) Raffaele Salmaso, 2005 PaulTT
This program is distributed under the modified BSD License
You are not allowed to remove the copyright notice

usage: %s [options] source [image]
  - source = the root directory and
  - image  = the filename of iso file, if omitted <source>.iso will be used.

  options:
    -h, --help  = show this help
    -q, --quiet = don't show output
    -l, --label = label name for the volume, if not specified,
                  defaults to the last path component of <source>

The .iso image will create with RockRidge
and Joliet extension
"""
        % (pkgname, pkgname)
    )


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
    except getopt.GetoptError:
        usage()
        sys.exit(-1)

    for o, a in opts:
        if o in ("-q", "--quiet"):
            quiet = quietOption[exe]
        elif o in ("-l", "--label"):
            label = labelOption[exe] % a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)

    source = args[0]
    if source.endswith("/"):
        source = source[:-1]
    if label == "":
        label = labelOption[exe] % os.path.basename(source)
    if len(args) < 2:
        output = source + ".iso"
    else:
        output = args[1]
    source = '"' + source + '"'
    cmd = " ".join([cmdline[exe] % output, label, source])

    os.system(cmd)
