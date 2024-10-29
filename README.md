# Page2TEI Export Splitter

This tool is designed to assist in splitting the page2tei export file using Python and XSLT.

## Usage Instructions

1. Place the file you want to split in the `export_files` folder.

2. Open the `python_processing/splitter.py` file and configure the variables for the metadata. Adjust the range of the pages to be extracted as needed.

3. Run the `splitter.py` script. The output files will be generated in the `output` folder.

4. The XSLT stylesheet located at `xslt/test-stylesheet.xsl` is automatically run by the Python script. This further refines the extracted files, so there's no need to use Oxygen or any other XSLT editor separately.

## Prerequisites

- Python
- The `os` module (should be included in the Python standard library)
- The `lxml` library for processing XML and XSLT

Ensure that you have the necessary modules and libraries installed before using this tool.

## Want to Contribute?

If you find this tool helpful and would like to contribute to its development, feel free to fork the repository, make changes, and submit a pull request. We welcome any improvements, bug fixes, or new features that you think would benefit the community.