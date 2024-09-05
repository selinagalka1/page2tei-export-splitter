import xml.etree.ElementTree as ET

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

# Find all 'surface' elements with xml:id="facs_1"
surface_elements = root.findall(".//tei:surface[@xml:id='facs_1']", namespaces)

# Process and print the attributes of <graphic> elements within the found <surface> elements
for surface in surface_elements:
    graphic = surface.find('tei:graphic', namespaces)
    if graphic is not None:
        print(graphic.attrib)

# If you want to print a prettified XML of the elements
for surface in surface_elements:
    et_str = ET.tostring(surface, encoding='unicode')
    print(et_str)