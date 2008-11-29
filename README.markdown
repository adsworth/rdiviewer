RDIViewer
==========

An application to view [SAP RDI][RDI] data files. It supports RDI and Simple RDI data files.

When opening a RDI file, the file is scanned and a list of documents is displayed. A new document starts
when a header line is found. This allows you to open data files of any size, if the single documents aren't to large.
A double click on a document in the document list will build a tree of SAPScript-Texts and their variables.
A second tab is provided to display the raw contents of the document.

[RDI]: http://help.sap.com/saphelp_nw04/helpdata/en/d2/cb3d32455611d189710000e8322d00/frameset.htm 
