import xml.etree.ElementTree as ET
from flask import Flask

app = Flask(__name__)

def rendernode(node):
	html = '<li>'
	
	html+= f"<strong>{node.tag}</strong>"
	
	if node.text and node.text.strip():
		html+= f":{node.text.strip()}"

	if node.attrib:
		attrs = ", ".join(f"{k}={v}" for k, v in node.attrib.items())
		html += f" <em>({attrs})</em>"

	children = list(node)
	if children:
		html += "<ul>"
		for child in children:
			html += rendernode(child)
		html += "</ul>"
	html+= "</li>"
	return html
	
	
@app.route("/")
def home():
	tree = ET.parse(r"example_otopark_data/data1.xml")
	root = tree.getroot()

	html = f"""
		<html>
	    <head>
	        <title>XML Live Viewer</title>
	        <style>
	            body {{ font-family: Arial; }}
	            ul {{ list-style-type: none; }}
	            li {{ margin: 4px 0; }}
				strong {{ color: #2c3e50; }}
			</style>
		</head>
		<body>
			<h1>Live XML Tree</h1>
			<ul>
			{rendernode(root)}
			</ul>
		</body>
	    </html>
	    """
	return html
app.run(debug=True)
	
#for node in root.findall('.//A1'): print(node.text)

#for node in root.iter(): print(node.tag, node.text)

