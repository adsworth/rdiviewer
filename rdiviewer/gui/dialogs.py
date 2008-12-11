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
import sys

import wx
import  wx.lib.filebrowsebutton as filebrowse

import rdiviewer.common as common

def _set_control_gap(sizer):
    sizer.SetHGap(10)
    sizer.SetVGap(2)

class AboutDialog(wx.Dialog):
    def __init__(
            self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize,  
            style=wx.DEFAULT_DIALOG_STYLE
            ):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI dialog using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, u"About", pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Author:")
        box.Add(label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        label = wx.StaticText(self, -1, u"Adi Jörg Sieker")
        box.Add(label, 1, wx.ALIGN_LEFT|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, u"Version:")
        box.Add(label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        label = wx.StaticText(self, -1, common.version)
        box.Add(label, 1, wx.ALIGN_LEFT|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, u"Homepage:")
        box.Add(label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        label = wx.StaticText(self, -1, u"http://www.sieker.info/")
        box.Add(label, 1, wx.ALIGN_LEFT|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, u"Environment:")
        box.Add(label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        label = wx.StaticText(self, -1, wx.VERSION_STRING + "," + sys.version.split(' ')[0])
        box.Add(label, 1, wx.ALIGN_LEFT|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, u"Copyright:")
        box.Add(label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        label = wx.StaticText(self, -1, u"Adi Jörg Sieker 2004-2008")
        box.Add(label, 1, wx.ALIGN_LEFT|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        box = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, wx.ID_OK, " OK ")
        btn.SetDefault()
        box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)

class PreferencesDialog(wx.Dialog):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, 
            style=wx.DEFAULT_DIALOG_STYLE):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI dialog using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, u"Preferences", pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # Now continue with the normal construction of the dialog
        # contents
        self._DefineControlAndEvents()

    def SetData(self, data):
        self.data = data
    
    def _GetPanel(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        #INI_SPOOL_DIR = "/Spool/Directory"
        self.spool_dir_dbb = filebrowse.DirBrowseButton(
            self, -1, size=(400, -1), labelText = u"Spoolverzeichnis:", buttonText = u"Auswählen", 
            startDirectory = wx.ConfigBase_Get().Read(common.INI_SPOOL_DIR, ""),changeCallback = self.OnSpoolDirCallback
            )
        sizer.Add(self.spool_dir_dbb, 1, wx.GROW|wx.ALL, 5)

        #INI_SPOOL_FILE_EXT = "/Spool/FileExtension"
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, u"Erweiterung Spooldatei:")
        box.Add(label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        self.spool_ext_ctrl = wx.TextCtrl(self, -1, size = (30, -1), value = wx.ConfigBase_Get().Read(common.INI_SPOOL_FILE_EXT, ""))
        box.Add(self.spool_ext_ctrl, 0, wx.ALIGN_LEFT, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        panel.Layout()
        return panel

    def _DefineControlAndEvents(self):
        self.panel = self._GetPanel()
        vsizer = wx.BoxSizer(wx.VERTICAL)
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.okButton = wx.Button(self, wx.ID_OK, "OK")
        self.okButton.SetDefault()
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel")

        buttonsizer.Add(self.okButton, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        buttonsizer.AddSpacer((10,10),0)
        buttonsizer.Add(self.cancelButton, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        buttonsizer.AddSpacer((10,10),0)

        vsizer.Add(self.panel,0, wx.EXPAND|wx.ALL, 5)
        vsizer.Add(buttonsizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.Layout()

    def OnSpoolDirCallback(self, event):
        wx.ConfigBase_Get().Write(common.INI_SPOOL_DIR, evt.GetString())