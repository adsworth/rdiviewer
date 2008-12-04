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

        label = wx.StaticText(self, -1, u"Adi J�rg Sieker")
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

        label = wx.StaticText(self, -1, u"Adi J�rg Sieker 2004-2008")
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

class LicenseDialog(wx.Dialog):
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

        label = wx.StaticText(self, -1, "Licensed for:")
        box.Add(label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        label = wx.StaticText(self, -1, common.L['name'])
        label.SetHelpText("Name of person or company this license is valid for")
        box.Add(label, 1, wx.ALIGN_LEFT|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)



        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "SpoolDir:")
        box.Add(label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        s = 'Beliebige SpoolDirs'
        if common.L.has_key('spooldir') and common.L['spooldir'] != '':
            s = common.L['spooldir']
        
        label = wx.StaticText(self, -1, s)
        label.SetHelpText("Directory in which the RDI files reside")
        box.Add(label, 1, wx.ALIGN_LEFT|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "License version:")
        box.Add(label, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        label = wx.StaticText(self, -1, common.L['version'])
        label.SetHelpText("Version of the license file format")
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

class advFilterDialog(wx.Dialog):
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
        


class advSTC(wx.stc.StyledTextCtrl):
    def __init__(self, parent, ID):
        wx.stc.StyledTextCtrl.__init__(self, parent, ID)

        self.Bind(wx.stc.EVT_STC_DO_DROP, self.OnDoDrop)
        self.Bind(wx.stc.EVT_STC_DRAG_OVER, self.OnDragOver)
        self.Bind(wx.stc.EVT_STC_START_DRAG, self.OnStartDrag)
        self.Bind(wx.stc.EVT_STC_MODIFIED, self.OnModified)

        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        if wx.Platform == '__WXMAC__':
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "size:%d,face:%s" % (12, 'Monaco'))
        else:
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "size:%d,face:%s" % (10, 'Courier New'))

    def GetValue(self):
        return self.GetText()

    def OnDestroy(self, evt):
        # This is how the clipboard contents can be preserved after
        # the app has exited.
        wx.TheClipboard.Flush()
        evt.Skip()


    def OnStartDrag(self, evt):
        if evt.GetPosition() < 250:
            evt.SetDragAllowMove(False)     # you can prevent moving of text (only copy)
            evt.SetDragText("DRAGGED TEXT") # you can change what is dragged
            #evt.SetDragText("")             # or prevent the drag with empty text


    def OnDragOver(self, evt):
        print(
            "OnDragOver: x,y=(%d, %d)  pos: %d  DragResult: %d\n"
            % (evt.GetX(), evt.GetY(), evt.GetPosition(), evt.GetDragResult())
            )

        if evt.GetPosition() < 250:
            evt.SetDragResult(wx.DragNone)   # prevent dropping at the beginning of the buffer


    def OnDoDrop(self, evt):
        print("OnDoDrop: x,y=(%d, %d)  pos: %d  DragResult: %d\n"
                       "\ttext: %s\n"
                       % (evt.GetX(), evt.GetY(), evt.GetPosition(), evt.GetDragResult(),
                          evt.GetDragText()))

        if evt.GetPosition() < 500:
            evt.SetDragText("DROPPED TEXT")  # Can change text if needed
            #evt.SetDragResult(wx.DragNone)  # Can also change the drag operation, but it
                                             # is probably better to do it in OnDragOver so
                                             # there is visual feedback

            #evt.SetPosition(25)             # Can also change position, but I'm not sure why
                                             # you would want to...




    def OnModified(self, event):
        event.Skip()

    def transModType(self, modType):
        st = ""
        table = [(wx.stc.STC_MOD_INSERTTEXT, "InsertText"),
                 (wx.stc.STC_MOD_DELETETEXT, "DeleteText"),
                 (wx.stc.STC_MOD_CHANGESTYLE, "ChangeStyle"),
                 (wx.stc.STC_MOD_CHANGEFOLD, "ChangeFold"),
                 (wx.stc.STC_PERFORMED_USER, "UserFlag"),
                 (wx.stc.STC_PERFORMED_UNDO, "Undo"),
                 (wx.stc.STC_PERFORMED_REDO, "Redo"),
                 (wx.stc.STC_LASTSTEPINUNDOREDO, "Last-Undo/Redo"),
                 (wx.stc.STC_MOD_CHANGEMARKER, "ChangeMarker"),
                 (wx.stc.STC_MOD_BEFOREINSERT, "B4-Insert"),
                 (wx.stc.STC_MOD_BEFOREDELETE, "B4-Delete")
                 ]

        for flag,text in table:
            if flag & modType:
                st = st + text + " "

        if not st:
            st = 'UNKNOWN'

        return st

class advDocSructure(wx.gizmos.TreeListCtrl):
    def __init__(self, parent, id, style):
        wx.gizmos.TreeListCtrl.__init__(self, parent, id, style=style)

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        self.img_fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        self.img_fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        self.img_fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.SetImageList(il)
        self.il = il
        self.columns = []

    def SetColumns(self, columns):
        config = wx.ConfigBase_Get()
        self.columns = columns
        idx = 0
        for col in columns:
            self.AddColumn(col["label"])
            ini_key = common.INI_COLUMN_WIDTH + str(idx)
            col_w = config.ReadInt(ini_key, 250)
            self.SetColumnWidth(idx, int(col_w))
            idx += 1

        self.SetMainColumn(0) # the one with the tree in it...
        self.SetLineSpacing(1)

    def ShowData(self, doc):
        self.DeleteAllItems()
        self.root = self.AddRoot('Dokument')

        root_nodes = doc.getRootNodes()
        if len(root_nodes) > 0:
            self._SetItemImages(self.root, self.img_fldridx, self.img_fldropenidx)
        else:
            self._SetItemImages(self.root, self.img_fileidx)

        for child in root_nodes:
            self._addChild(child, self.root)

    def _addChild(self,node,parent):
        child_node = self.AppendItem(parent, node.getData('name'))

        value = node.getData('value')

        self.SetItemText(child_node, value, 1)

        if( node.getType() == 'branch'):
            self._SetItemImages(child_node, self.img_fldridx, self.img_fldropenidx)
        else:
            self._SetItemImages(child_node, self.img_fileidx)

        children = node.getChildren()
        for child in children:
            self._addChild(child,child_node)

        if parent == self.root:
            self.Expand(child_node)
            self.SelectItem(child_node)

    def _SetItemImages(self,node, normal,expanded = None):
        self.SetItemImage(node, normal, which = wx.TreeItemIcon_Normal)
        if expanded <> None:
            self.SetItemImage(node, expanded, which = wx.TreeItemIcon_Expanded)


class SingleColListCtrl(wx.ListCtrl, wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style | wx.LC_VIRTUAL )
        wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin.__init__(self)

        self.InsertColumn(0, title)
        self.parent = parent

        self.numItems = 0
        self.groups = {}

    def Append(self,label,data):
        idx = len(self.groups)
        self.groups[idx] = data
        self.InsertStringItem(idx, label)
        self.SetItemData(idx, idx)
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def GetSelection(self):
        return self._selectedItem
    def GetClientData(self, index):
        return self.groups[index]
    def SetDocuments(self, docs):
        self.docs = docs
        self.SetItemCount(len(self.docs) )
    def OnGetItemText(self, item, col):
        return self.docs[item]["name"]
    def OnGetItemImage(self, item):
        return -1

    def OnGetItemAttr(self, item):
        return None

    def GetItemData(self, item):
        return self.docs[item]
