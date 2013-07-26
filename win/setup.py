#
# A command-line Last.fm scrobbler and a now-playing status updater.
# Copyright (C) 2013  Nikola "hauzer" Vukosavljević
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


from cx_Freeze import setup, Executable
import requests.certs


build_exe_options = {"include_files": [(requests.certs.where(), 'cacert.pem')]}

setup(name          = "scrobbler",
      version       = "1.0.3",
      description   = "My GUI application!",
      options       = {"build_exe": build_exe_options},
      executables   = [Executable("../scrobbler.py")])
