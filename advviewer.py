#! /System/Library/Frameworks/Python.framework/Versions/2.5/Resources/Python.app/Contents/MacOS/Python
# encoding: utf-8

import os
import os.path
import sys
import codecs
import base64 
import types

import sys

#if not hasattr(sys, "frozen"):
#    import wxversion
#    wxversion.select("2.5")

import wx

import controls
import filehandlers
import common
import filter

class advFrame(wx.Frame):
    def __init__(self, parent, id, title,pos=wx.Point(50,50), size=wx.Size(400, 400)):
        wx.Frame.__init__(self, parent, id, title, pos=pos, size=size,
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        wx.EVT_CLOSE(self, self.OnCloseWindow)

        self.currentItem = None

        self.CreateStatusBar()

        self._MakeMenu()
        self._MakeToolBar()             # toolbar

        self._DefineControlsAndEvents()

        self.__LoadFilters()

        self.__LoadIcon()
        #try:            # - don't sweat it if it doesn't load
            #self.SetIcon()
        #finally:
            #pass

        self.Show(True)

    def __LoadIcon(self):
        # load icon that has an id of 1
        dir = os.path.dirname(sys.argv[0])
        if dir == '':
            dir = os.getcwd()
        if sys.argv[0][-3:].lower() == 'exe':
            iconLoc = wx.IconLocation(sys.argv[0], 0)
        else:
            iconLoc = wx.IconLocation(dir + os.sep + 'advviewer.ico', 0)

        icon = wx.IconFromLocation(iconLoc)
        # set title bar icon to use this one
        self.SetIcon(icon)

    def __LoadFilters(self):
        config = wx.ConfigBase_Get()
        filter_file = config.Read(common.INI_FILTER_FILE)

        try:
            self.filter_list = filter.advFilterList(filter_file)
        except OSError:
            filter_file = self.__InitFilterFile()
            self.filter_list = filter.advFilterList(filter_file)

        filter_names = self.filter_list.GetFilterNames()
        filter_names.sort()
        
        self.doc_filters.Clear()
        
        for name in filter_names:
            self.doc_filters.Append(name)

    def __InitFilterFile(self):
        config = wx.ConfigBase_Get()
        dlg = wx.FileDialog(self, "Specify a filter file", style = wx.SAVE )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                config.Write(common.INI_FILTER_FILE, path)
                return path

    def OnFilterComboBoxKeyDown(self, event):
        if event.GetKeyCode() <> wx.WXK_RETURN:
            event.Skip()
            return

        if len(self.doc_filters.GetValue()) == 0:
            event.Skip()
            return

        if self.doc_filters.FindString(self.doc_filters.GetValue()) <> wx.NOT_FOUND and event.ControlDown() == True:
            dlg = controls.advFilterDialog(self)
            filter_data = self.filter_list.GetFilterData(self.doc_filters.GetValue())
            dlg.SetData(filter_data)
            dlg.ShowModal()
        elif self.doc_filters.FindString(self.doc_filters.GetValue()) == wx.NOT_FOUND :
            msgdlg = wx.MessageDialog(self, "%s isn't a valid filter\nDo you want to create a new filter?" 
                          %(self.doc_filters.GetValue()), "Unknown filter", 
                          style= wx.ICON_QUESTION | wx.YES_NO)
            if msgdlg.ShowModal() == wx.ID_YES:
                dlg = controls.advFilterDialog(self)
                filter_data = self.filter_list.NewFilter(self.doc_filters.GetValue())
                filter_data.SetName(self.doc_filters.GetValue())
                dlg.SetData(filter_data)
                dlg.ShowModal()
        else:
            pass

    def OnFilterComboBoxSelected(self, event):
        self.selected_filter = event.GetString()
        event.Skip()
    
    def _DefineControlsAndEvents(self):
        config = wx.ConfigBase_Get()
        wx.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
        self.splitter = wx.SplitterWindow(self, -1, style=wx.NO_3D)


        self.nb = wx.Notebook(self.splitter, -1, style=wx.CLIP_CHILDREN)

        self.lPanel = wx.Panel(self.splitter)

        self.doc_filters = wx.ComboBox(self.lPanel)
#        self.doc_filters.Bind(wx.EVT_TEXT_ENTER, self.OnFilterComboBoxEnter)
        self.doc_filters.Bind(wx.EVT_KEY_DOWN, self.OnFilterComboBoxKeyDown)
        self.doc_filters.Bind(wx.EVT_COMBOBOX, self.OnFilterComboBoxSelected)
        
        self.doc_list = controls.SingleColListCtrl(self.lPanel, -1, "Documents",
                                 style=wx.LC_REPORT | wx.NO_BORDER)

        self.lPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.lPanelSizer.Add(self.doc_filters, 0, wx.EXPAND, 0)
        self.lPanelSizer.Add(self.doc_list, 1, wx.EXPAND, 0)
        self.lPanel.SetAutoLayout(True)
        self.lPanel.SetSizer(self.lPanelSizer)

        self.doc_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDocListItemActivated)

        # create panel and tree control
        self.structure_panel = wx.Panel(self.nb, -1, style=wx.CLIP_CHILDREN| wx.TAB_TRAVERSAL )

        self.doc_structure = controls.advDocSructure(self.structure_panel, -1, style = wx.TR_DEFAULT_STYLE |
                                                     wx.TR_HIDE_ROOT |
                                                     wx.NO_BORDER
                                                     )
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED , self.OnNoteBookPageChanged)
        self.nb.Bind(wx.EVT_SET_FOCUS, self.OnNoteBookPageFocus)

        self.nb.AddPage(self.structure_panel, "Document Structure")
        wx.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        def OnDocStructureSize(evt, ctrl=self.doc_structure):
            ctrl.SetSize(evt.GetSize())
        wx.EVT_SIZE(self.structure_panel, OnDocStructureSize)

        # create panel and text control
        self.contents_panel = wx.Panel(self.nb, -1, style=wx.CLIP_CHILDREN)
        self.doc_contents = controls.advSTC(self.contents_panel, -1)

        self.nb.AddPage(self.contents_panel, 'Document Contents')

        def OnDocContentsSize(evt, ovr=self.doc_contents):
            ovr.SetSize(evt.GetSize())

        wx.EVT_SIZE(self.contents_panel, OnDocContentsSize)


        # add the windows to the splitter and split it.
        self.splitter.SplitVertically(self.lPanel, self.nb, config.ReadInt(common.INI_SPLITTER_POS,180))

        self.splitter.SetMinimumPaneSize(100)

        self.Bind(wx.EVT_FIND, self.OnFindInDocument)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFindInDocument)
        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindDlgClose)
        self.doc_list.SetFocus()

    def OnNoteBookPageFocus(self, event):
        wx.CallAfter(self.AfterOnNoteBookPageFocus)
        event.Skip()

    def AfterOnNoteBookPageFocus(self):
        try:
            panel = self.nb.GetPage(self.nb.GetSelection())


            if self.currentItem <> None and self.doc_contents.GetValue() <> "":
                if panel == self.doc_structure.GetParent():
                    self.doc_structure.SetFocus()                        
                else:
                    self.doc_contents.SetFocus()
        except:
            pass

    def OnNoteBookPageChanged(self, event):
        panel = self.nb.GetPage(event.GetSelection())


        if self.currentItem <> None and self.doc_contents.GetValue() <> "":
            if panel == self.doc_structure.GetParent():
                data = self.doc_contents.GetValue()
                doc = self.handler.GetDocumentFromData(data)
                self.doc_structure.ShowData(doc)
        event.Skip()

    def OnDocListItemActivated(self, event):
        if self.doc_list.GetSelectedItemCount() > 0:
            self.currentItem = event.m_itemIndex
            self.LoadDocument(self.currentItem)
            for mi in self.docMenuItems:
                mi.Enable(True)

            if self.handler.HasPrintAndPreview():
                if self.handler.IsDocPreview(self.currentItem):
                    self.printOrPreviewMenuItem.type = 'preview'
                    self.TogglePreviewPrintMenu('print')
                else:
                    self.TogglePreviewPrintMenu('preview')
                    self.printOrPreviewMenuItem.type = 'print'

    def LoadDocument(self, idx):
        doc_data = self.handler.GetDocumentData(idx)
        self.doc_contents.Clear()
        self.doc_contents.SetText(doc_data)
        self.doc_structure.ShowData(self.handler.GetDocument(idx))

    def TogglePreviewPrintMenu(self, type):
        assert(isinstance(self.printOrPreviewMenuItem,wx.MenuItem))
        if type == 'preview':
            self.printOrPreviewMenuItem.SetText('&Make preview\tCtrl-P')
        else:
            self.printOrPreviewMenuItem.SetText('&Make printable\tCtrl-P')

        self.printOrPreviewMenuItem.Enable(True)

    def OnCloseWindow(self, event):
        config = wx.ConfigBase_Get()

        frm_pos = self.GetPosition()
        config.WriteInt(common.INI_WINDOW_POS_X, frm_pos.x)
        config.WriteInt(common.INI_WINDOW_POS_Y, frm_pos.y)

        frm_size = self.GetSize()
        config.WriteInt(common.INI_WINDOW_SIZE_W, frm_size.width)
        config.WriteInt(common.INI_WINDOW_SIZE_H, frm_size.height)

        try:
            col_count = self.doc_structure.GetColumnCount()
            for idx in range(col_count):
                col_w = self.doc_structure.GetColumnWidth(idx)
                ini_key = common.INI_COLUMN_WIDTH + str(idx)
                config.WriteInt(ini_key, col_w)

        except:
            pass

        splttr_pos = self.splitter.GetSashPosition()
        config.WriteInt(common.INI_SPLITTER_POS, splttr_pos)


        return self.Destroy()

    def OnCopyNameOpen(self, event):
        try:
            item = self.doc_structure.GetSelection()
            text = self.doc_structure.GetItemText(item)

            isinstance(text, types.UnicodeType)

            text = text.replace('-','_')
            
            do = wx.TextDataObject()
            do.SetText(text)
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(do)
            wx.TheClipboard.Close()
            sb = self.GetStatusBar()
            isinstance(sb, wx.StatusBar)
            sb.SetStatusText('Copied text %s to clipboard' %(text),0)
        except:
            pass
        
    def OnFileOpen(self, event):
        config = wx.ConfigBase_Get()
        wildcard = "SAPScript RDI (*.rdi;*.dat;*.prt)|*.rdi;*.dat;*.prt|" \
                   "All files (*.*)|*.*"

        dir = config.Read(common.INI_FILEOPEN_DIR, os.getcwd())

        dlg = wx.FileDialog(self, "Choose a file", dir, "", wildcard,
                            wx.OPEN | wx.CHANGE_DIR
                            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                pass
            self.LoadFile(path)
            lastDir = os.path.dirname(path)
            config.Write(common.INI_FILEOPEN_DIR, lastDir)
            dlg.Destroy()
        self.doc_list.SetFocus()

    def LoadFile(self,path):

        if os.path.exists(path) <> True:
            wx.MessageBox("File %s doesn't exist" %(path), "Fehler", style= wx.ICON_EXCLAMATION | wx.OK)
            return

        self.handler = filehandlers.GetHandlerForFile(path)

        if self.handler <> None:
            self.handler.ScanForDocuments()
            doc_count = self.handler.GetDocumentCount()
            if  doc_count > 100:
                pass
                # Dialog for Filter
            doc_list = self.handler.GetDocumentList()
            self.doc_list.SetDocuments(doc_list)
            self.doc_list.SetItemState(0,wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
            self.doc_structure.SetColumns(self.handler.GetColumns())

    def OnEnqueue(self, event):
        config = wx.ConfigBase_Get()

        if self.doc_list.GetSelectedItemCount() == 0:
            return

        try:
            dir = config.Read(common.INI_SPOOL_DIR)
            assert dir <> ''
        except:
            # In this case we include a "New directory" button.
            dlg = wx.DirDialog(self, u"Verzeichnis auswählen:",
                              style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)

            # If the user selects OK, then we process the dialog's data.
            # This is done by getting the path data from the dialog - BEFORE
            # we destroy it.
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath()
                config.Write(common.INI_SPOOL_DIR, dir)
            dlg.Destroy()

        try:
            ext = config.Read(common.INI_SPOOL_FILE_EXT)
            assert ext <> ''
        except:
            dlg = wx.TextEntryDialog(
                    self, 'Bitte geben Sie eine Dateierweiterung an\n(ohne Punkt)',
                    'Dateierwiterung', 'DAT')

            if dlg.ShowModal() == wx.ID_OK:
                ext = dlg.GetValue()
                config.Write(common.INI_SPOOL_FILE_EXT, ext)
            dlg.Destroy()

        fileName = dir + os.sep + common.makeUniqueString() + '.' + ext

        try:
            default_encoding = config.Read(common.INI_CODECS_DEFAULT,'cp1250')
            if len(default_encoding) == 0:
               default_encoding = 'cp1250'
            fd = codecs.open(fileName,"w", default_encoding)
        except IOError, (errno, strerror):
            str = unicode("Fehler beim öffnen der Datei %s.\nBetriebsystem meldet: %s",'UTF-8','ignore') %(fileName,strerror)
            dlg = wx.MessageDialog(self, str, "Fehler", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            config.Write(common.INI_SPOOL_DIR, "")

        try:
            fd.write(self.doc_contents.GetValue())
            str = unicode("Datei %s im Spoolverzeichnis abgelegt",'UTF-8','ignore') %(fileName)
            dlg = wx.MessageDialog(self, str, "Fehler", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        except IOError, (errno, strerror):
            str = unicode("Fehler beim schreiben der Daten in die Datei %s.\nBetriebsystem meldet: %s",'UTF-8','ignore') %(fileName,strerror)
            dlg = wx.MessageDialog(self, str, "Fehler", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def OnFindMenuItem(self, event):
        config = wx.ConfigBase_Get()
        findFlags = config.ReadInt(common.INI_FIND_FLAGS,0)
        self.findData = wx.FindReplaceData()
        self.findData.SetFlags(findFlags)
        dlg = wx.FindReplaceDialog(self, self.findData, "Find",
                        wx.FR_NOUPDOWN |
                        wx.FR_NOMATCHCASE |
                        wx.FR_NOWHOLEWORD)
        dlg.Show(True)

    def OnPrintOrPreviewMenuItem(self, event):
        if self.printOrPreviewMenuItem.type == 'print':
            type = 'preview'
        else:
            type = 'print'

        self.handler.ChangeDocType(type, self.currentItem)
        self.LoadDocument(self.currentItem)

        if type == 'print':
            self.TogglePreviewPrintMenu('preview')
        else:
            self.TogglePreviewPrintMenu('print')

        self.printOrPreviewMenuItem.type = type

    def OnFindInDocument(self, event):
        et = event.GetEventType()

        if event.GetEventType() == wx.wxEVT_COMMAND_FIND_NEXT:
            idx = self.lastFindIdx
        else:
            idx = 0

        idx = self.doc_contents.FindText(idx, self.doc_contents.GetTextLength(), event.GetFindString())

        if idx <> -1:
            endIdx = idx+len(event.GetFindString())
            self.doc_contents.SetSelection(idx, endIdx)
            self.lastFindIdx = endIdx
        else:
            self.lastFindIdx = 0

    def OnFindDlgClose(self, event):
        config = wx.ConfigBase_Get()
        findFlags = self.findData.GetFlags()
        config.WriteInt(common.INI_FIND_FLAGS,findFlags)
        event.GetDialog().Destroy()
        event.Skip()

    def OnAboutDlg(self, event):
        dlg = controls.AboutDialog(self, -1, "About", size=(350, 200),
                 #style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME
                 style = wx.DEFAULT_DIALOG_STYLE
                 )

        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        dlg.Destroy()

    
    def OnLicenseDlg(self, event):
        dlg = controls.LicenseDialog(self, -1, "License", size=(350, 200),
                 #style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME
                 style = wx.DEFAULT_DIALOG_STYLE
                 )

        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        dlg.Destroy()
    
    def _MakeMenu(self):
        self.mainmenu = wx.MenuBar()

        menu = self.__MakeFileMenu()
        self.mainmenu.Append(menu, '&File')

        menu = self.__MakeDocumentMenu()

        self.mainmenu.Append(menu, '&Document')

        menu = self.__MakeEditMenu()

        self.mainmenu.Append(menu, '&Edit')

        menu = self.__MakeHelpMenu()

        self.mainmenu.Append(menu, '&Help')

        self.SetMenuBar(self.mainmenu)

    def __MakeEditMenu(self):
        menu = wx.Menu()

        mID = wx.NewId()
        menu.Append(mID, '&Copy Name\tAlt-C', 'Copy variable name to clipboard')
        wx.EVT_MENU(self, mID, self.OnCopyNameOpen)
        
        return menu

    def __MakeFileMenu(self):
        menu = wx.Menu()

        mID = wx.NewId()
        menu.Append(mID, '&Open\tCtrl-O', 'Open')
        wx.EVT_MENU(self, mID, self.OnFileOpen)

        mID = wx.NewId()
        menu.Append(mID, 'E&xit', 'Exit')
        wx.EVT_MENU(self, mID, self.OnCloseWindow)

        return menu

    def __MakeDocumentMenu(self):
        menu = wx.Menu()
        self.docMenuItems = []
        mID = wx.NewId()
        mi = menu.Append(mID, '&Enqueue\tCtrl-E', 'Enqueue')
        mi.Enable(False)
        wx.EVT_MENU(self, mID, self.OnEnqueue)
        self.docMenuItems.append(mi)

        mID = wx.NewId()
        mi = menu.Append(mID, '&Find\tCtrl-F', 'Find in Document')
        mi.Enable(False)
        wx.EVT_MENU(self, mID, self.OnFindMenuItem)
        self.docMenuItems.append(mi)

        mID = wx.NewId()
        self.printOrPreviewMenuItem = menu.Append(mID, '&Make Preview\tCtrl-P', 'Make this Document a Preview')
        self.printOrPreviewMenuItem.Enable(False)
        wx.EVT_MENU(self, mID, self.OnPrintOrPreviewMenuItem)

        return menu

    def __MakeHelpMenu(self):
        menu = wx.Menu()
        mID = wx.NewId()
        mi = menu.Append(mID, '&About...', 'About Dialog')
        wx.EVT_MENU(self, mID, self.OnAboutDlg)

        mID = wx.NewId()
        mi = menu.Append(mID, '&License', 'License information')
        wx.EVT_MENU(self, mID, self.OnLicenseDlg)

        return menu

    def _MakeToolBar(self):
        tb = self.CreateToolBar(wx.TB_HORIZONTAL|wx.NO_BORDER)

        #mID = wx.NewId()
        #self.__SetToolPath(self, tb, mID, images.getDbIncBitmap(), 'Inc Year')
        #wx.EVT_TOOL(self, mID, self.OnIncYear)

        tb.Realize()

    def __SetToolPath(self, tb, id, bmp, title):
        tb.AddSimpleTool(id, bmp, title, title)

class advApp(wx.App):
    def OnInit(self):
        self.SetAppName('advViewer')
        ini_filename = self.GetAppName().lower() + '.ini'
        self.config = wx.FileConfig( localFilename=ini_filename)
        self.config.SetRecordDefaults(True)
        wx.ConfigBase_Set(self.config)

        win_pos = wx.Point(self.config.ReadInt(common.INI_WINDOW_POS_X, 100),
                           self.config.ReadInt(common.INI_WINDOW_POS_Y, 100)
                           )
        win_size = wx.Size(self.config.ReadInt(common.INI_WINDOW_SIZE_W, 600),
                           self.config.ReadInt(common.INI_WINDOW_SIZE_H, 600)
                           )

        self.frame = advFrame(None, -1, "advViewer",pos=win_pos, size=win_size)
        self.frame.Show(True)

        if len(sys.argv) > 1:
            self.frame.LoadFile(sys.argv[1])

        return True


if __name__ == '__main__':
    app = advApp(False)
    app.MainLoop()
