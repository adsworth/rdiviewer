# encoding: utf-8

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