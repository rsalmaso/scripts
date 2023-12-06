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

try:
    import psycopg2
except ImportError:
    print("need psycopg2, please install it [pip install psycopg2]")
from stua import commands


class Command(commands.Command):
    help = """(C) Raffaele Salmaso
This program is distribuited under the MIT/X license
You are not allowed to remove the copyright notice

Backup PostgreSQL databases"""

    def add_arguments(self, parser):
        parser.add_argument(
            "-H",
            "--host",
            action="store",
            dest="host",
            default="localhost",
            help="the hostname",
        )
        parser.add_argument(
            "-u",
            "--user",
            action="store",
            dest="user",
            default="postgres",
            help="the user",
        )
        parser.add_argument(
            "-w",
            "--password",
            action="store",
            dest="user",
            help="",
        )
        parser.add_argument(
            "-p",
            "--port",
            action="store",
            dest="port",
            default=5432,
            help="the TCP port",
        )
        parser.add_argument(
            "-d",
            "--dest",
            action="store",
            dest="dest",
            default=".",
            help="where to put backup files",
        )
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            dest="all",
            default=False,
            help="dump all databases",
        )

    def handle(self, command, options):
        tm = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        user = options.user
        hostname = options.hostname
        password = options.password
        dest = options.dest
        port = options.port
        all = options.all

        try:
            conn = psycopg2.connect("dbname='template1' user='%(user)s'" % {"user": user, "hostname": hostname})
        except Exception as e:
            sys.stderr.write("%s\n" % e)
            sys.stderr.write("I am unable to connect to the database\n")
            sys.exit(1)

        cur = conn.cursor()
        cur.execute("""SELECT datname FROM pg_database WHERE datname not in ('template0', 'template1', 'postgres')""")
        rows = cur.fetchall()
        print("\nBackup the PostgreSQL databases:\n")
        os.system(
            """mkdir -p "%(dest)s/%(date)s/" """
            % {
                "date": tm,
                "dest": dest,
            }
        )
        for row in rows:
            print("   %s\n" % row[0])
            os.system(
                """pg_dump -U %(user)s %(db)s | xz > "%(dest)s/%(date)s/%(db)s_%(date)s.db.xz" """
                % {
                    "db": row[0],
                    "date": tm,
                    "user": user,
                    "hostname": hostname,
                    "dest": dest,
                }
            )

        if all:
            print("Dump all databases\n")
            os.system(
                """/usr/bin/pg_dumpall | xz > "%(dest)s/%(date)s/pg_dump_%(date)s.xz" """
                % {
                    "date": tm,
                    "user": user,
                    "hostname": hostname,
                    "dest": dest,
                }
            )


def main():
    cmd = Command()
    cmd.run(sys.argv)
