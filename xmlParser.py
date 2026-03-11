import xml.etree.ElementTree as ET

tree = ET.parse(r"example_otopark_data/data1.xml")

root = tree.getroot()

for node in root.findall('.//A1'): print(node.text)

A1 = root.find('.//A1').text
print(f"Is there a car: {A1}")


#root = etree.Element("root")
#child1 = etree.SubElement(root, "child1")

#print (root.tag)