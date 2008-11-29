# setup.py
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

from distutils.core import setup
import py2exe
import os, shutil
import datetime

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>RDIViewer</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

setup(
      name="RDIViewer",
      description = "RDIViewer",
      version = "0.0.1",
      windows=[
        { "script":             "rdiviewer.py",
          "icon_resources":     [(0,"RDIViewer.ico")],
          "other_resources":    [(24,1,manifest)]
        }
      ],
      options = {
        "py2exe": {"includes": ["stat", "encodings", "encodings.*"]}
      },
      data_files = [
                  (".",
                    [os.path.join('c:\\tools', 'Python24', 'msvcr71.dll')]
                  ),
      ],
)


if os.path.exists(".\\RDIViewer"):
    shutil.rmtree(".\\RDIViewer")

os.rename(".\\dist", ".\\RDIViewer")

d = datetime.datetime.now()

os.system("c:\\tools\\zip.exe -r .\\RDIViewer-%s-%02d-%02d.zip .\\RDIViewer" %(d.year,d.month,d.day))

