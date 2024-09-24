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
pub_place_text = 'Cambridge, MA'
publisher_text = 'Houghton Library, Harvard University'
title_series_text = 'Austrian Science Fund project "GuDiE" (FWF-Grant-DOI: 10.55776/P36729)'
idno_external_text = 'https://gams-staging.uni-graz.at/gamsdev/dittmann/iiif/manifests/MS_Thr_248-0.json'
facs_start_range = range(18,21) ## MOST IMPORTANT TO CHANGE

# Find all 'surface' elements with xml:id in the specified range
surface_elements = []
for facs_start in facs_start_range:
    surface_elements.extend(root.findall(f".//tei:surface[@xml:id='facs_{facs_start}']", namespaces))

# Extract table data
table_elements = []
for facs_start in facs_start_range:
    table_elements.extend(root.findall(f".//tei:table[@facs='#facs_{facs_start}_t1']", namespaces))

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
title.text = f'Repertoire de tous les Spectacles {year_of_volume}'

# Add the publicationStmt element after titleStmt
publication_stmt = etree.SubElement(file_desc, 'publicationStmt')
publisher = etree.SubElement(publication_stmt, 'publisher')
publisher.text = f'{publisher_text}'

pub_place = etree.SubElement(publication_stmt, 'pubPlace')
pub_place.text = f'{pub_place_text}'

date = etree.SubElement(publication_stmt, 'date')
date.text = f'{year_of_volume}'

# Add seriesStmt after publicationStmt
series_stmt = etree.SubElement(file_desc, 'seriesStmt')
title_series = etree.SubElement(series_stmt, 'title')
title_series.text = f'{title_series_text}'

# Add sourceDesc after seriesStmt
source_desc = etree.SubElement(file_desc, 'sourceDesc')
bibl = etree.SubElement(source_desc, 'bibl')
title_bibl = etree.SubElement(bibl, 'title', type='main')
title_bibl.text = f'Repertoire de tous les Spectacles {year_of_volume}'

#idno_transkribus = etree.SubElement(bibl, 'idno', type='Transkribus')
#idno_transkribus.text = '2430699'

idno_external = etree.SubElement(bibl, 'idno', type='external')
idno_external.text = f'{idno_external_text}'

note = etree.SubElement(bibl, 'note')
note.text = ('This manuscript, compiled by Philippe Gumpenhuber, contains a repertoire of all the spectacles performed in Vienna during the years 1758-1759, and 1761-1763.')

# Add the facsimile element
facsimile = etree.SubElement(tei_root, 'facsimile')

# Append the found <surface> elements inside the facsimile element
for surface in surface_elements:
    facsimile.append(surface)

# Add the text element with body and tables
text = etree.SubElement(tei_root, 'text')
body = etree.SubElement(text, 'body')

# Create a div element and append it to the body
div = etree.SubElement(body, 'div')

# Add page break and tables to the div
for facs_start in facs_start_range:
    pb = etree.SubElement(div, 'pb', facs=f"#facs_{facs_start}", n=str(facs_start), **{f'{{http://www.w3.org/XML/1998/namespace}}id': f"img_00{facs_start}"})
    
    for table in table_elements:
        if table.get('facs') == f"#facs_{facs_start}_t1":
            div.append(table)

# Convert the ElementTree to a string with XML declaration
tei_bytes = etree.tostring(tei_root, encoding='utf-8', xml_declaration=True, pretty_print=True)
tei_str = tei_bytes.decode('utf-8')

# Adjust the range formatting for single page
if facs_start_range.stop - facs_start_range.start == 1:
    range_str = f"{facs_start_range.start}"
else:
    range_str = f"{facs_start_range.start}-{facs_start_range.stop - 1}"

# Generate the output file name using the variables
output_file_path = f'output/{year_of_volume}_{range_str}.xml'

# Save the output to an XML file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(tei_str)

print(f"The XML output has been saved to {output_file_path}")
