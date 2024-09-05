import xml.etree.ElementTree as ET
import io
import re

# Define the path to your XML file
file_path = 'export_files/file.xml'

# Read and parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Define the namespaces including the 'xml' namespace
namespaces = {
    'tei': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace'  # Adding the 'xml' namespace explicitly
}

# Variables
year_of_volume = '1758'
facs_start = '1'


# Find all 'surface' elements with xml:id="facs_1"
surface_elements = root.findall(f".//tei:surface[@xml:id='facs_{facs_start}']", namespaces)

# Create a new Element as the root and add namespaces
tei_root = ET.Element('{http://www.tei-c.org/ns/1.0}TEI')
tei_root.set('xmlns', 'http://www.tei-c.org/ns/1.0')
tei_root.set('xmlns:xml', 'http://www.w3.org/XML/1998/namespace')

# Create and append the teiHeader element with its sub-elements
tei_header = ET.SubElement(tei_root, 'teiHeader')
file_desc = ET.SubElement(tei_header, 'fileDesc')

title_stmt = ET.SubElement(file_desc, 'titleStmt')
title = ET.SubElement(title_stmt, 'title', {'type': 'main'})
title.text = f'Repertoire de tous les Spectacles {year_of_volume} (Houghton)'

series_stmt = ET.SubElement(file_desc, 'seriesStmt')
title_series = ET.SubElement(series_stmt, 'title')
title_series.text = 'GuDiE'

source_desc = ET.SubElement(file_desc, 'sourceDesc')
bibl = ET.SubElement(source_desc, 'bibl')
title_bibl = ET.SubElement(bibl, 'title', {'type': 'main'})
title_bibl.text = 'Repertoire de tous les Spectacles 1758 (Houghton)'

idno_transkribus = ET.SubElement(bibl, 'idno', {'type': 'Transkribus'})
idno_transkribus.text = '2430699'

idno_external = ET.SubElement(bibl, 'idno', {'type': 'external'})
idno_external.text = 'https://gams-staging.uni-graz.at/gamsdev/dittmann/iiif/manifests/MS_Thr_248-0.json'

note = ET.SubElement(bibl, 'note')
note.text = ('This manuscript, compiled by Philippe Gumpenhuber, contains a repertoire '
             'of all the spectacles performed in Vienna during the years 1758-1759, 1761, '
             'and 1763. It is held at Houghton Library, Harvard University.')

# Append the found <surface> elements inside the root
for surface in surface_elements:
    tei_root.append(surface)

# Create an ElementTree object and write to a string with proper declaration
tei_tree = ET.ElementTree(tei_root)

with io.StringIO() as string_io:
    tei_tree.write(string_io, encoding='unicode', xml_declaration=True)
    # tei_str = string_io.getvalue()
    tei_str = re.sub(r'\bns0:', 'tei:', string_io.getvalue()) # Swap ns0 with tei

print(tei_str)