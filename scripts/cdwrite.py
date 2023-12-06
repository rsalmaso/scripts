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

shortopts = "hd:s:veql"
longopts = ["help", "device=", "speed=", "verify", "eject", "quiet", "list", "dummy"]


class App:
    def __init__(self, cmdline, device, speed, verify, eject, quiet, dummy, list):
        self._cmdline = cmdline
        self._device = device
        self._speed = speed
        self._verify = verify
        self._eject = eject
        self._quiet = quiet
        self._dummy = dummy
        self._list = list

    def __call__(self, args):
        return " ".join(
            [
                self._cmdline,
                self._device,
                self._speed,
                self._verify,
                self._eject,
                self._quiet,
                self._dummy,
                self._list,
                '"' + args + '"',
            ]
        )


class HdiUtil(App):
    def __init__(self):
        App.__init__(
            self,
            cmdline="hdiutil burn",
            device="",
            speed="",
            verify="-noverifyburn",
            eject="-noeject",
            quiet="",
            dummy="",
            list="",
        )

    def device(self, device):
        self._device = "-device %s" % device

    def speed(self, speed):
        self._speed = "-speed %s" % speed

    def verify(self):
        self._verify = "-verifyburn"

    def eject(self):
        self._eject = "-eject"

    def quiet(self):
        self._quiet = "-quiet"

    def dummy(self):
        self._dummy = "-testburn"

    def list(self):
        """hdiutil -list must be the only option"""
        self._device = ""
        self._speed = ""
        self._verify = ""
        self._eject = ""
        self._quiet = ""
        self._dummy = ""
        self._list = "-list"


class Cdrecord(App):
    def __init__(self):
        App.__init__(
            self,
            cmdline="cdrecord immed",
            device="dev=/dev/cdrom",
            speed="",
            verify="",
            eject="",
            quiet="-v",
            dummy="",
            list="",
        )

    def device(self, device):
        self._device = "dev=%s" % device

    def speed(self, speed):
        self._speed = "speed=%s" % speed

    def verify(self):
        self._verify = ""

    def eject(self):
        self._eject = "-eject"

    def quiet(self):
        self._quiet = ""

    def dummy(self):
        self._dummy = "-dummy"

    def list(self):
        self._device = ""
        self._speed = ""
        self._blank = ""
        self._eject = ""
        self._quiet = ""
        self._dummy = ""
        self._list = "-scanbus"


class Wodim(App):
    def __init__(self):
        App.__init__(
            self, cmdline="wodim", device="dev=/dev/cdrom", speed="", verify="", eject="", quiet="-v", dummy="", list=""
        )

    def device(self, device):
        self._device = "dev=%s" % device

    def speed(self, speed):
        self._speed = "speed=%s" % speed

    def verify(self):
        self._verify = ""

    def eject(self):
        self._eject = "-eject"

    def quiet(self):
        self._quiet = ""

    def dummy(self):
        self._dummy = "-dummy"

    def list(self):
        self._device = ""
        self._speed = ""
        self._blank = ""
        self._eject = ""
        self._quiet = ""
        self._dummy = ""
        self._list = "-scanbus"


if os.uname()[0] == "Darwin":
    exe = HdiUtil()
else:
    exe = Wodim()


def usage():
    pkgname = os.path.basename(sys.argv[0])
    print(
        """%s (C) Raffaele Salmaso
This program is distributed under the MIT/X License
You are not allowed to remove the copyright notice

usage: %s [options] <file.iso>
  - file.iso = the file to write on disk

  options:
    -h, --help = show this text
    -d, --device <path of the device>
    -s, --speed <1, 2, 4, 8, max [default]>
    -v, --verify = verify disk after writing [default=no]
    -e, --eject = eject disk after burning [default=no]
    -q, --quiet = no progress output will be provided
    -l, --list = list all burning devices, for --device
        --dummy = don't turn on laser
"""
        % (pkgname, pkgname)
    )


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
    except getopt.GetoptError:
        usage()
        sys.exit(-1)

    dolist = False
    for o, a in opts:
        if o in ("-d", "--device"):
            exe.device(a)
        elif o in ("-s", "--speed"):
            exe.speed(a)
        elif o in ("-v", "--verify"):
            exe.verify()
        elif o in ("-e", "--eject"):
            exe.eject()
        elif o in ("-l", "--list"):
            exe.list()
            dolist = True
        elif o in ("-q", "--quiet"):
            exe.quiet()
        elif o == "--dummy":
            exe.dummy()
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)

    if len(args) > 0:
        if os.path.isfile(args[0]):
            os.system(exe(args[0]))
            sys.exit(0)
        else:
            print('"%s" is not a file' % args[0])
    elif dolist:
        # dolist : doesn't need a file to be burn
        os.system(exe(""))
    else:
        print("You must provide a file to burn")
    sys.exit(-1)
