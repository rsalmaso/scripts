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

shortopts = "hfad:s:eql"
longopts = ["help", "fast", "all", "device=", "speed=", "eject", "quiet", "list", "dummy"]


class App:
    def __init__(self, cmdline, blank, device, speed, verify, eject, quiet, dummy, list):
        self._cmdline = cmdline
        self._blank = blank
        self._device = device
        self._speed = speed
        self._eject = eject
        self._quiet = quiet
        self._dummy = dummy
        self._list = list

    def __call__(self):
        return " ".join(
            [self._cmdline, self._blank, self._device, self._speed, self._eject, self._quiet, self._dummy, self._list]
        )


class HdiUtil(App):
    def __init__(self):
        App.__init__(
            self,
            cmdline="hdiutil burn",
            blank="-erase",
            device="",
            speed="",
            verify="-noverifyburn",
            eject="-noeject",
            quiet="-verbose",
            dummy="",
            list="",
        )

    def device(self, device):
        self._device = "-device %s" % device

    def speed(self, speed):
        self._speed = "-speed %s" % speed

    def blank(self, t):
        if t == "fast":
            self._blank = "-erase"
        else:
            self._blank = "-fullerase"

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
        self._blank = ""
        self._eject = ""
        self._quiet = ""
        self._dummy = ""
        self._list = "-list"


class Cdrecord(App):
    def __init__(self):
        App.__init__(
            self,
            cmdline="cdrecord immed",
            blank="-erase",
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

    def blank(self, t):
        if t == "fast":
            self._blank = "blank=fast"
        else:
            self._blank = "blank=disk"

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
    exe = Cdrecord()


def usage():
    pkgname = os.path.basename(sys.argv[0])
    print(
        """%s Raffaele Salmaso
This program is distributed under the MIT/X License
You are not allowed to remove the copyright notice

This program allows to blank a cd/dvd from commandline. It
supports MacOsX hdiutil and the ubiquitous cdrecord.

usage: %s [option]
  options:
    -h, --help = show this help
    -f, --fast = erase only TOC [default]
    -a, --all = completely erase all disk
    -d, --device [default]
    -s, --speed <1, 2, 4, 8, max [default]>
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

    for o, a in opts:
        if o in ("-a", "--all"):
            exe.blank("full")
        elif o in ("-f", "--fast"):
            exe.blank("fast")
        elif o in ("-d", "--device"):
            exe.device(a)
        elif o in ("-s", "--speed"):
            exe.speed()
        elif o in ("-q", "--quiet"):
            exe.quiet()
        elif o in ("-e", "--eject"):
            exe.eject()
        elif o in ("-l", "--list"):
            exe.list()
        elif o == "--dummy":
            exe.dummy()
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)

    os.system(exe())
