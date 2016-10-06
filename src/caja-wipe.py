 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Caja Wipe - Extension for Caja to wipe files and/or free disk space.
# Copyright (C) 2016 Caja Wipe authors.
# Dual-licensed under the GPLv2 (or, at your option, any later version) and
# custom licensing terms:
# GPL v2:
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Custom license terms:
#   You are hereby granted a perpetual, irrevocable license to copy, modify,
#   publish, release, and distribute this program as you see fit. However,
#   under no circumstances may you claim original authorship of this program;
#   you must credit the original author(s). You may not remove the listing of
#   the original author(s) from the source code, though you may change the
#   licensing terms. If you publish or release binaries or similarly compiled
#   files, you must credit the author(s) on your home and/or distribution page,
#   whichever applies. In your documentation, you must credit the author(s) for
#   the portions of their code you have used. This, of course, does not revoke
#   or change your right to claim original authorship to any portions of the
#   code that you have written.
#
#   You must agree to assume all liability for your use of the program, and to
#   indemnify and hold harmless the author(s) of this program from any liability
#   arising from use of this program, including, but not limited to: loss of
#   data, death, dismemberment, or injury, and all consequential and
#   inconsequential damages.
#
#   For clarification, contact Fred Barclay:
#       https://github.com/Fred-Barclay
#       BugsAteFred@gmail.com

import os
import subprocess
from gi.repository import Caja, GObject
from gettext import ngettext

class CajaWipe(GObject.GObject, Caja.MenuProvider):
	'''Simple Caja extension to wipe files, using the secure-delete suite.'''
	def __init__(self):
		pass

	# Choosing the file/directory
	def get_file_items(self, window, files):
		'''Returns the menu items to display when one or more files/folders are
		selected.'''

		# I need this in wipe_file
		global filelist
		global pwd

		pwd = None # is this necessary?
		filelist = []
		for file in files:
			if pwd == None: # first file: find path to directory
				pwd = file.get_parent_location().get_path()
			name = file.get_name()
			filelist += [name]

		if pwd == None or len(filelist) == 0:
			return

		# Make sure that the user has write permissions in this directory
		if not os.access(pwd, os.W_OK):
			return

		# If we're erasing only directories
		if file.is_directory():
			item = Caja.MenuItem(
				name='SimpleMenuExtension::Wipe_Directories',
				label=ngettext('_Wipe this folder', '_Wipe these folders', len(files)),
				tip=ngettext('Wipe this folder', 'Wipe these folders', len(files))
			)
			item.connect('activate', self.wipe_file, file)
			return [item]

		# If we're erasing pnly files, or both files and directories
		else:
			item = Caja.MenuItem(
				name='SimpleMenuExtension::Wipe_File',
				label=ngettext('_Wipe this file', '_Wipe these files', len(files)),
				tip=ngettext('Wipe this file', 'Wipe these files', len(files))
			)
			item.connect('activate', self.wipe_file, file)
			return [item]

	# Aaaannnnnndddddd....... ACTION!
	def wipe_file(self, menu, file):
		for filename in filelist:
			path = pwd+"/"+filename
			# path = str(path)
			if not os.access(path, os.W_OK):
				print("You do not have permission to wipe this file") # Debugging
				return
			print(path) # Debugging
			cmd = [ "srm", "-rv", path ]
			subprocess.call(cmd)
