import os
from lxml import etree

def parse_xml(file_path):
    """Reads and parses the XML file."""
    try:
        # Parse the XML file and get the root element
        tree = etree.parse(file_path)
        return tree.getroot()
    except IOError as e:
        # Print an error message if the file cannot be read and return None
        print(f"Error reading {file_path}: {e}")
        return None

def create_tei_header(year_of_volume, publisher_text, pub_place_text, title_series_text, idno_external_text):
    """Creates the TEI header element with metadata."""
    # Create the root TEI element with namespaces
    tei_root = etree.Element('{http://www.tei-c.org/ns/1.0}TEI', nsmap={
        None: 'http://www.tei-c.org/ns/1.0',  # Default namespace
        'xml': 'http://www.w3.org/XML/1998/namespace'
    })

    # Create the TEI header and its child elements with associated metadata
    tei_header = etree.SubElement(tei_root, 'teiHeader')
    file_desc = etree.SubElement(tei_header, 'fileDesc')

    title_stmt = etree.SubElement(file_desc, 'titleStmt')
    # Set the main title of the XML document
    title = etree.SubElement(title_stmt, 'title', type='main')
    title.text = f'Repertoire de tous les Spectacles {year_of_volume}'

    publication_stmt = etree.SubElement(file_desc, 'publicationStmt')
    # Set the publisher information
    publisher = etree.SubElement(publication_stmt, 'publisher')
    publisher.text = publisher_text

    # Set the publication place
    pub_place = etree.SubElement(publication_stmt, 'pubPlace')
    pub_place.text = pub_place_text

    # Set the publication date
    date = etree.SubElement(publication_stmt, 'date')
    date.text = year_of_volume

    # Set the series title
    series_stmt = etree.SubElement(file_desc, 'seriesStmt')
    title_series = etree.SubElement(series_stmt, 'title')
    title_series.text = title_series_text

    source_desc = etree.SubElement(file_desc, 'sourceDesc')
    bibl = etree.SubElement(source_desc, 'bibl')
    # Repeat the main title within the bibliographic description
    title_bibl = etree.SubElement(bibl, 'title', type='main')
    title_bibl.text = f'Repertoire de tous les Spectacles {year_of_volume}'

    # Set the external identifier
    idno_external = etree.SubElement(bibl, 'idno', type='external')
    idno_external.text = idno_external_text

    # Add a note describing the manuscript
    note = etree.SubElement(bibl, 'note')
    note.text = ('This manuscript, compiled by Philippe Gumpenhuber, contains a repertoire of all the spectacles '
                 'performed in Vienna during the years 1758-1759, and 1761-1763.')

    return tei_root

def extract_surface_elements(root, facs_start_range, namespaces):
    """Extracts surface elements with xml:id in the specified range."""
    surface_elements = []
    # Find and collect all surface elements that match the given range of IDs
    for facs_start in facs_start_range:
        surface_elements.extend(root.findall(f".//tei:surface[@xml:id='facs_{facs_start}']", namespaces))
    return surface_elements

def extract_table_elements(root, facs_start_range, namespaces):
    """Extracts table elements associated with the specified range."""
    table_elements = []
    # Find and collect all table elements that are associated with the specified range of facsimile IDs
    for facs_start in facs_start_range:
        table_elements.extend(root.findall(f".//tei:table[@facs='#facs_{facs_start}_t1']", namespaces))
    return table_elements

def save_xml_to_file(output_file_path, xml_string):
    """Saves the XML string to a file."""
    # Check if the output file already exists and print a warning if it does
    if os.path.exists(output_file_path):
        print(f"Warning: {output_file_path} already exists. It will be overwritten.")

    # Open the output file and save the XML string to it
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(xml_string)
        # Print a confirmation message
    print(f"The original XML output has been saved to {output_file_path}")

def transform_xml(xslt_path, xml_tree):
    """Performs XSLT transformation on the provided XML tree."""
    # Parse the XSLT file
    xslt_tree = etree.parse(xslt_path)
    # Create an XSLT transformation object
    transform = etree.XSLT(xslt_tree)
    # Apply the transformation to the XML tree and return the result
    return transform(xml_tree)

def clean_transformed_xml(transformed_tree):
    """Cleans the transformed XML to ensure correct formatting."""
    # Convert the transformed XML tree to a string with pretty printing
    transformed_xml_string = etree.tostring(
        transformed_tree, pretty_print=True, encoding='UTF-8', xml_declaration=True
    )
    # Adjust <lb> elements to ensure they are on a new line without adding extra blank lines
    transformed_xml_string = transformed_xml_string.replace(b'>\n<lb ', b'>\n<lb ').replace(b'\n<lb', b'<lb')
    return transformed_xml_string

# Main execution block
if __name__ == "__main__":
    # Define the path to your XML file
    file_path = 'output/file_1759_afterreason.xml'

    # Read and parse the XML file
    root = parse_xml(file_path)

    if root is None:
        exit()

    # Define the namespaces including the 'xml' namespace
    namespaces = {
        'tei': 'http://www.tei-c.org/ns/1.0',
        'xml': 'http://www.w3.org/XML/1998/namespace'
    }

    # Variables
    year_of_volume = '1759'
    pub_place_text = 'Cambridge, MA'
    publisher_text = 'Houghton Library, Harvard University'
    title_series_text = 'Austrian Science Fund project "GuDiE" (FWF-Grant-DOI: 10.55776/P36729)'
    idno_external_text = 'https://gams-staging.uni-graz.at/gamsdev/dittmann/iiif/manifests/MS_Thr_248-1.json'
    facs_start_range = range(70,89)  # MOST IMPORTANT TO CHANGE

    # Extract surface and table elements
    surface_elements = extract_surface_elements(root, facs_start_range, namespaces)
    table_elements = extract_table_elements(root, facs_start_range, namespaces)

    # Create TEI root and header
    tei_root = create_tei_header(year_of_volume, publisher_text, pub_place_text, title_series_text, idno_external_text)

    # Add the facsimile element
    facsimile = etree.SubElement(tei_root, 'facsimile')
    for surface in surface_elements:
        facsimile.append(surface)

    # Add the text element with body and tables
    text = etree.SubElement(tei_root, 'text')
    body = etree.SubElement(text, 'body')
    div = etree.SubElement(body, 'div')

    # Add page break and content to the div
    for facs_start in facs_start_range:
        pb = etree.SubElement(div, 'pb', facs=f"#facs_{facs_start}", n=str(facs_start),
                              **{f'{{http://www.w3.org/XML/1998/namespace}}id': f"img_00{facs_start}"})

        # Find table elements associated with the current facs_start
        current_table_elements = root.findall(f".//tei:table[@facs='#facs_{facs_start}_t1']", namespaces)

        # If table elements are found, append these to the div element
        if current_table_elements:
            for table in current_table_elements:
                div.append(table)
        else:
            # Find <ab> elements associated with the current facs_start
            text_elements = root.xpath(f".//tei:ab[contains(@facs, '#facs_{facs_start}_')]", namespaces=namespaces)
            for text_el in text_elements:
                div.append(text_el)

    # Convert the ElementTree to a string with XML declaration
    tei_bytes = etree.tostring(tei_root, encoding='utf-8', xml_declaration=True, pretty_print=True)
    tei_str = tei_bytes.decode('utf-8')

    # Generate output file name using the variables
    range_str = f"{facs_start_range.start}-{facs_start_range.stop - 1}" if facs_start_range.stop - facs_start_range.start > 1 else f"{facs_start_range.start}"
    output_file_path = f'output/{year_of_volume}_{range_str}_before.xml'

    # Save the original output to an XML file
    save_xml_to_file(output_file_path, tei_str)