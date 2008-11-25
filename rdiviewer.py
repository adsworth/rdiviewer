#! /System/Library/Frameworks/Python.framework/Versions/2.5/Resources/Python.app/Contents/MacOS/Python
# encoding: utf-8
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
