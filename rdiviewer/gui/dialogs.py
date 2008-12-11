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

        buttonsizer.Add(self.okButton,1, wx.EXPAND)
        buttonsizer.AddSpacer((10,10),0)
        buttonsizer.Add(self.cancelButton,1, wx.EXPAND)
        buttonsizer.AddSpacer((10,10),0)

        vsizer.Add(self.panel,0, wx.EXPAND)
        vsizer.AddSpacer((10, 10), 1)
        vsizer.Add(buttonsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.Layout()

    def OnSpoolDirCallback(self, event):
        wx.ConfigBase_Get().Write(common.INI_SPOOL_DIR, evt.GetString())

class FilterDialog(wx.Dialog):
    def __init__(self, parent, pos = wx.DefaultPosition, size = wx.DefaultSize):
        wx.Dialog.__init__(self, parent, -1, "Edit filter:", pos, size, style = wx.DEFAULT_DIALOG_STYLE)
        self.__DefineControlAndEvents()

    def SetData(self, data):
        self.data = data
        self._FillControlsFromData()

    def _FillControlsFromData(self):
        self.filter_name_text_ctrl.SetValue(self.data.GetName())

    def _set_control_gap(self, sizer):
        sizer.SetHGap(10)
        sizer.SetVGap(2)

    def _get_what_choices(self):
        return ["Text", "Group", "Variable", "Wert"]
    
    def _GetFilterSettingPanel(self):
        psizer = wx.GridBagSizer()
        nvsizer = wx.GridBagSizer()
        self._set_control_gap(psizer)
        self._set_control_gap(nvsizer)
        p = wx.Panel(self)

        psizer.Add(wx.StaticText(p, -1, "Filter name:"),(1,1), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.filter_name_text_ctrl = wx.TextCtrl(p)
        psizer.Add(self.filter_name_text_ctrl,(1,2))

        psizer.Add(wx.StaticText(p, -1, "What"),(2,1), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.what_combo = wx.ComboBox(p,style=wx.CB_READONLY)
        psizer.Add(self.what_combo,(2,2))

        nvsizer.Add(wx.StaticText(p, -1, "Name"),(1,1), flag=wx.ALIGN_BOTTOM)
        nvsizer.Add(wx.StaticText(p, -1, "Value"),(1,2), flag=wx.ALIGN_BOTTOM)
        self.name_text_ctrl = wx.TextCtrl(p)
        nvsizer.Add(self.name_text_ctrl,(2,1))

        self.value_text_ctrl = wx.TextCtrl(p)
        nvsizer.Add(self.value_text_ctrl,(2,2))

        psizer.Add(nvsizer,(3,1), (1,3))
        
        self.value_text_ctrl.Enable(False)
        self.what_combo.AppendItems(self._get_what_choices())

        p.SetAutoLayout(True)
        p.SetSizer(psizer)

        return p

    def _DefineControlAndEvents(self):
        self.p = self._GetFilterSettingPanel()
        vsizer = wx.BoxSizer(wx.VERTICAL)
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.okButton = wx.Button(self, wx.ID_OK, "OK")
        self.okButton.SetDefault()
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel")

        buttonsizer.Add(self.okButton,1, wx.EXPAND)
        buttonsizer.AddSpacer((10,10),0)
        buttonsizer.Add(self.cancelButton,1, wx.EXPAND)
        buttonsizer.AddSpacer((10,10),0)

        vsizer.Add(self.p,1, wx.EXPAND)
        vsizer.Add(buttonsizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        self.Layout()
