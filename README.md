# page2tei-export-splitter
 
1. open python_processing/splitter_10_fix-xml-id.py to split the page2tei export file
2. change variables for the metadata and most importantly, change the range of the pages to be extracted
3. the output file can be found in the output folder
4. then open the xslt stylesheet in xslt/test-stylesheet.xsl in Oxygen to run it through the output file(s)
5. voila: you have extracted the necessary files from your page2tei export