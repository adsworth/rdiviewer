#! /System/Library/Frameworks/Python.framework/Versions/2.5/Resources/Python.app/Contents/MacOS/Python
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

from rdiviewer.gui.frames import MainFrame
import rdiviewer.common as common

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

        self.frame = MainFrame(None, -1, "advViewer",pos=win_pos, size=win_size)
        self.frame.Show(True)

        if len(sys.argv) > 1:
            self.frame.LoadFile(sys.argv[1])

        return True


if __name__ == '__main__':
    app = advApp(False)
    app.MainLoop()
