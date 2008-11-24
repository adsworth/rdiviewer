# setup.py
# encoding: utf-8

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
<description>advViewer</description>
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
      name="advViewer",
      description = "advViewer",
      version = "0.0.1",
      windows=[
        { "script":             "advviewer.py",
          "icon_resources":     [(0,"advViewer.ico")],
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


if os.path.exists(".\\advViewer"):
    shutil.rmtree(".\\advViewer")

os.rename(".\\dist", ".\\advViewer")

d = datetime.datetime.now()

os.system("c:\\tools\\zip.exe -r .\\advViewer-%s-%02d-%02d.zip .\\advViewer" %(d.year,d.month,d.day))

