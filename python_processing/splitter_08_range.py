import io
from lxml import etree

# Define the path to your XML file
file_path = 'export_files/file.xml'

# Read and parse the XML file
tree = etree.parse(file_path)
root = tree.getroot()

# Define the namespaces including the 'xml' namespace
namespaces = {
    'tei': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}

# Variables
year_of_volume = '1758'
facs_start_range = range(13, 16)  # Range from 13 to 15 inclusive

# Find all 'surface' elements with xml:id in the specified range
surface_elements = []
for facs_start in facs_start_range:
    surface_elements.extend(root.findall(f".//tei:surface[@xml:id='facs_{facs_start}']", namespaces))

# Create a new Element as the root and add namespaces
tei_root = etree.Element('{http://www.tei-c.org/ns/1.0}TEI', nsmap={
    None: 'http://www.tei-c.org/ns/1.0',  # Default namespace
    'xml': 'http://www.w3.org/XML/1998/namespace'
})

# Create and append the teiHeader element with its sub-elements
tei_header = etree.SubElement(tei_root, 'teiHeader')
file_desc = etree.SubElement(tei_header, 'fileDesc')

# Add elements in the correct order
title_stmt = etree.SubElement(file_desc, 'titleStmt')
title = etree.SubElement(title_stmt, 'title', type='main')
title.text = f'Repertoire de tous les Spectacles {year_of_volume} (Houghton)'

# Add the publicationStmt element after titleStmt
publication_stmt = etree.SubElement(file_desc, 'publicationStmt')
publisher = etree.SubElement(publication_stmt, 'publisher')
publisher.text = 'Houghton Library, Harvard University'

pub_place = etree.SubElement(publication_stmt, 'pubPlace')
pub_place.text = 'Cambridge, MA'

date = etree.SubElement(publication_stmt, 'date')
date.text = f'{year_of_volume}'

# Add seriesStmt after publicationStmt
series_stmt = etree.SubElement(file_desc, 'seriesStmt')
title_series = etree.SubElement(series_stmt, 'title')
title_series.text = 'GuDiE'

# Add sourceDesc after seriesStmt
source_desc = etree.SubElement(file_desc, 'sourceDesc')
bibl = etree.SubElement(source_desc, 'bibl')
title_bibl = etree.SubElement(bibl, 'title', type='main')
title_bibl.text = f'Repertoire de tous les Spectacles {year_of_volume} (Houghton)'

idno_transkribus = etree.SubElement(bibl, 'idno', type='Transkribus')
idno_transkribus.text = '2430699'

idno_external = etree.SubElement(bibl, 'idno', type='external')
idno_external.text = 'https://gams-staging.uni-graz.at/gamsdev/dittmann/iiif/manifests/MS_Thr_248-0.json'

note = etree.SubElement(bibl, 'note')
note.text = ('This manuscript, compiled by Philippe Gumpenhuber, contains a repertoire of all the spectacles performed in Vienna during the years 1758-1759, 1761 and 1763. It is held at Houghton Library, Harvard University.')

# Add the facsimile element
facsimile = etree.SubElement(tei_root, 'facsimile')

# Append the found <surface> elements inside the facsimile element
for surface in surface_elements:
    facsimile.append(surface)

# Convert the ElementTree to a string with XML declaration
tei_bytes = etree.tostring(tei_root, encoding='utf-8', xml_declaration=True, pretty_print=True)
tei_str = tei_bytes.decode('utf-8')

#print(tei_str)

# Save the output to an XML file
output_file_path = 'output/test.xml'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(tei_str)

print(f"The XML output has been saved to {output_file_path}")
