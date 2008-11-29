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

import os
import re
import wx
import codecs

import common

# file handlers
LEN_NEWLINE = len('\n')
def GetHandlerForFile(file):
    for handler_class in handler_list:
        handler = handler_class(file)
        if handler.CanHandle():
            return handler
    return None

class advFileHandler(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.doc_list = []
        self.doc_count = 0
        config = wx.ConfigBase_Get()
        self.default_encoding = config.Read(common.INI_CODECS_DEFAULT,'cp1250')
        self.data_cache = {}

    def ScanForDocuments(self):
        self.doc_count = 0
        return False

    def GetDocumentCount(self):
        return len(self.doc_list)

    def GetDocumentList(self):
        return self.doc_list

    def GetDocumentData(self,idx):
        try:
            return self.data_cache[idx]
        except:
            config = wx.ConfigBase_Get()
            item = self.doc_list[idx]
            default_encoding = config.Read(common.INI_CODECS_DEFAULT,'cp1250')
            if len(default_encoding) == 0:
                default_encoding = 'cp1250'

            fo = codecs.open(self.file_name, 'rb', default_encoding)
            fo.seek(item["begin"])
            length = item["end"] - item["begin"]
            self.data_cache[idx] = fo.read(length)
    
            return self.data_cache[idx]

    def __dataFromFile(self, data):
        return
    def GetColumns(self):
        return [
            {"label":'Name'
            },
            {"label":'Value'
            }
           ]
    def GetDocument(self, item):
        return None

    def GetDocumentFromData(self, data):
        return None

    def HasPrintAndPreview(self):
        return False

    def IsDocPreview(self,doc_id):
        return False

    def ChangeDocType(self,type):
        return True

# Progressdialog functions
    def _OpenFileHandle(self, file_name):
        return codecs.open(file_name, 'rb', self.default_encoding)
    def _StartProgress(self, max, text):
        self.progress_last_percent = 0
        self.progress_percent = max / 20
        self.dlg = wx.ProgressDialog("Progress dialog",
                               text,
                               max,
                               None,
                               wx.PD_CAN_ABORT | wx.PD_APP_MODAL )
#|                               wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME)

    def _UpdateProgress(self,count, text=None):
        keepGoing = True
        cur_percent = count / self.progress_percent
        if cur_percent <= self.progress_last_percent:
            return keepGoing

        self.progress_last_percent = cur_percent
        
        if text != None:
            keepGoing = self.dlg.Update(count, text)
        else:
            keepGoing = self.dlg.Update(count)
        return keepGoing

    def _StopProgress(self):
        self.dlg.Destroy()
        
class advSimpleRdiHandler(advFileHandler):
    def __init__(self, file_name):
        advFileHandler.__init__(self,file_name)
        
    def CanHandle(self):
        fo = self._OpenFileHandle(self.file_name)
        data = fo.read(200)
        if re.match("^H[0-9][0-9][0-9][A-Z]1", data):
            return True
        if re.match("^\^JOB SAPRDI", data):
            return True
        
        return False
        
    def ScanForDocuments(self):
        try:
            fo = self._OpenFileHandle(self.file_name)
            self._StartProgress(os.path.getsize(self.file_name)+10000, 'Text analyse')
            regex = re.compile("^H[0-9a-zA-Z]")
            bytes_read = 0
            doc_begin_offset = 0
            doc_description = ""
            first_doc_len = 0
            line = ""
            while not regex.match(line):
                line = fo.readline()
                bytes_read += len(line)
            
            doc_begin_offset = bytes_read - len(line)
            doc_description = line.rstrip('\r\n')
            for line in fo:
                if regex.match(line):
                    doc = {"name":doc_description, 
                           "begin":doc_begin_offset,
                           "end": bytes_read}
                    self.doc_list.append(doc)
                    doc_begin_offset = bytes_read
                    doc_description = line.rstrip('\n\r')

                bytes_read += len(line)
                
                keepGoing = self._UpdateProgress(bytes_read)
                if keepGoing == False:
                    self.doc_list = []
                    break
    
            doc = {"name":doc_description, 
                   "begin":doc_begin_offset,
                   "end": bytes_read}
            self.doc_list.append(doc)

            self._StopProgress()
        except:
            self._StopProgress()
        return False

    def HasPrintAndPreview(self):
        return True

    def GetDocument(self, item):
        return self.GetDocumentFromData(self.GetDocumentData(item))

    def GetDocumentFromData(self, data):
        return advSimpleRdiDocument(data)

    def IsDocPreview(self,doc_id):
        data = self.GetDocumentData(doc_id)
        header = data.splitlines()[0]
        if header[185] == 'X':
            return True
        return False

    def ChangeDocType(self,type, item):
        data = self.GetDocumentData(item)
        data = data.splitlines()
        header = data[0]
        hostname = os.getenv("COMPUTERNAME")

        hostname = hostname + ( ' ' * ( 10 - len(hostname)))

        header = header[:45] + hostname + header[55:]
        if type == 'print':
            header = header[:185] + ' ' + header[186:]
        elif type == 'preview':
            header = header[:185] + 'X' + header[186:]

        data[0] = header
        data = os.linesep.join(data)
        self.data_cache[item] = data

class advSimpleRdiDocument(object):
    def __init__(self, data):
        self.data = data.split("\n")

        self.root_nodes = []

        self._BuildTree()
    def getRootNodes(self):
        return self.root_nodes

    def _BuildTree(self):
        parents = {}
        last_node = None
        last_level = 0
        cur_level = 0
        regexps = self._GetLevelRegEx()
        for line in self.data:
            found = False
            for level, regexp in regexps:
                if regexp.match(line):
                    cur_level = level
                    found = True
                    break

            if found == False:
                continue
                
            try:
                if cur_level > 0:
                    parent = parents[cur_level-1]
            except:
                parent = None

            node = simpleRdiNode(line, cur_level, parent)
            parents[cur_level] = node
            if parent <> None:
                parent.addChild(node)
            if cur_level == 1:
                self.root_nodes.append(node)

    def _GetLevelRegEx(self):
        return [ (3,re.compile('^D.*')),
                 (2,re.compile('^CRDI-(CONTROL|INC) %%LINES-BEGIN.*')),
                 (1,re.compile('^H.*'))
               ]


class simpleRdiNode(object):
    def __init__(self,data,level, parent):
        self.children = []
        self.level = level
        self.data = data
        self.parent = parent
    def addChild(self,child):
        self.children.append(child)
    def getParent(self):
        return self.parent
    def getLevel(self):
        return self.level
    def getRawData(self):
        return self.data
    def getChildren(self):
        return self.children
    def getType(self):
        type = 'branch'

        if self.level == 3:
            type = 'leave'

        return type

    def getData(self,type):
        value = ""
        if type == 'name':
            if self.level == 1:
                regexp = "^H.{20}([\s\S]{16}).*"
                group = 1
            elif self.level == 2:
                regexp = "^CRDI-(CONTROL|INC).{15}([\S]+)[\s]+.*"
                group = 2
            elif self.level == 3:
                regexp = "^D([\S]*).*"
                group = 1

        elif type == 'value':
            if self.level == 1:
                regexp = "^(H.{58}).*"
                group = 1
            elif self.level == 2:
                regexp = "^CRDI-(CONTROL|INC).{15}([\S]+)([\s]+.*)"
                group = 3
            elif self.level == 3:
                regexp = "^D[\S]* (.*)"
                group = 1

        try:
            m = re.match(regexp, self.data)
            try:
                value = m.group(group)
                value = value.strip()
            except:
                pass
            if value == "":
                value = "<leeres Feld>"
        except:
            value = 'Unknown level'

        return value


class advRDIHandler(advFileHandler):
    def __init__(self, file_name):
        advFileHandler.__init__(self,file_name)
        
    def CanHandle(self):
        fo = self._OpenFileHandle(self.file_name)
        data = fo.read(200)
        if re.match("^H[0-9][0-9][0-9][A-Z]0", data):
            return True
        if re.match("^\^JOB SAPRDI", data):
            return True
        
        return False
        
    def ScanForDocuments(self):
        try:
            fo = self._OpenFileHandle(self.file_name)
            self._StartProgress(os.path.getsize(self.file_name)+10000, 'Text analyse')
            regex = re.compile("^H[0-9a-zA-Z]")
            bytes_read = 0
            doc_begin_offset = 0
            doc_description = ""
            first_doc_len = 0
            line = ""
            while not regex.match(line):
                line = fo.readline()
                bytes_read += len(line)
            
            doc_begin_offset = bytes_read - len(line)
            doc_description = line.rstrip('\r\n')
            for line in fo:
                if regex.match(line):
                    doc = {"name":doc_description, 
                           "begin":doc_begin_offset,
                           "end": bytes_read}
                    self.doc_list.append(doc)
                    doc_begin_offset = bytes_read
                    doc_description = line.rstrip('\n\r')

                bytes_read += len(line)
                
                keepGoing = self._UpdateProgress(bytes_read)
                if keepGoing == False:
                    self.doc_list = []
                    break
    
            doc = {"name":doc_description, 
                   "begin":doc_begin_offset,
                   "end": bytes_read}
            self.doc_list.append(doc)

            self._StopProgress()
        except:
            self._StopProgress()
        return False

    def GetDocument(self, item):
        return self.GetDocumentFromData(self.GetDocumentData(item))

    def GetDocumentFromData(self, data):
        return advRDIDocument(data)

    def HasPrintAndPreview(self):
        return True

    def IsDocPreview(self,doc_id):
        data = self.GetDocumentData(doc_id)
        header = data.splitlines()[0]
        if header[185] == 'X':
            return True
        return False

    def ChangeDocType(self,type, item):
        data = self.GetDocumentData(item)
        data = data.splitlines()
        header = data[0]
        hostname = os.getenv("COMPUTERNAME")

        hostname = hostname + ( ' ' * ( 10 - len(hostname)))

        header = header[:45] + hostname + header[55:]
        if type == 'print':
            header[185] = ' '
        elif type == 'preview':
            header[185] = 'X'

class advRDIDocument(object):
    def __init__(self, data):
        self.data = data.split("\n")

        self.root_nodes = []

        self._BuildTree()
    def getRootNodes(self):
        return self.root_nodes

    def _BuildTree(self):
        parents = {}
        last_node = None
        last_level = 0
        cur_level = 0
        regexps = self._GetLevelRegEx()
        for line in self.data:
            found = False
            for level, regexp in regexps:
                if regexp.match(line):
                    cur_level = level
                    found = True
                    break

            if found == False:
                continue
                
            try:
                if cur_level > 0:
                    parent = parents[cur_level-1]
            except:
                parent = None

            node = rdiNode(line, cur_level, parent)
            parents[cur_level] = node
            if parent <> None:
                parent.addChild(node)
            if cur_level == 1:
                self.root_nodes.append(node)

    def _GetLevelRegEx(self):
        return [ (3,re.compile('^D[A-Z]{4}[\S\s]{36}[A-Za-z].*')),
                 (2,re.compile('^CRDI-(CONTROL|INC) %%LINES-BEGIN.*')),
                 (1,re.compile('^H.*'))
               ]


class rdiNode(object):
    def __init__(self,data,level, parent):
        self.children = []
        self.level = level
        self.data = data
        self.parent = parent

    def addChild(self,child):
        self.children.append(child)

    def getParent(self):
        return self.parent

    def getLevel(self):
        return self.level

    def getRawData(self):
        return self.data

    def getChildren(self):
        return self.children
    
    def getType(self):
        type = 'branch'

        if self.level == 3:
            type = 'leave'

        return type

    def getData(self,type):
        if type == 'name':
            if self.level == 1:
                regexp = "^H.{20}([\s\S]{16}).*"
                group = 1
            elif self.level == 2:
                regexp = "^CRDI-(CONTROL|INC).{15}([\S]+)[\s]+.*"
                group = 2
            elif self.level == 3:
                regexp = "^D.{40}([\s\S]{100}).*"
                group = 1

        elif type == 'value':
            if self.level == 1:
                regexp = "^(H.{58}).*"
                group = 1
            elif self.level == 2:
                regexp = "^CRDI-(CONTROL|INC).{15}([\S]+)([\s]+.*)"
                group = 3
            elif self.level == 3:
                regexp = "^D.{174}(.*)"
                group = 1

        try:
            m = re.match(regexp, self.data)
            value = m.group(group)
            value = value.strip()
            if value == "":
                value = "<kein Daten>"
        except:
            value = 'Unknown level'

        return value


class advJetFormHandler(advFileHandler):
    def __init__(self, file_name):
        advFileHandler.__init__(self, file_name)
        
    def CanHandle(self):
        fo = self._OpenFileHandle(self.file_name)
        data = fo.read(200)
        if re.match("^\^job", data):
            return True
        
        return False

    def ScanForDocuments(self):
        fo = self._OpenFileHandle(self.file_name)
        regex = re.compile("^\^page 1")
        bytes_read = 0
        doc_begin_offset = 0
        doc_end_offset = 0
        doc_description = ""
        doc_open = False
        
        idx = 0
        for line in fo:
            if regex.match(line):
                if doc_open == True:
                  idx += 1
#                  doc_end_offset = bytes_read + len(line)
                  doc = {"name":doc_description, 
                         "begin":doc_begin_offset,
                         "end":bytes_read}
                  self.doc_list.append(doc)
                  doc_begin_offset = bytes_read + 1
                  doc_description = "%s %s" %(idx, line)
                else:
                    idx += 1
                    doc_open = True
                    doc_begin_offset = bytes_read
                    doc_description = "%s %s" %(idx, line)
            bytes_read += len(line)
            
        return False

handler_list = []
handler_list.append(advSimpleRdiHandler)
handler_list.append(advRDIHandler)
handler_list.append(advJetFormHandler)
