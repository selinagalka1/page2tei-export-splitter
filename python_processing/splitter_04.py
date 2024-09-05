import xml.etree.ElementTree as ET
import io
import re

# Define the path to your XML file
file_path = 'export_files/file.xml'

# Read and parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Define the namespaces for parsing (we will remove them later)
namespaces = {
    'tei': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}

# Variables
year_of_volume = '1758'
facs_start = '13'

# Find all 'surface' elements with xml:id="facs_13" (which are in the tei namespace)
surface_elements = root.findall(f".//tei:surface[@xml:id='facs_{facs_start}']", namespaces)

# Create a new root element <TEI> without any namespaces
tei_root = ET.Element('TEI')

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
title_bibl.text = f'Repertoire de tous les Spectacles {year_of_volume} (Houghton)'

idno_transkribus = ET.SubElement(bibl, 'idno', {'type': 'Transkribus'})
idno_transkribus.text = '2430699'

idno_external = ET.SubElement(bibl, 'idno', {'type': 'external'})
idno_external.text = 'https://gams-staging.uni-graz.at/gamsdev/dittmann/iiif/manifests/MS_Thr_248-0.json'

note = ET.SubElement(bibl, 'note')
note.text = ('This manuscript, compiled by Philippe Gumpenhuber, contains a repertoire of all the spectacles performed in Vienna during the years 1758-1759, 1761 and 1763. It is held at Houghton Library, Harvard University.')

# Create a <facsimile> element
facsimile = ET.SubElement(tei_root, 'facsimile')

# Append the found <surface> elements inside the facsimile element without namespace
for surface in surface_elements:
    facsimile.append(surface)

# Use a regex pattern to match elements with 'facs' attributes starting with "facs_13"
regex_pattern = re.compile(r'facs_13\S*')

# Extract the specified elements based on the regex pattern for the 'facs' attribute
extracted_elements = root.findall(".//*[@facs]", namespaces)
filtered_elements = [element for element in extracted_elements if regex_pattern.search(element.get('facs'))]

# Append the extracted elements inside the proper structure without namespaces
# Create <text>, <body>, and <div> elements (without namespace)
text_element = ET.SubElement(tei_root, 'text')
body_element = ET.SubElement(text_element, 'body')
div_element = ET.SubElement(body_element, 'div')

# Append the filtered elements to <div>
for element in filtered_elements:
    div_element.append(element)

# Add a <pb> tag after the <div> elements to maintain the structure
#pb_element = ET.SubElement(div_element, 'pb')

# Function to remove namespaces from element tags
def strip_namespace(elem):
    elem.tag = elem.tag.split('}', 1)[-1]  # Strip namespace if present
    for subelem in elem:
        strip_namespace(subelem)

# Strip namespaces from the root and all elements
strip_namespace(tei_root)

# Create an ElementTree object and write to a string with proper declaration
tei_tree = ET.ElementTree(tei_root)

# Write the XML string without namespaces
with io.StringIO() as string_io:
    tei_tree.write(string_io, encoding='unicode', xml_declaration=True)
    tei_str = string_io.getvalue()

# Save the output to an XML file
output_file_path = 'output/test.xml'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(tei_str)

print(f"The XML output has been saved to {output_file_path}")
