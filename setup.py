#!/usr/bin/env python
# coding=utf-8

#
# A command-line Last.fm scrobbler and a now-playing status updater.
# Copyright (C) 2013  Никола "hauzer" Вукосављевић
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from    scrobbler   import  info
from    setuptools  import  setup, find_packages


setup(name              = "{}h".format(info.NAME),
      version           = info.VERSION,
      packages          = find_packages(),
      install_requires  = ["appdirs", "docopt", "lfmh"],
      entry_points      = {
        "console_scripts": [
            "scrobbler = scrobbler.scrobbler:main"
        ],
      },

      author            = info.AUTHOR,
      author_email      = "hauzer.nv@gmail.com",
      description       = "A command-line Last.fm scrobbler and a now-playing status updater.",
      long_description  = open("README.rst", "r").read(),
      license           = "GPLv3",
      url               = "https://github.com/{}/{}/".format(info.AUTHOR_NICK, info.NAME),
      # download_url      = "https://bitbucket.org/{}/{}/downloads".format(info.AUTHOR_NICK, info.NAME),
      
      classifiers = [
                     "Development Status :: 4 - Beta",
                     "Environment :: Console",
                     "Intended Audience :: End Users/Desktop",
                     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 3",
                    ],
      )

