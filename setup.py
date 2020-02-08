# -*- coding: utf-8 -*-

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

from __future__ import absolute_import, division, print_function #, unicode_literals
import io
import os
from setuptools import setup
import scripts

setup(
    packages=["scripts"],
    include_package_data=True,
    name="scripts",
    version=scripts.__version__,
    description = io.open(os.path.join(os.path.dirname(__file__), "README.md"), "rU").read(),
    long_description="",
    author=scripts.__author__,
    author_email=scripts.__author_email__,
    url="https://bitbucket.org/rsalmaso/scripts",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
    entry_points={
        'console_scripts': [
            'cdblank = scripts.cdblank:main',
            'cdriso = scripts.cdriso:main',
            'cdwrite = scripts.cdwrite:main',
            'my-backup = scripts.my_backup:main',
            'pg-backup = scripts.pg_backup:main',
            'pkg = scripts.pkg:main',
            'unpkg = scripts.unpkg:main',
        ],
    },
    scripts=[
        'bin/myip',
        'bin/pycclean',
    ],
    install_requires=["stua"],
    zip_safe=False,
)
