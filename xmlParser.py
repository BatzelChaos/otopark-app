import xml.etree.ElementTree as ET
from flask import Flask, render_template

app = Flask(__name__)

def parsenode(node):
	return {
		"tag": node.tag,
		"value": (node.text or "").strip().lower(),
		"attributes": node.attrib,
		"children": [parsenode(child) for child in node]
	}

@app.route("/")
def home():
	tree = ET.parse(r"example_otopark_data/data1.xml")
	root = tree.getroot()
	
	data = parsenode(root)
	return render_template("index.html", node=data)
	
	return html
app.run(debug=True)