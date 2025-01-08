from lxml import etree

# Load the XML and XSLT files
xml_file = "output/file_1759.xml"  # Replace with the path to your XML file
xslt_file = "xslt/reason_tb.xsl"  # Replace with the path to your XSLT file

# Parse the XML and XSLT
xml_tree = etree.parse(xml_file)
xslt_tree = etree.parse(xslt_file)

# Create an XSLT transformer
transform = etree.XSLT(xslt_tree)

# Apply the transformation
result_tree = transform(xml_tree)

# Save the transformed XML to a new file
output_file = "output/file_1759_afterreason.xml"  # Replace with your desired output file path
with open(output_file, "wb") as f:
    f.write(etree.tostring(result_tree, pretty_print=True, xml_declaration=True, encoding="UTF-8"))

print(f"Transformation completed. Output saved to {output_file}")