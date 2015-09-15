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
import getopt
import datetime
import MySQLdb

shortopts = 'h:U:W:d:p:a'
longopts = [ 'host=', 'username=', 'password=', 'dest=', 'port=', 'all', 'help', ]

def usage():
    pkgname = os.path.basename(sys.argv[0])
    print('''%(pkgname)s (C) 1999-2015, Raffaele Salmaso
This program is distribuited under the MIT/X license
You are not allowed to remove the copyright notice

Backup MySQL databases

usage: %(pkgname)s <options>

  options:
        --help = show this text
    -h, --host = the hostname (default=localhost)
    -U, --username = the user (default=postgres)
    -W, --password = the user password (default=None)
    -p, --port = the TCP port (default=5432)
    -d, --dest <dir> where to put backup files (default=.)
''' % { 'pkgname': pkgname })

def main():
    try:
        opts, pkgs = getopt.getopt(sys.argv[1:], shortopts, longopts)
    except getopt.GetoptError:
        usage()
        sys.exit(0)

    tm = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    user = 'root'
    host = 'localhost'
    passwd = ''
    dest = '.'
    port = '3306'
    all = False

    for o, a in opts:
        if o in ('-h', '--host'):
            host = a
        elif o in ('-U', '--user'):
            user = a
        elif o in ('-W', '--password'):
            password = a
        elif o in ('-p', '--port'):
            port = a
        elif o in ('-d', '--dest'):
            dest = a
        elif o in ('-a', '--all'):
            all = True
        elif o == '--help':
            usage()
            sys.exit(0)

    try:
        conn = MySQLdb.connect(user=user, passwd=passwd, host=host, db='') #user='%(user)s'" % { 'user': user, 'hostname': hostname});
    except Exception, e:
        sys.stderr.write('%s\n' % e)
        sys.stderr.write("I am unable to connect to the database\n")
        sys.exit(1)

    cur = conn.cursor()
    cur.execute("""show databases""")
    rows = cur.fetchall()
    print("\nBackup the MySQL databases:\n")
    os.system("""mkdir -p "%(dest)s/%(date)s/" """ % {
        'date': tm,
        'dest': dest,
    })

    if passwd:
        passwd = '--password=%s' % passwd
    if host:
        host = '--host=%s' % host
    if port:
        port = '--port=%s' % port

    for row in rows:
        print("   %s\n" % row[0])
        os.system("""/usr/bin/mysqldump --user=%(user)s %(host)s %(port)s %(passwd)s %(db)s | xz > "%(dest)s/%(date)s/%(db)s_%(date)s.db.xz" """ % {
            'db': row[0],
            'date': tm,
            'user': user,
            'host': host,
            'port': port,
            'dest': dest,
            'passwd': passwd,
        })

    if all:
        print("Dump all databases\n")
        os.system("""/usr/bin/mysqldump --all-databases --user=%(user)s %(host)s %(port)s %(passwd)s | xz > "%(dest)s/%(date)s/mysqldump_%(date)s.xz" """ % {
            'date': tm,
            'user': user,
            'host': host,
            'port': port,
            'dest': dest,
            'passwd': passwd,
        })

if __name__ == "__main__":
    main()
