# encoding: utf-8
#
# RDIViewer, an application to view SAP-RDI datafiles.
# Copyright (C) 2006,2007,2008 Adi J. Sieker
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import ConfigParser
import os.path

class advFilterData(object):
    def __init__(self):
        self.name = ""

    def SetName(self, name):
        self.name = name
    def GetName(self):
        return self.name

class advFilterList(object):
    def __init__(self, file):
        self.file = file
        self.cp = ConfigParser.ConfigParser()
        self.__read_file()
        self.filters = None

    def __read_file(self):
        ret = ''
        if 0:
            type(self.cp, ConfigParser.ConfigParser)

        if os.path.exists(self.file) == True:
            ret = self.cp.read(self.file)
        #if os.path.exists(self.file) <> True:
            #raise OSError
        #ret = self.cp.read(self.file)
        print ret 

    def GetFilterNames(self):
        section_list = self.cp.sections()
        return section_list

    def GetFilterData(self, filter_name):
        fd = advFilterData()
        fd.SetName(filter_name)
        return fd
    
    def NewFilter(self, name):
        filter = advFilterData()
        filter.SetName(name)
        return filter