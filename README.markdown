RDIViewer
==========

An application to view [SAP RDI][RDI] data files. It supports RDI and Simple RDI data files.

When opening a RDI file, the file is scanned and a list of documents is displayed. This allows you to open
data files of any size.
A double click on a document in the document list will build a tree of SAPScript-Texts and their variables.
A second tab is provided to display the raw contents of the document.

Currently new nodes in the tree are created when a new SAP-Scripttext is found. I know this doesn't work very well for normal
print  reports/programs, but I nearly always work with the Printer Workbench which uses lot of different texts and doesn't use elements.
Support for elements is on my todo list, but if someone beats me to it and sends in a patch I'll be glad to submit it.

[RDI]: http://help.sap.com/saphelp_nw04/helpdata/en/d2/cb3d32455611d189710000e8322d00/frameset.htm 
