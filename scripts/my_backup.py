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
    import pymysql
except ImportError:
    print("need pymysql, please install it [pip install pymysql]")
from stua import commands


class Command(commands.Command):
    help = """(C) Raffaele Salmaso
This program is distribuited under the MIT/X license
You are not allowed to remove the copyright notice

Backup MySQL databases"""

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
            default="root",
            help="the user",
        )
        parser.add_argument(
            "-w",
            "--password",
            action="store",
            dest="user",
            default="",
            help="password",
        )
        parser.add_argument(
            "-p",
            "--port",
            action="store",
            dest="port",
            default=3306,
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
        tm = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        try:
            conn = pymysql.connect(
                user=user,
                passwd=password,
                host=hostname,
                db="",
            )
        except Exception as e:
            sys.stderr.write("%s\n" % e)
            sys.stderr.write("I am unable to connect to the database\n")
            sys.exit(1)

        cur = conn.cursor()
        cur.execute("""show databases""")
        rows = cur.fetchall()
        print("\nBackup the MySQL databases:\n")
        os.system(
            """mkdir -p "%(dest)s/%(date)s/" """
            % {
                "date": tm,
                "dest": dest,
            }
        )

        if password:
            password = "--password=%s" % password
        if hostname:
            hostname = "--host=%s" % hostname
        if port:
            port = "--port=%s" % port

        for row in rows:
            print("   %s\n" % row[0])
            os.system(
                """/usr/bin/mysqldump --user=%(user)s %(host)s %(port)s %(passwd)s %(db)s | xz > "%(dest)s/%(date)s/%(db)s_%(date)s.db.xz" """  # noqa: E501
                % {
                    "db": row[0],
                    "date": tm,
                    "user": user,
                    "host": hostname,
                    "port": port,
                    "dest": dest,
                    "passwd": password,
                }
            )

        if all:
            print("Dump all databases\n")
            os.system(
                """/usr/bin/mysqldump --all-databases --user=%(user)s %(host)s %(port)s %(passwd)s | xz > "%(dest)s/%(date)s/mysqldump_%(date)s.xz" """  # noqa: E501
                % {
                    "date": tm,
                    "user": user,
                    "host": hostname,
                    "port": port,
                    "dest": dest,
                    "passwd": password,
                }
            )


def main():
    cmd = Command()
    cmd.run(sys.argv)
