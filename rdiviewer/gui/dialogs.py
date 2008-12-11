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

import wx
import wx.gizmos
import wx.stc
import wx.lib.mixins.listctrl

import rdiviewer.common as common

class AboutDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE
            ):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI dialog using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

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
