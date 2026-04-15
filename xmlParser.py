import xml.etree.ElementTree as ET
from flask import Flask, render_template

app = Flask(__name__)

def parsenode(node):
	return {
		"tag": node.tag,
		"value": (node.text or "").strip(),
		"attributes": node.attrib,
		"children": [parsenode(child) for child in node]
	}

def get_cells(node):
	cells=[]
	
	if node["tag"]=="cell":
		cells.append(node)
	for child in node["children"]:
		cells.extend(get_cells(child))
	return cells
	
@app.route("/")
def home():
	tree = ET.parse(r"example_otopark_data/data1.xml")
	root = tree.getroot()
	
	grid_node = root.find("grid")
	data = parsenode(grid_node)
	cells = get_cells(data)
	return render_template("index.html", node=data, cells=cells)
app.run(debug=True)